import paramiko
import sys

host = "194.163.151.182"
user = "root"
password = "rakeshmaity"
project_path = "/home/kodeclouds-tylerboudreau/htdocs/tylerboudreau.kodeclouds.com"

commands = [
    "echo '=== Server Info ==='",
    "whoami",
    "pwd",
    f"mkdir -p {project_path}",
    f"ls -la /home/kodeclouds-tylerboudreau/htdocs/",
    "which git 2>/dev/null && git --version || echo 'git: not found'",
    "which rsync 2>/dev/null && rsync --version | head -1 || echo 'rsync: not found'",
    "which php 2>/dev/null && php --version | head -1 || echo 'php: not found'",
    f"chmod -R 775 {project_path}",
    f"ls -la {project_path}",
    "echo '=== Setup Complete ==='",
]

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {host} as {user}...")
    client.connect(host, port=22, username=user, password=password, timeout=15, allow_agent=False, look_for_keys=False)
    print("Connected!\n")

    for cmd in commands:
        print(f"$ {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        if out: print(out)
        if err: print(f"  (stderr: {err})")
        print()

    client.close()
    print("Server setup complete!")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
