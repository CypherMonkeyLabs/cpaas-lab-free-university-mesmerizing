# SHAKEN, PASSporT, and the Identity header

Study notes. Not vendor documentation and not legal advice.

- The Wikipedia article says SHAKEN stands for Signature-based Handling of Asserted information using toKENs.
- It says SHAKEN was developed by the SIP Forum and ATIS to implement STIR, and that STIR is designed for calls routed through VoIP rather than the SS7 telephone network.
- The article says a STIR system produces a token with the originating number, the called number, and the attestation level, and that this is appended to the SIP request in an Identity field.
- RFC 8225 defines PASSporT, a Personal Assertion Token that cryptographically verifies an originating identity.
- RFC 8224 defines authenticated identity management in SIP and says the baseline SIP security mechanisms are inadequate for assuring end-user identity in an interdomain context. The page says it obsoletes RFC 4474.

Draw SIP, then an Identity header, then the called party. Label the token PASSporT from RFC 8225. Label the profile SHAKEN from the article. If the call is still on SS7 only, write the article's limit: STIR is specified for the VoIP section.

