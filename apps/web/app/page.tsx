"use client";

import { useEffect } from "react";
import { Calculator } from "@/components/Calculator";
import { WaitlistForm } from "@/components/WaitlistForm";
import { trackEvent } from "@/lib/analytics";

const disclaimer =
  "This is an educational risk estimation tool, not financial advice. Exchange-specific liquidation prices may differ due to fees, maintenance margin, funding, margin mode, and exchange rules.";

export default function Home() {
  useEffect(() => {
    trackEvent("landing_page_viewed");
  }, []);

  return (
    <main>
      <section className="mx-auto grid min-h-screen max-w-6xl content-center px-5 py-16">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.28em] text-guard">
            LiquidationGuard.app
          </p>
          <h1 className="mt-5 text-5xl font-bold tracking-tight text-white md:text-7xl">
            Stop Getting Liquidated.
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
            Know your position size, margin requirement, and liquidation risk before you enter a futures trade.
          </p>
          <a
            href="#calculator"
            className="mt-8 inline-flex rounded-lg bg-guard px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-emerald-300"
          >
            Calculate Risk
          </a>
        </div>
      </section>

      <section className="border-y border-white/10 bg-white/[0.03]">
        <div className="mx-auto grid max-w-6xl gap-6 px-5 py-16 md:grid-cols-3">
          {[
            ["The problem", "Leverage makes small sizing mistakes expensive. Many traders enter before understanding where liquidation sits relative to their stop."],
            ["How it works", "Enter account size, direction, entry, stop, leverage, and risk. LiquidationGuard calculates sizing and highlights trade danger."],
            ["Core features", "Position sizing, margin estimate, liquidation distance, safety status, warnings, interpretation, and a copyable summary."],
          ].map(([title, body]) => (
            <article key={title} className="rounded-2xl border border-white/10 bg-slate-950 p-6">
              <h2 className="text-xl font-semibold text-white">{title}</h2>
              <p className="mt-3 leading-7 text-slate-300">{body}</p>
            </article>
          ))}
        </div>
      </section>

      <Calculator />

      <section className="mx-auto max-w-6xl px-5 py-16">
        <div className="grid gap-6 md:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6">
            <h2 className="text-2xl font-semibold text-white">Pro coming soon</h2>
            <p className="mt-3 leading-7 text-slate-300">
              Built for traders who want stronger risk controls before adding more leverage.
            </p>
            <ul className="mt-4 space-y-3 text-slate-300">
              {["Saved profiles", "Trade history", "Alerts", "Portfolio risk", "Exchange-specific models", "Advanced risk reports"].map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <WaitlistForm />
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6">
            <h2 className="text-2xl font-semibold text-white">Disclaimer</h2>
            <p className="mt-4 leading-7 text-slate-300">{disclaimer}</p>
          </div>
        </div>
      </section>
    </main>
  );
}
