# How a guide tells you to get a number

Study notes. Not vendor documentation and not legal advice.

- Telnyx's first-message guide says to buy two numbers so you can test messaging between them without registration requirements.
- The guide's steps name Numbers, then Search and Buy, an area code or region, and an SMS feature check.
- It then says to add a messaging profile and assign that profile to each number.
- The send call in the guide is an HTTP POST to https://api.telnyx.com/v2/messages with a Bearer token.
- The JSON fields the guide shows are from, to, and text. The sample digits in the guide are placeholders, not a number this lab assigns.

In a lab notebook, write the four Telnyx steps and then the word secret next to the API key. Do not paste the key. Write confirm next to any monthly number fee. That fee was not on this guide.

