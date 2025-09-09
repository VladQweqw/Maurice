import psutil
import pyshark
import asyncio

import dns.resolver
import dns.reversename

def find_interfaces():
    addresses = []

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2:
                addresses.append(
                   (interface, addr.address, addr.netmask)
                )
    
    return addresses


def convert_IP_to_binary(ip):
    new_ip = ""
    
    for octet in ip.split("."):
        octet = int(octet)
        n = 7
        binary_octet = ""

        while(octet >= 0 and n >= 0):
            power = 2 ** n

            if octet - power >= 0:
                octet -= power
                binary_octet += "1"
            else:
                binary_octet += "0"

            n -= 1
        
        new_ip += binary_octet

    return new_ip

def get_network_ip(host_ip, subnet_mask):
    host_ip_bin = convert_IP_to_binary(host_ip)
    subnet_bin = convert_IP_to_binary(subnet_mask)

    network_ip = ""
    for idx in range(32):
        if (host_ip_bin[idx] == subnet_bin[idx]) and host_ip_bin[idx] == "1":
            network_ip += "1"
        else:
            network_ip += "0"
            
    return network_ip





def dnsResolve(ip):
    try:
        reverse_name = dns.reversename.from_address(ip)
        answer = dns.resolver.resolve(reverse_name, 'PTR')

        for val in answer:
            return val.to_text()
    except Exception as e:
        return 'ERROR'

def is_IP_in_network(host_ip, network_ip, subnet_bits):
    host_ip_bin = convert_IP_to_binary(host_ip)
    
    for bit in range(subnet_bits.count("1")):
        if host_ip_bin[bit] != network_ip[bit]: return False

    return True