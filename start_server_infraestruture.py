import subprocess

scripts = ["servidor.py", "edgeComputing_server1.py","edgeComputing_server2.py","dnsServer.py", "loadBalance.py"]

for script in scripts:
    subprocess.Popen(['start', 'cmd', '/k', 'python', script], shell=True)