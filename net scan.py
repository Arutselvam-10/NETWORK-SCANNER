import tkinter as tk
from tkinter import ttk, messagebox
import socket, subprocess, platform, threading, time, random, math
import psutil

def matrix_effect():
    canvas.delete("matrix")
    for x in range(0, WIDTH, 20):
        y = random.randint(0, HEIGHT)
        char = random.choice("01ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        canvas.create_text(x, y, text=char, fill="#00ff88",
                           font=("Consolas", 12), tags="matrix")
    root.after(120, matrix_effect)

def get_ip():
    return socket.gethostbyname(socket.gethostname())

def firewall_status():
    try:
        r = subprocess.check_output(
            "netsh advfirewall show allprofiles",
            shell=True, text=True
        )
        return "ON" if "ON" in r else "OFF"
    except:
        return "UNKNOWN"

def arp_devices():
    devices = []
    try:
        output = subprocess.check_output("arp -a", shell=True, text=True)
        for line in output.splitlines():
            if "-" in line and "." in line:
                parts = line.split()
                devices.append(parts[0])
    except:
        pass
    return list(set(devices))

def password_strength(pw):
    length = len(pw)
    variety = sum([
        any(c.islower() for c in pw),
        any(c.isupper() for c in pw),
        any(c.isdigit() for c in pw),
        any(c in "!@#$%^&*()" for c in pw)
    ])
    entropy = length * math.log2(26 + 26 + 10 + 10)
    if entropy > 70:
        return "STRONG", entropy
    elif entropy > 40:
        return "MEDIUM", entropy
    else:
        return "WEAK", entropy

def malware_scan():
    suspicious = []
    for proc in psutil.process_iter(['pid','name','cpu_percent']):
        try:
            name = proc.info['name']
            cpu = proc.info['cpu_percent']
            if cpu > 30 or any(x in name.lower() for x in ["tmp","xyz","hack"]):
                suspicious.append(f"{name} | CPU {cpu}%")
        except:
            pass
    return suspicious[:5]

def live_stats():
    io1 = psutil.net_io_counters()
    time.sleep(1)
    io2 = psutil.net_io_counters()
    return (io2.bytes_sent - io1.bytes_sent,
            io2.bytes_recv - io1.bytes_recv)

def attack_simulation():
    logs = [
        "⚠ Port scan detected from 192.168.1.12",
        "⚠ Brute force attempt blocked",
        "⚠ Traffic anomaly detected",
        "⚠ Suspicious ICMP flood"
    ]
    return random.choice(logs)

def start_scan():
    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.insert(tk.END, "[*] Starting security scan...\n")
    output.config(state="disabled")
    threading.Thread(target=run_scan).start()

def run_scan():
    ip = get_ip()
    fw = firewall_status()
    devices = arp_devices()
    sent, recv = live_stats()
    malware = malware_scan()

    ip_card.config(text=f"IP\n{ip}")
    fw_card.config(text=f"FIREWALL\n{fw}")
    score_card.config(text=f"DEVICES\n{len(devices)}")

    output.config(state="normal")
    output.insert(tk.END, f"\nSYSTEM IP: {ip}")
    output.insert(tk.END, f"\nFIREWALL: {fw}")
    output.insert(tk.END, f"\nCONNECTED DEVICES: {devices}")
    output.insert(tk.END, f"\nUPLOAD: {sent//1024} KB/s")
    output.insert(tk.END, f"\nDOWNLOAD: {recv//1024} KB/s\n")

    if malware:
        output.insert(tk.END, "\n⚠ SUSPICIOUS PROCESSES:\n")
        for m in malware:
            output.insert(tk.END, f" - {m}\n")

    output.config(state="disabled")

def check_password():
    pw = pw_entry.get()
    if not pw:
        return
    strength, entropy = password_strength(pw)
    pw_label.config(text=f"{strength} ({int(entropy)} bits)")

def simulate_attacks():
    output.config(state="normal")
    output.insert(tk.END, f"\n{attack_simulation()}\n")
    output.see(tk.END)
    output.config(state="disabled")
    root.after(2000, simulate_attacks)

root = tk.Tk()
WIDTH, HEIGHT = 1100, 650
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Cyber Network Defense Dashboard")
root.configure(bg="#02040a")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                   bg="#02040a", highlightthickness=0)
canvas.place(x=0, y=0)
matrix_effect()

tk.Label(root, text="CYBER NETWORK DEFENSE DASHBOARD",
         fg="#00ffe1", bg="#02040a",
         font=("Consolas", 24, "bold")).place(x=280, y=20)

style = {"bg":"#050a14","fg":"#00ff88","font":("Consolas",12,"bold"),"width":18,"height":3}
ip_card = tk.Label(root, text="IP\n--", **style)
fw_card = tk.Label(root, text="FIREWALL\n--", **style)
score_card = tk.Label(root, text="DEVICES\n--", **style)
ip_card.place(x=150,y=90)
fw_card.place(x=430,y=90)
score_card.place(x=710,y=90)

output = tk.Text(root, bg="#010308", fg="#00ff88",
                 font=("Consolas",11), borderwidth=0)
output.place(x=150,y=200,width=800,height=300)
output.config(state="disabled")

tk.Button(root,text="START SCAN",command=start_scan,
          bg="#00ffe1",fg="black",
          font=("Consolas",12,"bold"),width=15).place(x=300,y=530)

tk.Button(root,text="SIMULATE ATTACKS",command=simulate_attacks,
          bg="#ff3355",fg="white",
          font=("Consolas",12,"bold"),width=18).place(x=520,y=530)

tk.Label(root,text="PASSWORD CHECK",
         fg="#00ff88",bg="#02040a",
         font=("Consolas",11,"bold")).place(x=150,y=570)

pw_entry = tk.Entry(root, show="*", width=25, font=("Consolas",11))
pw_entry.place(x=300,y=570)

tk.Button(root,text="CHECK",command=check_password,
          bg="#00ff88",fg="black").place(x=530,y=567)

pw_label = tk.Label(root,text="",fg="#ffaa00",bg="#02040a",
                    font=("Consolas",11,"bold"))
pw_label.place(x=620,y=570)

root.mainloop()
