---
name: crm-browser
description: Access the Lake Salt CRM using a headless-safe connector first, with browser automation as an optional desktop enhancement.
---

## Access Methods

| Method | Availability | Role |
|---|---|---|
| Firestore API (via Zapier Firebase actions, or a native Firestore connector) | Headless/cloud and desktop | **DEFAULT** and headless-safe |
| Browser automation via Claude in Chrome | Desktop with a connected browser | **OPTIONAL** enhancement only |

Use Firestore first. If Chrome is not connected, go straight to the Firestore reference doc and do not treat the missing browser as an error. Preserve the existing CRM field schema and security rules.

Load `skills/quote-intake/references/crm-structure.md` before making CRM changes.
