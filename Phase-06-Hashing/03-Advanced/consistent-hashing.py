"""
consistent-hashing.py — Distributed Hashing for Sharded Systems

CONSISTENT HASHING answers "which server owns this key?" in a way that
keeps MOST keys on the same server when servers are added or removed.

---------------------------------------------------
The Problem It Solves:

You have N servers and a stream of keys. You want to shard by hashing:

    server_index = hash(key) % N

This works — until N changes. If you add/remove a server, N changes,
and ALMOST EVERY key suddenly maps to a different server. In practice,
that means:

    - a cache-invalidation stampede
    - a database re-shard of the entire keyspace
    - minutes of downtime during scaling

Consistent hashing achieves: when adding or removing one server,
only ~1/N of the keys change ownership. The rest stay put.

Used by:
    - Amazon DynamoDB / Riak (originally from the Dynamo paper)
    - Memcached's "ketama" client-side sharding
    - Cassandra's token ring
    - Most CDN request routing
    - Discord's Elixir-based message routing

---------------------------------------------------
The Idea — a Hash Ring:

1. Imagine a RING labelled 0 .. 2^64 - 1 (the full hash space).
2. Each SERVER is placed at one or more points on the ring (based on
   hash(server_name)).
3. A KEY is placed on the ring at hash(key).
4. To look up a key's server: walk CLOCKWISE on the ring from the key's
   position; the first server you encounter OWNS the key.

Adding a server: only the keys between the new server's position and
the previous clockwise server move. Everything else is unchanged.

Removing a server: its keys all shift to the next clockwise server.
Everything else is unchanged.

---------------------------------------------------
Virtual Nodes (aka vnodes):

With only N ring points (one per server), load distribution is lumpy:
the gaps between servers on the ring are random, so one server might
own 30% of the keyspace while another owns 5%.

Fix: place each server at MANY ring points (e.g. 100-200), each at
hash(server_name + ":0"), hash(server_name + ":1"), etc. With enough
virtual nodes, the probabilistic gaps even out, and each server owns
close to 1/N of the keyspace.

Typical production value: 100-200 vnodes per server.

---------------------------------------------------
Lookup Complexity:

Naïve: binary search on a sorted list of ring positions → O(log(N*V))
       where V is virtual-nodes-per-server.
Alternative: a SortedList / SkipList / balanced BST.

We use Python's `bisect` on a sorted list. O(log n) per lookup, O(n log n)
for building the ring once; O(log n + V) to add/remove a server.
"""

import bisect
import hashlib


def _stable_hash(s):
    """
    A stable 64-bit hash. Python's built-in hash() is randomized per
    process, which ruins ring deterministic behaviour across restarts.
    Here we use MD5 (fast, well-distributed; we're not using it for
    security, just spreading points on a ring).
    """
    return int.from_bytes(hashlib.md5(str(s).encode()).digest()[:8], "big")


class ConsistentHashRing:
    """
    Consistent-hash ring with configurable virtual nodes per server.

    Usage:
        ring = ConsistentHashRing(vnodes=100)
        ring.add_server("server-A")
        ring.add_server("server-B")
        ring.get_server("user:12345")      → "server-A" or "server-B"
    """

    def __init__(self, vnodes=100):
        self.vnodes = vnodes
        # Parallel sorted arrays: _positions[i] is a ring position,
        # _owners[i] is the server that owns it. bisect operates on _positions.
        self._positions = []
        self._owners = []
        self._servers = set()

    # ------------------------------------------------------------------
    # Building / maintaining the ring
    # ------------------------------------------------------------------

    def add_server(self, server):
        """Place `vnodes` copies of `server` onto the ring. O(V log n)."""
        if server in self._servers:
            raise ValueError(f"server {server!r} already in ring")
        self._servers.add(server)

        for i in range(self.vnodes):
            pos = _stable_hash(f"{server}#{i}")
            idx = bisect.bisect_left(self._positions, pos)
            self._positions.insert(idx, pos)
            self._owners.insert(idx, server)

    def remove_server(self, server):
        """Remove every vnode belonging to `server`. O(n)."""
        if server not in self._servers:
            raise KeyError(server)
        self._servers.remove(server)

        # Rebuild parallel arrays without this server's vnodes
        kept = [(p, o) for p, o in zip(self._positions, self._owners) if o != server]
        self._positions = [p for p, _ in kept]
        self._owners = [o for _, o in kept]

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get_server(self, key):
        """
        Return the server that owns `key`. O(log n).

        Raises LookupError if no servers have been registered.
        """
        if not self._positions:
            raise LookupError("no servers in ring")

        pos = _stable_hash(key)
        idx = bisect.bisect_right(self._positions, pos)
        if idx == len(self._positions):
            idx = 0                                # wrap around
        return self._owners[idx]

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def distribution(self, keys):
        """Count how many of `keys` each server owns. Useful for checking balance."""
        counts = {s: 0 for s in self._servers}
        for k in keys:
            counts[self.get_server(k)] += 1
        return counts

    def servers(self):
        return set(self._servers)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Basic: three servers, lookups are deterministic
    ring = ConsistentHashRing(vnodes=100)
    ring.add_server("server-A")
    ring.add_server("server-B")
    ring.add_server("server-C")

    keys = [f"user:{i}" for i in range(10_000)]
    initial = {k: ring.get_server(k) for k in keys}

    # Check distribution is within ~30% of even (1/3 = 3333)
    dist = ring.distribution(keys)
    print(f"\nDistribution with 3 servers, 100 vnodes each:")
    for s, c in sorted(dist.items()):
        print(f"   {s}: {c:5}  ({100 * c / len(keys):.1f}%)")
    for s, c in dist.items():
        share = c / len(keys)
        assert 0.2 < share < 0.45, f"{s} has uneven share {share:.2f}"

    # Lookups should be deterministic on repeat
    for k in keys[:100]:
        assert ring.get_server(k) == initial[k]

    # ---- Adding a server moves only ~1/4 of keys (not 3/4!) ----
    ring.add_server("server-D")
    moved = sum(1 for k in keys if ring.get_server(k) != initial[k])
    moved_frac = moved / len(keys)
    print(f"\nAdded server-D — key movement: {moved_frac:.1%}  "
          f"(expected ~25% with 4 servers)")
    assert 0.15 < moved_frac < 0.35, f"too many keys moved: {moved_frac:.2%}"

    # ---- By contrast, naïve hash%N moves ~3/4 on the same change ----
    def naive_server(key, servers):
        return sorted(servers)[_stable_hash(key) % len(servers)]

    servers_3 = ["server-A", "server-B", "server-C"]
    servers_4 = servers_3 + ["server-D"]
    naive_moved = sum(1 for k in keys if naive_server(k, servers_3) != naive_server(k, servers_4))
    naive_frac = naive_moved / len(keys)
    print(f"   vs. naïve hash%N on same change: {naive_frac:.1%}  "
          f"(nearly everything shifts)")
    assert naive_frac > 0.5, "naïve sharding should move >50% of keys"

    # ---- Removing a server moves ~1/4 of keys ----
    after_add = {k: ring.get_server(k) for k in keys}
    ring.remove_server("server-B")
    moved_after_remove = sum(1 for k in keys if ring.get_server(k) != after_add[k])
    print(f"\nRemoved server-B — key movement: "
          f"{100 * moved_after_remove / len(keys):.1f}%  "
          f"(expected ~25% — server-B's share)")
    assert 0.15 < moved_after_remove / len(keys) < 0.35

    # ---- Virtual-node count affects balance ----
    print(f"\nBalance improves with more vnodes:")
    for vnodes in (1, 10, 100, 500):
        r = ConsistentHashRing(vnodes=vnodes)
        for s in servers_3:
            r.add_server(s)
        dist = r.distribution(keys)
        shares = [c / len(keys) for c in dist.values()]
        spread = max(shares) - min(shares)
        print(f"   vnodes={vnodes:4}:  max-min share spread = {spread:.2%}")

    # Duplicate server add — error
    try:
        ring.add_server("server-A")
    except ValueError:
        pass
    else:
        raise AssertionError("expected duplicate add to raise")

    # Unknown server remove — error
    try:
        ring.remove_server("no-such-server")
    except KeyError:
        pass
    else:
        raise AssertionError("expected unknown remove to raise")

    # Empty ring lookup — error
    empty = ConsistentHashRing()
    try:
        empty.get_server("anything")
    except LookupError:
        pass
    else:
        raise AssertionError("expected empty-ring lookup to raise")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Follow-ups You Might Read About:
    #
    #   - Jump Consistent Hash (Lamping & Veach, Google 2014):
    #     no ring, no vnodes, O(log N) per lookup with just a
    #     number and a loop. Beats the ring on simplicity and
    #     memory; only limitation is servers must be numbered 0..N-1.
    #
    #   - Rendezvous hashing / Highest Random Weight:
    #     for each key, compute hash(server, key) for every server
    #     and pick the max. O(N) per lookup but no virtual-node
    #     balancing needed. Used in CARP and by Akamai.
    #
    #   - Maglev hashing (Google 2016): a finite lookup table plus
    #     careful permutation to achieve near-perfect balance and
    #     minimal disruption on server changes. Used in GCP's
    #     load balancer.
    # ---------------------------------------------------------------
