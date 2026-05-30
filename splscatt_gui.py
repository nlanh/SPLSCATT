#!/usr/bin/env python3

import numpy as np
from scipy.special import spherical_jn, spherical_yn, eval_legendre
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def kinetic_factor(mu):
    return HBARC**2 / (2.0 * mu * AMU)

# -----------------------------
# Read potential
# -----------------------------
def read_potential(filename):
    data = np.loadtxt(filename)
    r = data[:,0]
    V = data[:,1]
    return r, V

# -----------------------------
# Numerov solver
# -----------------------------
def numerov(r, k2, l):
    h = r[1] - r[0]
    u = np.zeros_like(r)

    # regular solution near origin
    u[0] = 0.0
    u[1] = r[1]**(l+1)

    for i in range(1, len(r)-1):
        f_im1 = 1 + h**2 * k2[i-1] / 12.0
        f_i   = 1 + h**2 * k2[i]   / 12.0
        f_ip1 = 1 + h**2 * k2[i+1] / 12.0

        u[i+1] = (
            2*(1 - 5*h**2*k2[i]/12.0)*u[i]
            - f_im1*u[i-1]
        ) / f_ip1

    return u

# -----------------------------
# Phase shift from matching
# -----------------------------
def phase_shift(r, u, l, k):
    # choose asymptotic points
    n1 = -5
    n2 = -2

    r1, r2 = r[n1], r[n2]
    u1, u2 = u[n1], u[n2]

    ratio = u2/u1

    kr1, kr2 = k*r1, k*r2

    jl1 = spherical_jn(l, kr1)
    jl2 = spherical_jn(l, kr2)

    nl1 = spherical_yn(l, kr1)
    nl2 = spherical_yn(l, kr2)

    num = ratio*jl1 - jl2
    den = ratio*nl1 - nl2

    delta = np.arctan2(num, den)
    return delta

# -----------------------------
# Compute phase shifts
# -----------------------------
def compute_phase_shifts(r, V, mu, E, lmax=10):
    alpha = kinetic_factor(mu)

    if E <= 0:
        raise ValueError("Scattering energy must be positive")

    k = np.sqrt(E / alpha)

    deltas = []
    ulist = []

    for l in range(lmax+1):

        # avoid division by zero
        centrifugal = np.zeros_like(r)
        centrifugal[1:] = l*(l+1)/r[1:]**2
        centrifugal[0] = centrifugal[1]

        k2 = (E - V)/alpha - centrifugal

        u = numerov(r, k2, l)

        # normalize to avoid overflow
        u /= np.max(np.abs(u))
        ulist.append(u.copy())

        delta = phase_shift(r, u, l, k)
        deltas.append(delta)

    return k, np.array(deltas), np.array(ulist)

# -----------------------------
# Scattering amplitude
# -----------------------------
def scattering_amplitude(theta, k, deltas):
    costh = np.cos(theta)
    f = np.zeros_like(theta, dtype=complex)

    for l, delta in enumerate(deltas):
        Sl = np.exp(2j*delta)
        Pl = eval_legendre(l, costh)
        f += (2*l+1)*(Sl-1)*Pl

    f /= (2j*k)
    return f
    
def get_inputs():

    result = {}

    def browse():

        filename = filedialog.askopenfilename(

            title="Select potential file"

        )

        if filename:

            file_entry.delete(0, tk.END)

            file_entry.insert(0, filename)

    def run():

        try:
            unit_system = unit_var.get()

            filename = file_entry.get()

            mu = float(mu_entry.get())

            E = float(E_entry.get())

            lmax = int(lmax_entry.get())

            status_label.config(

                text="Running...",

                fg="orange"

            )

            root.update()

            run_scatt(

                unit_system,

                filename,

                mu,

                E,

                lmax

            )

            status_label.config(

                text="Calculation finished. Output written to scatt.out",

                fg="green"

            )
        except Exception as err:

            messagebox.showerror(

                "Input error",

                str(err)

            )

    root = tk.Tk()

    root.title("SPLSCATT")

    root.geometry("600x550")

    tk.Label(

        root,

        text="SPLSCATT",

        font=("Arial",18,"bold")

    ).pack(pady=(10,0))

    tk.Label(

        root,

        text="A Spinless Partial-Wave Elastic Scattering Code",

        font=("Arial",10)

    ).pack()

    tk.Label(

        root,

        text="for Finite-Range Central Potentials",

        font=("Arial",10)

    ).pack(pady=(0,15))

    unit_var = tk.IntVar(value=1)

    tk.Label(

        root,

        text="Unit system"

    ).pack()

    tk.Radiobutton(

        root,

        text="Nuclear units (MeV, fm)",

        variable=unit_var,

        value=1

    ).pack(anchor="w", padx=30)

    tk.Radiobutton(

        root,

        text="Natural units (ħ = c = 1)",

        variable=unit_var,

        value=2

    ).pack(anchor="w", padx=30)

    tk.Label(

        root,

        text="Potential file"

    ).pack(pady=(10,0))

    file_frame = tk.Frame(root)

    file_frame.pack()

    file_entry = tk.Entry(

        file_frame,

        width=40

    )

    file_entry.pack(side="left")

    file_entry.insert(0, "potential.dat")

    tk.Button(

        file_frame,

        text="Browse",

        command=browse

    ).pack(side="left", padx=5)

    tk.Label(

        root,

        text="Reduced mass μ (amu)"

    ).pack()

    mu_entry = tk.Entry(root)

    mu_entry.pack()
    
    mu_entry.insert(0, "1")

    tk.Label(

        root,

        text="Scattering energy E (MeV)"

    ).pack()

    E_entry = tk.Entry(root)

    E_entry.pack()
    
    E_entry.insert(0, "1")

    tk.Label(

        root,

        text="lmax"

    ).pack()

    lmax_entry = tk.Entry(root)

    lmax_entry.pack()

    lmax_entry.insert(0, "10")

    tk.Button(

        root,

        text="Run",

        command=run

    ).pack(pady=15)

    tk.Label(

        root,

        text="SPLSCATT v0.1 | © 2026 Nguyen Le Anh (PhD), HCMUE",

        fg="gray40"

    ).pack(side="bottom", pady=10)

    status_label = tk.Label(
        root,
        text="Ready",
        fg="blue"
    )

    status_label.pack(pady=10)
    
    root.mainloop()

    return result

# -----------------------------
# Run calculation
# -----------------------------
def run_scatt(
    unit_system,
    filename,
    mu,
    E,
    lmax
):

    # -----------------------------
    # Unit system
    # -----------------------------

    global HBARC, AMU

    if unit_system == 1:

        HBARC = 197.3269804  # MeV fm
        AMU   = 931.49410242 # MeV/c^2

        UNIT_NAME = "Nuclear units"

    elif unit_system == 2:

        HBARC = 1.0
        AMU   = 1.0

        UNIT_NAME = "Natural units"

    else:

        raise ValueError("Unknown unit system")
    
    # -----------------------------
    # Potential
    # -----------------------------

    r, V = read_potential(filename)

    k, deltas, ulist = compute_phase_shifts(
        r, V, mu, E, lmax
    )

    theta_deg = np.arange(0.0, 181.0, 1.0)
    theta = np.radians(theta_deg)

    f = scattering_amplitude(theta, k, deltas)

    dsdO = np.abs(f)**2
    dsdO_barn = dsdO / 100.0

    # -------------------------------------
    # Total cross section
    # -------------------------------------

    sigma_tot = (
        4.0 * np.pi / k**2
        * np.sum(
            (2 * np.arange(len(deltas)) + 1)
            * np.sin(deltas)**2
        )
    )

    sigma_tot_barn = sigma_tot / 100.0

    # -------------------------------------
    # Low-energy scattering parameters
    # -------------------------------------

    low_energy = (E < 1.0e-4) or (k * r[-1] < 0.5)

    if low_energy:

        a_s = -np.tan(deltas[0]) / k

        sigma_th = 4.0 * np.pi * a_s**2
        sigma_th_barn = sigma_th / 100.0

    else:

        a_s = None
        sigma_th = None
        sigma_th_barn = None

    # -------------------------------------
    # Partial cross sections
    # -------------------------------------

    l_values = np.arange(len(deltas))

    sigma_l = (
        4.0 * np.pi / k**2
        * (2 * l_values + 1)
        * np.sin(deltas)**2
    )

    sigma_l_barn = sigma_l / 100.0

    # -------------------------------------
    # Effective potentials
    # -------------------------------------

    alpha = kinetic_factor(mu)

    veff = []

    for l in range(lmax + 1):

        cent = np.zeros_like(r)

        cent[1:] = (
            alpha
            * l * (l + 1)
            / r[1:]**2
        )

        cent[0] = cent[1]

        veff.append(V + cent)

    veff = np.array(veff)

    # -------------------------------------
    # Write output
    # -------------------------------------

    with open("scatt.out", "w") as fout:

        fout.write("============================================================\n")
        fout.write("SPLSCATT\n")
        fout.write("A Spinless Partial-Wave Elastic Scattering Code\n")
        fout.write("for Finite-Range Central Potentials\n")
        fout.write("============================================================\n\n")

        fout.write("Numerov integration of the radial Schrodinger equation\n")
        fout.write("Phase-shift analysis and differential cross sections\n\n")

        fout.write("Developed by\n\n")

        fout.write("Dr. Nguyen Le Anh\n")
        fout.write("Department of Physics\n")
        fout.write("Ho Chi Minh City University of Education (HCMUE)\n\n")

        fout.write("============================================================\n\n")

        fout.write("Unit system\n")
        fout.write("-----------------------------------------\n")
        fout.write(f"{UNIT_NAME}\n\n")
        fout.write("Input parameters\n")
        fout.write("-----------------------------------------\n")
        fout.write(f"Potential file : {filename}\n")
        fout.write(f"hbar*c         : {HBARC:.8f} MeV fm\n")
        fout.write(f"mu             : {mu:.8f} amu\n")
        fout.write(f"E              : {E:.8f} MeV\n")
        fout.write(f"lmax           : {lmax:d}\n\n")

        fout.write("Derived quantities\n")
        fout.write("-----------------------------------------\n")
        fout.write(f"alpha          : {alpha:.8f} MeV fm^2\n")
        fout.write(f"k              : {k:.8f} fm^-1\n\n")

        # ---------------------------------
        # Potential
        # ---------------------------------

        fout.write("Potential\n")
        fout.write("-----------------------------------------\n")

        header = f"{'r(fm)':>12s}{'V(MeV)':>14s}"

        for l in range(lmax + 1):
            header += f"{('Veff'+str(l)):>14s}"

        fout.write(header + "\n")

        for i in range(len(r)):

            line = f"{r[i]:12.6f}{V[i]:14.6f}"

            for l in range(lmax + 1):
                line += f"{veff[l, i]:14.5E}"

            fout.write(line + "\n")

        fout.write("\n")
        
        # ---------------------------------
        # Radial wave functions
        # ---------------------------------

        fout.write("Radial wave functions\n")
        fout.write("-----------------------------------------\n")
        header = f"{'r(fm)':>12s}"

        for l in range(lmax + 1):
            header += f"{('u'+str(l)):>16s}"

        fout.write(header + "\n")
        
        for i in range(len(r)):

            line = f"{r[i]:12.6f}"

            for l in range(lmax + 1):
                line += f"{ulist[l, i]:16.5E}"

            fout.write(line + "\n")

        fout.write("\n")

        # ---------------------------------
        # Phase shifts
        # ---------------------------------

        fout.write(
            "Phase shifts and partial cross sections\n"
        )

        fout.write(
            "-----------------------------------------\n"
        )

        fout.write(
            f"{'l':>4s}"
            f"{'delta(rad)':>16s}"
            f"{'delta(deg)':>16s}"
            f"{'sigma_l(fm^2)':>18s}"
            f"{'sigma_l(b)':>18s}\n"
        )

        for l in range(len(deltas)):

            fout.write(
                f"{l:4d}"
                f"{deltas[l]:16.6f}"
                f"{np.degrees(deltas[l]):16.6f}"
                f"{sigma_l[l]:18.6f}"
                f"{sigma_l_barn[l]:18.6f}\n"
            )

        fout.write("\n")

        # ---------------------------------
        # Total cross section
        # ---------------------------------

        fout.write(
            "Total elastic cross section\n"
        )

        fout.write(
            "-----------------------------------------\n"
        )

        fout.write(
            f"sigma_tot = {sigma_tot:16.6f} fm^2\n"
        )

        fout.write(
            f"sigma_tot = {sigma_tot_barn:16.6f} b\n\n"
        )

        # ---------------------------------
        # Low-energy scattering parameters
        # ---------------------------------

        if low_energy:

            fout.write(
                "Low-energy scattering parameters\n"
            )

            fout.write(
                "-----------------------------------------\n"
            )

            fout.write(
                f"Scattering length a_s = {a_s:12.6f} fm\n"
            )

            fout.write(
                f"sigma_th = {sigma_th:12.6f} fm^2\n"
            )

            fout.write(
                f"sigma_th = {sigma_th_barn:12.6f} b\n\n"
            )

        # ---------------------------------
        # Differential cross section
        # ---------------------------------

        fout.write(
            "Differential cross section\n"
        )

        fout.write(
            "-----------------------------------------\n"
        )

        fout.write(
            f"{'theta(deg)':>12s}"
            f"{'dsdO(fm^2/sr)':>20s}"
            f"{'dsdO(b/sr)':>20s}\n"
        )

        for th, x1, x2 in zip(
            theta_deg,
            dsdO,
            dsdO_barn
        ):

            fout.write(
                f"{th:12.6f}"
                f"{x1:20.5E}"
                f"{x2:20.5E}\n"
            )

        fout.write("\n")
        fout.write("============================================================\n")
        fout.write("End of elastic-scattering calculation.\n")
        fout.write("============================================================\n")

if __name__ == "__main__":
    get_inputs()
