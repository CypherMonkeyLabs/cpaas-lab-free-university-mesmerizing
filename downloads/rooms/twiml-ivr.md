# TwiML verbs and what an IVR is

Study notes. Not vendor documentation and not legal advice.

- Wikipedia says an IVR interacts with callers, gathers information, and routes calls, using speech recognition and DTMF from the keypad.
- The article says IVR is often combined with an automated attendant and an automatic call distributor.
- Twilio's TwiML page lists voice nouns and verbs including Say, Play, Gather, Dial, Conference, Queue, Record, Redirect, Hangup, Pause, Pay, Refer, Reject, and Sip.
- The voice navigation also names Build IVR phone trees and a VirtualAgent noun.
- RFC 4733 is still the RTP payload for the keypad digits. Gather is Twilio's verb. They are not the same document.

A business-hours menu: Gather a digit, Redirect to a queue or Dial a number, and Hangup on a timeout. Cite TwiML for the verbs and the IVR article for the idea. Cite RFC 4733 only if you are explaining the digit in RTP.

