import sys

from function_def import (
    calculate_broadcast_address,
    calculate_network_address,
    calculate_total_hosts,
    cidr_to_mask,
    get_ip_class,
    valid_ip_address,
    valid_subnet_mask,
)

if len(sys.argv) > 1:                   # use input from CLI if user provide
    ip = sys.argv[1]
else:
    while True:
        ip = input("Enter IP address:  ")
        if valid_ip_address(ip):
            break
        print("Invalid IP, Try again.")

if len(sys.argv) > 2:
    subnet_mask_input = sys.argv[2]
else:
    subnet_mask_input = input("Enter the Subnet Mask (dotted or CIDR like 24 or /24):  ")

mask_input = subnet_mask_input.strip().removeprefix('/')
if mask_input.isdigit():
    cidr = int(mask_input)
    if 0 <= cidr <= 32:
        subnet_mask = cidr_to_mask(cidr)
    else:
        print("Invalid CIDR value. Please enter 0-32.")
        subnet_mask_input = input("Enter the Subnet Mask:  ")
        mask_input = subnet_mask_input.strip().removeprefix('/')
        while not mask_input.isdigit() or not (0 <= int(mask_input) <= 32):
            print("Invalid CIDR value. Please enter 0-32.")
            subnet_mask_input = input("Enter the Subnet Mask:  ")
            mask_input = subnet_mask_input.strip().removeprefix('/')
        subnet_mask = cidr_to_mask(int(mask_input))
else:
    while True:
        subnet_mask = mask_input
        if valid_subnet_mask(subnet_mask):
            break
        print("Invalid Subnet Mask, Try again.")
        subnet_mask_input = input("Enter the Subnet Mask:  ")
        mask_input = subnet_mask_input.strip().removeprefix('/')


net = calculate_network_address(ip, subnet_mask)
bcast = calculate_broadcast_address(ip, subnet_mask)
total, usable = calculate_total_hosts(subnet_mask)



print(f"IP address is: {ip}")
print(f"Subnet Mask is: {subnet_mask}")
print(f"Network address is: {net}")
print(f"Broadcast address is: {bcast}")
print(f"Total addresses in subnet: {total}")
print(f"Usable hosts in subnet: {usable}")
print(f"IP class: {get_ip_class(ip)}")

