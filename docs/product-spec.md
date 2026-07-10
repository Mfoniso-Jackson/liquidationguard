# LiquidationGuard Product Spec

## Promise

Know your risk before you enter a trade.

## Audience

Futures traders who want a calm pre-trade sizing and liquidation check before opening leveraged positions.

## Tone

Calm, professional, trustworthy, and risk-first. Avoid hype, casino language, and profit promises.

## v1 Scope

- Landing page
- Risk calculator
- Backend API calculation engine
- Anonymous calculation persistence foundation
- Feedback capture
- Shareable result summary with copy action
- Pro roadmap placeholder
- Pro waitlist capture
- Legal and safety disclaimer

## Pro Waitlist

The waitlist validates demand before adding subscriptions or payment rails.

Fields:

- Email
- Trader type optional
- Desired Pro feature optional

## Out of Scope

- Authentication
- Subscriptions or payments
- Exchange APIs
- AI
- Tokens
- Trading execution
- Exchange-specific margin engines

## Core Calculation

The product estimates position sizing, notional value, margin required, money at risk, account risk, approximate liquidation price, distance to stop, distance to liquidation, safety status, warnings, and a plain-English interpretation.

Liquidation estimates are intentionally approximate and educational.
