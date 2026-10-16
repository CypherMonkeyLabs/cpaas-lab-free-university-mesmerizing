# A ladder you are allowed to draw

Study notes. Not vendor documentation and not legal advice.

- SIP sets up the session. RTP carries the media. The webhook tells your app that something happened.
- Twilio's voice docs also name Media Streams and a WebSocket for consuming a real-time stream.
- Bandwidth returns 202 when a message is queued, then a delivered or failed webhook.
- A SIP trunk's private and public domains still apply when the IVR is hosted.
- No customer packet capture was opened. Every ladder in this lab is a teaching sketch.

Sketch: caller, platform, your webhook, agent. SIP between caller and platform, RTP as a dashed line that need not hairpin, HTTP from the platform to your app. Stop. Add Refer only as a named verb, not as a captured call.

