#!/bin/bash

echo "========================================="
echo " SPLSCATT Launcher"
echo "========================================="

# -----------------------------
# Detect package manager
# -----------------------------

PKG=""

if command -v dnf >/dev/null 2>&1
then
    PKG="dnf"

elif command -v apt >/dev/null 2>&1
then
    PKG="apt"

else
    echo "Unsupported Linux distribution"
    exit 1
fi

# -----------------------------
# Check Python
# -----------------------------

if ! command -v python3 >/dev/null 2>&1
then
    echo "python3 not found"
    exit 1
fi

# -----------------------------
# Check modules
# -----------------------------

MISSING=0

for module in numpy scipy tkinter matplotlib
do
    python3 -c "import $module" 2>/dev/null

    if [ $? -ne 0 ]
    then
        echo "$module not found"
        MISSING=1
    fi
done

# -----------------------------
# Install if needed
# -----------------------------

if [ $MISSING -eq 1 ]
then

    if [ "$PKG" = "dnf" ]
    then

        sudo dnf install -y \
            python3-numpy \
            python3-scipy \
            python3-tkinter \
            python3-matplotlib

    else

        sudo apt update

        sudo apt install -y \
            python3-numpy \
            python3-scipy \
            python3-tk \
            python3-matplotlib

    fi

fi

# -----------------------------
# Verify files
# -----------------------------

[ -f potgen_gui.py ] || { echo "potgen_gui.py not found"; exit 1; }
[ -f splscatt_gui.py ] || { echo "splscatt_gui.py not found"; exit 1; }

# -----------------------------
# Launch
# -----------------------------

echo "Starting POTGEN..."
python3 potgen_gui.py &

sleep 1

echo "Starting SPLSCATT..."
python3 splscatt_gui.py &

wait
