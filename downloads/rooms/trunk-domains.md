# Two domains and a SIP trunk

Study notes. Not vendor documentation and not legal advice.

- Wikipedia says SIP trunking is how Internet telephony service providers deliver telephone services to customers with a SIP-based IP-PBX.
- The article splits the network into a private domain, connected to a PBX or unified communications server, and a public domain, toward the PSTN or PLMN.
- It says the interconnection between those domains must occur through a SIP trunk.
- Twilio's Elastic SIP Trunking docs opened, including emergency calling, codecs, and calls per second as page names.
- Telnyx's SIP trunking guide says inbound traffic and authentication use SIP connections, and outbound routing uses outbound voice profiles.

Label a PBX as private and the PSTN as public. Put Twilio or Telnyx on the trunk, and write the authentication method only if you copied it from the Telnyx guide: credentials, IP address, or FQDN.

