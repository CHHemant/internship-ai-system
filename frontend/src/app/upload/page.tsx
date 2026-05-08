"use client";

import { useState } from "react";

import { Nav } from "@/components/nav";
import api from "@/lib/api";

export default function UploadPage() {
  const [status, setStatus] = useState<string>("");
  const [error, setError] = useState<string>("");

  async function handleUpload(formData: FormData) {
    const file = formData.get("resume") as File | null;
    if (!file) {
      setError("");
      setStatus("Please select a resume file.");
      return;
    }

    try {
      const payload = new FormData();
      payload.append("file", file);
      const response = await api.post("/api/resume/upload", payload, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setError("");
      setStatus(`Uploaded candidate #${response.data.candidate_id}`);
    } catch (uploadError) {
      console.error(uploadError);
      setStatus("");
      setError("Upload failed. Please verify the backend is running and try again.");
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white">
      <div className="mx-auto max-w-3xl py-10">
        <Nav />
        <h1 className="mb-4 text-3xl font-semibold">Resume Upload</h1>
        <form action={handleUpload} className="space-y-4 rounded-2xl border border-white/20 bg-white/5 p-6">
          <input className="w-full rounded bg-black/30 p-3" type="file" name="resume" accept=".pdf,.docx,.txt" />
          <button className="rounded bg-cyan-500 px-4 py-2 font-medium text-slate-950" type="submit">
            Upload & Parse
          </button>
        </form>
        {status && <p className="mt-4 text-cyan-300">{status}</p>}
        {error && <p className="mt-4 text-rose-300">{error}</p>}
      </div>
    </main>
  );
}
