#!/usr/bin/env python3
"""
Lambda7 Common Constants

Shared constants for pi-algebra mass formulas.
All masses expressed in electron mass units (m_e).
"""

import math

# Fundamental constants
PI = math.pi
M_E = 0.51099895  # Electron mass in MeV
E_NEG_PI = math.exp(-PI)  # e^(-π) ≈ 0.04321

# Powers of pi (precomputed for efficiency)
PI2 = PI ** 2
PI3 = PI ** 3
PI4 = PI ** 4
PI5 = PI ** 5
PI6 = PI ** 6
PI7 = PI ** 7

# q-calculus integers at base π
Q3_PI = PI2 + PI + 1  # [3]_π = π² + π + 1 ≈ 14.01 (charm base)
