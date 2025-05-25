#!/bin/bash
set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Banner
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}TR_tts Project Runner${NC}"
echo -e "${GREEN}================================${NC}"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo -e "\n${YELLOW}Activating virtual environment...${NC}"
    source .venv/bin/activate
    echo -e "${GREEN}Virtual environment activated.${NC}"
fi

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

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
    echo -e "${YELLOW}Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set${NC}"
    echo "You may need to set up Google Cloud credentials before TTS functionality will work."
    echo "See: https://cloud.google.com/docs/authentication/application-default-credentials"
fi

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create necessary directories
echo -e "\n${YELLOW}Setting up directories...${NC}"
mkdir -p output work

# Run the application
echo -e "\n${GREEN}Starting TR_tts application...${NC}"
echo -e "${GREEN}Access the web interface at http://127.0.0.1:5000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}\n"
python app.py

