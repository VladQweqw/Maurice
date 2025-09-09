from tkinter import *
from tkinter import ttk
import psutil
import threading

# get interfaces
from helpers import find_interfaces, capture_live_packets, get_network_ip, convert_IP_to_binary, dnsResolve

dnsResolve("5.12.125.226")

root = Tk()
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
    print(selected_interface)

    current_lan_ip.set(addresses[selected_interface][1])
    current_lan_network.set(addresses[selected_interface][2])

dropdown.bind("<<ComboboxSelected>>", on_interface_change)

# list
listbox = Listbox(root, font=("Roboto", 16))
listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)

def insert_row(text):
    listbox.insert(START, text)


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
            current_lan_ip.get(),
            get_network_ip(current_lan_ip.get(), current_lan_network.get()), 
            convert_IP_to_binary(current_lan_network.get())
        ), daemon=True).start()
    

btn_text_var = StringVar(value="Scan")
scan_btn = Button(root, textvariable=btn_text_var, font=("Roboto", 16), command=start_scanning).pack(pady=10)

root.mainloop()