import { Nav } from "@/components/nav";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-cyan-950 p-6 text-white">
      <div className="mx-auto max-w-5xl py-10">
        <Nav />
        <section className="rounded-3xl border border-white/20 bg-white/10 p-10 shadow-2xl backdrop-blur">
          <p className="mb-4 text-sm uppercase tracking-[0.2em] text-cyan-300">AI Internship Copilot</p>
          <h1 className="mb-5 text-4xl font-semibold">Autonomous Multi-Agent Internship Application System</h1>
          <p className="max-w-3xl text-white/80">
            Parse resumes and job descriptions, generate ATS-ready resumes and personalized cover letters,
            verify quality, and run retry-based orchestration with intelligent agent routing.
          </p>
        </section>
      </div>
    </main>
  );
}
