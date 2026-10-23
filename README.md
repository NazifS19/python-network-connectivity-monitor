# python-network-connectivity-monitor

A simple Python-based network monitoring tool that automates device reachability checks, records timestamped results, and provides an online/offline summary.

I built this project to combine the networking fundamentals I am learning with Python automation and gain more hands-on experience with network troubleshooting.

---

## Overview

The program reads a list of devices from a JSON configuration file and checks whether each device responds to a ping.

For every device, it:

1. Reads the device name and IP address
2. Sends a ping request
3. Determines whether a response was received
4. Records the result with a timestamp
5. Saves the result to a CSV log
6. Displays an online/offline summary

### Basic Flow

```text
devices.json
     |
     v
Load device list
     |
     v
Ping each device
     |
     v
Response received?
   /           \
 Yes            No
  |              |
ONLINE         OFFLINE
   \             /
     v
Add timestamp
     |
     v
Display result
     |
     v
Save to CSV log
     |
     v
Print final summary
