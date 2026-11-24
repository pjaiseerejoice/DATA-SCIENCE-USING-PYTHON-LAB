"""
Word count in Hadoop Streaming style.
Local simulation : python exp14.py
Hadoop Streaming : hadoop jar hadoop-streaming.jar \
-files exp14.py -mapper "python exp14.py map" \
-reducer "python exp14.py reduce" \
-input /data/news -output /out/wc
Unix pipe test : cat news.txt | python exp14.py map | sort | python exp14.py reduce
"""
import re
import sys
from itertools import groupby

def mapper(lines):
    for line in lines:
        for word in re.findall(r"[a-z]+", line.lower()):
            yield f"{word}\t1"

def reducer(lines):
    pairs = (line.rstrip("\n").split("\t") for line in lines)
    for word, group in groupby(pairs, key=lambda kv: kv[0]):
        yield f"{word}\t{sum(int(c) for _, c in group)}"

if len(sys.argv) > 1 and sys.argv[1] == "map":
    for out in mapper(sys.stdin):
        print(out)
    sys.exit()

if len(sys.argv) > 1 and sys.argv[1] == "reduce":
    for out in reducer(sys.stdin):
        print(out)
    sys.exit()

# ---------------- Local simulation of the Hadoop job ----------------
splits = {
    "split-1 (node1)": [
        "Data science uses data to create value",
        "Big data needs distributed storage",
    ],
    "split-2 (node2)": [
        "Hadoop stores big data in HDFS",
        "MapReduce processes data in parallel",
    ],
    "split-3 (node3)": [
        "Spark and Hadoop process big data",
        "Data drives science",
    ],
}

print("MapReduce Word Count on News Headlines")
print("=" * 42)

print("\n--- MAP PHASE ---")
mapped = {}
for split, lines in splits.items():
    out = list(mapper(lines))
    mapped[split] = out
    print(
        f"{split}: {len(out)} pairs ->",
        ", ".join(o.replace("\t", ":") for o in out[:6]),
        "...",
    )

print("\n--- COMBINER (local aggregation on each mapper) ---")
combined = []
for split, out in mapped.items():
    local = list(reducer(sorted(out)))
    combined.extend(local)
    print(f"{split}: {len(out)} pairs reduced to {len(local)}")

print("\n--- SHUFFLE AND SORT ---")
shuffled = sorted(combined)
for key, grp in groupby(shuffled, key=lambda s: s.split("\t")[0]):
    values = [g.split("\t")[1] for g in grp]
    if len(values) > 1:
        print(f" {key:<12} -> {values}")
print(" (keys appearing on only one mapper are not shown)")

print("\n--- REDUCE PHASE ---")
result = [r.split("\t") for r in reducer(shuffled)]
result.sort(key=lambda kv: (-int(kv[1]), kv[0]))
print(f"{'WORD':<12}COUNT")
for word, count in result:
    print(f"{word:<12}{count}")

print("\nDistinct words :", len(result))
print("Total words :", sum(int(c) for _, c in result))
print("Top 3 words :", [w for w, _ in result[:3]])