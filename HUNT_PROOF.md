# JUMPERZ Spark Compete Proof Packet

## Hunt Status

- Team: JUMPERZ
- Members: JUMPERZ, Basjee01, acexqt
- Device-holder GitHub: jumperz11
- LLM provider: Other LLM
- Hunt registration: registered on 2026-05-17 at 21:47:08 UTC
- Public board status at registration check: Registered
- Repository: https://github.com/jumperz11/spark-hunt-jumperz
- Branch: `codex/spark-os-compile-command`

## Routing Status

This proof packet is intentionally kept inside the standalone `jumperz11/spark-hunt-jumperz` repository.

No active pull request is open into `vibeforge1111/vibeship-spark-intelligence`. A previous draft PR was closed after confirming the team wanted a clean standalone hunt workspace instead of proposing changes upstream.

## Finding

The Spark Compete site instructs agents to start discovery with:

```bash
spark os compile --json
```

The installed Spark CLI did not expose an `os` command, so the first agent-readable mission step failed before discovery could begin.

## Before Evidence

Command:

```bash
spark os compile --json
```

Observed failure:

```text
spark: error: argument command: invalid choice: 'os'
```

Impact:

- Agents following the public hunt brief cannot run the advertised discovery command.
- The failure blocks the capability, authority, trace, memory, repo-board, and gap inspection loop described by the hunt site.

## Fix

Added a safe `spark os compile` CLI route that emits a redacted `spark.os.compile.v1` JSON snapshot.

The snapshot includes:

- Capability view
- Authority and output boundary view
- Trace health summary
- Memory aggregate summary
- Project summary
- Repo-board summary
- Gap signals

The output is aggregate-only and explicitly excludes:

- Raw secret values
- Raw logs
- Raw conversations
- Raw memory rows
- Absolute local paths

## After Evidence

Command:

```bash
spark os compile --json
```

Observed success excerpt:

```json
{
  "schema": "spark.os.compile.v1",
  "authority": {
    "output_boundary": "aggregates_only",
    "surface": "public_track"
  },
  "capability": {
    "cli": "spark"
  }
}
```

## Validation

Focused test run:

```bash
uv run --extra dev pytest tests/test_cli_os.py
```

Result:

```text
3 passed
```

Manual smoke:

```bash
spark os compile --json
```

Result:

```text
Emits a redacted JSON discovery snapshot with schema spark.os.compile.v1.
```

## Changed Files

- `spark/cli.py`
- `tests/test_cli_os.py`
- `README.md`
- `HUNT_PROOF.md`

## Reviewer Notes

This packet is ready for reviewer routing. It demonstrates the bug and fix in a clean public repo under `jumperz11`, without proposing or pushing any active change into the upstream repository.
