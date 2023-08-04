import sys
import ipaddress

def read_networks_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    full_network = lines[0].strip()
    used_subnets = [line.strip() for line in lines[1:]]
    return full_network, used_subnets

def find_unused_subnets(network, used_subnets):
    full_network = ipaddress.IPv6Network(network)
    used_subnets = [ipaddress.IPv6Network(subnet) for subnet in used_subnets]

    # Sort the used subnets by their starting address
    used_subnets.sort(key=lambda x: x.network_address)

    unused_subnets = []

    # Check if there are any free subnets between the full network and the first used subnet
    first_used_subnet = used_subnets[0]
    if full_network.network_address < first_used_subnet.network_address:
        unused_subnet = ipaddress.summarize_address_range(full_network.network_address, first_used_subnet.network_address - 1)
        unused_subnets.extend(unused_subnet)

    # Check for free subnets between the used subnets
    for i in range(len(used_subnets) - 1):
        start = int(used_subnets[i].broadcast_address) + 1
        end = int(used_subnets[i + 1].network_address) - 1
        if start < end and (end - start + 1) >= 2 ** (128 - 48):
            unused_subnet = ipaddress.summarize_address_range(ipaddress.IPv6Address(start), ipaddress.IPv6Address(end))
            unused_subnets.extend(unused_subnet)

    # Check if there are any free subnets between the last used subnet and the full network
    last_used_subnet = used_subnets[-1]
    if last_used_subnet.broadcast_address < full_network.broadcast_address:
        unused_subnet = ipaddress.summarize_address_range(last_used_subnet.broadcast_address + 1, full_network.broadcast_address)
        unused_subnets.extend(unused_subnet)

    return [subnet.with_prefixlen for subnet in unused_subnets]

if len(sys.argv) != 2:
    print("Usage: python3 ips.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
full_network, used_subnets = read_networks_from_file(filename)

# Example usage:
unused_subnets = find_unused_subnets(full_network, used_subnets)
if unused_subnets:
    for subnet in unused_subnets:
        print(subnet)
else:
    print("No free subnets of /48 or larger.")
