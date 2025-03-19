#!/bin/bash

# CloudShell saves the files you have created but not installed packages and software
# so you may need to run this after being inactive on CloudShell

curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh
chmod +x install-opentofu.sh
./install-opentofu.sh --install-method standalone --skip-verify
rm install-opentofu.sh

# Define paths
CACHE_DIR="$HOME/.terraform.d/plugin-cache"
CONFIG_FILE="$HOME/.tofurc"

# Ensure the cache directory exists
if [ ! -d "$CACHE_DIR" ]; then
  echo "📂 Creating OpenTofu provider cache directory..."
  mkdir -p "$CACHE_DIR"
fi

# Set up OpenTofu/Terraform to use the cache
echo "⚙️ Configuring OpenTofu provider cache..."
cat <<EOF > "$CONFIG_FILE"
plugin_cache_dir = "$CACHE_DIR"
EOF

tofu init