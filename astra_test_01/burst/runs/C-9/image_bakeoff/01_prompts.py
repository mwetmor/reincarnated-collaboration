#!/usr/bin/env python3
"""C-9 image bake-off (R-C9-79): the prompt each candidate receives, built from what ASTRA received.

    python3 01_prompts.py

"The same inputs and brief text Astra had" is taken literally: the source is the lane's own
rendered brief (~/astra-burst/runs/C-9/<burst>/brief.txt), the file the Astra agent actually
read. The lane builds it as REGISTER CARD + BURST RULES + TASK + REFERENCES + RETURN. A raw
image model gets:

    REGISTER CARD        verbatim (lines before "## 4. Typed bursts")
    TASK                 the task text, minus the LANE's operational sentences only
    REFERENCES           the same roles, in the same order as the images are attached

and NOT the burst rules or the return schema, which instruct an AGENT about its sandbox,
its receipt and its retries -- none of which a direct API call has. Every removal is a
listed string, checked to be present before it is removed, and recorded next to the prompt,
so the difference between what Astra read and what a candidate read is exactly that list.

What is NOT equalised, and is reported rather than hidden: Astra is an AGENT. It read the
brief, wrote its own image prompt, looked at its results and retried the ones it judged
wrong (NB-1 used 4 image calls for 2 deliveries, NB-G1 3, T8P-B 2). The candidates get one
call per variant and no judgement. That is the actual trade on offer -- a pay-per-image
model in place of an agentic lane -- so the comparison is left in that shape.
"""
import hashlib
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
BURST = HERE.parents[2]
LANE = pathlib.Path.home() / "astra-burst" / "runs" / "C-9"

# job -> (Astra burst whose brief.txt is the source, aspect for the call)
JOBS = {"J1": ("NB-1", "2:3"), "J2": ("NB-G1", "2:3"), "J3": ("T8P-B", "3:2"), "J4": ("IBO-J4", "3:2")}

# (burst, exact string to remove or replace, replacement) -- lane operations only
EDITS = [
    ("NB-G1", "Use image_gen in EDIT mode on IMAGE 1 and deliver", "EDIT IMAGE 1 and deliver"),
    ("NB-G1", " If the image model returns a darker or gradient background anyway, DO NOT spend a "
              "retry on it; deliver the image.", ""),
    ("T8P-B", "Use image_gen in EDIT mode on IMAGE 1 and deliver", "EDIT IMAGE 1 and deliver"),
    ("T8P-B", " If the image model returns a darker or gradient background anyway, DO NOT spend a "
              "retry on it and still deliver the image: the figures are cut out afterwards by their "
              "exact 3D outlines, so the background colour does not decide success. Spend retries "
              "ONLY on the faults named below.", ""),
]


def main() -> None:
    out = HERE / "prompts"
    out.mkdir(exist_ok=True)
    rec = {}
    for job, (bid, aspect) in JOBS.items():
        brief = (LANE / bid / "brief.txt").read_text()
        card = brief.split("## 4. Typed bursts")[0].rstrip()
        task = json.loads((BURST / "briefs" / "C-9" / ("%s.task.json" % bid)).read_text())
        text, removed = task["text"], []
        # 1. the burst header paragraph ("GENERATE BURST ... task_id ...")
        head, rest = text.split("\n\n", 1)
        assert head.startswith("GENERATE BURST"), (job, head[:40])
        removed.append(head)
        text = rest
        # 2. everything from the lane's call/retry/receipt paragraph to the end
        cut = min(i for i in (text.find("Two image_gen"), text.find("One image_gen")) if i >= 0)
        removed.append(text[cut:])
        text = text[:cut].rstrip()
        # 3. named in-line lane sentences
        for b, old, new in EDITS:
            if b != bid:
                continue
            assert old in text, (job, old[:50])
            text = text.replace(old, new)
            removed.append(old.strip() + ("  ->  " + new if new else ""))
        refs = ["Image %d: %s" % (i, r["role"]) for i, r in enumerate(task["references"], 1)]
        prompt = card + "\n\nTASK\n" + text + "\n\nREFERENCES\n" + "\n".join(refs) + "\n"
        (out / ("%s.txt" % job)).write_text(prompt)
        rec[job] = {"source_brief": str(LANE / bid / "brief.txt"),
                    "source_brief_sha256": hashlib.sha256((LANE / bid / "brief.txt").read_bytes()).hexdigest(),
                    "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                    "chars": len(prompt), "aspect_ratio": aspect,
                    "images_in_order": [r["path"] for r in task["references"]],
                    "removed_lane_operations": removed}
        print("%s <- %-7s %5d chars, %d images, aspect %s, %d lane removals"
              % (job, bid, len(prompt), len(refs), aspect, len(removed)))
    (out / "prompts.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
