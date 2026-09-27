"""Assemble everything for the final synthesis agent into synthesis/.

Outputs:
  ledger_by_decision/<Q..>.md   every ledger line (all waves) grouped by decision keyword
  cards_merged.jsonl            all abstract-screening cards (relevance 2-3), deduplicated by title
  cards_by_decision/<Q..>.md    compact claim lists per decision from the cards
  NOTES_INDEX.md                every full-text note: path | title line | wave
  STATS.md                      counts
"""
import glob, json, re
from collections import defaultdict
from pathlib import Path

LR = Path(__file__).resolve().parent.parent
OUT = LR / "synthesis"

DECISIONS = {
    "Q01_action_head": r"head|q01|regress|diffusion|flow|vq|cvae|l1|mse|token",
    "Q02_action_space": r"action_space|q02|delta|absolute|joint|velocity|end.?effector|relative",
    "Q03_vision_encoder": r"vision|encoder|q03|dino|siglip|clip|mae|r3m|vc-1|frozen|fine.?tun|pretrain|backbone",
    "Q04_3d_depth": r"3d|q04|depth|point|voxel",
    "Q05_augmentation": r"augment|q05|green|jitter|background|relight",
    "Q06_chunking_horizon": r"chunk|q06|horizon|ensembl",
    "Q07_history_proprio": r"history|q07|memory|proprio|copycat",
    "Q08_language": r"language|q08|film|instruction|text",
    "Q09_aux_objectives": r"aux|q09|future|world.?model|inverse|reconstruct",
    "Q10_latency_async": r"latency|q10|async|real.?time|execution|smooth|jerk|rtc|hz",
    "Q11_cameras": r"camera|q11|wrist|view",
    "Q12_model_size": r"size|q12|param|small|large|scale",
    "Q13_data": r"data|q13|demo|diversity|recovery|quality|co.?train",
    "Q14_robustness": r"robust|q14|lighting|ood|generaliz|shift|distractor|novel",
}
DRX = {k: re.compile(v, re.I) for k, v in DECISIONS.items()}

# ---- ledgers
ledger_files = [LR / "fulltext/LEDGER.md", LR / "wave3/LEDGER.md", LR / "wave4/LEDGER.md"]
by_dec = defaultdict(list)
n_ledger = 0
for lf in ledger_files:
    if not lf.exists():
        continue
    wave = lf.parent.name
    for line in lf.read_text(errors="replace").splitlines():
        if "|" not in line or line.startswith("#"):
            continue
        n_ledger += 1
        parts = [p.strip() for p in line.split("|")]
        key = parts[1] if len(parts) > 1 else line
        hit = [k for k, rx in DRX.items() if rx.search(key)] or [k for k, rx in DRX.items() if rx.search(line)][:1]
        for k in hit or ["UNSORTED"]:
            by_dec[k].append(f"[{wave}] {line}")
(OUT / "ledger_by_decision").mkdir(parents=True, exist_ok=True)
for k, lines in by_dec.items():
    (OUT / "ledger_by_decision" / f"{k}.md").write_text(f"# {k} — {len(lines)} ledger lines\n" + "\n".join(lines) + "\n")

# ---- cards
cards, seen = [], set()
for f in sorted(glob.glob(str(LR / "screen/cards_*.jsonl")) + glob.glob(str(LR / "screen/rcards_*.jsonl"))):
    for line in open(f, errors="replace"):
        try:
            c = json.loads(line)
        except ValueError:
            continue
        t = re.sub(r"[^a-z0-9]", "", (c.get("title") or "").lower())
        if not t or t in seen:
            continue
        seen.add(t)
        cards.append(c)
with (OUT / "cards_merged.jsonl").open("w") as f:
    for c in cards:
        f.write(json.dumps(c) + "\n")
qmap = {k.split("_")[0]: k for k in DECISIONS}
by_q = defaultdict(list)
for c in cards:
    for cl in c.get("claims") or []:
        q = (cl.get("decision") or "")[:3]
        if q in qmap:
            by_q[qmap[q]].append(
                f"- ({c.get('year')}, rel{c.get('relevance')}, {c.get('evidence_strength')}) {c.get('title','')[:90]} :: "
                f"{cl.get('claim','')[:300]} → {cl.get('direction','')[:80]} [{cl.get('conditions','')[:120]}]")
(OUT / "cards_by_decision").mkdir(exist_ok=True)
for k, lines in by_q.items():
    (OUT / "cards_by_decision" / f"{k}.md").write_text(f"# {k} — {len(lines)} abstract-level claims\n" + "\n".join(lines) + "\n")

# ---- notes index
rows = []
for wave in ["fulltext", "wave3", "wave4", "realtime"]:
    for p in sorted(glob.glob(str(LR / wave / "notes/*.md"))):
        if p.endswith("_TEMPLATE.md"):
            continue
        first = open(p, errors="replace").readline().strip()
        rows.append(f"{wave} | {Path(p).relative_to(LR)} | {first[:160]}")
(OUT / "NOTES_INDEX.md").write_text("# Full-text notes index (wave | path | title line)\n" + "\n".join(rows) + "\n")

stats = {
    "ledger_lines": n_ledger,
    "cards": len(cards),
    "cards_rel3": sum(1 for c in cards if c.get("relevance") == 3),
    "fulltext_notes": len(rows),
    "notes_per_wave": {w: sum(1 for r in rows if r.startswith(w + " ")) for w in ["fulltext", "wave3", "wave4", "realtime"]},
    "ledger_lines_per_decision": {k: len(v) for k, v in sorted(by_dec.items())},
    "card_claims_per_decision": {k: len(v) for k, v in sorted(by_q.items())},
}
(OUT / "STATS.md").write_text("# Evidence base statistics\n```json\n" + json.dumps(stats, indent=1) + "\n```\n")
print(json.dumps(stats, indent=1))
