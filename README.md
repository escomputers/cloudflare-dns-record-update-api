### Description
Update host client public IP address on Cloudflare DNS type A records via API using 3 different endpoints for fetching.

### Requirements
This script requires:
* an existing Cloudflare DNS A record
* 3 environment variables:
  * CLOUDFLARE_ZONEID (the zone ID of DNS record to be updated)
  * CLOUDFLARE_ACCOUNTID (your Cloudflare account ID)
  * CLOUDFLARE_TOKEN (Authorization Bearer Token needed to access API)

### Usage
Run this command by passing your Cloudflare DNS A record to be updated:
```bash
python -m pip install -r requirements.txt
python update.py <cloudflarednsArecord>
```