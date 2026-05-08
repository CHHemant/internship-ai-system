import { Nav } from "@/components/nav";

export default function SettingsPage() {
  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white">
      <div className="mx-auto max-w-4xl py-10">
        <Nav />
        <h1 className="mb-4 text-3xl font-semibold">Settings</h1>
        <section className="rounded-2xl border border-white/20 bg-white/5 p-6">
          <p className="mb-3 text-white/80">Configure the deployment with environment variables:</p>
          <ul className="list-disc space-y-1 pl-6 text-white/70">
            <li>NEXT_PUBLIC_API_URL</li>
            <li>OPENAI_API_KEY</li>
            <li>OPENAI_MODEL</li>
            <li>DATABASE_URL</li>
            <li>REDIS_URL</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
