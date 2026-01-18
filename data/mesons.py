#!/usr/bin/env python3
"""
Lambda7 Meson & Lepton Data

Pi-algebra mass formulas with Lorentz corrections.
All masses expressed in electron mass units (m_e).

Formula structure:
    mass = c5*pi^5 + c4*pi^4 + c3*pi^3 + c2*pi^2 + c1*pi + c0 + correction

Key patterns:
    - Pion: c5 = 1 (lightest meson)
    - Kaon/eta: c5 = 3 (one strange)
    - Vector mesons: c5 = 5 (J=1)
    - D mesons: c5 = 12 = 2×6 (charm + light)
    - J/ψ: c5 = 20 = 4×5 (charm-anticharm)
    - B mesons: c5 = 34 = 6²-2 (bottom + light)
    - Υ: c5 = 61 = 64-3 (bottom-antibottom)
"""

import math
from dataclasses import dataclass
from typing import Optional, Callable

# Constants
PI = math.pi
M_E = 0.51099895  # Electron mass in MeV
E_NEG_PI = math.exp(-PI)  # e^(-pi) = 0.04321...

# Powers of pi
PI2 = PI ** 2
PI3 = PI ** 3
PI4 = PI ** 4
PI5 = PI ** 5


@dataclass
class Meson:
    """Meson or lepton with pi-algebra mass formula."""
    name: str
    symbol: str
    latex_symbol: str
    mass_exp: float  # Experimental mass in MeV
    quark_content: str  # e.g., "u\bar{d}"

    # Polynomial coefficients
    c5: float = 0
    c4: float = 0
    c3: float = 0
    c2: float = 0
    c1: float = 0  # coefficient of pi
    c0: float = 0  # constant term

    # Correction
    correction_func: Optional[Callable[[], float]] = None
    correction_latex: str = ""

    # Metadata
    spin: int = 0  # J quantum number
    particle_type: str = "meson"  # meson or lepton

    def mass_base(self) -> float:
        """Base mass from polynomial (in m_e)."""
        return self.c5*PI5 + self.c4*PI4 + self.c3*PI3 + self.c2*PI2 + self.c1*PI + self.c0

    def correction(self) -> float:
        """Correction term (in m_e)."""
        return self.correction_func() if self.correction_func else 0

    def mass_me(self) -> float:
        """Total mass in m_e."""
        return self.mass_base() + self.correction()

    def mass_mev(self) -> float:
        """Calculated mass in MeV."""
        return self.mass_me() * M_E

    def error_mev(self) -> float:
        """Error in MeV."""
        return self.mass_mev() - self.mass_exp

    def error_kev(self) -> float:
        """Error in keV."""
        return self.error_mev() * 1000

    def error_percent(self) -> float:
        """Error as percentage."""
        return 100 * abs(self.error_mev()) / self.mass_exp

    def formula_latex(self) -> str:
        """Full formula in LaTeX."""
        terms = []

        if self.c5:
            if self.c5 == 1:
                terms.append(r"\pi^5")
            elif self.c5 == -1:
                terms.append(r"-\pi^5")
            else:
                terms.append(f"{int(self.c5)}\\pi^5")

        if self.c4:
            sign = "+" if self.c4 > 0 and terms else ""
            if self.c4 == 1:
                terms.append(f"{sign}\\pi^4")
            elif self.c4 == -1:
                terms.append("-\\pi^4")
            else:
                terms.append(f"{sign}{int(self.c4)}\\pi^4")

        if self.c3:
            sign = "+" if self.c3 > 0 and terms else ""
            if self.c3 == 1:
                terms.append(f"{sign}\\pi^3")
            elif self.c3 == -1:
                terms.append("-\\pi^3")
            else:
                terms.append(f"{sign}{int(self.c3)}\\pi^3")

        if self.c2:
            sign = "+" if self.c2 > 0 and terms else ""
            if self.c2 == 1:
                terms.append(f"{sign}\\pi^2")
            elif self.c2 == -1:
                terms.append("-\\pi^2")
            else:
                terms.append(f"{sign}{int(self.c2)}\\pi^2")

        if self.c1:
            sign = "+" if self.c1 > 0 and terms else ""
            if self.c1 == 1:
                terms.append(f"{sign}\\pi")
            elif self.c1 == -1:
                terms.append("-\\pi")
            elif self.c1 == int(self.c1):
                terms.append(f"{sign}{int(self.c1)}\\pi")
            else:
                # Fractional coefficient
                from fractions import Fraction
                frac = Fraction(self.c1).limit_denominator(10)
                if frac.denominator == 1:
                    terms.append(f"{sign}{frac.numerator}\\pi")
                else:
                    sign_str = "-" if frac.numerator < 0 else ("+" if terms else "")
                    terms.append(f"{sign_str}\\frac{{{abs(frac.numerator)}}}{{{frac.denominator}}}\\pi")

        if self.c0:
            sign = "+" if self.c0 > 0 and terms else ""
            if self.c0 == int(self.c0):
                terms.append(f"{sign}{int(self.c0)}")
            else:
                from fractions import Fraction
                frac = Fraction(self.c0).limit_denominator(10)
                if frac.denominator == 1:
                    terms.append(f"{sign}{frac.numerator}")
                else:
                    sign_str = "-" if frac.numerator < 0 else ("+" if terms else "")
                    terms.append(f"{sign_str}\\frac{{{abs(frac.numerator)}}}{{{frac.denominator}}}")

        base = " ".join(terms)

        if self.correction_latex:
            if self.correction_latex.startswith("-"):
                return f"{base} {self.correction_latex}"
            else:
                return f"{base} + {self.correction_latex}"
        return base


# =============================================================================
# CORRECTION FUNCTIONS
# =============================================================================

def pion_pm_corr():
    """Pion± Lorentz correction: 6e^(-π)"""
    return 6 * E_NEG_PI

def muon_corr():
    """Muon Lorentz correction: -20e^(-π)"""
    return -20 * E_NEG_PI


# =============================================================================
# MESON DATABASE
# =============================================================================

MESONS = {
    # --- LIGHT MESONS ---

    'pi_pm': Meson(
        name='Pion±', symbol='π±', latex_symbol=r'\pi^\pm',
        mass_exp=139.57039,
        quark_content=r'u\bar{d}',
        c5=1, c3=-1, c1=-1, c0=1,
        correction_func=pion_pm_corr,
        correction_latex=r'6e^{-\pi}',
        spin=0, particle_type='meson'
    ),

    'pi_0': Meson(
        name='Pion⁰', symbol='π⁰', latex_symbol=r'\pi^0',
        mass_exp=134.9768,
        quark_content=r'u\bar{u}, d\bar{d}',
        c5=1, c3=-1, c2=-1, c0=-1,
        spin=0, particle_type='meson'
    ),

    'rho': Meson(
        name='Rho', symbol='ρ', latex_symbol=r'\rho',
        mass_exp=775.11,
        quark_content=r'u\bar{d}',
        c5=5, c2=-1, c1=-6/5, c0=2/5,
        spin=1, particle_type='meson'
    ),

    'omega': Meson(
        name='Omega', symbol='ω', latex_symbol=r'\omega',
        mass_exp=782.66,
        quark_content=r'u\bar{u}, d\bar{d}',
        c5=5, c1=3/5, c0=-2/5,
        spin=1, particle_type='meson'
    ),

    # --- STRANGE MESONS ---

    'K_pm': Meson(
        name='Kaon±', symbol='K±', latex_symbol=r'K^\pm',
        mass_exp=493.677,
        quark_content=r'u\bar{s}',
        c5=3, c3=1, c2=2, c1=-4/5,
        spin=0, particle_type='meson'
    ),

    'K_0': Meson(
        name='Kaon⁰', symbol='K⁰', latex_symbol=r'K^0',
        mass_exp=497.611,
        quark_content=r'd\bar{s}',
        c5=3, c3=2, c1=-2,
        spin=0, particle_type='meson'
    ),

    'eta': Meson(
        name='Eta', symbol='η', latex_symbol=r'\eta',
        mass_exp=547.862,
        quark_content=r'u\bar{u}, d\bar{d}, s\bar{s}',
        c5=3, c4=1, c3=2, c1=-2, c0=1,
        spin=0, particle_type='meson'
    ),

    'eta_prime': Meson(
        name='Eta\'', symbol='η\'', latex_symbol=r"\eta'",
        mass_exp=957.78,
        quark_content=r'u\bar{u}, d\bar{d}, s\bar{s}',
        c5=6, c3=1, c1=2, c0=1,
        spin=0, particle_type='meson'
    ),

    'phi': Meson(
        name='Phi', symbol='φ', latex_symbol=r'\phi',
        mass_exp=1019.461,
        quark_content=r's\bar{s}',
        c5=6, c4=2, c3=-1, c1=-7/5, c0=-2/5,
        spin=1, particle_type='meson'
    ),

    # --- CHARM MESONS ---

    'D_pm': Meson(
        name='D±', symbol='D±', latex_symbol=r'D^\pm',
        mass_exp=1869.66,
        quark_content=r'c\bar{d}',
        c5=12, c2=-2, c1=2,
        spin=0, particle_type='meson'
    ),

    'D_0': Meson(
        name='D⁰', symbol='D⁰', latex_symbol=r'D^0',
        mass_exp=1864.84,
        quark_content=r'c\bar{u}',
        c5=12, c2=-2, c1=-1,
        spin=0, particle_type='meson'
    ),

    'D_s': Meson(
        name='Ds', symbol='Ds', latex_symbol=r'D_s',
        mass_exp=1968.35,
        quark_content=r'c\bar{s}',
        c5=13, c4=-1, c3=-1, c1=4/5, c0=-2/5,
        spin=0, particle_type='meson'
    ),

    'J_psi': Meson(
        name='J/ψ', symbol='J/ψ', latex_symbol=r'J/\psi',
        mass_exp=3096.900,
        quark_content=r'c\bar{c}',
        c5=20, c3=-2, c1=4/5, c0=-2/5,
        spin=1, particle_type='meson'
    ),

    # --- BOTTOM MESONS ---

    'B_pm': Meson(
        name='B±', symbol='B±', latex_symbol=r'B^\pm',
        mass_exp=5279.34,
        quark_content=r'u\bar{b}',
        c5=34, c3=-2, c1=-3, c0=-9/5,
        spin=0, particle_type='meson'
    ),

    'B_0': Meson(
        name='B⁰', symbol='B⁰', latex_symbol=r'B^0',
        mass_exp=5279.65,
        quark_content=r'd\bar{b}',
        c5=34, c3=-2, c1=-3, c0=-6/5,
        spin=0, particle_type='meson'
    ),

    'B_s': Meson(
        name='Bs', symbol='Bs', latex_symbol=r'B_s',
        mass_exp=5366.92,
        quark_content=r's\bar{b}',
        c5=34, c4=1, c1=4/5, c0=-9/5,
        spin=0, particle_type='meson'
    ),

    'Upsilon': Meson(
        name='Υ(1S)', symbol='Υ', latex_symbol=r'\Upsilon(1S)',
        mass_exp=9460.30,
        quark_content=r'b\bar{b}',
        c5=61, c4=-1, c3=-2, c1=6/5, c0=9/5,
        spin=1, particle_type='meson'
    ),
}


# =============================================================================
# LEPTON DATABASE
# =============================================================================

LEPTONS = {
    'muon': Meson(
        name='Muon', symbol='μ', latex_symbol=r'\mu',
        mass_exp=105.6583755,
        quark_content='lepton',
        c5=1, c4=-1, c0=-1,
        correction_func=muon_corr,
        correction_latex=r'-20e^{-\pi}',
        spin=0, particle_type='lepton'
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_light_mesons():
    """Get light mesons (pion, rho, omega)."""
    return [MESONS[k] for k in ['pi_pm', 'pi_0', 'rho', 'omega']]

def get_strange_mesons():
    """Get strange mesons (kaon, eta, phi)."""
    return [MESONS[k] for k in ['K_pm', 'K_0', 'eta', 'eta_prime', 'phi']]

def get_charm_mesons():
    """Get charm mesons (D, J/psi)."""
    return [MESONS[k] for k in ['D_pm', 'D_0', 'D_s', 'J_psi']]

def get_bottom_mesons():
    """Get bottom mesons (B, Upsilon)."""
    return [MESONS[k] for k in ['B_pm', 'B_0', 'B_s', 'Upsilon']]

def get_all_mesons():
    """Get all mesons sorted by mass."""
    return sorted(MESONS.values(), key=lambda m: m.mass_exp)


# =============================================================================
# C5 PATTERN DATA
# =============================================================================

C5_PATTERN = [
    {'mesons': r'\pi', 'c5': 1, 'pattern': 'Lightest meson'},
    {'mesons': r'K, \eta', 'c5': 3, 'pattern': 'One strange quark'},
    {'mesons': r'\rho, \omega', 'c5': 5, 'pattern': 'Vector mesons (J=1)'},
    {'mesons': r"\eta', \phi", 'c5': 6, 'pattern': 'Heavier strange'},
    {'mesons': r'D', 'c5': 12, 'pattern': r'12 = 2\times 6 (charm + light)'},
    {'mesons': r'D_s', 'c5': 13, 'pattern': '13 = 12+1 (charm + strange)'},
    {'mesons': r'J/\psi', 'c5': 20, 'pattern': r'20 = 4\times 5 (charm-anticharm)'},
    {'mesons': r'B', 'c5': 34, 'pattern': r'34 = 6^2-2 (bottom + light)'},
    {'mesons': r'\Upsilon', 'c5': 61, 'pattern': '61 = 64-3 (bottom-antibottom)'},
]


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Lambda7 Meson Data")
    print("=" * 80)

    for m in sorted(list(MESONS.values()) + list(LEPTONS.values()), key=lambda x: x.mass_exp):
        err = m.error_kev()
        print(f"{m.symbol:8} {m.formula_latex():50} {m.mass_mev():10.2f} MeV  err: {err:+8.1f} keV")
