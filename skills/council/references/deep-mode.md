# Deep council mode

For decisions that actually matter. Each speaking member runs as an independent
subagent so their reasoning is genuinely separate rather than one model producing six
voices that quietly converge.

## When to use

- The user says "deep council", "full council", or "really think about this"
- The decision is expensive, hard to reverse, or the user has clearly been going back
  and forth on it
- A standard session produced suspiciously easy consensus

Don't default to it. It's slower and costs meaningfully more tokens. Most questions
don't need it.

## How to run it

1. **Chair frames first**, inline, before spawning anything. Restate the question,
   decide who's being called on. Show this to the user — they may want to redirect
   before you spend the tokens.

2. **Spawn each member in parallel**, one Agent call per member, all in a single
   message so they run concurrently. Each agent gets:
   - The member's profile file contents
   - Their notes file contents, if it exists
   - The user's context profile
   - The question
   - The sourcing rules (sourced vs. extrapolated, no impressions)
   - An explicit instruction: *"Do not hedge toward agreement. If you disagree with
     what the others are likely to say, say so directly. Your job is your view, not
     a balanced overview."*

   Critically, **do not tell each agent what the others are saying.** Independence is
   the entire point of this mode.

3. **Print every member's response in full.** Not summarized. The user asked for deep
   mode to see the actual reasoning — collapsing it into a Chair summary defeats the
   purpose and hides exactly the disagreement they're paying for.

4. **Chair synthesizes last**, after all responses are visible: where the room split,
   what the split turns on, the call, the best counterargument, one next action.

## Optional second round

If two members landed in direct conflict, you can run one rebuttal round — spawn each
of those two again with the other's actual response and ask them to respond to it
specifically. Only do this when the disagreement is load-bearing for the decision.
Cap it at one round; a third round is diminishing returns.

## Cost note

Six subagents plus a synthesis pass is not cheap. If the user seems to be invoking deep
mode casually or repeatedly, mention once that standard mode handles most questions
fine. Don't lecture.
