import { Nav } from "@/components/nav";

const cards = [
  ["Resume Parser", "Extracts profile JSON from PDF/DOCX with OCR fallback"],
  ["JD Parser", "Extracts skills, keywords, responsibilities, and eligibility"],
  ["ATS Generator", "Builds country-formatted ATS-safe resumes"],
  ["Cover Letter Agent", "Generates concise and academic motivation letters"],
  ["Verification Agent", "Scores ATS fit, relevance, grammar, and hallucination risk"],
  ["Router + Feedback", "Routes with LangGraph and retries until quality threshold"],
];

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white">
      <div className="mx-auto max-w-5xl py-10">
        <Nav />
        <h1 className="mb-6 text-3xl font-semibold">Agent Dashboard</h1>
        <div className="grid gap-4 md:grid-cols-2">
          {cards.map(([title, desc]) => (
            <article key={title} className="rounded-2xl border border-cyan-500/30 bg-cyan-900/10 p-5">
              <h2 className="mb-2 text-xl">{title}</h2>
              <p className="text-white/80">{desc}</p>
            </article>
          ))}
        </div>
      </div>
    </main>
  );
}
