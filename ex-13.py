import hashlib
import itertools

BLOCK_SIZE = 64  # bytes (scaled down from HDFS default of 128 MB)
REPLICATION = 3

class DataNode:
    def __init__(self, name, rack):
        self.name, self.rack, self.alive = name, rack, True
        self.blocks = {}

class NameNode:
    """Keeps only metadata: file -> blocks, block -> DataNodes."""

    def __init__(self, datanodes):
        self.datanodes = datanodes
        self.namespace = {}  # path -> list of block ids
        self.block_map = {}  # block id -> list of DataNode names
        self._rr = itertools.cycle(range(len(datanodes)))
        self._next_id = 1

    def choose_targets(self):
        """Rack-aware: 1st replica on one rack, 2nd and 3rd on another rack."""
        live = [d for d in self.datanodes if d.alive]
        turn = next(self._rr)
        first = live[turn % len(live)]
        others = [d for d in live if d.rack != first.rack]
        second = others[turn % len(others)]
        third = [d for d in others if d.rack == second.rack and d is not second][
            0
        ]
        return [first, second, third]

    def put(self, path, data):
        ids = []
        for start in range(0, len(data), BLOCK_SIZE):
            chunk = data[start: start + BLOCK_SIZE]
            bid = f"blk_{self._next_id:04d}"
            self._next_id += 1
            targets = self.choose_targets()
            for dn in targets:  # replication pipeline
                dn.blocks[bid] = chunk
            self.block_map[bid] = [dn.name for dn in targets]
            ids.append(bid)
        self.namespace[path] = ids
        return ids

    def get(self, path):
        out = []
        for bid in self.namespace[path]:
            for name in self.block_map[bid]:
                dn = self.node(name)
                if dn.alive:  # read from first live replica
                    out.append(dn.blocks[bid])
                    break
        return "".join(out)

    def node(self, name):
        return next(d for d in self.datanodes if d.name == name)

    def handle_failure(self, name):
        failed = self.node(name)
        failed.alive = False
        repaired = 0
        for bid, holders in self.block_map.items():
            if name in holders:
                holders.remove(name)
                source = self.node(holders[0])
                spare = [
                    d for d in self.datanodes if d.alive and d.name not in holders
                ][0]
                spare.blocks[bid] = source.blocks[bid]
                holders.append(spare.name)
                repaired += 1
        return repaired

def checksum(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

cluster = [
    DataNode("DN1", "Rack-1"),
    DataNode("DN2", "Rack-1"),
    DataNode("DN3", "Rack-1"),
    DataNode("DN4", "Rack-2"),
    DataNode("DN5", "Rack-2"),
    DataNode("DN6", "Rack-2"),
]
nn = NameNode(cluster)

log = "\n".join(
    f"2026-03-0{d} 10:{m:02d} sensor={s} temp={30 + (d * m + s) % 9}"
    for d in range(1, 3)
    for m in (5, 20)
    for s in (1, 2)
)

print("Distributed File System Simulation (HDFS)")
print("=" * 45)
print(f"Block size = {BLOCK_SIZE} bytes | Replication factor = {REPLICATION}")
print("Cluster :", ", ".join(f"{d.name}({d.rack})" for d in cluster))

print("\n$ hdfs dfs -put sensor_log.txt /data/sensor_log.txt")
blocks = nn.put("/data/sensor_log.txt", log)
print(f"File size = {len(log)} bytes -> {len(blocks)} blocks")

print("\nNameNode metadata (block -> DataNodes):")
for bid in blocks:
    racks = {nn.node(n).rack for n in nn.block_map[bid]}
    print(f" {bid} {nn.block_map[bid]} racks={sorted(racks)}")

print("\nDataNode storage report:")
for d in cluster:
    print(f" {d.name} blocks={sorted(d.blocks)}")

print("\n$ hdfs dfs -cat /data/sensor_log.txt | head -3")
data = nn.get("/data/sensor_log.txt")
print("\n".join(data.splitlines()[:3]))
print("Checksum original =", checksum(log), "| read back =", checksum(data))

print("\n*** DataNode DN1 fails (heartbeat lost) ***")
fixed = nn.handle_failure("DN1")
print("Under-replicated blocks re-replicated:", fixed)
for bid in blocks:
    print(f" {bid} {nn.block_map[bid]}")

data2 = nn.get("/data/sensor_log.txt")
print(
    "File readable after failure:", data2 == log, "| checksum =", checksum(data2)
)

print("\n$ hdfs fsck /data/sensor_log.txt -files -blocks")
healthy = all(len(v) == REPLICATION for v in nn.block_map.values())
print(
    f"Total blocks: {len(blocks)} | Replication: {REPLICATION} | "
    f"Status: {'HEALTHY' if healthy else 'CORRUPT'}"
)