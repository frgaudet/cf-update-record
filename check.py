#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CloudFlare
import tenacity
import requests
import os
import json
import sys
import time
import socket

exit=False

# Mandatory arguments
try:
    CF_TOKEN=os.environ['CF_TOKEN']
except KeyError as e:
    print("Missing env variable : " + str(e))
    exit=True

try:
    HOSTNAME=os.environ['HOSTNAME']
except KeyError as e:
    print("Missing env variable : " + str(e))
    exit=True

try:
    ZONE_ID=os.environ['ZONE_ID']
except KeyError as e:
    print("Missing env variable : " + str(e))
    exit=True

try:
    RECORD_ID=os.environ['RECORD_ID']
except KeyError as e:
    print("Missing env variable : " + str(e))
    exit=True

if exit:
    sys.exit(1)

try:
    WAIT_FIXED=int(os.environ['WAIT_FIXED'])
except:
    WAIT_FIXED=2
    pass

try:
    STOP_AFTER_ATTEMPT=int(os.environ['STOP_AFTER_ATTEMPT'])
except:
    STOP_AFTER_ATTEMPT=2
    pass

@tenacity.retry(wait=tenacity.wait_fixed(WAIT_FIXED),
        stop=tenacity.stop_after_attempt(STOP_AFTER_ATTEMPT))
def update_record_and_retry(cf, ZONE_ID, RECORD_ID, new_dns_record):
    update_record(cf, ZONE_ID, RECORD_ID, new_dns_record)

def update_record(cf, ZONE_ID, RECORD_ID, new_dns_record):
    try:
        ret = cf.zones.dns_records.put(ZONE_ID, RECORD_ID, data=new_dns_record)
        print(ret)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        print('/zones/dns_records.put %d %s - api call failed' % (e, e))

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
    except socket.error:
        return False
    return True

def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    return True

if __name__ == "__main__":
    
    cf = CloudFlare.CloudFlare(token=CF_TOKEN)
    current_dns_record = cf.zones.dns_records.get(ZONE_ID, RECORD_ID)
    print("Starting checking")

    while True:
        get_my_current_ip = requests.get('https://api.ipify.org').text
        
        if is_valid_ipv4_address(get_my_current_ip) and is_valid_ipv4_address(current_dns_record['content']) and (get_my_current_ip not in current_dns_record['content']):
            print("Old IP address: " + current_dns_record['content'] + " - New IP address: " + get_my_current_ip)
            new_dns_record = {'name':HOSTNAME, 'type':'A', 'content':get_my_current_ip, 'proxied':True}        
            try:
                update_record_and_retry(cf, ZONE_ID, RECORD_ID, new_dns_record)
                json.dump(update_record_and_retry.retry.statistics, sys.stdout)
            except tenacity.RetryError as e:
                print(e)
                pass
            except Exception as e:
                pass
        
        time.sleep(30)
