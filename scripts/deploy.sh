#!/usr/bin/env bash
#
# Manual deployment script for Tyler Boudreau
# Usage: bash scripts/deploy.sh
#
# Prerequisites:
#   - SSH key configured for server access (or password)
#   - rsync installed locally
#
set -euo pipefail

# ── Configuration ───────────────────────────────────────────────
SERVER_HOST="194.163.151.182"
SERVER_USER="root"
SERVER_PORT="22"
PROJECT_PATH="/home/kodeclouds-tylerboudreau/htdocs/tylerboudreau.kodeclouds.com"

# ── Colors ──────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ── Pre-flight checks ──────────────────────────────────────────
info "Running pre-flight checks..."

command -v ssh  >/dev/null 2>&1 || error "SSH is not available"

# ── Deploy ──────────────────────────────────────────────────────
info "Deploying to ${SERVER_USER}@${SERVER_HOST}:${PROJECT_PATH}"

# Create target directory if it doesn't exist
ssh -p "$SERVER_PORT" "${SERVER_USER}@${SERVER_HOST}" \
  "mkdir -p ${PROJECT_PATH}"

# Sync all site files to server
rsync -avz --delete \
  --exclude='.git/' \
  --exclude='.github/' \
  --exclude='scripts/' \
  --exclude='*.png' \
  --exclude='.gitattributes' \
  --exclude='.gitignore' \
  -e "ssh -p ${SERVER_PORT}" \
  ./ \
  "${SERVER_USER}@${SERVER_HOST}:${PROJECT_PATH}/"

# ── Verify ──────────────────────────────────────────────────────
info "Verifying deployment..."

ssh -p "$SERVER_PORT" "${SERVER_USER}@${SERVER_HOST}" bash <<REMOTE
  if [ -f "${PROJECT_PATH}/index.html" ]; then
    echo "✓ index.html found"
    echo "✓ Files: \$(ls -1 ${PROJECT_PATH} | wc -l) items"
    echo "✓ Deployed at: \$(date)"
  else
    echo "✗ index.html NOT found — deployment may have failed"
    exit 1
  fi
REMOTE

info "Deployment complete! → https://tylerboudreau.kodeclouds.com"
