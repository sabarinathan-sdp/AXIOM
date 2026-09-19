# AXIOM

Deterministic policy gate and capability registry for a local, single-user
agentic AI system. Built on the premise that the LLM is an untrusted
component: it proposes actions, deterministic code disposes of them.

The name reflects the core design rule: every decision in the trust
boundary reduces to a fixed set of boolean checks — axioms, not scores.
Nothing in the security-critical path depends on a weighted estimate
that could be argued with.

## Design principles

- **Default deny.** An action not declared in the capability registry
  cannot run. An action with an empty `scope` is declared but not
  authorized.
- **Simulate before execute.** Any action tagged as requiring
  simulation *cannot pass the gate* until a `simulate()` preview has
  been shown for that specific task. Enforced at registry load time,
  not by convention.
- **No scoring in the security boundary.** The gate is a sequence of
  boolean checks, not a weighted utility function. A bad `risk` score
  cannot be offset by a good `value` score for irreversible actions.
- **Reliability informs, never explores.** Tool trust is tracked with
  a Beta posterior per `(tool, task_type)`, updated only from real
  outcomes. The system never deliberately tries an unreliable tool to
  gather data — that would mean risking real files to learn.

## What's actually implemented

| Component | Status |
|---|---|
| Capability registry (`config/capability_registry.yaml`) | Working |
| Policy gate (`src/axiom/policy_gate.py`) | Working, tested |
| Reliability tracker (`src/axiom/reliability.py`) | Working, SQLite-backed |
| End-to-end demo (`examples/demo.py`) | Working — proves the gate refuses execution pre-simulation and allows it post-simulation |
| Audit log (hash-chained trace) | Not built |
| Task graph builder / DAG validator | Not built |
| MCP broker | Not built |
| Role router | Not built |
| Scheduler daemon | Not built |
| Real `tools.fs.*` / `tools.scheduler.*` / `tools.net.*` implementations | Not built — demo inlines its own `simulate_write`/`execute_write` as a worked example only |

This is early. Don't read the table of contents in the docstrings as
a feature list — read the "Status" column above.

## Install

```bash
git clone <this-repo>
cd axiom
pip install -e .
```

## Run the demo

```bash
python3 examples/demo.py
```

Expected: the gate returns `ASK` on the first pass (no simulation
shown yet), the simulation runs without touching disk, the gate
returns `ALLOW` on the second pass, the write executes, and the
reliability posterior updates.

## Repo layout

```
axiom/
├── config/
│   └── capability_registry.yaml   # the security boundary, as data
├── src/axiom/
│   ├── policy_gate.py             # allow / deny / ask, deterministic
│   └── reliability.py             # Beta posterior per (tool, task_type)
├── examples/
│   └── demo.py                    # working end-to-end walkthrough
└── setup.py
```

## Roadmap

1. Hash-chained audit log tying every gate decision to a registry
   version and a signed trace.
2. Task graph builder — Kahn's topological sort for validated DAG
   decomposition, capped depth and fan-out.
3. MCP broker — every external tool response enters tagged untrusted
   and can populate a slot but never act as an instruction.
4. Role router — cosine similarity over role profiles plus historical
   success rate, 3–5 roles total.
5. Scheduler daemon — SQLite-backed deadlines and reminders, polled
   by a background process, separate from the per-request pipeline.

## License

MIT — see `LICENSE`.
