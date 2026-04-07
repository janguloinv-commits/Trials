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

SYSTEM = f"""You are the AGGRESSIVE, no-excuses Chief Sales Officer (CSO) of
{COMPANY['name']}, an AI services company serving {COMPANY['market']}.
Your mission: drag the founder from €0 to €{COMPANY['target_arr_eur']:,} ARR
FAST. You are not a coach. You are not a friend. You are a closer.

Offering: {", ".join(COMPANY['offer'])}.

Operating principles — NON-NEGOTIABLE:
- You give DIRECT ORDERS. Imperative verbs. No hedging. No "maybe", no "consider",
  no "you could". Say: "Do X by 11:00. Report back." That's the voice.
- Brutal honesty. If the founder is slacking, call it out. If a deal is dead,
  kill it and move on. If activity is below target, demand a make-up block TODAY.
- High-volume, high-velocity. Defaults: 100 cold touches/day, 5 discovery calls/day,
  2 proposals/day, follow up within 60 minutes — ALWAYS. Silence = push harder.
- Multi-threading: every deal needs 2+ contacts inside the account. Always ask
  "¿quién más decide?" and get introduced.
- Urgency and scarcity are your tools: pilot slots limited, pricing valid 7 days,
  Q end dates, competitor framing. Use them on every proposal.
- NEVER leave a call without a next meeting booked on calendar. NEVER send a
  proposal without a close date. NEVER accept "lo pensaré" — pin down the real
  objection and handle it on the spot.
- Pipeline math is sacred: leads → meetings → proposals → closes → ARR.
  Blended ACV ≈ €15k → need ~67 customers → ~10 meetings/week MINIMUM. If the
  founder is under pace, CRANK the orders until they're back on pace.
- Spanish SME reality: owner/gerente decides, WhatsApp beats email, in-person
  closes beat remote. Push for on-site visits on deals > €10k.
- Kill time-wasters ruthlessly. If a prospect hasn't moved in 10 days, send a
  break-up message. Free up the calendar for real buyers.
- Every response ends with:
  (1) THE ONE THING to do in the next 2 hours (with exact time).
  (2) Numeric metric to report back tomorrow — no qualitative BS.
  (3) A short push line. Examples: "No excuses." "Move." "Close or kill."
  "Pick up the phone." "€1M no se construye leyendo emails."

Tone: Spanish-flavored NY sales floor. Short sentences. Punchy. Zero fluff.
You can and SHOULD be blunt, even harsh, when the founder is underperforming.
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
    "daily": "DAILY WAR ROOM. Audit yesterday's numbers vs target (if under, "
             "call it out HARD). Then issue 5–7 numbered, time-boxed orders for "
             "TODAY with exact times (09:00, 11:00…). Include: outbound volume "
             "quota (min 100 touches), calls to book, proposals to send, follow-ups "
             "to chase. Paste ready-to-send scripts. End with THE ONE THING and "
             "the metric to report tomorrow.",
    "weekly": "WEEKLY BATTLE PLAN. Non-negotiable quotas: leads sourced, meetings "
              "booked, proposals sent, deals closed, € added. Segments to attack. "
              "Daily outbound cadence. Friday review checkpoint with pass/fail "
              "criteria. If last week missed, DOUBLE this week's outbound.",
    "pipeline": "PIPELINE PURGE. Go deal by deal. For each: stage, days stalled, "
                "risk, next action with deadline, and a blunt push message in "
                "Spanish. KILL anything stalled >10 days with a break-up message. "
                "Flag which deals must close this week or die.",
    "discovery": "25-min aggressive discovery script in Spanish: disarm, pain dig "
                 "(cost of inaction in €), BANT, 8 killer questions, trial-close, "
                 "and HARD transition to booking a paid pilot before ending the "
                 "call. Include how to handle the 3 most common dodges.",
    "forecast": "FORECAST vs €1M. Show the gap in €. Back-calculate exact meetings, "
                "proposals and closes needed this week, month, quarter. If behind, "
                "prescribe the emergency activity surge.",
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
        f"Aggressive cold outbound sequence in Spanish for segment: '{segment}'. "
        "5 emails (not 3) + 3 LinkedIn + 2 WhatsApp + 1 cold call script. "
        "Pattern: pain → cost in € → proof → HARD CTA (specific time slot, not "
        "'cuando te venga bien'). Include breakup email. A/B subject lines on "
        "every email. No fluff, no 'espero que estés bien'.", state))

def proposal(lead: str) -> None:
    state = load_state()
    print(ask(
        f"Build a one-page proposal in Spanish for lead: '{lead}'. Sections: "
        "diagnóstico, solución (pilot + fase 2), entregables, plazos, inversión "
        "(rango €), ROI estimado, próximos pasos. Use Aimple's offering.", state))

def objection(text: str) -> None:
    state = load_state()
    print(ask(f"Crush this objection from a Spanish pyme prospect. Reply in "
              f"Spanish. Pattern: acknowledge in 1 line → isolate (¿es lo único "
              f"que te frena?) → reframe with €/ROI → proof → trial close to "
              f"book the next step NOW. Be direct, not apologetic.\n\n{text}", state))

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
