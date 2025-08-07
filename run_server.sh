#!/bin/bash
cd /Users/ud/whatsapp-cloud-api-mcp-server
export META_ACCESS_TOKEN="EAAMexKBZAbb0BO2SCgi092ScWMfsKrcsAaKnJhBnjX0ZCWxCVn6qWquoSjvaHNrttGgmJIFdffxLnwn8qlcJbPh8ZCjsfZAmGXfZAWal9GRy9w5gImztuDUmdRRumOvrJ7OfXzMxHUpUpUkZBiTYDzHFikMPi58sKGzZCKm5HMwFkQRzOlE4JXwGxsg6eugAQgz"
export META_PHONE_NUMBER_ID="2395491917210830"
export META_BUSINESS_ACCOUNT_ID="226989664581568"
export WABA_ID="354081058707811"
export META_APP_ID="878254782770621"
export WHATSAPP_API_VERSION="v22.0"
exec /Users/ud/whatsapp-cloud-api-mcp-server/venv/bin/python main.py "$@"
