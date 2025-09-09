from tkinter import *
from tkinter import ttk
import psutil

# get interfaces
from helpers import find_interfaces

root = Tk()
root.geometry('300x500')
title = Label(root, text="Network spy", font=("Roboto", 16)).pack(pady=10)


current_lan_ip = StringVar(value="LAN IP:")
current_lan_network = StringVar(value="LAN Network:")

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

    current_lan_ip.set("LAN IP: " + addresses[selected_interface][1])
    current_lan_network.set("LAN Network: " + addresses[selected_interface][2])

dropdown.bind("<<ComboboxSelected>>", on_interface_change)


items = ['a', 'c', 'd']
# list
listbox = Listbox(root, font=("Roboto", 16))
listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)

for item in items:
    listbox.insert(END, item)

def add_item():
    listbox.insert(END, "d")

scan_btn = Button(root, text="Scan", font=("Roboto", 16), command=add_item).pack(pady=10)

root.mainloop()