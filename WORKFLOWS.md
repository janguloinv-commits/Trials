# Aimple CSO Bot — Workflows

An **aggressive, no-excuses** Chief Sales Officer bot that drags you from €0 → **€1M ARR** at Aimple (AI services for Spanish SMEs). It gives direct orders, calls you out when you're behind quota, kills dead deals, and demands numeric report-backs every day.

## Operating mode: AGGRESSIVE
- Imperative orders with exact times. No hedging, no "maybe".
- Daily quotas: **100 cold touches, 5 discovery calls, 2 proposals, <60-min follow-ups.**
- Multi-threading required on every deal (2+ contacts inside the account).
- Urgency + scarcity baked into every proposal (7-day price validity, limited pilot slots).
- Never leave a call without the next meeting booked. Never send a proposal without a close date.
- Break-up message on any deal stalled >10 days — free the calendar.
- Daily standup = war room. If yesterday missed target, today's orders double the outbound.

## The pipeline math (anchor everything to this)
Target: **€1,000,000 ARR**. Assume blended ACV ≈ **€15,000**.
→ **~67 closed customers/year** → ~270 qualified proposals → ~540 discovery calls → ~5,400 qualified leads. Weekly: **~10 meetings, ~5 proposals, ~1.3 closes**.

---

## Core workflows

| # | Command | What it does |
|---|---|---|
| 1 | `daily` | Morning standup. 3–5 numbered orders for today + #1 priority + tomorrow's report-back. |
| 2 | `weekly` | Weekly plan: targets, segments, cadence, checkpoints. |
| 3 | `pipeline` | Deal-by-deal review, risk, next action, Spanish nudge messages. |
| 4 | `forecast` | ARR forecast vs €1M, gap analysis, required activity. |
| 5 | `outreach "<segment>"` | 3 emails + LinkedIn + WhatsApp cold sequence in Spanish, with A/B subject lines. |
| 6 | `discovery` | 25-min discovery call script in Spanish (BANT + pain + 8 questions + transition). |
| 7 | `proposal "<lead>"` | One-page Spanish proposal: diagnóstico, solución, plazos, inversión, ROI. |
| 8 | `objection "<text>"` | Empathy → reframe → proof → CTA in Spanish. |
| 9 | `chat` | Free-form CSO conversation with state context. |

## Recommended segments (Spanish SMEs)
- **Clínicas** (dentales, estética, fisio) → appointment agents + WhatsApp bots
- **Asesorías / gestorías** → document processing + RAG knowledge base
- **Inmobiliarias** → lead qualification + follow-up agents
- **E-commerce / retail** → customer support chatbot + returns automation
- **Hostelería / restaurantes** → reservations + reviews management
- **Despachos de abogados** → document drafting + intake agents
- **Talleres / servicios técnicos** → scheduling + parts lookup

## Offer ladder
1. **Audit AI (€1.5–3k, 2 semanas)** — low-friction entry, discovers pains.
2. **Pilot (€6–12k, 4–6 semanas)** — one high-ROI use case in production.
3. **Retainer (€1.5–4k/mes)** — iteration, monitoring, new use cases → recurring ARR.
4. **Suite Aimple (€20–40k + retainer)** — multi-workflow transformation.

## Weekly cadence the bot will enforce
- **Mon** — Weekly plan + 50 new leads sourced.
- **Tue/Thu** — Outbound blocks (email/LinkedIn/WhatsApp), 2h each.
- **Wed** — Discovery calls day. Target: 4+.
- **Fri** — Pipeline review, proposals sent, forecast update, retros.

## State tracked (`state.json`)
`mrr_eur`, `arr_eur`, `pipeline[]` (name, stage, value, next_step, due), `activity[]` log. Update manually or ask the bot in `chat` mode to update it for you.

## Run it
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python cso_bot.py              # today's orders
python cso_bot.py weekly
python cso_bot.py outreach "clínicas dentales Barcelona"
python cso_bot.py chat
```
