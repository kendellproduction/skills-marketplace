# Lake Salt CRM Structure

CRM URL: https://lakesalt.us/admin/#crm

## Pipeline Stages (Kanban columns, left to right)

| Stage | When to use |
|-------|-------------|
| **New Lead** | Inquiry just came in, not yet reviewed |
| **Contacted** | We've received the inquiry and responded / have enough to follow up |
| **Proposal Sent** | Quote has been sent to the client |
| **Booked** | Client confirmed — calendar blocked |
| **Completed** | Event has taken place |

## Lead Card Fields

| Field | Notes |
|-------|-------|
| **Name** | Client full name |
| **Email** | Client email address |
| **Type** | Event type: Wedding, Corporate, Birthday, Private Party, etc. |
| **Date** | Event date (YYYY-MM-DD format) |
| **Guests** | Guest count or range (e.g. 50–100) |
| **Venue** | Venue name + address |
| **Budget** | Client's stated budget (leave blank if not stated) |
| **Source** | Website Form / Email Inquiry / Referral / etc. |
| **Priority** | Normal / High / Low |
| **Message** | Free-text field — paste full email content, drink preferences, special requests, quote amount |
| **Pipeline Stage** | Dropdown — matches kanban columns above |

## How to Create a New Lead
1. Navigate to https://lakesalt.us/admin/#crm
2. Click **"+ Add Lead"** button (top right)
3. Fill in available fields from the inquiry
4. Set Pipeline Stage appropriately
5. Save

## How to Update / Move a Lead
1. Click on the lead card to open the detail modal
2. To move pipeline stage: change the **Pipeline Stage** dropdown in the modal
3. To edit details: click **"Edit"** button in the modal, update fields, save
4. To delete: click **"Delete"** button (only use if Kendell instructs)

## Stage Transition Map

```
New Lead → Contacted      (after reviewing and responding to inquiry)
Contacted → Proposal Sent (after sending a quote)
Proposal Sent → Booked    (after client confirms — also block calendar)
Booked → Completed        (after the event has taken place)
```
