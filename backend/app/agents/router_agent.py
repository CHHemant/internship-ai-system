from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.ats_resume_generator_agent import ATSResumeGeneratorAgent
from app.agents.cover_letter_generator_agent import CoverLetterGeneratorAgent
from app.agents.verification_agent import VerificationAgent
from app.models.schemas import JobDescriptionData, ResumeProfile, VerificationResult


class WorkflowState(TypedDict):
    profile: ResumeProfile
    job: JobDescriptionData
    country: str
    generated_resume: str
    generated_cover_letter: str
    verification: VerificationResult | None
    retries: int


class RouterAgent:
    def __init__(self, max_retries: int = 2) -> None:
        self.max_retries = max_retries
        self.resume_agent = ATSResumeGeneratorAgent()
        self.cover_agent = CoverLetterGeneratorAgent()
        self.verification_agent = VerificationAgent()
        self.graph = self._build_graph().compile()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(WorkflowState)

        graph.add_node("generate", self._generate_node)
        graph.add_node("verify", self._verify_node)
        graph.add_node("improve", self._improve_node)

        graph.set_entry_point("generate")
        graph.add_edge("generate", "verify")
        graph.add_conditional_edges(
            "verify",
            self._needs_improvement,
            {"improve": "improve", "end": END},
        )
        graph.add_edge("improve", "verify")

        return graph

    def _generate_node(self, state: WorkflowState) -> WorkflowState:
        state["generated_resume"] = self.resume_agent.generate(state["profile"], state["job"], state["country"])
        state["generated_cover_letter"] = self.cover_agent.generate(state["profile"], state["job"], state["country"])
        return state

    def _verify_node(self, state: WorkflowState) -> WorkflowState:
        state["verification"] = self.verification_agent.verify(
            state["generated_resume"],
            state["generated_cover_letter"],
            state["job"],
        )
        return state

    def _improve_node(self, state: WorkflowState) -> WorkflowState:
        state["retries"] += 1
        state["generated_resume"] = self.resume_agent.generate(state["profile"], state["job"], state["country"])
        state["generated_cover_letter"] = self.cover_agent.generate(state["profile"], state["job"], state["country"])
        return state

    def _needs_improvement(self, state: WorkflowState) -> str:
        verification = state.get("verification")
        if verification and verification.score < 80 and state["retries"] < self.max_retries:
            return "improve"
        return "end"

    def run(self, profile: ResumeProfile, job: JobDescriptionData, country: str) -> WorkflowState:
        return self.graph.invoke(
            {
                "profile": profile,
                "job": job,
                "country": country,
                "generated_resume": "",
                "generated_cover_letter": "",
                "verification": None,
                "retries": 0,
            }
        )
