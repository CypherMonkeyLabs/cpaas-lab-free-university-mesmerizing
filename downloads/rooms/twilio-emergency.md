# Twilio's emergency calling page

Study notes. Not vendor documentation and not legal advice.

- Twilio's SIP trunking emergency page says the feature routes emergency calls to PSAPs in the US, Canada, the UK, Australia, Ireland, France, Germany, and Austria.
- In the US and Canada it says Twilio supports both Enhanced 911 and Basic 911.
- E911, on that page, routes to the PSAP for the address associated with the Twilio number and includes the number and the address for the dispatcher.
- Basic 911 routes to the PSAP for that address, and the dispatcher does not receive the number or address unless the caller speaks them.
- The page says some Twilio numbers have neither service, and those 911 calls go to a national emergency call center. A Programmable Voice emergency page also opened.

A US number with an emergency address: write E911 and list number plus address, because that is the page's sentence. A number the page would class as Basic: write that the dispatcher will not see the address unless the caller says it. Do not promise the same behavior in a country that is not on the list.

