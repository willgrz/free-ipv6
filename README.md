# free-ipv6
This calculates free subnets in a specific netblock when supplied with the netblock and the already used subnets.

Requires: python3 (Tested on Linux, no reason it should not work on anything else also)

Notice: By default this only prints free /48 and larger (smaller cannot be used for BGP), this can be easily adapted in the code

Usage:

1. clone repo

2. create file with your network and all used subnets like this:
   - First line is the total network
   - Any following line is an assigned/allocated subnet

2a06:1287::/32

2a06:1287:2::/48

2a06:1287:3::/48

2a06:1287:10::/44

2a06:1287:30::/44

etc

3. run with:
   - python3 ips.py FILENAME
  
4. results are printed to stdout
