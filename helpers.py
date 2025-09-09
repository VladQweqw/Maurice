import psutil
import pyshark
import asyncio

def find_interfaces():
    addresses = []

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2:
                addresses.append(
                   (interface, addr.address, addr.netmask)
                )
    
    return addresses


def capture_live_packets(isScanning):
    # createa a loop for asyncio thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    capture = pyshark.LiveCapture(interface='Ethernet')
    for raw_packet in capture.sniff_continuously():
        if not isScanning:
            capture.close()
            break
        else:
            try:
                if "IP" in raw_packet:
                    print(f"{raw_packet.ip.src} -> {raw_packet.ip.dst}")
            except Exception as e:
                print(f"Error {e}")