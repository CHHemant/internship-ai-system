"use client";

import { useState } from "react";

import { Nav } from "@/components/nav";
import api from "@/lib/api";

type GenerationResult = {
  resume: string;
  cover_letter: string;
  verification: Record<string, unknown>;
};

export default function ResultsPage() {
  const [candidateId, setCandidateId] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [country, setCountry] = useState("global");
  const [result, setResult] = useState<GenerationResult | null>(null);

  async function runWorkflow() {
    const response = await api.post("/api/applications/run", {
      candidate_id: Number(candidateId),
      job_description: jobDescription,
      country,
    });
    setResult(response.data);
  }

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white">
      <div className="mx-auto max-w-5xl py-10">
        <Nav />
        <h1 className="mb-4 text-3xl font-semibold">Generation Results</h1>
        <div className="mb-5 grid gap-3 rounded-2xl border border-white/20 bg-white/5 p-5">
          <input
            className="rounded bg-black/30 p-3"
            placeholder="Candidate ID"
            value={candidateId}
            onChange={(event) => setCandidateId(event.target.value)}
          />
          <input
            className="rounded bg-black/30 p-3"
            placeholder="Country (usa/canada/germany/uk/europe/global)"
            value={country}
            onChange={(event) => setCountry(event.target.value)}
          />
          <textarea
            className="min-h-40 rounded bg-black/30 p-3"
            placeholder="Paste job description"
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
          />
          <button className="w-fit rounded bg-cyan-500 px-4 py-2 font-medium text-slate-950" onClick={runWorkflow}>
            Generate Application
          </button>
        </div>

        {result && (
          <div className="grid gap-4 lg:grid-cols-2">
            <section className="rounded-2xl border border-cyan-500/30 bg-cyan-900/10 p-4">
              <h2 className="mb-2 text-xl">Resume</h2>
              <pre className="overflow-auto whitespace-pre-wrap text-sm text-white/80">{result.resume}</pre>
            </section>
            <section className="rounded-2xl border border-purple-500/30 bg-purple-900/10 p-4">
              <h2 className="mb-2 text-xl">Cover Letter</h2>
              <pre className="overflow-auto whitespace-pre-wrap text-sm text-white/80">{result.cover_letter}</pre>
            </section>
            <section className="rounded-2xl border border-emerald-500/30 bg-emerald-900/10 p-4 lg:col-span-2">
              <h2 className="mb-2 text-xl">Verification</h2>
              <pre className="whitespace-pre-wrap text-sm text-white/80">{JSON.stringify(result.verification, null, 2)}</pre>
            </section>
          </div>
        )}
      </div>
    </main>
  );
}
