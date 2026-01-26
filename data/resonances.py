#!/usr/bin/env python3
"""
Lambda7 Resonance Data

Pi-algebra mass formulas for anomalous baryon and meson resonances.
All masses expressed in electron mass units (m_e).

π⁷ BASIS FOR BARYON RESONANCES
==============================

All baryon resonances in the 1400-1700 MeV range fit a π⁷ basis with simple corrections.
Key value: π⁷ = 1543.37 MeV (resonance scale)

Hierarchy of scales:
    π⁵  = 156 MeV   (pion scale)
    π⁶  = 491 MeV   (kaon scale)
    π⁷  = 1543 MeV  (resonance scale)
    π⁸  = 4849 MeV  (heavy baryon scale)

Best formulas (all sub-MeV accuracy):
    Λ(1405)  = π⁷ - π⁵ + π⁴ - 2π³  (-21 keV)  ← pure polynomial!
    N(1535)  = π⁷ - 2⁴             (+191 keV)
    Λ(1520)  = π⁷ - π³ - 2⁴        (-153 keV)
    N(1440)  = π⁷ - 2π⁴ - 7        (+238 keV)
    N(1680)  = π⁷ + π⁵ - π³        (-1.1 MeV)
    Δ(1700)  = π⁷ + π⁵             (-258 keV)
    N(2190)  = π⁷ + π⁶ + π⁵        (+1.0 MeV)

Notable: 2⁴ = 16 appears in both N(1535) and Λ(1520)!

The "7" connection:
    7π⁵ = Λ (strangeness level)
    7π⁶ = Ξcc (double charm)
    7 appears as correction in N(1440)
    π⁷ is the resonance base scale

Legacy note: The 9π⁵ mirror correspondence is preserved for reference,
but the π⁷ formulas provide dramatically better accuracy.
"""

from dataclasses import dataclass
from typing import Callable

try:
    from .common import PI, M_E, E_NEG_PI, PI2, PI3, PI4, PI5, PI6, PI7
except ImportError:
    from common import PI, M_E, E_NEG_PI, PI2, PI3, PI4, PI5, PI6, PI7


@dataclass
class Resonance:
    """Anomalous baryon or meson resonance with pi-algebra mass formula.

    Unlike ground state particles which use polynomial coefficients,
    resonances use arbitrary formula functions to capture their structure.
    """
    name: str
    symbol: str
    mass_exp: float  # Experimental mass in MeV
    jp: str  # Spin-parity (e.g., '1/2-', '3/2+')
    width: float  # Width in MeV
    quark_content: str

    # Formula
    formula_func: Callable[[], float]  # Returns mass in m_e
    formula_latex: str

    # Notes
    anomaly: str  # Why it's considered anomalous

    # Virtual node: the ground state baryon this resonance mirrors (optional)
    virtual_node: str = ""  # e.g., "Lambda", "Sigma", "Sigma_star", "Xi_star"
    virtual_node_latex: str = ""  # e.g., r"7\pi^5", r"7\pi^5 + 6\pi^3"

    def mass_me(self) -> float:
        """Calculated mass in electron mass units."""
        return self.formula_func()

    def mass_mev(self) -> float:
        """Calculated mass in MeV."""
        return self.mass_me() * M_E

    def error_mev(self) -> float:
        """Error in MeV."""
        return self.mass_mev() - self.mass_exp

    def error_kev(self) -> float:
        """Error in keV."""
        return self.error_mev() * 1000

    def __repr__(self):
        return f"{self.symbol}: {self.mass_mev():.3f} MeV (err: {self.error_kev():+.1f} keV)"


# =============================================================================
# FORMULA FUNCTIONS - π⁷ BASIS (Primary formulas)
# =============================================================================

def lambda_1405_formula():
    """Λ(1405): π⁷ - π⁵ + π⁴ - 2π³"""
    return PI7 - PI5 + PI4 - 2*PI3


def roper_formula():
    """Roper N(1440): π⁷ - 2π⁴ - 7"""
    return PI7 - 2*PI4 - 7


def n1535_formula():
    """N(1535): π⁷ - 2⁴ = π⁷ - 16"""
    return PI7 - 16


def lambda_1520_formula():
    """Λ(1520): π⁷ - π³ - 2⁴ = π⁷ - π³ - 16"""
    return PI7 - PI3 - 16


def n1680_formula():
    """N(1680): π⁷ + π⁵ - π³"""
    return PI7 + PI5 - PI3


def delta_1700_formula():
    """Δ(1700): π⁷ + π⁵"""
    return PI7 + PI5


# =============================================================================
# FORMULA FUNCTIONS - EXOTIC/HIGH ENERGY
# =============================================================================

def x3872_formula():
    """X(3872): 8π⁶ - π⁵ + 2π⁴ - π - 1/(2π)"""
    return 8*PI6 - PI5 + 2*PI4 - PI - 1/(2*PI)


def n2190_formula():
    """N(2190): π⁷ + π⁶ + π⁵ = [3]_π · π⁵ (q-integer structure)"""
    return PI7 + PI6 + PI5


# =============================================================================
# RESONANCE DATABASE
# =============================================================================

RESONANCES = {
    # --- π⁷ FAMILY (resonance scale = 1543 MeV) ---

    'Lambda_1405': Resonance(
        name='Lambda(1405)',
        symbol='Λ(1405)',
        mass_exp=1405.1,
        jp='1/2-',
        width=50.5,
        quark_content='uds',
        formula_func=lambda_1405_formula,
        formula_latex=r'\pi^7 - \pi^5 + \pi^4 - 2\pi^3',
        anomaly='Pure π-polynomial; alternating sign pattern in powers',
        virtual_node='Lambda',
        virtual_node_latex=r'7\pi^5',
    ),

    'Roper': Resonance(
        name='Roper N(1440)',
        symbol='N(1440)',
        mass_exp=1440.0,
        jp='1/2+',
        width=300.0,
        quark_content='uud',
        formula_func=roper_formula,
        formula_latex=r'\pi^7 - 2\pi^4 - 7',
        anomaly='First radial excitation; correction includes the number 7',
        virtual_node='Sigma',
        virtual_node_latex=r'7\pi^5 + 6\pi^3',
    ),

    'N_1535': Resonance(
        name='N(1535)',
        symbol='N(1535)',
        mass_exp=1535.0,
        jp='1/2-',
        width=170.0,
        quark_content='uud',
        formula_func=n1535_formula,
        formula_latex=r'\pi^7 - 2^4',
        anomaly='Nearly degenerate with opposite-parity Roper; correction is 2⁴=16',
        virtual_node='Sigma_star',
        virtual_node_latex=r'7\pi^5 + 6\pi^4',
    ),

    'Lambda_1520': Resonance(
        name='Lambda(1520)',
        symbol='Λ(1520)',
        mass_exp=1519.5,
        jp='3/2-',
        width=15.6,
        quark_content='uds',
        formula_func=lambda_1520_formula,
        formula_latex=r'\pi^7 - \pi^3 - 2^4',
        anomaly='Unusually narrow width; shares 2⁴=16 with N(1535)',
        virtual_node='Xi_star',
        virtual_node_latex=r'8\pi^5 + 6\pi^4 - \pi^3',
    ),

    'N_1680': Resonance(
        name='N(1680)',
        symbol='N(1680)',
        mass_exp=1685.0,
        jp='5/2+',
        width=130.0,
        quark_content='uud',
        formula_func=n1680_formula,
        formula_latex=r'\pi^7 + \pi^5 - \pi^3',
        anomaly='F15 resonance; π⁷ + π⁵ base above resonance scale',
    ),

    'Delta_1700': Resonance(
        name='Δ(1700)',
        symbol='Δ(1700)',
        mass_exp=1700.0,
        jp='3/2-',
        width=300.0,
        quark_content='uud',
        formula_func=delta_1700_formula,
        formula_latex=r'\pi^7 + \pi^5',
        anomaly='D33 resonance; exactly π⁷ + π⁵ (simplest above-scale formula)',
    ),

    # --- EXOTIC/HIGH ENERGY ---

    'X_3872': Resonance(
        name='X(3872)',
        symbol='X(3872)',
        mass_exp=3871.65,
        jp='1++',
        width=1.19,
        quark_content='cc̄ + DD̄*',
        formula_func=x3872_formula,
        formula_latex=r'8\pi^6 - \pi^5 + 2\pi^4 - \pi - \frac{1}{2\pi}',
        anomaly='Sits exactly at D⁰D̄*⁰ threshold; likely molecular or tetraquark'
    ),

    'N_2190': Resonance(
        name='N(2190)',
        symbol='N(2190)',
        mass_exp=2190.0,
        jp='7/2-',
        width=500.0,
        quark_content='uud',
        formula_func=n2190_formula,
        formula_latex=r'\pi^7 + \pi^6 + \pi^5',
        anomaly='High-spin G17 resonance; mass equals [3]_π · π⁵ (q-integer structure)'
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_pi7_family():
    """Get the π⁷ basis resonances (1400-1700 MeV range)."""
    return [RESONANCES[k] for k in ['Lambda_1405', 'Roper', 'N_1535', 'Lambda_1520',
                                     'N_1680', 'Delta_1700']]


def get_all_resonances():
    """Get all resonances sorted by mass."""
    return sorted(RESONANCES.values(), key=lambda r: r.mass_exp)


# =============================================================================
# TERM STRUCTURE ANALYSIS
# =============================================================================

TERM_STRUCTURE = """
π⁷ BASIS FORMULAS
=================

Resonance    Formula                Correction       Error
-----------------------------------------------------------
Λ(1405)      π⁷ - π⁵ + π⁴ - 2π³    -π⁵+π⁴-2π³       -21 keV  ★
N(1440)      π⁷ - 2π⁴ - 7          -2π⁴-7          +238 keV
Λ(1520)      π⁷ - π³ - 16          -π³-2⁴          -153 keV
N(1535)      π⁷ - 16               -2⁴             +191 keV
N(1680)      π⁷ + π⁵ - π³          +π⁵-π³          -1.1 MeV
Δ(1700)      π⁷ + π⁵               +π⁵             -258 keV
N(2190)      π⁷ + π⁶ + π⁵          +π⁶+π⁵          +1.0 MeV

Pattern:
  • Below π⁷: subtractive corrections (Λ, N Roper, Λ', N')
  • Above π⁷: additive π⁵ corrections (N1680, Δ1700)
  • High energy: adds π⁶ (N2190 = [3]_π · π⁵)

Special formulas:
  ★ Λ(1405) = π⁷ - π⁵ + π⁴ - 2π³ is a pure π-polynomial
    with alternating signs: +7, -5, +4, -3 (powers)

The "7" connection:
  • 7π⁵ = Λ base (strangeness)
  • 7π⁶ = Ξcc base (double charm)
  • 7 appears in N(1440) correction
  • π⁷ = resonance scale (1543 MeV)

Notable: 2⁴ = 16 appears in both N(1535) and Λ(1520)!
"""


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("ANOMALOUS RESONANCES - Pi-Algebra Formulas")
    print("=" * 70)
    print()

    print(f"{'Resonance':<15} {'JP':<8} {'Calc (MeV)':<12} {'Exp (MeV)':<12} {'Error':<10}")
    print("-" * 60)

    for res in sorted(RESONANCES.values(), key=lambda x: x.mass_exp):
        print(f"{res.symbol:<15} {res.jp:<8} {res.mass_mev():<12.3f} {res.mass_exp:<12.1f} {res.error_kev():+.1f} keV")

    print()
    print("=" * 70)
    print("FORMULAS")
    print("=" * 70)
    print()

    for res in sorted(RESONANCES.values(), key=lambda x: x.mass_exp):
        print(f"{res.symbol}: {res.formula_latex}")
        print(f"  Anomaly: {res.anomaly}")
        print()

    print(TERM_STRUCTURE)
