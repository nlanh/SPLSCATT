#!/usr/bin/env python3

import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

# --------------------------------------------------
# Mesh
# --------------------------------------------------

rmin = 0.05
rmax = 15.0
dr   = 0.05

r = np.arange(rmin, rmax + dr, dr)

# --------------------------------------------------
# Potential definitions
# --------------------------------------------------

POTENTIALS = {

    "Square well": {
        "formula":
        "V(r) = V0   (r <= R), 0 otherwise",

        "params": [
            ("V0", "Depth (MeV)"),
            ("R",  "Radius (fm)")
        ]
    },

    "Woods-Saxon": {
        "formula":
        "V(r) = V0 / [1 + exp((r-R)/a)]",

        "params": [
            ("V0", "Depth (MeV)"),
            ("R",  "Radius (fm)"),
            ("a",  "Diffuseness (fm)")
        ]
    },

    "One-Yukawa": {
        "formula":
        "V(r) = V1 exp(-mu1 r) / r",

        "params": [
            ("V1",  "Strength (MeV fm)"),
            ("mu1", "Range parameter (fm^-1)")
        ]
    },

    "Two-Yukawa (Malfliet-Tjon)": {
        "formula":
        "V(r)=VR exp(-muR r)/r - VA exp(-muA r)/r",

        "params": [
            ("VR",  "Repulsive strength (MeV fm)"),
            ("muR", "Repulsive range (fm^-1)"),
            ("VA",  "Attractive strength (MeV fm)"),
            ("muA", "Attractive range (fm^-1)")
        ]
    },

    "Three-Yukawa": {
        "formula":
        "V(r)=Σ Vi exp(-mui r)/r",

        "params": [
            ("V1",  "Strength 1 (MeV fm)"),
            ("mu1", "Range 1 (fm^-1)"),
            ("V2",  "Strength 2 (MeV fm)"),
            ("mu2", "Range 2 (fm^-1)"),
            ("V3",  "Strength 3 (MeV fm)"),
            ("mu3", "Range 3 (fm^-1)")
        ]
    },

    "Gaussian": {
        "formula":
        "V(r) = V0 exp[-(r/a)^2]",

        "params": [
            ("V0", "Depth (MeV)"),
            ("a",  "Range (fm)")
        ]
    }
}

# --------------------------------------------------
# Global storage
# --------------------------------------------------

entries = {}

# --------------------------------------------------
# Update GUI fields
# --------------------------------------------------

def update_fields(event=None):

    ptype = combo.get()

    formula_label.config(
        text=POTENTIALS[ptype]["formula"]
    )

    for widget in param_frame.winfo_children():
        widget.destroy()

    entries.clear()

    for name, description in POTENTIALS[ptype]["params"]:

        row = tk.Frame(param_frame)
        row.pack(fill="x", pady=3)

        tk.Label(
            row,
            text=name,
            width=10,
            anchor="w"
        ).pack(side="left")

        entry = tk.Entry(row, width=20)

        entry.pack(
            side="left",
            padx=5
        )

        tk.Label(
            row,
            text=description,
            anchor="w"
        ).pack(side="left")

        entries[name] = entry

# --------------------------------------------------
# Generate potential
# --------------------------------------------------

def generate():

    try:

        ptype = combo.get()

        # ------------------------------
        # Square well
        # ------------------------------

        if ptype == "Square well":

            V0 = float(entries["V0"].get())
            R  = float(entries["R"].get())

            V = np.where(r <= R, V0, 0.0)

            metadata = [
                "# Potential type : Square well",
                f"# V0 = {V0} MeV",
                f"# R  = {R} fm"
            ]

        # ------------------------------
        # Woods-Saxon
        # ------------------------------

        elif ptype == "Woods-Saxon":

            V0 = float(entries["V0"].get())
            R  = float(entries["R"].get())
            a  = float(entries["a"].get())

            V = V0 / (
                1.0 + np.exp((r - R)/a)
            )

            metadata = [
                "# Potential type : Woods-Saxon",
                f"# V0 = {V0} MeV",
                f"# R  = {R} fm",
                f"# a  = {a} fm"
            ]

        # ------------------------------
        # One Yukawa
        # ------------------------------

        elif ptype == "One-Yukawa":

            V1  = float(entries["V1"].get())
            mu1 = float(entries["mu1"].get())

            V = V1*np.exp(-mu1*r)/r

            metadata = [
                "# Potential type : One-Yukawa",
                f"# V1  = {V1} MeV fm",
                f"# mu1 = {mu1} fm^-1"
            ]

        # ------------------------------
        # Two Yukawa
        # ------------------------------

        elif ptype == "Two-Yukawa (Malfliet-Tjon)":

            VR  = float(entries["VR"].get())
            muR = float(entries["muR"].get())

            VA  = float(entries["VA"].get())
            muA = float(entries["muA"].get())

            V = (
                VR*np.exp(-muR*r)/r
                - VA*np.exp(-muA*r)/r
            )

            metadata = [
                "# Potential type : Two-Yukawa",
                f"# VR  = {VR} MeV fm",
                f"# muR = {muR} fm^-1",
                f"# VA  = {VA} MeV fm",
                f"# muA = {muA} fm^-1"
            ]

        # ------------------------------
        # Three Yukawa
        # ------------------------------

        elif ptype == "Three-Yukawa":

            V1  = float(entries["V1"].get())
            mu1 = float(entries["mu1"].get())

            V2  = float(entries["V2"].get())
            mu2 = float(entries["mu2"].get())

            V3  = float(entries["V3"].get())
            mu3 = float(entries["mu3"].get())

            V = (
                V1*np.exp(-mu1*r)/r
                + V2*np.exp(-mu2*r)/r
                + V3*np.exp(-mu3*r)/r
            )

            metadata = [
                "# Potential type : Three-Yukawa"
            ]

        # ------------------------------
        # Gaussian
        # ------------------------------

        elif ptype == "Gaussian":

            V0 = float(entries["V0"].get())
            a  = float(entries["a"].get())

            V = V0*np.exp(
                -(r/a)**2
            )

            metadata = [
                "# Potential type : Gaussian",
                f"# V0 = {V0} MeV",
                f"# a  = {a} fm"
            ]

        else:

            raise ValueError(
                "Unknown potential type"
            )

        header = "\n".join(metadata)
        header += "\n#\n# r(fm)      V(MeV)"

        np.savetxt(
            "potential.dat",
            np.column_stack((r, V)),
            fmt="%14.6E",
            header=header,
            comments=""
        )

        status_label.config(
            text="potential.dat written successfully"
        )

    except Exception as err:

        messagebox.showerror(
            "Error",
            str(err)
        )

# --------------------------------------------------
# GUI
# --------------------------------------------------

root = tk.Tk()

root.title("POTGEN")
root.geometry("720x550")

title = tk.Label(
    root,
    text="Potential Generator for SPLSCATT",
    font=("Arial", 14, "bold")
)

title.pack(pady=10)

# Potential selection

selection_frame = tk.Frame(root)
selection_frame.pack(pady=5)

tk.Label(
    selection_frame,
    text="Potential type:"
).pack(side="left")

combo = ttk.Combobox(
    selection_frame,
    width=35,
    state="readonly",
    values=list(POTENTIALS.keys())
)

combo.pack(side="left", padx=5)

combo.current(1)

# Formula

formula_label = tk.Label(
    root,
    text="",
    font=("Courier", 11),
    justify="left"
)

formula_label.pack(pady=10)

# Parameters

param_frame = tk.LabelFrame(
    root,
    text="Parameters",
    padx=10,
    pady=10
)

param_frame.pack(
    fill="x",
    padx=10,
    pady=5
)

# Generate button

button = tk.Button(
    root,
    text="Generate potential.dat",
    command=generate,
    width=30,
    height=2
)

button.pack(pady=15)

# Status

status_frame = tk.Frame(root)
status_frame.pack(
    side="bottom",
    fill="x",
    padx=5,
    pady=5
)

status_label = tk.Label(
    status_frame,
    text="Ready",
    anchor="w"
)

status_label.pack(
    side="left"
)

copyright_label = tk.Label(
    status_frame,
    text="POTGEN v0.1 | © 2026 Nguyen Le Anh (PhD), HCMUE",
    fg="gray40"
)

copyright_label.pack(
    side="right"
)

# Description

description = tk.LabelFrame(
    root,
    text="Description",
    padx=10,
    pady=10
)

description.pack(
    fill="x",
    padx=10,
    pady=10
)

tk.Label(
    description,
    justify="left",
    text=
    "V0 : potential depth\n"
    "R  : radius parameter\n"
    "a  : diffuseness or range\n"
    "mu : inverse range parameter\n"
    "Generated potential is saved to potential.dat"
).pack(anchor="w")

combo.bind(
    "<<ComboboxSelected>>",
    update_fields
)

update_fields()

root.mainloop()
