"use client";

import { FormEvent, useState } from "react";
import { joinWaitlist } from "@/lib/api";
import { trackEvent } from "@/lib/analytics";

const inputClass =
  "mt-2 w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none transition focus:border-guard";

const proFeatures = [
  "Saved profiles",
  "Trade history",
  "Alerts",
  "Portfolio risk",
  "Exchange-specific models",
  "Advanced risk reports",
];

export function WaitlistForm() {
  const [email, setEmail] = useState("");
  const [traderType, setTraderType] = useState("");
  const [desiredFeature, setDesiredFeature] = useState("Portfolio risk");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus(null);
    setError(null);
    setIsSubmitting(true);

    try {
      await joinWaitlist({
        email,
        trader_type: traderType || undefined,
        desired_feature: desiredFeature || undefined,
      });
      trackEvent("pro_waitlist_joined", { desiredFeature, traderType });
      setStatus("You're on the Pro waitlist.");
      setEmail("");
      setTraderType("");
      setDesiredFeature("Portfolio risk");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not join the waitlist.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="rounded-2xl border border-guard/20 bg-guard/10 p-6">
      <p className="text-sm font-semibold uppercase tracking-[0.22em] text-emerald-200">
        Pro waitlist
      </p>
      <h2 className="mt-3 text-2xl font-semibold text-white">Join the Pro waitlist</h2>
      <p className="mt-3 leading-7 text-slate-300">
        Pro is being built for traders who want stronger pre-trade risk controls:
        saved profiles, trade history, alerts, portfolio risk, exchange-specific
        liquidation models, and advanced risk reports.
      </p>

      <form onSubmit={onSubmit} className="mt-6 space-y-4">
        <label className="block text-sm font-medium text-slate-200">
          Email
          <input
            required
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className={inputClass}
            type="email"
            placeholder="you@example.com"
          />
        </label>

        <label className="block text-sm font-medium text-slate-200">
          Trader type optional
          <input
            value={traderType}
            onChange={(event) => setTraderType(event.target.value)}
            className={inputClass}
            type="text"
            placeholder="Scalper, swing trader, prop trader..."
          />
        </label>

        <label className="block text-sm font-medium text-slate-200">
          Most wanted Pro feature optional
          <select
            value={desiredFeature}
            onChange={(event) => setDesiredFeature(event.target.value)}
            className={inputClass}
          >
            {proFeatures.map((feature) => (
              <option key={feature}>{feature}</option>
            ))}
          </select>
        </label>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-lg bg-guard px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? "Joining..." : "Join Pro Waitlist"}
        </button>
      </form>

      {status ? <p className="mt-4 text-sm font-medium text-emerald-100">{status}</p> : null}
      {error ? <p className="mt-4 text-sm font-medium text-red-200">{error}</p> : null}
    </div>
  );
}
