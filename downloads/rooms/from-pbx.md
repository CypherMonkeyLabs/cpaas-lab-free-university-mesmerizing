# Leaving a PBX without inventing a cutover

Study notes. Not vendor documentation and not legal advice.

- Asterisk's article calls it a software PBX, created in 1999 by Mark Spencer, with voicemail, conferencing, IVR, and automatic call distribution.
- The Asterisk dialplan page says the dialplan is extensions.conf, typically in /etc/asterisk, and that dialplan reload loads it without disrupting service.
- DID and SIP trunking are how the outside world reaches that PBX, on the articles already opened.
- A CPaaS trunk can sit in the public domain while the PBX stays in the private domain.
- No cutover calendar, no dual-run week count, and no CUCM menu were opened.

One number. Write its E.164 form, its DID or DNIS, the PBX extension, the trunk provider, and the emergency address owner. The date of the move stays blank until you have a change window. That blank is confirm, not a weekend you invented.

