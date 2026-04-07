"""
Aimple CSO Bot — Your AI Chief Sales Officer.

Goal: Drive Aimple (AI services for Spanish SMEs) from €0 to €1M ARR.
Usage:
    export ANTHROPIC_API_KEY=...
    python cso_bot.py                      # Daily standup: today's orders
    python cso_bot.py weekly               # Weekly plan
    python cso_bot.py pipeline             # Review pipeline & next actions
    python cso_bot.py outreach "<segment>" # Draft cold outreach (ES)
    python cso_bot.py discovery            # Discovery call script
    python cso_bot.py proposal "<lead>"    # Build a proposal
    python cso_bot.py objection "<text>"   # Handle objection
    python cso_bot.py forecast             # ARR forecast vs €1M target
    python cso_bot.py chat                 # Free-form CSO chat
"""

from __future__ import annotations
import json, os, sys, datetime, pathlib
from anthropic import Anthropic

MODEL = "claude-opus-4-6"
ROOT = pathlib.Path(__file__).parent
STATE = ROOT / "state.json"

COMPANY = {
    "name": "Aimple",
    "market": "Spanish SMEs (pymes)",
    "offer": [
        "Chatbots (web, WhatsApp, voice)",
        "Internal workflow automation (RPA + LLM)",
        "Appointment management & scheduling agents",
        "Lead generation & outbound AI",
        "Document processing / RAG knowledge bases",
        "Custom AI integrations (ERP/CRM)",
    ],
    "target_arr_eur": 1_000_000,
    "language": "es-ES",
}

SYSTEM = f"""You are the Chief Sales Officer (CSO) of {COMPANY['name']}, an AI
services company serving {COMPANY['market']}. Your mission: take the founder
from €0 to €{COMPANY['target_arr_eur']:,} ARR.

Offering: {", ".join(COMPANY['offer'])}.

Operating principles:
- You give ORDERS, not suggestions. Short, numbered, time-boxed, concrete.
- Every order must be executable today and tied to pipeline math
  (leads → meetings → proposals → closes → ARR).
- Assume the founder is solo or small team. Prioritize leverage.
- Spanish SME reality: relationship-driven, price-sensitive, WhatsApp-native,
  decision-makers = owner/gerente. Prefer ES when drafting customer-facing copy.
- Benchmarks to anchor targets: ACV €6k–€30k, sales cycle 3–8 weeks,
  close rate 15–25% from qualified meetings. Adjust as real data lands.
- Always end with: (1) today's single most important action, (2) what to
  report back tomorrow.
"""

def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {
        "created": str(datetime.date.today()),
        "mrr_eur": 0, "arr_eur": 0,
        "pipeline": [],  # {name, stage, value_eur, next_step, due}
        "activity": [],  # log of daily orders/results
    }

def save_state(s: dict) -> None:
    STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False))

def ask(prompt: str, state: dict) -> str:
    client = Anthropic()
    ctx = f"\n\n<state>\n{json.dumps(state, ensure_ascii=False)}\n</state>"
    msg = client.messages.create(
        model=MODEL, max_tokens=2000, system=SYSTEM,
        messages=[{"role": "user", "content": prompt + ctx}],
    )
    return msg.content[0].text

WORKFLOWS = {
    "daily": "Run the daily standup. Given the state, issue 3–5 numbered orders "
             "for TODAY to advance pipeline toward €1M ARR. Include exact scripts/"
             "messages where relevant. End with the #1 priority and tomorrow's report-back.",
    "weekly": "Produce the weekly sales plan: targets (leads, meetings, proposals, "
              "closes, €), segments to hit this week, content/outbound cadence, "
              "and review checkpoints.",
    "pipeline": "Review every deal in pipeline. For each: diagnose stage risk, "
                "next best action, and a nudge message in Spanish. Flag stalled deals.",
    "discovery": "Give me a 25-minute discovery call script in Spanish for a pyme "
                 "gerente: qualification (BANT+pain), 8 killer questions, and a "
                 "transition to proposing a paid pilot.",
    "forecast": "Compute ARR forecast from pipeline vs €1M target. Show the gap "
                "and the exact number of meetings/proposals needed this quarter to close it.",
}

def run_workflow(key: str, extra: str = "") -> None:
    state = load_state()
    prompt = WORKFLOWS[key] + (f"\n\nExtra: {extra}" if extra else "")
    out = ask(prompt, state)
    print(out)
    state["activity"].append({"date": str(datetime.date.today()), "workflow": key, "output": out[:500]})
    save_state(state)

def outreach(segment: str) -> None:
    state = load_state()
    print(ask(
        f"Draft a cold outbound sequence in Spanish for segment: '{segment}'. "
        "3 emails + 1 LinkedIn + 1 WhatsApp. Short, specific pain, soft CTA to a "
        "15-min call. Include subject lines and A/B variant for email 1.", state))

def proposal(lead: str) -> None:
    state = load_state()
    print(ask(
        f"Build a one-page proposal in Spanish for lead: '{lead}'. Sections: "
        "diagnóstico, solución (pilot + fase 2), entregables, plazos, inversión "
        "(rango €), ROI estimado, próximos pasos. Use Aimple's offering.", state))

def objection(text: str) -> None:
    state = load_state()
    print(ask(f"Handle this objection from a Spanish pyme prospect, in Spanish, "
              f"with empathy + reframe + proof + CTA:\n\n{text}", state))

def chat() -> None:
    state = load_state()
    print("CSO chat (Ctrl-C to exit). Ask anything.")
    history = []
    client = Anthropic()
    while True:
        try:
            u = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); return
        if not u: continue
        history.append({"role": "user", "content": u})
        r = client.messages.create(
            model=MODEL, max_tokens=1500,
            system=SYSTEM + f"\n\n<state>{json.dumps(state, ensure_ascii=False)}</state>",
            messages=history)
        t = r.content[0].text
        history.append({"role": "assistant", "content": t})
        print(f"\ncso> {t}")

def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY first.", file=sys.stderr); sys.exit(1)
    argv = sys.argv[1:]
    cmd = argv[0] if argv else "daily"
    arg = " ".join(argv[1:])
    if cmd in WORKFLOWS: run_workflow(cmd)
    elif cmd == "outreach": outreach(arg or "clínicas dentales Madrid")
    elif cmd == "proposal": proposal(arg or "unnamed lead")
    elif cmd == "objection": objection(arg or "Es demasiado caro")
    elif cmd == "chat": chat()
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
