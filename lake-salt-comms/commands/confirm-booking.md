---
description: Confirm a booking — block calendar and move lead to Booked in CRM
allowed-tools: mcp__Claude_in_Chrome__*, mcp__zapier__*
argument-hint: "[client name] [date] [start time] [end time] [location]"
---

A client has confirmed their booking. Kendell has provided the confirmed event details. Execute both actions below.

## Action 1 — Block Google Calendar

List available tools and detect whatever Google Calendar tool is connected at runtime. If none is connected, skip this optional step gracefully and report that Calendar was unavailable; do not fail the run. When available, create an event on contact@lakesalt.us's calendar:
- **Title**: `LAKE SALT — [Client Name] @ [Venue Name]`
- **Date**: The confirmed event date
- **Start**: 1 hour before bar service start (setup buffer)
- **End**: 30 minutes after bar service end (breakdown buffer)
- **Description**:
  ```
  CLIENT: [name] | [email]
  BAR SERVICE: [start time] – [end time]
  LOCATION: [venue name + address]
  GUESTS: ~[count]
  DRINKS: [packages]
  BAR SETUP: [bring bar / venue has bar]
  SPECIAL REQUESTS: [details or none]
  QUOTE: $[amount]
  ```

## Action 2 — Update CRM to "Booked"

Navigate to https://lakesalt.us/admin/#crm using Claude in Chrome.

### If the client already has a lead card:
1. Search for the client by name in the search bar
2. Click on their lead card to open the detail modal
3. Click the **"Edit"** button in the modal
4. Update any fields that have changed or were previously missing:
   - Date, Guests, Venue, Message (add quote amount and final drink packages)
5. Change the **Pipeline Stage** dropdown to **"Booked"**
6. Save the record

### If no lead card exists yet:
1. Click **"+ Add Lead"** (top right)
2. Fill in all available fields:
   - Name, Email, Type, Date, Guests, Venue
   - Source: direct inquiry
   - Message: include drink packages, bar setup, special requests, quote amount
   - **Pipeline Stage: "Booked"**
3. Save

## Action 3 — Send Booking Confirmation Email (Ask Kendell)

Ask Kendell: "Want me to send a booking confirmation email to [client name]?"

If yes, draft using the Booking Confirmation template from `references/response-templates.md`, fill in all event details, show to Kendell for approval, then send via Zapier.

## Report Back

Confirm to Kendell:
- ✅ Calendar blocked: [event title] — [date], [setup time – breakdown time]
- ✅ CRM updated: [client name] → Pipeline Stage: **Booked**
- ✅ / ⏳ Confirmation email: [sent to email / pending Kendell approval]
