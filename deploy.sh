#!/bin/bash
set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Banner
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}TR_tts Project Deployment${NC}"
echo -e "${GREEN}================================${NC}"

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    echo -e "\n${YELLOW}Creating virtual environment...${NC}"
    python3.13 -m venv .venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

if [ -d ".venv" ]; then
    echo -e "\n${YELLOW}Activating virtual environment...${NC}"
    source .venv/bin/activate
    echo -e "${GREEN}Virtual environment activated.${NC}"
fi


# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
PYTHON_VERSION=$(python3.13 --version 2>/dev/null | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ -z "$PYTHON_VERSION" ]; then
    echo -e "${RED}Error: python3.13 is not installed or not in PATH${NC}"
    exit 1
fi
if [ "$PYTHON_MAJOR" -lt 3 ] || [ "$PYTHON_MAJOR" -eq 3 -a "$PYTHON_MINOR" -lt 13 ]; then
    echo -e "${RED}Error: Python 3.13+ is required. Found $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}Python $PYTHON_VERSION found. OK!${NC}"

# Check FFmpeg
echo -e "\n${YELLOW}Checking FFmpeg...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}Error: FFmpeg is not installed or not in PATH${NC}"
    echo "Please install FFmpeg from https://github.com/BtbN/FFmpeg-Builds/releases"
    exit 1
fi
echo -e "${GREEN}FFmpeg is installed. OK!${NC}"

# Check Google Cloud credentials
echo -e "\n${YELLOW}Checking Google Cloud credentials...${NC}"
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    # Check for default credentials location
    DEFAULT_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"
    if [ -f "$DEFAULT_CREDENTIALS" ]; then
        export GOOGLE_APPLICATION_CREDENTIALS="$DEFAULT_CREDENTIALS"
        echo -e "${GREEN}Found default Google Cloud credentials at $DEFAULT_CREDENTIALS${NC}"
    else
        echo -e "${YELLOW}Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set${NC}"
        echo "You may need to set up Google Cloud credentials before TTS functionality will work."
        echo "See: https://cloud.google.com/docs/authentication/application-default-credentials"
    fi
else
    echo -e "${GREEN}GOOGLE_APPLICATION_CREDENTIALS is set.${NC}"
fi

# Ensure pip is installed for Python 3.13
echo -e "\n${YELLOW}Checking pip for Python 3.13...${NC}"
if ! python3.13 -m pip --version &> /dev/null; then
    echo -e "${YELLOW}pip not found for Python 3.13. Installing...${NC}"
    python3.13 -m ensurepip --upgrade || \
    (curl -O https://bootstrap.pypa.io/get-pip.py && python3.13 get-pip.py)
    python3.13 -m pip install --upgrade pip
fi

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
python3.13 -m pip install --upgrade pip
python3.13 -m pip install -r requirements.txt

echo -e "\n${YELLOW}Create your own variables.cfg from variables.cfg_default${NC}"
if [ -f variables.cfg ]; then
    echo -e "${YELLOW}variables.cfg already exists.${NC}"
    read -p "Overwrite variables.cfg with default? [y/N]: " overwrite_cfg
    if [[ "$overwrite_cfg" =~ ^[Yy]$ ]]; then
        cp variables.cfg_default variables.cfg
        echo -e "${GREEN}variables.cfg overwritten with default.${NC}"
    else
        echo -e "${YELLOW}Skipped overwriting variables.cfg.${NC}"
    fi
else
    cp variables.cfg_default variables.cfg
    echo -e "${GREEN}variables.cfg created from default. ${NC}"
fi

echo -e "\n${YELLOW}Define required directories: output pictures files/combined_audio files/videos${NC}"
mkdir -p output pictures files/combined_audio files/videos
echo -e "${GREEN}Directories created.${NC}"
