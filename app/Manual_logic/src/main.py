from function_def import (
    calculate_broadcast_address,
    calculate_network_address,
    calculate_total_hosts,
    cidr_to_mask,
    get_ip_class,
    valid_ip_address,
    valid_subnet_mask,
)

ip = input("Enter IP address:  ")
if not valid_ip_address(ip):
    print("Invalid IP, Try again.")

# # Accept CIDR or dotted-decimal mask
subnet_mask_input = input("Enter the Subnet Mask (dotted or CIDR like 24 or /24):  ")
mask_input = subnet_mask_input.strip()
mask_input = mask_input.removeprefix('/')
if mask_input.isdigit():
    cidr = int(mask_input)
    if 0 <= cidr <= 32:
        subnet_mask = cidr_to_mask(cidr)
    else:
        print("Invalid CIDR value. Please enter 0-32.")
        subnet_mask = input("Enter the Subnet Mask:  ")
else:
    subnet_mask = mask_input
if valid_subnet_mask(subnet_mask) == False:
    print("Invalid Subnet Mask, Try again.")
    subnet_mask = input("Enter the Subnet Mask:  ")

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

