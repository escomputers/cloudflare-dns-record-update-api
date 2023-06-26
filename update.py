import requests
import os
import sys
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# DNS name to keep updated
dns_pattern = re.compile(r'^(?!http[s]?://)(?:[\w.-]+)\.[a-zA-Z]{2,7}(?:/[\w.-]*)*/?$')

urls = [
    'https://checkip.amazonaws.com/',
    'https://cloudflare.com/cdn-cgi/trace/',
    'https://api.ipify.org/'
]

# cloudflare settings
CLOUDFLARE_TOKEN = os.getenv('CLOUDFLARE_TOKEN')
CLOUDFLARE_ZONEID = os.getenv('CLOUDFLARE_ZONEID')
CLOUDFLARE_ACCOUNTID = os.getenv('CLOUDFLARE_ACCOUNTID')
cloudflare_url = 'https://api.cloudflare.com/client/v4/zones/' + CLOUDFLARE_ZONEID + '/dns_records/' + CLOUDFLARE_ACCOUNTID


def update_ip(url, ip, dns_name):
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + CLOUDFLARE_TOKEN
    }

    data = {
        'content': ip,
        'name': dns_name,
        'type': 'A',
        'comment': 'Updated by Python DNS update script'
    }
    r = requests.put(url, headers=headers, json=data)
    if r.status_code == 200:
        logging.info('Cloudflare DNS record updated successfully')
    else:
        logging.error('Error during DNS record update process, check Cloudflare settings')


def get_ip(url):
    try:
        response = requests.get(url)
        ip = response.text
        return ip
    except requests.exceptions.ConnectionError:
        pass # variable response set as empty intentionally


def make_requests(cloudflare_url, dns_name):
    # try each endpoint sequentially
    ip = get_ip(urls[0])
    update_ip(cloudflare_url, ip, dns_name)
    if ip is None:
        ip = get_ip(urls[1])
        update_ip(cloudflare_url, ip, dns_name)
        if ip is None:
            ip = get_ip(urls[2])
            update_ip(cloudflare_url, ip, dns_name)
            if ip is None:
                logging.error('3/3 endpoints failed, check urls and internet connection')


def is_valid_url(dns_name, dns_pattern):
    if re.match(dns_pattern, dns_name):
        return True
    else:
        return False

def main():
    try:
        dns_name = sys.argv[1]
        if not is_valid_url(dns_name, dns_pattern):
            logging.error("Invalid URL provided.")
        else:
            make_requests(cloudflare_url, dns_name)
    except IndexError:
        logging.info("Please provide a URL as an argument.")


if __name__ == '__main__':
    main()