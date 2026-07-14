#!/bin/bash
# ===================================================================
# Deploy script for Tyler Boudreau therapy website
# This script runs ON THE SERVER after GitHub Actions connects via SSH
# ===================================================================

set -e  # Exit immediately if a command exits with a non-zero status

WEB_ROOT="/home/kodeclouds-tylerboudreau/htdocs/tylerboudreau.kodeclouds.com"
REPO_URL="https://github.com/rakeshmaity271/tylerboudreau.git"
BRANCH="main"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Ensure we're in the web root directory
cd "$WEB_ROOT" || {
    log_error "Failed to navigate to web root: $WEB_ROOT"
    exit 1
}

log_info "Starting deployment in: $(pwd)"

# Check if this is a git repository
if [ ! -d ".git" ]; then
    log_warn "Not a git repository. Cloning fresh into temp directory..."
    TMP_DIR=$(mktemp -d)
    git clone "$REPO_URL" "$TMP_DIR"
    # Move files from temp to web root, overwriting existing placeholder files
    shopt -s dotglob
    mv "$TMP_DIR"/* "$WEB_ROOT"/ 2>/dev/null || true
    rm -rf "$TMP_DIR"
    log_info "Repository cloned to web root."
else
    # Reset any local changes and pull latest code
    log_info "Pulling latest code from $BRANCH branch..."
    git reset --hard HEAD
    git clean -fd
    git pull origin "$BRANCH"
fi

# Verify the pull was successful
if [ $? -ne 0 ]; then
    log_error "Git pull failed. Deployment aborted."
    exit 1
fi

# Set correct ownership/permissions (optional, adjust as needed)
log_info "Setting file permissions..."
chown -R www-data:www-data "$WEB_ROOT" 2>/dev/null || true
find "$WEB_ROOT" -type d -exec chmod 755 {} \; 2>/dev/null || true
find "$WEB_ROOT" -type f -exec chmod 644 {} \; 2>/dev/null || true

log_info "Deployment completed successfully!"
log_info "Site live at: https://tylerboudreau.kodeclouds.com"
