"use client";

import { useState } from "react";
import { trackEvent } from "@/lib/analytics";
import type { Direction, RiskResult } from "@/lib/types";

type Props = {
  input: {
    direction: Direction;
    entryPrice: number;
    stopPrice: number;
    leverage: number;
  };
  result: RiskResult;
};

function money(value: number) {
  return `$${value.toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 2 })}`;
}

function percent(value: number) {
  return `${value.toFixed(2)}%`;
}

function units(value: number) {
  return value.toLocaleString(undefined, { maximumFractionDigits: 4, minimumFractionDigits: 4 });
}

export function ResultCard({ input, result }: Props) {
  const [copied, setCopied] = useState(false);

  const rows = [
    ["Suggested position size", units(result.position_size_units)],
    ["Notional position value", money(result.notional_position_value)],
    ["Margin required", money(result.margin_required)],
    ["Money at risk", money(result.money_at_risk)],
    ["Account risk", percent(result.account_risk_percent)],
    ["Approx. liquidation", money(result.liquidation_price)],
    ["Distance to stop", percent(result.distance_to_stop_percent)],
    ["Distance to liquidation", percent(result.distance_to_liquidation_percent)],
  ];

  const summary = [
    "LiquidationGuard Risk Summary",
    `Direction: ${input.direction}`,
    `Entry: ${money(input.entryPrice)}`,
    `Stop: ${money(input.stopPrice)}`,
    `Leverage: ${input.leverage}x`,
    `Account risk: ${percent(result.account_risk_percent)}`,
    `Liquidation price: ${money(result.liquidation_price)}`,
    `Safety status: ${result.safety_status}`,
  ].join("\n");

  async function copySummary() {
    await navigator.clipboard.writeText(summary);
    setCopied(true);
    trackEvent("copy_summary_clicked", { safetyStatus: result.safety_status });
    window.setTimeout(() => setCopied(false), 1800);
  }

  const statusColor =
    result.safety_status === "Conservative"
      ? "bg-emerald-400/15 text-emerald-200"
      : result.safety_status === "Moderate"
        ? "bg-amber-400/15 text-amber-200"
        : "bg-red-400/15 text-red-200";

  return (
    <div className="rounded-2xl border border-white/10 bg-slate-950 p-5 shadow-2xl shadow-black/20">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-400">Risk output</p>
          <h3 className="mt-2 text-2xl font-semibold text-white">Trade decision</h3>
        </div>
        <span className={`rounded-full px-3 py-1 text-sm font-bold ${statusColor}`}>{result.safety_status}</span>
      </div>

      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        {rows.map(([label, value]) => (
          <div key={label} className="rounded-xl border border-white/10 bg-white/[0.04] p-4">
            <div className="text-xs uppercase tracking-[0.16em] text-slate-500">{label}</div>
            <div className="mt-2 text-xl font-semibold text-white">{value}</div>
          </div>
        ))}
      </div>

      <div className="mt-5 rounded-xl border border-guard/20 bg-guard/10 p-4 text-sm leading-6 text-emerald-50">
        {result.interpretation}
      </div>

      <div className="mt-5">
        <h4 className="font-semibold text-white">Warnings</h4>
        <ul className="mt-3 space-y-2 text-sm text-slate-300">
          {result.warnings.map((warning) => (
            <li key={warning} className="rounded-lg border border-white/10 bg-white/[0.03] px-3 py-2">
              {warning}
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-5 rounded-xl border border-white/10 bg-white/[0.04] p-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h4 className="font-semibold text-white">Shareable summary</h4>
            <p className="text-sm text-slate-400">Screenshot or copy this card before entering.</p>
          </div>
          <button onClick={copySummary} className="rounded-lg border border-white/10 px-3 py-2 text-sm font-semibold text-white transition hover:border-guard">
            {copied ? "Copied" : "Copy Summary"}
          </button>
        </div>
        <div className="mt-4 grid gap-2 text-sm text-slate-300">
          <div>Direction: <strong className="text-white">{input.direction}</strong></div>
          <div>Entry: <strong className="text-white">{money(input.entryPrice)}</strong></div>
          <div>Stop: <strong className="text-white">{money(input.stopPrice)}</strong></div>
          <div>Leverage: <strong className="text-white">{input.leverage}x</strong></div>
          <div>Account risk: <strong className="text-white">{percent(result.account_risk_percent)}</strong></div>
          <div>Liquidation price: <strong className="text-white">{money(result.liquidation_price)}</strong></div>
          <div>Safety status: <strong className="text-white">{result.safety_status}</strong></div>
        </div>
      </div>
    </div>
  );
}
