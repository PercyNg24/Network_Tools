# This task is for learning Python fundamentals through a networking-related exercise.
# The goal is to build a small script that takes an IP address and subnet mask, performs subnet calculations, 
# and progressively adds functionality such as geolocation lookup and file storage.
# ------------------------------------------------------------------------------------------------------------

# Phase 1 – Manual Logic
# Validate IP and mask format. (192.168.1.1/24)
def valid_ip_address(ip):   

    octet = ip.split(".")           # splits ip address into each octet. It will split when seeing (".") and return a list of octets
    if len(octet) != 4:             # Using len() to check if the length of the list is 4, which is the required number of octets for a valid IP address.
        return False
    for o in octet:                 # Looping into each octet in the list to check if it is a digit and within the valid range of 0-255.
        if not o.isdigit():         # making sure that it is digits only or else return False
            return False
        num = int(o)                # Make sure that input is with in 0-255 range.
        if num < 0 or num > 255:    # Make the values cannot be outside these ranges
            return False
    return True

def valid_subnet_mask(mask):

    octet = mask.split(".") 
    if not valid_ip_address(mask): 
        return False 
        return False
    binary_mask = ip_to_binary(mask)  # Convert the subnet mask to binary representation

    if binary_mask[0] != '1':                   # Mask must start with 1 and may contain only one transition from 1 to 0.
        return False
    first_zero = binary_mask.find('0')

    if first_zero == -1:
        return True
    return '1' not in binary_mask[first_zero:]

# convert IP to Binary
def ip_to_binary(ip):
    """
Split IP into octet, convert each octet to binary using format(int(o), '08b'), and join the binary octets into a single string.
"""
    return ''.join(format(int(o), '08b') for o in ip.split('.'))


# convert binary to IP address
def binary_to_ip(binary_str):
    ip_octet = []

    for i in range(0, 32, 8): 
        segment = binary_str[i:i+8]  # Get 8 bits for the current segment
        ip_octet.append(str(int(segment, 2)))  # Convert to decimal and append to list
    return '.'.join(ip_octet)


def cidr_to_mask(cidr):
    cidr = int(cidr)
    mask_bin = '1' * cidr + '0' * (32 - cidr)
    return binary_to_ip(mask_bin)

# Network address
def calculate_network_address(ip,subnet_mask):     ### To do

    ip_binary = ip_to_binary(ip)
    mask_binary = ip_to_binary(subnet_mask) 

    """
Using zip() to iterate over the bits of the IP address and subnet mask simultaneously, 
and applying a bitwise AND operation to calculate the network address in binary. 
Then converting the binary network address back to dotted-decimal format.

Aim here to zero out the host bits which leave the network part.
"""    
    network_binary = ""
    for ip_bit, mask_bit in zip(ip_binary, mask_binary):  
        if ip_bit == '1' and mask_bit == '1':   
            network_binary += '1'
        else:
            network_binary += '0'
    return binary_to_ip(network_binary)   


def calculate_broadcast_address(ip, mask):

    network_binary = ip_to_binary(calculate_network_address(ip, mask))
    subnet_mask_binary = ip_to_binary(mask)
    
    broadcast_binary = ""                                                        
    for net_bit, mask_bit in zip(network_binary, subnet_mask_binary):
        if mask_bit == '0':  
            broadcast_binary += '1'
        else:                
            broadcast_binary += net_bit
    return binary_to_ip(broadcast_binary)
    
    #broadcast_bin = ''.join('1' if subnet_mask_binary[i] == '0' or network_binary[i] == '1' else '0' for i in range(32))  ### To do: review logic for broadcast address calculation

# Total number of hosts

def calculate_total_hosts(mask):
    mask_bin = ip_to_binary(mask)
    host_bits = mask_bin.count('0')
    total = 2 ** host_bits
    usable = 1 if host_bits == 0 else 0 if host_bits == 1 else total - 2
    # /32 -> 1 usable, /31 -> 0 usable, otherwise total minus network+broadcast.
    return total, usable
    
# def calculate_total_hosts(mask):
#     mask_bin = ip_to_binary(mask)
#     host_bits = mask_bin.count('0')
#     total = 2 ** host_bits
#     # Usable hosts: for /32 (host_bits==0) usable=1 (single host); for /31 usable=0 (special point-to-point)
#     if host_bits == 0:     #### To do
#         usable = 1
#     elif host_bits == 1:
#         usable = 0
#     else:
#         usable = total - 2
#     return total, usable

# # Accept an IP and subnet mask as input.
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
