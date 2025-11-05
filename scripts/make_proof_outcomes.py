#!/usr/bin/env python3
"""
Create a JSON file that mimics `proof_outcomes_by_problem.json`
from the folder hierarchy produced by the *corrected_proofs* zip.

Directory layout (after unzip):
    <root>/
        0/
            AI-MO_Kimina-Prover-Preview-Distill-7B/
                1.txt ... 8.txt   # present ⇒ correct proof (1), absent ⇒ 0
            ByteDance-Seed_BFS-Prover/
                …
        1/
            …
        …
"""

import sys
import os
import json
from typing import Dict, List

MAX_ATTEMPTS = 24

def build_outcomes(root: str) -> Dict[str, Dict[str, List[int]]]:
    outcomes: Dict[str, Dict[str, List[int]]] = {}

    prob_dirs = [d for d in os.listdir(root)
                 if os.path.isdir(os.path.join(root, d)) and d.isdigit()]
    for prob_name in sorted(prob_dirs, key=int):
        prob_path = os.path.join(root, prob_name)
        outcomes[prob_name] = {}

        for model_name in sorted(os.listdir(prob_path)):
            model_path = os.path.join(prob_path, model_name)
            if not os.path.isdir(model_path):
                continue

            attempts = [0] * MAX_ATTEMPTS          # 1-based → 0…max_attempt-1

            # --- second pass to set 1s -------------------------------
            for entry in os.listdir(model_path):
                if not entry.lower().endswith('.txt'):
                    continue
                try:
                    num = int(os.path.splitext(entry)[0])
                except ValueError:
                    continue
                if 1 <= num <= MAX_ATTEMPTS:
                    attempts[num - 1] = 1

            outcomes[prob_name][model_name] = attempts

    return outcomes



def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python make_proof_outcomes.py <root_dir> <output_json>", file=sys.stderr)
        sys.exit(1)

    root_dir, out_path = sys.argv[1], sys.argv[2]

    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    data = build_outcomes(root_dir)

    # pretty‑print with 2‑space indent (matches the example you gave)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Finished – JSON saved to {out_path}")


if __name__ == "__main__":
    main()
