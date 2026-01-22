#!/usr/bin/env python3
"""
Lambda7 Resonance Data

Pi-algebra mass formulas for anomalous baryon and meson resonances.
All masses expressed in electron mass units (m_e).

These resonances share structural patterns that suggest deep connections:
- 9π⁵ base resonances: Mirror states of ground state baryon sequence (6→2 scaling)
- X(3872): Exotic meson at D⁰D̄*⁰ threshold
- N(2190): High-spin resonance with q-integer structure

Mirror correspondence (9π⁵ resonances):
    Ground state → 9π⁵ mirror (6/3 = 2 scaling)
    ─────────────────────────────────────────────
    Λ (nothing)     → Λ(1405) λ-type (stripped)
    Σ (6π³)         → N(1440) σ-type (2π³)
    Σ* (6π⁴ - 2π²)  → N(1535) η-type (2π⁴ + π²/2)
    Ξ* (6π⁴ - π³)   → Λ(1520) η'-type (2π⁴ + π³)
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
# FORMULA FUNCTIONS - 9π⁵ FAMILY (Mirror states)
# =============================================================================

def lambda_1405_formula():
    """Λ(1405): 9π⁵ - π - 1 - 1/π (λ-type: stripped)"""
    return 9*PI5 - PI - 1 - 1/PI


def roper_formula():
    """Roper N(1440): 9π⁵ + 2π³ + π²/2 - π (σ-type: mirrors Σ with 6→2)"""
    return 9*PI5 + 2*PI3 + PI2/2 - PI


def n1535_formula():
    """N(1535): 9π⁵ + 2π⁴ + π²/2 + π/3 (η-type: mirrors Σ* with 6→2)"""
    return 9*PI5 + 2*PI4 + PI2/2 + PI/3


def lambda_1520_formula():
    """Λ(1520): 9π⁵ + 2π⁴ + π³ - 2π - 1/(2π) (η'-type: mirrors Ξ* with 6→2)"""
    return 9*PI5 + 2*PI4 + PI3 - 2*PI - 1/(2*PI)


# =============================================================================
# FORMULA FUNCTIONS - EXOTIC/HIGH ENERGY
# =============================================================================

def x3872_formula():
    """X(3872): 8π⁶ - π⁵ + 2π⁴ - π - 1/(2π)"""
    return 8*PI6 - PI5 + 2*PI4 - PI - 1/(2*PI)


def n2190_formula():
    """N(2190): π⁷ + π⁶ + π⁵ - 2 = [3]_π · π⁵ - 2 (q-integer structure)"""
    return PI7 + PI6 + PI5 - 2


def n1680_formula():
    """N(1680): 9π⁵ + 6π⁴ - π³ - π² - 1/π"""
    return 9*PI5 + 6*PI4 - PI3 - PI2 - 1/PI


def delta_1700_formula():
    """Δ(1700): 9π⁵ + 6π⁴ - π² - 2"""
    return 9*PI5 + 6*PI4 - PI2 - 2


# =============================================================================
# RESONANCE DATABASE
# =============================================================================

RESONANCES = {
    # --- 9π⁵ FAMILY (Mirror states of ground baryons) ---

    'Lambda_1405': Resonance(
        name='Lambda(1405)',
        symbol='Λ(1405)',
        mass_exp=1405.1,
        jp='1/2-',
        width=50.5,
        quark_content='uds',
        formula_func=lambda_1405_formula,
        formula_latex=r'9\pi^5 - \pi - 1 - \frac{1}{\pi}',
        anomaly='Too light by ~100-200 MeV; may be K̄N molecular state',
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
        formula_latex=r'9\pi^5 + 2\pi^3 + \frac{\pi^2}{2} - \pi',
        anomaly='First radial excitation appears below orbital excitations',
        virtual_node='Sigma',
        virtual_node_latex=r'7\pi^5 + 6\pi^3',
    ),

    'N_1535': Resonance(
        name='N(1535)',
        symbol='N(1535)',
        mass_exp=1510.0,
        jp='1/2-',
        width=170.0,
        quark_content='uud',
        formula_func=n1535_formula,
        formula_latex=r'9\pi^5 + 2\pi^4 + \frac{\pi^2}{2} + \frac{\pi}{3}',
        anomaly='Nearly degenerate with opposite-parity Roper',
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
        formula_latex=r'9\pi^5 + 2\pi^4 + \pi^3 - 2\pi - \frac{1}{2\pi}',
        anomaly='Unusually narrow width; well-established D-wave state',
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
        formula_latex=r'9\pi^5 + 6\pi^4 - \pi^3 - \pi^2 - \frac{1}{\pi}',
        anomaly='F15 resonance; shares 9π⁵ + 6π⁴ base structure',
    ),

    'Delta_1700': Resonance(
        name='Δ(1700)',
        symbol='Δ(1700)',
        mass_exp=1700.0,
        jp='3/2-',
        width=300.0,
        quark_content='uud',
        formula_func=delta_1700_formula,
        formula_latex=r'9\pi^5 + 6\pi^4 - \pi^2 - 2',
        anomaly='D33 resonance; shares 9π⁵ + 6π⁴ base structure',
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
        formula_latex=r'\pi^7 + \pi^6 + \pi^5 - 2',
        anomaly='High-spin G17 resonance; mass equals [3]_π · π⁵ - 2 (q-integer structure)'
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_9pi5_family():
    """Get the 9π⁵ mirror state resonances."""
    return [RESONANCES[k] for k in ['Lambda_1405', 'Roper', 'N_1535', 'Lambda_1520']]


def get_all_resonances():
    """Get all resonances sorted by mass."""
    return sorted(RESONANCES.values(), key=lambda r: r.mass_exp)


# =============================================================================
# TERM STRUCTURE ANALYSIS
# =============================================================================

TERM_STRUCTURE = """
Term-by-term comparison (9π⁵ family):

Term       Λ(1405)      Roper        N(1535)      Λ(1520)
----------------------------------------------------------
π⁵         9            9            9            9
π⁴         0            0            +2           +2
π³         0            +2           0            +1
π²/2       0            +1           +1           0
π          -1           -1           +1/3         -2
const      -1           0            0            0
1/π        -1           0            0            -1/2

Mirror correspondence:
  • Λ(1405) λ-type: stripped (neither π⁴ nor π³)
  • Roper σ-type: +2π³ (mirrors Σ with 6π³ → 2π³)
  • N(1535) η-type: +2π⁴ (mirrors Σ* with 6π⁴ → 2π⁴)
  • Λ(1520) η'-type: +2π⁴ + π³ (mirrors Ξ* with 6π⁴ - π³ → 2π⁴ + π³)

The 6/3 = 2 rule: Ground state "6" coefficients become "2" in mirror states.
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
