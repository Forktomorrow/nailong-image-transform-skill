#!/usr/bin/env python3
"""Score a Nailong transformation using the documented human-review rubric."""
import argparse, json

WEIGHTS = {"recognition": 15, "topology": 20, "composition": 20, "style": 25, "fusion": 20}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sample", required=True)
    p.add_argument("--scores", required=True, help="JSON, each value 0..5")
    p.add_argument("--notes", default="")
    args = p.parse_args()
    scores = json.loads(args.scores)
    if set(scores) != set(WEIGHTS) or any(not isinstance(scores[k], (int, float)) or not 0 <= scores[k] <= 5 for k in WEIGHTS):
        raise SystemExit("必须提供 recognition/topology/composition/style/fusion 五项 0..5 评分")
    total = round(sum(scores[k] / 5 * w for k, w in WEIGHTS.items()), 1)
    result = {"sample": args.sample, "scores": scores, "total": total,
              "gate": "usable" if total >= 70 else "layout-only" if total >= 50 else "reject",
              "notes": args.notes}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
