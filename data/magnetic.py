#!/usr/bin/env python3
"""
Lambda7 Magnetic Moment Data

Baryon magnetic moments as π-fractions in nuclear magnetons (μ_N).

Formula patterns:
    - Q > 0: μ = Nπ/9 (denominator 9 = 3², color factor)
    - Q ≤ 0: μ = N/π^k (k increases with strangeness)

Key numerators (q-integers):
    - 4 = ⌊[2]_π⌋ = ⌊π + 1⌋
    - 6 = ⌊2π⌋
    - 7 = ⌈2π⌉
    - 8 = ⌊2π⌋ + 2
    - 9 = 3² = ⌊π²⌋
    - 20 = 2 × ⌈π²⌉ = 4 × 5
    - 36 = 6² = ⌊2π⌋²
"""

import math
from dataclasses import dataclass
from typing import Callable

# Constants
PI = math.pi
PI2 = PI ** 2
PI3 = PI ** 3


@dataclass
class MagneticMoment:
    """Baryon magnetic moment with π-formula."""
    name: str
    symbol: str
    latex_symbol: str
    mu_exp: float  # Experimental value in nuclear magnetons

    # Formula components
    numerator: int
    pi_power: int  # Power of π in denominator (negative means π in numerator)
    denominator: int = 1  # Additional integer denominator (for Nπ/9 type)

    # Metadata
    charge: int = 0
    strangeness: int = 0
    family: str = ""  # e.g., "6-chain", "20-family"

    def mu_calc(self) -> float:
        """Calculate magnetic moment from formula."""
        if self.pi_power < 0:
            # Form: Nπ/D (π in numerator)
            return self.numerator * (PI ** (-self.pi_power)) / self.denominator
        elif self.pi_power == 0:
            # Form: N/D (no π)
            return self.numerator / self.denominator
        else:
            # Form: N/π^k
            return self.numerator / (PI ** self.pi_power)

    def error_percent(self) -> float:
        """Error as percentage."""
        return 100 * abs(self.mu_calc() - self.mu_exp) / abs(self.mu_exp)

    def formula_latex(self) -> str:
        """Formula in LaTeX."""
        sign = "" if self.mu_exp >= 0 else "-"

        if self.pi_power < 0:
            # Form: Nπ/D (π in numerator)
            power = -self.pi_power
            if power == 1:
                return f"{sign}\\frac{{{abs(self.numerator)}\\pi}}{{{self.denominator}}}"
            else:
                return f"{sign}\\frac{{{abs(self.numerator)}\\pi^{power}}}{{{self.denominator}}}"
        elif self.pi_power == 0:
            # Form: N/D (no π)
            return f"{sign}\\frac{{{abs(self.numerator)}}}{{{self.denominator}}}"
        else:
            # Form: N/π^k
            if self.pi_power == 1:
                return f"{sign}\\frac{{{abs(self.numerator)}}}{{\\pi}}"
            else:
                return f"{sign}\\frac{{{abs(self.numerator)}}}{{\\pi^{self.pi_power}}}"


# =============================================================================
# MAGNETIC MOMENT DATABASE
# =============================================================================

MAGNETIC_MOMENTS = {
    # --- POSITIVE CHARGE: μ = Nπ/9 ---

    'p': MagneticMoment(
        name='Proton', symbol='p', latex_symbol='p',
        mu_exp=2.7928473508,
        numerator=8, pi_power=-1, denominator=9,
        charge=1, strangeness=0, family='positive'
    ),

    'Sigma+': MagneticMoment(
        name='Sigma+', symbol='Σ⁺', latex_symbol=r'\Sigma^+',
        mu_exp=2.458,
        numerator=7, pi_power=-1, denominator=9,
        charge=1, strangeness=-1, family='positive'
    ),

    # --- NEUTRAL: μ = N/π^k ---

    'n': MagneticMoment(
        name='Neutron', symbol='n', latex_symbol='n',
        mu_exp=-1.9130427,
        numerator=-6, pi_power=1,
        charge=0, strangeness=0, family='6-chain'
    ),

    'Lambda': MagneticMoment(
        name='Lambda', symbol='Λ', latex_symbol=r'\Lambda',
        mu_exp=-0.613,
        numerator=-6, pi_power=2,
        charge=0, strangeness=-1, family='6-chain'
    ),

    'Xi0': MagneticMoment(
        name='Xi0', symbol='Ξ⁰', latex_symbol=r'\Xi^0',
        mu_exp=-1.250,
        numerator=-4, pi_power=1,
        charge=0, strangeness=-2, family='neutral'
    ),

    # --- NEGATIVE CHARGE: μ = N/π^k ---

    'Sigma-': MagneticMoment(
        name='Sigma-', symbol='Σ⁻', latex_symbol=r'\Sigma^-',
        mu_exp=-1.160,
        numerator=-36, pi_power=3,
        charge=-1, strangeness=-1, family='6-chain'
    ),

    'Xi-': MagneticMoment(
        name='Xi-', symbol='Ξ⁻', latex_symbol=r'\Xi^-',
        mu_exp=-0.6507,
        numerator=-20, pi_power=3,
        charge=-1, strangeness=-2, family='20-family'
    ),

    'Omega': MagneticMoment(
        name='Omega', symbol='Ω⁻', latex_symbol=r'\Omega^-',
        mu_exp=-2.02,
        numerator=-20, pi_power=2,
        charge=-1, strangeness=-3, family='20-family'
    ),
}


# =============================================================================
# Q-CALCULUS VOCABULARY
# =============================================================================

Q_VOCABULARY = [
    {'N': 4, 'expression': r'\lfloor [2]_\pi \rfloor = \lfloor \pi + 1 \rfloor', 'appears_in': r'\Xi^0'},
    {'N': 6, 'expression': r'\lfloor 2\pi \rfloor', 'appears_in': r'n, \Lambda'},
    {'N': 7, 'expression': r'\lceil 2\pi \rceil', 'appears_in': r'\Sigma^+'},
    {'N': 8, 'expression': r'\lfloor 2\pi \rfloor + 2', 'appears_in': 'p'},
    {'N': 9, 'expression': r'3^2 = \lfloor \pi^2 \rfloor', 'appears_in': 'denominator for Q > 0'},
    {'N': 20, 'expression': r'2 \times \lceil \pi^2 \rceil = 4 \times 5', 'appears_in': r'\Xi^-, \Omega^-'},
    {'N': 36, 'expression': r'6^2 = \lfloor 2\pi \rfloor^2', 'appears_in': r'\Sigma^-'},
]


# =============================================================================
# MASS VS MAGNETIC MOMENT COEFFICIENTS
# =============================================================================

MASS_VS_MU = [
    {'particle': 'p', 'latex': 'p', 'mass_c5': 6, 'mu_num': 8, 'relation': r'\mu = m + 2'},
    {'particle': 'n', 'latex': 'n', 'mass_c5': 6, 'mu_num': 6, 'relation': r'\mu = m'},
    {'particle': 'Lambda', 'latex': r'\Lambda', 'mass_c5': 7, 'mu_num': 6, 'relation': r'\mu = m - 1 \text{ (inherits from n)}'},
    {'particle': 'Sigma+', 'latex': r'\Sigma^+', 'mass_c5': 7, 'mu_num': 7, 'relation': r'\mu = m'},
    {'particle': 'Sigma-', 'latex': r'\Sigma^-', 'mass_c5': 7, 'mu_num': 36, 'relation': r'\mu = 6^2'},
    {'particle': 'Omega', 'latex': r'\Omega^-', 'mass_c5': 9, 'mu_num': 20, 'relation': r'\mu = 2 \times \lceil \pi^2 \rceil'},
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_positive_charge():
    """Get particles with positive charge."""
    return [m for m in MAGNETIC_MOMENTS.values() if m.charge > 0]

def get_neutral():
    """Get neutral particles."""
    return [m for m in MAGNETIC_MOMENTS.values() if m.charge == 0]

def get_negative_charge():
    """Get particles with negative charge."""
    return [m for m in MAGNETIC_MOMENTS.values() if m.charge < 0]

def get_six_chain():
    """Get particles in the 6-chain family."""
    return [m for m in MAGNETIC_MOMENTS.values() if m.family == '6-chain']

def get_twenty_family():
    """Get particles in the 20-family."""
    return [m for m in MAGNETIC_MOMENTS.values() if m.family == '20-family']

def get_all_moments():
    """Get all magnetic moments sorted by strangeness then charge."""
    return sorted(MAGNETIC_MOMENTS.values(), key=lambda m: (m.strangeness, -m.charge))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Lambda7 Magnetic Moment Data")
    print("=" * 70)
    print(f"{'Particle':10} {'Formula':20} {'Calc':10} {'Exp':10} {'Error':8}")
    print("-" * 70)

    for m in get_all_moments():
        print(f"{m.symbol:10} {m.formula_latex():20} {m.mu_calc():+10.4f} {m.mu_exp:+10.4f} {m.error_percent():7.2f}%")
