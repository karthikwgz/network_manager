import subprocess as sp
from getpass import getpass
from rich import print
from datetime import datetime
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.console import Console

console = Console()

grid = Table.grid(expand=True)
grid.add_column(justify="center", ratio=1)
grid.add_column(justify="right")
grid.add_row(
    "Network Management Tool",
    datetime.now().ctime().replace(":", "[blink]:[/]"),
)
print(Panel(grid, style="white on red"))

def fn_menu():
    grid1 = Table(expand=True,border_style="#FFFF00")
    grid1.add_column("[#79FE0C]Choice[#79FE0C]",justify="right",style="#79FE0C")
    grid1.add_column("[#79FE0C]Details[#79FE0C]",justify="center",style="#79FE0C")
    grid1.add_row(
        "1","Assign IP address"
    )
    grid1.add_row(
        "2","Delete IP address"
    )
    grid1.add_row(
        "3","Display IP address"
    )
    grid1.add_row(
        "4","Display all interfaces"
    )
    grid1.add_row(
        "5","Configure routing"
    )
    grid1.add_row(
        "6","Turn On/Off interface"
    )
    grid1.add_row(
        "7","Add ARP entry"
    )
    grid1.add_row(
        "8","Delete ARP Entry"
    )
    grid1.add_row(
        "9","Restart Network"
    )
    grid1.add_row(
        "10","Change hostname"
    )
    grid1.add_row(
        "11","Add DNS server entry"
    )
    print(grid1)
    console.print("Enter your choice : ",style="magenta")


devi = ""

def interface_menu():
    global devi
    print("___________Interfaces___________\n")
    x = sp.Popen("ls /sys/class/net".split(),stdout=sp.PIPE)
    x = str(x.communicate()[0],"utf-8").rstrip().split("\n")
    for i,ni in enumerate(x):
        console.print(f"Press {i} for {ni}",style="green")
    try:
        ch = int(input())
        if ch >=0 and ch < len(x):
            devi = x[ch]
        else:
            print("Invalid choice")
            interface_menu()
    except:
        print("Enter int value")
        interface_menu()


def display_ip():
    sp.call("ip -c=auto -br address".split())

def find_ip(devi):
    sp.call(f"ip -4 a show {devi}".split())

def display_interface():
    sp.call(f"ip link".split())

def assign_ip(ipadr,devi):
    find_ip(devi)
    password = getpass("Please enter your password: ")
    proc = sp.Popen(f"sudo ip address add {ipadr} dev {devi}".split(), stdin=sp.PIPE)
    proc.communicate(password.encode())
    find_ip(devi)

def delete_ip(ipadr,devi):
    find_ip(devi)
    password = getpass("Please enter your password: ")
    proc = sp.Popen(f"sudo ip address delete {ipadr} dev {devi}".split(), stdin=sp.PIPE)
    proc.communicate(password.encode())
    find_ip(devi)

def on_ni(devi):
    sp.call(f"ip link set dev {devi} up".split())

def off_ni(devi):
    sp.call(f"ip link set dev {devi} down".split())

def ntwrk_restart():
    sp.call("sudo systemctl restart networking".split())

def add_ARP(ipadr,devi):
    mac = input("Enter mac address")
    sp.call(f"ip n add {ipadr} lladdr {mac} dev {devi} nud permanent")
    sp.call("ip n show".split())

def delete_ARP(ipadr,devi):
    sp.call(f"ip n del {ipadr} dev {devi}")
    sp.call("ip n show".split())

def change_hostname():
    host = input("Enter new host name")
    password = getpass("Please enter your password: ")
    proc = sp.Popen(f"sudo hostname {host}".split(), stdin=sp.PIPE)
    proc.communicate(password.encode())

def add_dns():
    dn = input("Enter dns")
    password = getpass("Please enter your password: ")
    x = sp.Popen(f"sudo echo 'nameserver {dn} >> /etc/resolv.conf".split(),stdin=sp.PIPE)
    x = x.communicate(password.encode())

def route(ipadr):
    sp.call(f"ip r add {ipadr} via 192.168.1.1".split())
    sp.call("ip route".split())

def get_ip():
    ipadr = input("Enter ip address")
    return ipadr

def choice():
    fn_menu()
    try:
        ch = int(input())
        if ch == 1:
            interface_menu()
            assign_ip(get_ip(),devi)
        elif ch == 2:
            interface_menu()
            delete_ip(get_ip(),devi)
        elif ch == 3:
            display_ip()
        elif ch == 4:
            display_interface()
        elif ch == 5:
            route(get_ip())
        elif ch == 6:
            print("1.for turn on interface")
            print("2.for turn off interface")
            cho = int(input())
            if cho == 1:
                interface_menu()
                on_ni(devi)
            elif cho == 2:
                interface_menu()
                off_ni(devi)
            else:
                print("invalid")
        elif ch == 7:
            interface_menu()
            add_ARP(get_ip(),devi)
        elif ch == 8:
            interface_menu()
            delete_ARP(get_ip(),devi)
        elif ch == 9:
            ntwrk_restart()
        elif ch == 10:
            change_hostname()
        elif ch == 11:
            add_dns()
    except:
        print("Enter int value")
        choice()
choice()
