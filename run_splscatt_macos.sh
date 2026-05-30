#!/bin/bash

echo "========================================="
echo " SPLSCATT Launcher (macOS)"
echo "========================================="

# --------------------------------------------------

# Check Python

# --------------------------------------------------

if ! command -v python3 >/dev/null 2>&1
then
echo "ERROR: python3 not found."
echo "Install Python first:"
echo "brew install python"
exit 1
fi

# --------------------------------------------------

# Check required modules

# --------------------------------------------------

MISSING=0

for module in numpy scipy tkinter matplotlib
do
python3 -c "import $module" 2>/dev/null

```
if [ $? -ne 0 ]
then
    echo "$module not found"
    MISSING=1
fi
```

done

# --------------------------------------------------

# Install missing modules

# --------------------------------------------------

if [ $MISSING -eq 1 ]
then

```
echo ""
echo "Installing missing Python packages..."
echo ""

python3 -m pip install --upgrade pip

python3 -m pip install \
    numpy \
    scipy \
    matplotlib
```

fi

# --------------------------------------------------

# Verify tkinter again

# --------------------------------------------------

python3 -c "import tkinter" 2>/dev/null

if [ $? -ne 0 ]
then

```
echo ""
echo "ERROR: tkinter is not available."
echo ""

echo "Install a Python distribution that includes Tk:"
echo "  brew install python-tk@3.13"
echo "or"
echo "  https://www.python.org/downloads/mac-osx/"

exit 1
```

fi

# --------------------------------------------------

# Verify files

# --------------------------------------------------

[ -f potgen_gui.py ] || {
echo "ERROR: potgen_gui.py not found"
exit 1
}

[ -f splscatt_gui.py ] || {
echo "ERROR: splscatt_gui.py not found"
exit 1
}

# --------------------------------------------------

# Launch programs

# --------------------------------------------------

echo ""
echo "Starting POTGEN..."
python3 potgen_gui.py &

sleep 1

echo "Starting SPLSCATT..."
python3 splscatt_gui.py &

echo ""
echo "Both programs are running."
echo ""

wait
