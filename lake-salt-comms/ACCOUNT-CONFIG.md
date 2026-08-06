# Account configuration

Account-specific values baked into this plugin:

- Owner name: `Kendell`
- Owner notification email: `kendellproduction@gmail.com`
- Owner phone: `+17027216004`
- Business inbox: `contact@lakesalt.us`
- CRM domain: `lakesalt.us/admin/#crm`
- Zapier MCP URL in `.mcp.json` (account-specific)
- Business-specific pricing, voice, and information references under `skills/quote-intake/references/`

## Reuse checklist

1. Replace the owner, notification, phone, inbox, and CRM values throughout the plugin.
2. Review or replace pricing, voice, business-information, templates, and CRM reference documents.
3. Regenerate the `.mcp.json` Zapier URL for the new account, or omit Zapier when native connectors are available.
4. Verify native Gmail and Firestore access, then test optional Calendar and desktop enhancements separately.
5. Review security and approval rules before enabling unattended runs.
