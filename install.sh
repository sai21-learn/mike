#!/bin/bash
#
# Mike Installer - Local-first AI Assistant
# Usage: curl -fsSL https://raw.githubusercontent.com/sai21-learn/mike/main/install.sh | bash
#

set -e

REPO="sai21-learn/mike"
INSTALL_DIR="$HOME/.mike"
BIN_DIR="$HOME/.local/bin"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "           _ _        "
echo " _ __ ___ (_) | _____ "
echo " | '_ \` _ \| | |/ / _ \\"
echo " | | | | | | |   <  __/"
echo " |_| |_| |_|_|_|\\_\\___|"
echo -e "${NC}"
echo "Mike: Your Local AI Assistant"
echo "=============================="
echo

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
            return 0
        fi
    fi

    echo -e "${RED}✗${NC} Python 3.10+ required"
    echo "  Install from: https://www.python.org/downloads/"
    exit 1
}

# Check Ollama
check_ollama() {
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}✓${NC} Ollama found"
        return 0
    fi

    echo -e "${YELLOW}!${NC} Ollama not found"
    echo "  Install from: https://ollama.ai"
    echo "  Continuing anyway - you'll need it to run Mike"
    return 0
}

# Install Mike
install_mike() {
    echo
    echo "Installing Mike..."

    # Create directories
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"

    # Clone or download
    if command -v git &> /dev/null; then
        echo "Cloning repository..."
        if [ -d "$INSTALL_DIR/src" ]; then
            cd "$INSTALL_DIR/src" && git pull
        else
            git clone "https://github.com/$REPO.git" "$INSTALL_DIR/src"
        fi
    else
        echo "Downloading source..."
        curl -sL "https://github.com/$REPO/archive/main.tar.gz" | tar xz -C "$INSTALL_DIR"
        rm -rf "$INSTALL_DIR/src"
        mv "$INSTALL_DIR/mike-main" "$INSTALL_DIR/src"
    fi

    # Create environment
    if command -v uv &> /dev/null; then
        echo "Using 'uv' for environment setup..."
        cd "$INSTALL_DIR/src"
        uv venv "$INSTALL_DIR/venv" --python 3.13 || uv venv "$INSTALL_DIR/venv"
        source "$INSTALL_DIR/venv/bin/activate"
        uv pip install -e ".[all]"
    else
        echo "Setting up Python venv..."
        python3 -m venv "$INSTALL_DIR/venv"
        source "$INSTALL_DIR/venv/bin/activate"
        pip install --upgrade pip
        pip install -e "$INSTALL_DIR/src[all]"
    fi

    # Create wrapper script
    cat > "$BIN_DIR/mike" << 'WRAPPER'
#!/bin/bash
if [ -f "$HOME/.mike/venv/bin/activate" ]; then
    source "$HOME/.mike/venv/bin/activate"
    python -m mike.cli "$@"
else
    echo "Mike environment not found. Please reinstall."
    exit 1
fi
WRAPPER
    chmod +x "$BIN_DIR/mike"

    echo -e "${GREEN}✓${NC} Mike installed successfully"
}

# Add to PATH if needed
setup_path() {
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo
        echo "Adding $BIN_DIR to PATH..."

        SHELL_RC=""
        if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -f "$HOME/.bashrc" ]; then
            SHELL_RC="$HOME/.bashrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            SHELL_RC="$HOME/.bash_profile"
        fi

        if [ -n "$SHELL_RC" ]; then
            if ! grep -q "$BIN_DIR" "$SHELL_RC"; then
                echo -e "\n# Mike Assistant\nexport PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
                echo -e "${GREEN}✓${NC} Added to $SHELL_RC"
                echo -e "${YELLOW}!${NC} Run: source $SHELL_RC"
            fi
        else
            echo -e "${YELLOW}!${NC} Add to your shell config: export PATH=\"\$HOME/.local/bin:\$PATH\""
        fi
    fi
}

# Download recommended models
setup_models() {
    echo
    echo -e "${BLUE}Recommended Models:${NC}"
    echo "  - qwen2.5:3b    (Fast, balanced)"
    echo "  - llama3.2      (Modern, capable)"
    echo "  - llava         (Vision support)"
    echo
    read -p "Download recommended Ollama models now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v ollama &> /dev/null; then
            echo "Pulling models..."
            ollama pull qwen2.5:3b || true
            ollama pull llama3.2 || true
            ollama pull llava || true
            echo -e "${GREEN}✓${NC} Models ready"
        else
            echo -e "${YELLOW}!${NC} Ollama not found, pull manually later: ollama pull qwen2.5:3b"
        fi
    fi
}

# Main
main() {
    check_python
    check_ollama
    install_mike
    setup_path
    setup_models

    echo
    echo -e "${GREEN}Installation complete!${NC}"
    echo
    echo "Try it out:"
    echo "  mike chat \"hello\""
    echo "  mike --dev"
    echo
    echo "Full documentation: https://github.com/sai21-learn/mike"
}

main
