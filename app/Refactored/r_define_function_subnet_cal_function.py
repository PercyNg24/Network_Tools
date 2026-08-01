# This task is for learning Python fundamentals through a networking-related exercise.
# The goal is to build a small script that takes an IP address and subnet mask, performs subnet calculations, 
# and progressively adds functionality such as geolocation lookup and file storage.
# ------------------------------------------------------------------------------------------------------------

# Phase 1 – Manual Logic
# Validate IP and mask format.
import ipaddress

def get_ip_class(ip): 
    first_octet = int(ip.split('.')[0])  #split the IP address into octets and convert the first octet to an integer
    if first_octet <= 127:               #Determine the class based on the value of the first octet
        return 'A'
    elif first_octet <= 191:
        return 'B'
    elif first_octet <= 223:
        return 'C'
    elif first_octet <= 239:
        return 'D (Multicast)'
    else:
        return 'E (Reserved)'

def valid_ip_inp(ip): 
    try:
        ipaddress.IPv4Address(ip)  # Use ipaddress module to validate the IP address
        return True
    except ipaddress.AddressValueError:
        return False
    
def valid_subnet_input(mask):  ## refactored
    try:
        ipaddress.IPv4Network(f"1.1.1.1/{mask}", strict=False)  # Use ipaddress module to validate the subnet mask
        return True
    except ValueError:
        return False

def cidr_to_mask(prefix):   ## refactored
    return str(ipaddress.ip_network(f"0.0.0.0/{prefix}"))  # Use ipaddress module to convert CIDR prefix to subnet mask

def calculate_network_address(ip,subnet_mask):     ## refactored

    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)  # Use ipaddress module to calculate network address    
    return str(network.network_address)

def calculate_broadcast_address(ip, mask): ## refactored
    network =ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)  # Use ipaddress module to calculate broadcast address
    return str(network.broadcast_address)
def calculate_total_hosts(mask): ## refactored
    network = ipaddress.IPv4Network(f"0.0.0.0/{mask}", strict=False) # calculate the size of the subnet based on input subnet mask
    total_hosts = network.num_addresses
    prefix = network.prefixlen   #convert the subnet mask to CIDR prefix length
   
    if prefix == 32:
        usable_hosts = 1
    elif prefix == 31:
        usable_hosts = 0
    else:
        usable_hosts = total_hosts - 2
    return total_hosts, usable_hosts

##