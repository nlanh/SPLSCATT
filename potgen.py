#!/usr/bin/env python3

import numpy as np

# --------------------------------------------------
# Mesh
# --------------------------------------------------

rmin = 0.05
rmax = 15.0
dr   = 0.05

r = np.arange(rmin, rmax + dr, dr)

# --------------------------------------------------
# Header
# --------------------------------------------------

print("========================================")
print("POTGEN")
print("Potential Generator for SPLSCATT")
print("========================================")

print("\nPotential type")
print("1. Square well")
print("2. Woods-Saxon")
print("3. One-Yukawa")
print("4. Two-Yukawa (Malfliet-Tjon)")
print("5. Three-Yukawa")
print("6. Gaussian")

ptype = int(input("\nChoice = "))

# --------------------------------------------------
# Square well
# --------------------------------------------------

if ptype == 1:

    print("\nSquare-well potential")

    V0 = float(input("V0 (MeV) = "))
    R  = float(input("R  (fm)  = "))

    V = np.where(r <= R, V0, 0.0)

# --------------------------------------------------
# Woods-Saxon
# --------------------------------------------------

elif ptype == 2:

    print("\nWoods-Saxon potential")

    V0 = float(input("V0 (MeV) = "))
    R  = float(input("R  (fm)  = "))
    a  = float(input("a  (fm)  = "))

    V = V0 / (1.0 + np.exp((r - R)/a))

# --------------------------------------------------
# One Yukawa
# --------------------------------------------------

elif ptype == 3:

    print("\nOne-Yukawa potential")

    V1  = float(input("V1  (MeV fm) = "))
    mu1 = float(input("mu1 (fm^-1)  = "))

    V = V1 * np.exp(-mu1*r) / r

# --------------------------------------------------
# Two Yukawa (Malfliet-Tjon)
# --------------------------------------------------

elif ptype == 4:

    print("\nTwo-Yukawa (Malfliet-Tjon) potential")

    print("\nRepulsive part")
    VR  = float(input("VR  (MeV fm) = "))
    muR = float(input("muR (fm^-1)  = "))

    print("\nAttractive part")
    VA  = float(input("VA  (MeV fm) = "))
    muA = float(input("muA (fm^-1)  = "))

    V = (
        VR*np.exp(-muR*r)/r
        - VA*np.exp(-muA*r)/r
    )

# --------------------------------------------------
# Three Yukawa
# --------------------------------------------------

elif ptype == 5:

    print("\nThree-Yukawa potential")

    V = np.zeros_like(r)

    for i in range(3):

        print(f"\nTerm {i+1}")

        Vi  = float(input(f"V{i+1}  (MeV fm) = "))
        mui = float(input(f"mu{i+1} (fm^-1)  = "))

        V += Vi*np.exp(-mui*r)/r

# --------------------------------------------------
# Gaussian
# --------------------------------------------------

elif ptype == 6:

    print("\nGaussian potential")

    V0 = float(input("V0 (MeV) = "))
    a  = float(input("a  (fm)  = "))

    V = V0 * np.exp(-(r/a)**2)

# --------------------------------------------------
# Invalid option
# --------------------------------------------------

else:

    raise ValueError("Unknown potential type.")

# --------------------------------------------------
# Save potential
# --------------------------------------------------

data = np.column_stack((r, V))

np.savetxt(
    "potential.dat",
    data,
    fmt="%14.6E",
    header="r(fm)      V(MeV)"
)

print("\nPotential saved to potential.dat")

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\nFirst few points:")

for i in range(min(10, len(r))):
    print(f"{r[i]:10.4f}  {V[i]:14.6E}")
