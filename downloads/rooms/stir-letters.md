# A, B, and C on the STIR article

Study notes. Not vendor documentation and not legal advice.

- Wikipedia says STIR/SHAKEN is a suite of protocols and procedures intended to combat caller ID spoofing.
- It says STIR is Secure Telephone Identity Revisited, defined in IETF RFCs, and that it adds a digital certificate to the SIP information used to route VoIP calls.
- The article says there are three attestation levels. A, Full Attestation, means the provider recognizes the entire phone number as registered to the originating subscriber.
- B, Partial Attestation, means the call came from a known customer but the entire number cannot be verified, as with a PBX extension the provider has not registered.
- C, Gateway Attestation, means the call can only be verified as coming from a known gateway, for example a connection from another provider.

Three calls. A desk phone whose number the provider registered: write A. A PBX extension the provider has never seen: write B, using the article's example. A call that only proves which carrier handed it over: write C.

