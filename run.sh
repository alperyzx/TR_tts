#!/bin/bash
set -e

# Color codes for output
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

# Run the application
echo -e "\n${GREEN}Starting TR_tts application...${NC}"
echo -e "${GREEN}Access the web interface at http://127.0.0.1:5000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}\n"
python3.13 app.py

