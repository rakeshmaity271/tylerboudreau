import paramiko
import sys

host = "194.163.151.182"
user = "root"
password = "rakeshmaity"
project_path = "/home/kodeclouds-tylerboudreau/htdocs/tylerboudreau.kodeclouds.com"

commands = [
    # Rename index.php so Nginx serves index.html instead
    f"mv {project_path}/index.php {project_path}/index.php.bak 2>/dev/null || echo 'No index.php to rename'",
    f"echo '=== index.php renamed ==='",
    # Verify index.html is correct
    f"head -5 {project_path}/index.html",
    # Check HTML pages exist
    f"ls -la {project_path}/*.html 2>/dev/null || echo 'No HTML files'",
    # Check images are present
    f"ls -la {project_path}/images/ 2>/dev/null | head -5 || echo 'No images dir'",
    # Set correct permissions
    f"chmod -R 755 {project_path}",
    f"chown -R www-data:www-data {project_path} 2>/dev/null || chown -R kodeclouds-tylerboudreau:kodeclouds-tylerboudreau {project_path}",
    # Reload Nginx to pick up changes
    "systemctl reload nginx 2>/dev/null || echo 'nginx reload skipped'",
    "echo '=== Nginx reloaded ==='",
    # Verify the site serves index.html now
    f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:8080/ 2>/dev/null || echo 'curl check skipped'",
    f"echo ''",
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
        err = stderr.read().decode().strip()
        if out: print(out)
        if err: print(f"  (stderr: {err})")
        print()

    client.close()
    print("\nFix applied! The site should now serve the Tyler Boudreau website.")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
