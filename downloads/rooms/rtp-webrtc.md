# RTP, SRTP, and WebRTC

Study notes. Not vendor documentation and not legal advice.

- Wikipedia says RTP delivers audio and video over IP, typically over UDP, and that RTCP monitors transmission statistics and quality of service.
- The same article says RFC 3550 in 2003 superseded RFC 1889, and that RTP is often used with a signaling protocol such as SIP.
- RFC 3711 is the Secure Real-time Transport Protocol, SRTP.
- RFC 8825 is an overview of real-time protocols for browser-based applications. The abstract says the document is an applicability statement and does not itself specify a protocol.
- Wikipedia says WebRTC lets audio and video work inside web pages by direct peer-to-peer communication, and that ICE, STUN, and TURN are the NAT traversal techniques it uses.

A browser call fails only for some home routers. Write WebRTC, then ICE, STUN, and TURN as the article's traversal names. Write confirm beside any port you did not read. If the call is a SIP phone with one-way audio, start from RTP and RTCP instead.

