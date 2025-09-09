import psutil

def find_interfaces():
    addresses = []

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2:
                addresses.append(
                   (interface, addr.address, addr.netmask)
                )
    
    return addresses

