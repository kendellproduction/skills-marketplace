# Context setup

The context profile is what makes the council better than watching the videos. It is
also the part that must never reach the repo.

## Where it lives

```
~/.claude/council-data/context/profile.md
```

Outside the skill directory, outside the repo, per-machine. The skill is generic and
portable; the context is local and private. Same skill on a work account reads a
different profile and behaves appropriately for that setting.

## Setting it up on a new machine

The repo ships `context-profile.template.md`. Copy it and fill it in:

```bash
mkdir -p ~/.claude/council-data/context
cp <skill-dir>/context-profile.template.md ~/.claude/council-data/context/profile.md
```

Nothing is auto-synced between machines, deliberately. Personal context stays on the
personal machine and work context stays on the work machine.

## What belongs in it

Enough that advice lands specifically rather than generically:

- Current projects and where each one actually stands
- What the user is trying to decide right now
- Skills, tools, and stacks already in use — prevents recommending things they have
- What they've already tried and abandoned, and why
- Constraints: time, budget, what they don't want to do
- How they like to work and be talked to

## What does not belong in it

- Credentials, API keys, tokens of any kind
- Client names or details that shouldn't leave their machine
- Anything the user wouldn't want read aloud in the setting that machine lives in

On a work machine, be more conservative than feels necessary. The work profile should
contain what's useful for work advice and nothing about the personal side of the user's
life, and vice versa.

## Using it in sessions

Read it before responding. Use it to filter and sharpen, not to flatter — knowing what
someone is working on makes it easier to tell them a project is a bad idea, not harder.

If the profile is missing, run the session anyway. Mention once that context isn't set
up and advice will be generic, then drop it. Don't nag.

If the profile is clearly stale — it describes a project the user has since talked about
finishing — offer to update it at the end of the session rather than interrupting.
