"use client";

import { FormEvent, useState } from "react";
import { submitFeedback } from "@/lib/api";
import { trackEvent } from "@/lib/analytics";

export function FeedbackForm() {
  const [rating, setRating] = useState(5);
  const [message, setMessage] = useState("");
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await submitFeedback({
      rating,
      message: message || undefined,
      email: email || undefined,
    });
    trackEvent("feedback_submitted", { rating });
    setStatus("Thanks. Your feedback was recorded.");
    setMessage("");
    setEmail("");
  }

  return (
    <form onSubmit={onSubmit} className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
      <h3 className="text-lg font-semibold text-white">Was this useful?</h3>
      <div className="mt-4 grid gap-4 sm:grid-cols-[120px_1fr]">
        <label className="text-sm text-slate-300">
          Rating
          <select value={rating} onChange={(event) => setRating(Number(event.target.value))} className="mt-2 w-full rounded-lg border border-white/10 bg-white/5 px-3 py-3 text-white outline-none focus:border-guard">
            {[1, 2, 3, 4, 5].map((value) => (
              <option key={value} value={value}>{value}</option>
            ))}
          </select>
        </label>
        <label className="text-sm text-slate-300">
          Email optional
          <input value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 w-full rounded-lg border border-white/10 bg-white/5 px-3 py-3 text-white outline-none focus:border-guard" type="email" />
        </label>
      </div>
      <label className="mt-4 block text-sm text-slate-300">
        Message optional
        <textarea value={message} onChange={(event) => setMessage(event.target.value)} className="mt-2 min-h-24 w-full rounded-lg border border-white/10 bg-white/5 px-3 py-3 text-white outline-none focus:border-guard" />
      </label>
      <button className="mt-4 rounded-lg border border-white/10 px-4 py-2 text-sm font-semibold text-white transition hover:border-guard" type="submit">
        Send feedback
      </button>
      {status ? <p className="mt-3 text-sm text-emerald-200">{status}</p> : null}
    </form>
  );
}
