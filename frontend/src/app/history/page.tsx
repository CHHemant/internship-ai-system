"use client";

import { useEffect, useState } from "react";

import { Nav } from "@/components/nav";
import api from "@/lib/api";

type HistoryItem = {
  id: number;
  candidate_id: number | null;
  country: string;
  verification_score: number;
  created_at: string;
};

export default function HistoryPage() {
  const [items, setItems] = useState<HistoryItem[]>([]);

  useEffect(() => {
    api.get("/api/applications/history").then((response) => setItems(response.data));
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white">
      <div className="mx-auto max-w-5xl py-10">
        <Nav />
        <h1 className="mb-4 text-3xl font-semibold">Application History</h1>
        <div className="overflow-hidden rounded-2xl border border-white/20">
          <table className="w-full text-left text-sm">
            <thead className="bg-white/10">
              <tr>
                <th className="p-3">ID</th>
                <th className="p-3">Candidate</th>
                <th className="p-3">Country</th>
                <th className="p-3">Score</th>
                <th className="p-3">Created</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id} className="border-t border-white/10">
                  <td className="p-3">{item.id}</td>
                  <td className="p-3">{item.candidate_id ?? "-"}</td>
                  <td className="p-3">{item.country}</td>
                  <td className="p-3">{item.verification_score}</td>
                  <td className="p-3">{new Date(item.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
