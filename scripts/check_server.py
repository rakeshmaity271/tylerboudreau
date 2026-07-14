import paramiko
import sys

host = "194.163.151.182"
user = "root"
password = "rakeshmaity"
project_path = "/home/kodeclouds-tylerboudreau/htdocs/tylerboudreau.kodeclouds.com"

commands = [
    f"echo '=== Files in project dir ==='",
    f"ls -la {project_path}/",
    f"echo '=== Check index.html ==='",
    f"head -5 {project_path}/index.html 2>/dev/null || echo 'No index.html found'",
    f"echo '=== Check for images ==='",
    f"ls -la {project_path}/images/ 2>/dev/null || echo 'No images dir'",
    f"echo '=== Check HTML pages ==='",
    f"ls {project_path}/*.html 2>/dev/null || echo 'No HTML files'",
    f"echo '=== Nginx/Apache config ==='",
    f"ls /etc/nginx/sites-enabled/ 2>/dev/null || echo 'No nginx sites-enabled'",
    f"cat /etc/nginx/sites-enabled/*tyler* 2>/dev/null || echo 'No tylerboudreau nginx config'",
    f"ls /etc/apache2/sites-enabled/ 2>/dev/null || echo 'No apache sites-enabled'",
    f"echo '=== CloudPanel vhost ==='",
    f"ls /etc/nginx/sites-enabled/ 2>/dev/null",
    f"echo '=== Web root check ==='",
    f"find /home/kodeclouds-tylerboudreau -name 'index.html' -type f 2>/dev/null",
]

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=22, username=user, password=password, timeout=15, allow_agent=False, look_for_keys=False)
    print("Connected!\n")

    for cmd in commands:
        print(f"$ {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode().strip()
        if out: print(out)
        print()

    client.close()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
