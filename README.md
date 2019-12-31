## What's this ?

This image is intended to update CloudFlare DNS record.

## Usage

Here is a usage example :

```yaml
version: '3'

services:
  cf-update-record:
    image: frgaudet/cf-update-record:0.0.3
    networks:
      private:

networks:
  private:
```

## Arguments

The following env variable are mandatory :

`CF_TOKEN` : CloudFlare API token

`HOSTNAME` : Hostname to update

`ZONE_ID` : your Zone ID

`RECORD_ID` : the hostname record ID


These variables are optional and define how many retries will be done to update the record :

`WAIT_FIXED` : Time between each attempt

`STOP_AFTER_ATTEMPT` : Max number of attempt

Default config is :

```bash
WAIT_FIXED=2
STOP_AFTER_ATTEMPT=2
```

## Output

When the IP is updated, statistics shows how many retries were necessary :

Example :
```
Old IP address: xxx.xxx.xxx.xxx - New IP address: yyy.yyy.yyy.yyy
{"start_time": 183753.9955154, "attempt_number": 1, "idle_for": 0, "delay_since_first_attempt": 0.102977144997567}
```
