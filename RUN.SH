#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
VENV_DIR="${BACKEND_DIR}/.venv"

cd "${BACKEND_DIR}"

if [[ ! -d "${VENV_DIR}" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "מפעיל את מחולל ברכות סבתא..."
echo "פתחי http://127.0.0.1:5000 בדפדפן"
echo "לחצי Ctrl+C לעצירה"
echo ""

flask --app app run --debug
