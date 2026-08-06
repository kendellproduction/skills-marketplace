# Codex entry point

When running this plugin under Codex, load `agents/comms-agent.md`, then `skills/quote-intake/SKILL.md` and its required references, and `skills/crm-browser/SKILL.md` when CRM access is needed.

Prefer Codex's native Gmail and Firestore connectors over the Zapier MCP declared in `.mcp.json`. Zapier is the portable fallback and has been unreliable. The `.mcp.json` Zapier URL is tied to one specific business/account's Zapier account and must be regenerated per account if Zapier is used.

Codex has no reachable Chrome, computer-use, or Messages integration for this plugin. Email is the default owner-notification channel. Calendar is optional: detect a connected Google Calendar tool at runtime and skip gracefully when absent.
