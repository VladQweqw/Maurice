from tkinter import *
from tkinter import ttk
import psutil
import threading
import pyshark
import asyncio

# get interfaces
from helpers import find_interfaces, convert_IP_to_binary, get_network_ip, dnsResolve, is_IP_in_network


root = Tk()
root.title("Network Spy")
root.geometry('300x500')
title = Label(root, text="Network spy", font=("Roboto", 16)).pack(pady=10)


current_lan_ip = StringVar(value="0.0.0.0")
current_lan_network = StringVar(value="0.0.0.0")

user_ip_label = Label(root, textvariable=current_lan_ip, font=("Roboto", 12)).pack(pady=2)
network_ip_label = Label(root, textvariable=current_lan_network, font=("Roboto", 12)).pack(pady=2)

addresses = find_interfaces()
addresses_interfaces = []

# get only the name of the interface
for interface_tupl in addresses:
    addresses_interfaces.append(interface_tupl[0])

selected_option = StringVar()

dropdown = ttk.Combobox(root, textvariable=selected_option, values=addresses_interfaces, state="readonly")
dropdown.pack(pady=20)


def on_interface_change(event):
    selected_interface = addresses_interfaces.index(selected_option.get())

    current_lan_ip.set(addresses[selected_interface][1])
    current_lan_network.set(addresses[selected_interface][2])

dropdown.bind("<<ComboboxSelected>>", on_interface_change)

# list
listbox = Listbox(root, font=("Roboto", 10))
listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)

def insert_row(text):
    listbox.insert(0, text)


def capture_live_packets(isScanning, network_ip, subnet_bits):
    # createa a loop for asyncio thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    capture = pyshark.LiveCapture(selected_option.get())
    for raw_packet in capture.sniff_continuously():
        if not isScanning:
            capture.close()
            break
        else:
            try:
                if "IP" in raw_packet:
                    ip_src = raw_packet.ip.src
                    ip_dest = raw_packet.ip.dst
                    
                    if is_IP_in_network(ip_src, network_ip, subnet_bits):
                        dns_res = dnsResolve(ip_dest)
                        if dns_res == "ERROR": dns_res = "Failed to lookup"

                        insert_row(f"Your PC -> {dns_res} ({ip_dest})")
                
        
            except Exception as e:
                print(f"Error {e}")

isScanning = False
def start_scanning():
    global isScanning

    if isScanning:
        btn_text_var.set("Scan")
        isScanning = False
    else:
        btn_text_var.set("Stop SCAN")
        isScanning = True
        threading.Thread(target=capture_live_packets, args=(
            isScanning, 
            get_network_ip(current_lan_ip.get(), current_lan_network.get()), 
            convert_IP_to_binary(current_lan_network.get())
        ), daemon=True).start()
    

btn_text_var = StringVar(value="Scan")
scan_btn = Button(root, textvariable=btn_text_var, font=("Roboto", 16), command=start_scanning).pack(pady=10)

root.mainloop()