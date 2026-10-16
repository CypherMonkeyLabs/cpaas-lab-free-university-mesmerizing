# Webhooks come inbound

Study notes. Not vendor documentation and not legal advice.

- Twilio's webhook introduction says Twilio uses webhooks to notify your web app when events such as incoming calls or SMS messages occur.
- It says the REST API handles requests from your app to Twilio, and webhooks handle the reverse, requests from Twilio to your app.
- The same docs area names signing webhooks with shared keys, and authentication with OAuth 2.0, Basic, or Digest.
- Bandwidth's messaging guide says a create call returns HTTP 202 Accepted, meaning the message is queued.
- Bandwidth says it retries a webhook for 24 hours until your server returns an HTTP 2xx, and then it stops.

Draw two arrows. App to Twilio: REST. Twilio to app: webhook. For Bandwidth, write 202 on the create response and 2xx on the webhook response. Write the shared-key signature as a check you still have to implement from the Twilio page, not as a secret you paste here.

