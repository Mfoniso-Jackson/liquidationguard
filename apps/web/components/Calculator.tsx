"use client";

import { FormEvent, useMemo, useState } from "react";
import { calculateRisk } from "@/lib/api";
import { trackEvent } from "@/lib/analytics";
import type { Direction, RiskResponse } from "@/lib/types";
import { FeedbackForm } from "./FeedbackForm";
import { ResultCard } from "./ResultCard";

const inputClass =
  "mt-2 w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none transition focus:border-guard";

const presets = [
  { label: "Conservative", value: 1 },
  { label: "Standard", value: 2 },
  { label: "Aggressive", value: 5 },
];

export function Calculator() {
  const [accountBalance, setAccountBalance] = useState(1000);
  const [direction, setDirection] = useState<Direction>("Long");
  const [entryPrice, setEntryPrice] = useState(100);
  const [stopPrice, setStopPrice] = useState(95);
  const [leverage, setLeverage] = useState(10);
  const [riskPercent, setRiskPercent] = useState(2);
  const [result, setResult] = useState<RiskResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const summaryInput = useMemo(
    () => ({ direction, entryPrice, stopPrice, leverage }),
    [direction, entryPrice, stopPrice, leverage],
  );

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    trackEvent("calculation_submitted", { direction, leverage, riskPercent });

    try {
      const response = await calculateRisk({
        account_balance: accountBalance,
        direction,
        entry_price: entryPrice,
        stop_price: stopPrice,
        leverage,
        risk_percent: riskPercent,
        client_metadata: { source: "web" },
      });
      setResult(response);
    } catch (caught) {
      setResult(null);
      setError(caught instanceof Error ? caught.message : "Something went wrong.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section id="calculator" className="mx-auto max-w-6xl px-5 py-20">
      <div className="mb-8 max-w-2xl">
        <p className="text-sm font-semibold uppercase tracking-[0.24em] text-guard">Risk calculator</p>
        <h2 className="mt-3 text-3xl font-semibold text-white md:text-4xl">
          Know your risk before you enter a trade.
        </h2>
        <p className="mt-4 text-slate-300">
          Enter the trade setup, then review sizing, margin, liquidation distance, warnings, and a plain-English decision.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_0.95fr]">
        <form onSubmit={onSubmit} className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 shadow-2xl shadow-black/20">
          <div className="grid gap-5 md:grid-cols-2">
            <label className="text-sm font-medium text-slate-200">
              Account balance
              <input className={inputClass} min="0" step="0.01" type="number" value={accountBalance} onChange={(event) => setAccountBalance(Number(event.target.value))} />
            </label>

            <label className="text-sm font-medium text-slate-200">
              Trade direction
              <select className={inputClass} value={direction} onChange={(event) => setDirection(event.target.value as Direction)}>
                <option>Long</option>
                <option>Short</option>
              </select>
            </label>

            <label className="text-sm font-medium text-slate-200">
              Entry price
              <input className={inputClass} min="0" step="0.0001" type="number" value={entryPrice} onChange={(event) => setEntryPrice(Number(event.target.value))} />
            </label>

            <label className="text-sm font-medium text-slate-200">
              Stop price
              <input className={inputClass} min="0" step="0.0001" type="number" value={stopPrice} onChange={(event) => setStopPrice(Number(event.target.value))} />
            </label>

            <label className="text-sm font-medium text-slate-200">
              Leverage
              <input className={inputClass} min="1" step="0.1" type="number" value={leverage} onChange={(event) => setLeverage(Number(event.target.value))} />
            </label>

            <label className="text-sm font-medium text-slate-200">
              Risk percentage
              <input className={inputClass} min="0.01" max="10" step="0.01" type="number" value={riskPercent} onChange={(event) => setRiskPercent(Number(event.target.value))} />
            </label>
          </div>

          <div className="mt-5 flex flex-wrap gap-2">
            {presets.map((preset) => (
              <button
                key={preset.value}
                type="button"
                onClick={() => setRiskPercent(preset.value)}
                className="rounded-full border border-white/10 px-3 py-2 text-sm text-slate-200 transition hover:border-guard hover:text-white"
              >
                {preset.label} {preset.value}%
              </button>
            ))}
          </div>

          {error ? (
            <div className="mt-5 rounded-lg border border-danger/30 bg-danger/10 p-4 text-sm text-red-100">
              {error}
            </div>
          ) : null}

          <button
            type="submit"
            disabled={isSubmitting}
            className="mt-6 w-full rounded-lg bg-guard px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting ? "Calculating..." : "Calculate Risk"}
          </button>
        </form>

        <div className="space-y-6">
          {result ? (
            <>
              <ResultCard input={summaryInput} result={result.result} />
              <FeedbackForm />
            </>
          ) : (
            <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6 text-slate-300">
              Results will appear here after calculation. Use them as a pre-trade risk check, not as a signal to enter.
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
