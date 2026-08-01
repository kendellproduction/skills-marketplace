# Transcript pipeline

How the council stays current. Run weekly (or on demand when the user asks
"what's the council been saying").

## Noise is the main problem, not volume

Across these five channels a normal week is ~31 uploads, and roughly a third of that is
clips and shorts. The worst offender is All-In: one flagship episode plus six to ten
clips **cut from that same episode**, so they're not just noise, they're redundant.
Nate B Jones posts roughly one substantive video plus a short most days.

`fetch_new_videos.py` filters these by default using per-channel rules in
`channels.json` (measured: 31 uploads → 20 kept, no false positives). Pass
`--keep-noise` to see what was dropped.

Do not undo this filter to "be thorough." A council that ingests every clip produces
notes full of the same argument restated six times, which makes the personas repetitive
and the digest useless. If the filter starts dropping real videos, tighten the regex in
`channels.json` rather than disabling it.

## The two-tier reality

**Tier 1 — video descriptions.** Come from the RSS feed, always work, no dependencies,
no IP restrictions. For these five creators the descriptions are unusually substantive —
often a full paragraph laying out the actual argument. Good enough to decide whether
something is relevant and to capture a member's current position.

**Tier 2 — full transcripts.** Richer and quotable with timestamps, but YouTube blocks
caption requests from datacenter IPs. **This means transcripts fail from a cloud session
and work from the user's own machine.**

Practical consequence: the weekly digest runs on Tier 1. When something clears the
relevance bar and the user wants depth, pull the full transcript — either by running
the script locally, or via `device_bash` if the user's desktop is connected.

Don't treat Tier 2 failing as an error. It's expected in the cloud.

## Running it

```bash
cd <skill-dir>/scripts

# what's new in the last week, descriptions only
python3 fetch_new_videos.py --since 7

# full depth on one member (run on the user's own machine)
python3 fetch_new_videos.py --member nate-b-jones --since 7 --transcripts

# after processing, record what you've handled
python3 fetch_new_videos.py --since 7 --mark-seen
```

State lives in `~/.claude/council-data/seen_videos.json` so the same video isn't
processed twice.

## Distilling into notes

**Never store raw transcripts in the notes files.** They're enormous and mostly filler.
Distill instead — but distill in a way that stays traceable, which is the whole point.

For each video worth keeping, append to `~/.claude/council-data/notes/<member>.md`:

```markdown
### 2026-07-26 — [This AI Technology Will Replace Millions](https://youtube.com/watch?v=...)

**Claim:** Agentic AI is already doing a large share of in-company task work, and the
individual response is to move up the stack rather than compete with it.

**In their words:**
> "the bottleneck was never the technology, it was who's willing to sell the outcome"
> — [12:40](https://youtube.com/watch?v=...&t=760s)

**Why it matters:** Sharpens his standing position — the opportunity claim now has a
specific timeline attached, where before it was open-ended.

**Type:** position shift
```

Types worth tagging: `recommendation` (a tool/workflow to try), `position shift`
(changed or sharpened view), `prediction` (falsifiable claim worth revisiting),
`reference` (background, low urgency).

If you only have the description and no transcript, still write the entry — just
attribute it to the description rather than fabricating a quote. Say
`**Source:** video description` instead of a timestamped quote. **Never invent a quote
or a timestamp.** A wrong timestamp is worse than no timestamp, because it looks
verified.

## Keeping profiles from bloating

Five channels at this cadence is roughly a thousand videos a year. Without pruning the
notes files become useless.

- **Recent takes** holds roughly the last 8 weeks, or ~15 entries per member.
- When something ages out, either drop it (most things) or move it to **Archive** if it
  captured a real position change worth remembering.
- When a new entry contradicts an existing one, **replace rather than append**, and move
  the old one to Archive with a note. A member who holds two contradictory positions
  simultaneously is a broken persona.
- Prune ruthlessly. A member with 15 sharp entries is far more useful than one with 200.

## The digest

Ruthlessly filtered, by explicit design. Read the user's context profile first, then ask
of each item: *does this connect to something they are actually working on or deciding
right now?*

If yes, surface it with the source link and one line on why it's relevant. If no, drop
it silently — do not include it as filler.

**"Nothing this week" is a valid and good digest.** A digest that always finds something
is one the user stops reading by week three. Protect the signal.

Cap it at three items. If more than three clear the bar, take the three strongest and
say how many you dropped.

Anything that's a concrete recommendation the user might act on also goes in
`backlog.md`, so the council remembers what it already suggested.
