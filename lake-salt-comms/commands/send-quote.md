---
description: Draft and send a quote, then move lead to Proposal Sent in CRM
allowed-tools: mcp__zapier__*, mcp__Claude_in_Chrome__*
argument-hint: "[client name] [price] [any notes]"
---

Kendell has reviewed the event summary and approved a quote price. Draft, show, send, and update the CRM.

## Step 1 — Draft the Quote Email

Using the quote template from `references/response-templates.md`, draft the email:
- Fill in all confirmed event details (date, time, location, guests, drink packages)
- Insert the price Kendell approved
- Add any notes Kendell provided (what's included, deposit info, etc.)
- Sign: "— The Lake Salt Team"

## Step 2 — Show to Kendell for Approval

Present the fully drafted email. Ask: "Here's the quote — does this look good to send?"

**Do NOT send without Kendell's explicit approval.**

## Step 3 — Send via Zapier

Once Kendell approves, use the Zapier MCP Gmail action to send the email.

Confirm: "Quote sent to [client name] at [email]."

## Step 4 — Update CRM to "Proposal Sent"

Navigate to https://lakesalt.us/admin/#crm using Claude in Chrome:

1. Search for the client's lead card
2. Click the card to open the detail modal
3. Click **"Edit"**
4. Update the **Message** field to include the quoted amount
5. Change **Pipeline Stage** dropdown to **"Proposal Sent"**
6. Save

Confirm: "CRM updated — [client name] moved to Proposal Sent."
