# Skills Marketplace

Kendell's individually installable Claude skills.

## Install

```bash
git clone https://github.com/kendellproduction/skills-marketplace.git
cd skills-marketplace
./install.sh
```

Install everything with `./install.sh`, or install one skill with `./install.sh <skill-name>`.

## Available skills

| Skill | Description |
|---|---|
| [council](skills/council) | Convene advisor personas to pressure-test decisions and plans. |
| [personal-career-evidence](skills/personal-career-evidence) | Collect personal and public-safe project evidence for AI consulting and job applications. |
| [adobe-career-evidence](skills/adobe-career-evidence) | Track confidential Adobe AI, automation, leadership, and promotion evidence. |
| [consulting-delivery-roi](skills/consulting-delivery-roi) | Analyze client workflows, find high-ROI AI opportunities, and deliver safe pilots. |

Each skill is a separate marketplace entry and can be installed independently.

## Design rules

Skills are generic. Personal, Adobe, and client-specific context belongs outside this repository. Never commit confidential Adobe data, customer data, credentials, or private business records.

Each skill directory contains a required `SKILL.md` with frontmatter `name` and `description`.
