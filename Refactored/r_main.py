
from r_define_function_subnet_cal_function import valid_ip_address, valid_subnet_mask, cidr_to_mask, calculate_network_address, calculate_broadcast_address, calculate_total_hosts, get_ip_class
import ipaddress
ip = input("Enter IP address:  ")
if not valid_ip_address(ip):
    print("Invalid IP, Try again.")
    exit()
# # Accept CIDR or dotted-decimal mask
subnet_mask = input("Enter the Subnet Mask (dotted or CIDR like 24 or /24):  ")
prefix = int(subnet_mask.replace('/',""))
subnet_mask = ipaddress.ip_network(f"0.0.0.0/{prefix}").netmask



print(f"IP address is: {ip}")
print(f"Subnet Mask is: {subnet_mask}")
net = calculate_network_address(ip,prefix)
bcast = calculate_broadcast_address(ip, prefix)
total, usable = calculate_total_hosts(prefix)
print(f"Network address is: {net}")
print(f"Broadcast address is: {bcast}")
print(f"Total addresses in subnet: {total}")
print(f"Usable hosts in subnet: {usable}")
print(f"IP class: {get_ip_class(ip)}")

## Private or Public IP address
ip_obj = ipaddress.ip_address(ip)

if ip_obj.is_private:
    print("IP type: Private")
elif ip_obj.is_global:
    print("IP type: Public")
else:
    print("IP type: Special/Reserved")
