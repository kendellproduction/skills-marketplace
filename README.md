# Skills Marketplace

Personal catalog of Claude skills, built once and reused across accounts. Private repo —
clone it anywhere you use Claude, run `install.sh`, and the skills are available without
rebuilding them.

## Install

```bash
git clone https://github.com/kendellproduction/skills-marketplace.git
cd skills-marketplace
./install.sh
```

Installs into `~/.claude/skills/`. Override with `CLAUDE_SKILLS_DIR` if your setup
differs. Install a single skill with `./install.sh council`.

To update later: `git pull && ./install.sh`

## Catalog

| Skill | What it does |
|---|---|
| [`council`](skills/council) | A council of advisor personas — modeled on creators you follow, plus synthetic seats for pushback — that you convene to think through decisions. Stays current by pulling new videos from their channels. |

## Design rules for this repo

These exist so skills stay portable and nothing private leaks.

**Skills are generic. Context is local.** A skill never contains personal or client
details. Anything specific to you lives in a data directory outside the repo (for the
council, `~/.claude/council-data/`) and is gitignored. This is what lets the same skill
run on a personal and a work account with appropriate behavior on each.

**Everything a skill needs travels with it.** Scripts, reference docs, and templates live
in the skill's own folder. If it depends on something external, the SKILL.md says so and
degrades gracefully when it's missing.

**Fail loud, not silent.** A skill that quietly does nothing when a dependency is absent
is worse than one that says what's missing.

**Assume you'll return cold.** Six months from now on another machine you won't remember
how any of this works. Write for that reader.

## Adding a skill

```
skills/<name>/
├── SKILL.md          # required — YAML frontmatter with name + description
├── references/       # detail loaded on demand, keeps SKILL.md short
├── scripts/          # executable helpers
└── ...
```

The `description` in the frontmatter is what determines whether the skill triggers.
Write it as a list of concrete situations and phrases, not an abstract summary.

Then add a row to the catalog table above.
