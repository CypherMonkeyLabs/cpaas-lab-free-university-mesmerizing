# What observability meant on the pages

Study notes. Not vendor documentation and not legal advice.

- LiveKit Cloud's agents page says observability there includes transcripts and traces.
- Twilio's voice navigation names Voice Insights, Call Summary, and Trust and Engagement Insights.
- Twilio's docs also name a Debugger and usage records on the general usage pages reached from the webhook introduction.
- Bandwidth says it stores message metadata, not the text, after the webhook succeeds.
- No page opened in this session defined a numeric service level or a jitter budget.

After a test call, list the artifacts you actually have: webhook status, Bandwidth metadata if that API was used, a LiveKit trace if the agent ran in LiveKit Cloud. Write confirm next to MOS.

