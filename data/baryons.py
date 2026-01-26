#!/usr/bin/env python3
"""
Lambda7 Baryon Data

Pi-algebra mass formulas with corrections.
All masses expressed in electron mass units (m_e).

Formula structure:
    mass = c6·π⁶ + c5·π⁵ + c4·π⁴ + c3·π³ + c2·π² + correction

Key patterns:
    - Octet (spin-1/2):   c4 = 0 (except Xi with c4=1)
    - Decuplet (spin-3/2): c4 = 6 (universal marker)
    - Strangeness: c5 = 6 + |S|

Key naming convention:
    - Underscore separates particle name from charge
    - Charge: plus, minus, zero, pp (++), mm (--)
    - Examples: Sigma_plus, Sigma_c_pp, Xi_cc_pp
"""

from dataclasses import dataclass
from typing import Optional, Callable, List

try:
    from .common import PI, M_E, E_NEG_PI, PI2, PI3, PI4, PI5, PI6, PI7, Q3_PI, LN_PI, PHI
except ImportError:
    from common import PI, M_E, E_NEG_PI, PI2, PI3, PI4, PI5, PI6, PI7, Q3_PI, LN_PI, PHI


@dataclass
class Particle:
    """Baryon with π-algebra mass formula.

    Mass formula: c6·π⁶ + c5·π⁵ + c4·π⁴ + c3·π³ + c2·π² + correction

    The correction field handles all sub-π² terms:
    - Constants: -4, +1
    - π terms: 8/π, -2/π
    - Exponential: (4/5)e^(-π)
    - Combined: -(6/5)(π - e^(-π))
    """
    name: str
    symbol: str           # Unicode display symbol (e.g., 'Σ⁺')
    latex_symbol: str     # LaTeX symbol (e.g., r'\Sigma^+')
    mass_exp: float       # Experimental mass in MeV
    node_id: str          # Unique ID for tree visualization (ASCII only)

    # Polynomial coefficients (π^n where n >= 2)
    c6: float = 0
    c5: float = 0
    c4: float = 0
    c3: float = 0
    c2: float = 0

    # Correction (sub-π² terms)
    correction_func: Optional[Callable[[], float]] = None
    correction_latex: str = ""

    # Metadata
    spin: str = ""
    charge: int = 0
    strangeness: int = 0
    multiplet: str = ""
    quarks: str = ""  # Quark content (e.g., "uud", "uds", "css")

    def mass_base(self) -> float:
        """Base mass from polynomial (in m_e)."""
        return self.c6*PI6 + self.c5*PI5 + self.c4*PI4 + self.c3*PI3 + self.c2*PI2

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

    def error_ev(self) -> float:
        """Error in eV."""
        return self.error_mev() * 1e6

    def error_ppm(self) -> float:
        """Error in parts per million."""
        return 1e6 * self.error_mev() / self.mass_exp

    def base_latex(self) -> str:
        """LaTeX for polynomial part."""
        terms = []

        if self.c6:
            coef = int(self.c6) if self.c6 == int(self.c6) else self.c6
            terms.append(f"{coef}\\pi^6")
        if self.c5:
            sign = "+" if self.c5 > 0 and terms else ""
            coef = int(self.c5) if self.c5 == int(self.c5) else self.c5
            terms.append(f"{sign}{coef}\\pi^5")
        if self.c4:
            sign = "+" if self.c4 > 0 else ""
            if abs(self.c4) == 1:
                terms.append(f"{sign}\\pi^4" if self.c4 > 0 else "-\\pi^4")
            else:
                coef = int(self.c4) if self.c4 == int(self.c4) else self.c4
                terms.append(f"{sign}{coef}\\pi^4")
        if self.c3:
            sign = "+" if self.c3 > 0 else ""
            if abs(self.c3) == 1:
                terms.append(f"{sign}\\pi^3" if self.c3 > 0 else "-\\pi^3")
            else:
                coef = int(self.c3) if self.c3 == int(self.c3) else self.c3
                terms.append(f"{sign}{coef}\\pi^3")
        if self.c2:
            sign = "+" if self.c2 > 0 else ""
            if abs(self.c2) == 1:
                terms.append(f"{sign}\\pi^2" if self.c2 > 0 else "-\\pi^2")
            else:
                coef = int(self.c2) if self.c2 == int(self.c2) else self.c2
                terms.append(f"{sign}{coef}\\pi^2")

        return " ".join(terms)

    def formula_latex(self) -> str:
        """Full formula in LaTeX."""
        base = self.base_latex()
        if self.correction_latex:
            if self.correction_latex.startswith("-"):
                return f"{base} {self.correction_latex}"
            else:
                return f"{base} + {self.correction_latex}"
        return base

    def full_latex(self) -> str:
        """Full equation m_X = formula."""
        return f"m_{{{self.latex_symbol}}} = {self.formula_latex()}"


# =============================================================================
# CORRECTION FUNCTIONS
# =============================================================================

def proton_corr():
    return (4/5) * E_NEG_PI

def neutron_corr():
    return 8 / PI

def lambda_corr():
    """Λ correction: φ/5 (golden ratio / F₅)."""
    return PHI / 5

def sigma_plus_corr():
    return -2 / PI  # ~-0.637 m_e

def sigma_zero_corr():
    return -4  # Simple correction

def sigma_minus_corr():
    return -23 / 5  # -4.6 m_e

def xi_zero_corr():
    return -PI - 1/PI  # = -(π² + 1)/π

def xi_minus_corr():
    return 1 / (5 * PI)

def delta_corr():
    return (1/5) * (PI - 2 + 4 * E_NEG_PI)

def sigma_star_plus_corr():
    return (1/5) * (PI - 7 - E_NEG_PI)

def sigma_star_zero_corr():
    return 1  # Exactly +1, 0.01σ accurate!

def sigma_star_minus_corr():
    return -2  # Simple correction

def xi_star_zero_corr():
    return -(1/5) * (5*PI + 4)

def xi_star_minus_corr():
    return (1/5) * (4*PI - 1)

def omega_corr():
    return -(6/5) * (PI - E_NEG_PI)


# =============================================================================
# CHARM BARYON CORRECTION FUNCTIONS
# =============================================================================

def lambda_c_corr():
    return -23/5

def sigma_c_pp_corr():
    return -(1/5) * PI + 3/5

def sigma_c_p_corr():
    return (3/5) * PI - 4

def sigma_c_0_corr():
    return PI - 18/5

def sigma_c_star_pp_corr():
    return -PI + 4/5

def sigma_c_star_p_corr():
    return -(4/5) * PI - 8/5

def sigma_c_star_0_corr():
    return -11/5

def xi_c_p_corr():
    return (7/5) * PI - 6/5

def xi_c_0_corr():
    return -PI + 9/5

def xi_c_star_p_corr():
    return (4/5) * PI

def xi_c_star_0_corr():
    return (13/10) * PI

def omega_c_corr():
    return -(4/5) * PI + 4/5

def omega_c_star_corr():
    """Ωc*⁰ correction: -ln(π) - 1/2."""
    return -LN_PI - 1/2


# =============================================================================
# DOUBLE-CHARM BARYON CORRECTION FUNCTIONS
# =============================================================================

def xi_cc_pp_corr():
    """Ξcc++ correction: π/6 (from 22π⁵ Archimedes formula)."""
    return PI / 6


# =============================================================================
# BOTTOM BARYON CORRECTION FUNCTIONS
# =============================================================================

def lambda_b_corr():
    """Λb⁰ correction: π/10."""
    return PI / 10

def sigma_b_plus_corr():
    """Σb⁺ correction: 1/30."""
    return 1/30

def sigma_b_minus_corr():
    """Σb⁻ correction: 28/5 = (L₄×L₃)/F₅."""
    return 28/5

def xi_b_zero_corr():
    """Ξb⁰ correction: 19/10."""
    return 19/10

def xi_b_minus_corr():
    """Ξb⁻ correction: 2 (integer)."""
    return 2

def omega_b_corr():
    """Ωb⁻ correction: -3/2."""
    return -3/2

def sigma_b_star_plus_corr():
    """Σb*⁺ correction: -7/9."""
    return -7/9

def sigma_b_star_minus_corr():
    """Σb*⁻ correction: 21/10 = F₈/(2F₅)."""
    return 21/10


# =============================================================================
# PARTICLE DATABASE - LIGHT BARYONS
# =============================================================================

PARTICLES = {
    # --- OCTET (spin-1/2) ---

    'proton': Particle(
        name='Proton', symbol='p', latex_symbol='p',
        mass_exp=938.27208816, node_id='p',
        c5=6,
        correction_func=proton_corr,
        correction_latex=r'\frac{4}{5}e^{-\pi}',
        spin='1/2', charge=1, strangeness=0, multiplet='octet', quarks='uud'
    ),

    'neutron': Particle(
        name='Neutron', symbol='n', latex_symbol='n',
        mass_exp=939.56542052, node_id='n',
        c5=6,
        correction_func=neutron_corr,
        correction_latex=r'\frac{8}{\pi}',
        spin='1/2', charge=0, strangeness=0, multiplet='octet', quarks='udd'
    ),

    'Lambda': Particle(
        name='Lambda', symbol='Λ', latex_symbol=r'\Lambda',
        mass_exp=1115.683, node_id='L0',
        c5=7, c3=1, c2=1,
        correction_func=lambda_corr,
        correction_latex=r'\frac{\varphi}{5}',
        spin='1/2', charge=0, strangeness=-1, multiplet='octet', quarks='uds'
    ),

    'Sigma_plus': Particle(
        name='Sigma+', symbol='Σ⁺', latex_symbol=r'\Sigma^+',
        mass_exp=1189.37, node_id='S_plus',
        c5=7, c3=6,
        correction_func=sigma_plus_corr,
        correction_latex=r'-\frac{2}{\pi}',
        spin='1/2', charge=1, strangeness=-1, multiplet='octet', quarks='uus'
    ),

    'Sigma_zero': Particle(
        name='Sigma0', symbol='Σ⁰', latex_symbol=r'\Sigma^0',
        mass_exp=1192.642, node_id='S_zero',
        c5=7, c3=6, c2=1,
        correction_func=sigma_zero_corr,
        correction_latex=r'-4',
        spin='1/2', charge=0, strangeness=-1, multiplet='octet', quarks='uds'
    ),

    'Sigma_minus': Particle(
        name='Sigma-', symbol='Σ⁻', latex_symbol=r'\Sigma^-',
        mass_exp=1197.449, node_id='S_minus',
        c5=7, c3=6, c2=2,
        correction_func=sigma_minus_corr,
        correction_latex=r'-\frac{23}{5}',
        spin='1/2', charge=-1, strangeness=-1, multiplet='octet', quarks='dds'
    ),

    'Xi_zero': Particle(
        name='Xi0', symbol='Ξ⁰', latex_symbol=r'\Xi^0',
        mass_exp=1314.86, node_id='X_zero',
        c5=8, c4=1, c3=1,
        correction_func=xi_zero_corr,
        correction_latex=r'-\pi - \frac{1}{\pi}',
        spin='1/2', charge=0, strangeness=-2, multiplet='octet', quarks='uss'
    ),

    'Xi_minus': Particle(
        name='Xi-', symbol='Ξ⁻', latex_symbol=r'\Xi^-',
        mass_exp=1321.71, node_id='X_minus',
        c5=8, c4=1, c3=1, c2=1,
        correction_func=xi_minus_corr,
        correction_latex=r'\frac{1}{5\pi}',
        spin='1/2', charge=-1, strangeness=-2, multiplet='octet', quarks='dss'
    ),

    # --- DECUPLET (spin-3/2, c4=6) ---
    # Delta is a single resonance with 4 charge states (not 4 particles)

    'Delta': Particle(
        name='Delta', symbol='Δ', latex_symbol=r'\Delta',
        mass_exp=1232.0, node_id='D',
        c5=6, c4=6, c2=-1,
        correction_func=delta_corr,
        correction_latex=r'\frac{1}{5}\left(\pi - 2 + 4e^{-\pi}\right)',
        spin='3/2', charge=0, strangeness=0, multiplet='decuplet', quarks='uud'
    ),

    'Sigma_star_plus': Particle(
        name='Sigma*+', symbol='Σ*⁺', latex_symbol=r'\Sigma^{*+}',
        mass_exp=1382.80, node_id='Ss_plus',
        c5=7, c4=6, c2=-2,
        correction_func=sigma_star_plus_corr,
        correction_latex=r'\frac{1}{5}\left(\pi - 7 - e^{-\pi}\right)',
        spin='3/2', charge=1, strangeness=-1, multiplet='decuplet', quarks='uus'
    ),

    'Sigma_star_zero': Particle(
        name='Sigma*0', symbol='Σ*⁰', latex_symbol=r'\Sigma^{*0}',
        mass_exp=1383.7, node_id='Ss_zero',
        c5=7, c4=6, c2=-2,
        correction_func=sigma_star_zero_corr,
        correction_latex=r'+1',
        spin='3/2', charge=0, strangeness=-1, multiplet='decuplet', quarks='uds'
    ),

    'Sigma_star_minus': Particle(
        name='Sigma*-', symbol='Σ*⁻', latex_symbol=r'\Sigma^{*-}',
        mass_exp=1387.2, node_id='Ss_minus',
        c5=7, c4=6, c2=-1,
        correction_func=sigma_star_minus_corr,
        correction_latex=r'-2',
        spin='3/2', charge=-1, strangeness=-1, multiplet='decuplet', quarks='dds'
    ),

    'Xi_star_zero': Particle(
        name='Xi*0', symbol='Ξ*⁰', latex_symbol=r'\Xi^{*0}',
        mass_exp=1531.80, node_id='Xs_zero',
        c5=8, c4=6, c3=-1,
        correction_func=xi_star_zero_corr,
        correction_latex=r'-\frac{1}{5}(5\pi + 4)',
        spin='3/2', charge=0, strangeness=-2, multiplet='decuplet', quarks='uss'
    ),

    'Xi_star_minus': Particle(
        name='Xi*-', symbol='Ξ*⁻', latex_symbol=r'\Xi^{*-}',
        mass_exp=1535.0, node_id='Xs_minus',
        c5=8, c4=6, c3=-1,
        correction_func=xi_star_minus_corr,
        correction_latex=r'\frac{1}{5}(4\pi - 1)',
        spin='3/2', charge=-1, strangeness=-2, multiplet='decuplet', quarks='dss'
    ),

    'Omega': Particle(
        name='Omega', symbol='Ω⁻', latex_symbol=r'\Omega^-',
        mass_exp=1672.45, node_id='Om',
        c5=9, c4=6, c3=-2,
        correction_func=omega_corr,
        correction_latex=r'-\frac{6}{5}\left(\pi - e^{-\pi}\right)',
        spin='3/2', charge=-1, strangeness=-3, multiplet='decuplet', quarks='sss'
    ),
}


# =============================================================================
# CHARM BARYON DATABASE
# =============================================================================

CHARM_PARTICLES = {
    # --- CHARM OCTET-LIKE (spin-1/2) ---

    'Lambda_c': Particle(
        name='Lambda_c+', symbol='Λc⁺', latex_symbol=r'\Lambda_c^+',
        mass_exp=2286.46, node_id='Lc',
        c5=14, c4=2,
        correction_func=lambda_c_corr,
        correction_latex=r'-\frac{23}{5}',
        spin='1/2', charge=1, strangeness=0, multiplet='charm-octet', quarks='udc'
    ),

    'Sigma_c_pp': Particle(
        name='Sigma_c++', symbol='Σc⁺⁺', latex_symbol=r'\Sigma_c^{++}',
        mass_exp=2453.97, node_id='Sc_pp',
        c5=14, c4=5, c3=1,
        correction_func=sigma_c_pp_corr,
        correction_latex=r'-\frac{\pi}{5} + \frac{3}{5}',
        spin='1/2', charge=2, strangeness=0, multiplet='charm-octet', quarks='uuc'
    ),

    'Sigma_c_plus': Particle(
        name='Sigma_c+', symbol='Σc⁺', latex_symbol=r'\Sigma_c^+',
        mass_exp=2452.9, node_id='Sc_plus',
        c5=14, c4=5, c3=1,
        correction_func=sigma_c_p_corr,
        correction_latex=r'\frac{3\pi}{5} - 4',
        spin='1/2', charge=1, strangeness=0, multiplet='charm-octet', quarks='udc'
    ),

    'Sigma_c_zero': Particle(
        name='Sigma_c0', symbol='Σc⁰', latex_symbol=r'\Sigma_c^0',
        mass_exp=2453.75, node_id='Sc_zero',
        c5=14, c4=5, c3=1,
        correction_func=sigma_c_0_corr,
        correction_latex=r'\pi - \frac{18}{5}',
        spin='1/2', charge=0, strangeness=0, multiplet='charm-octet', quarks='ddc'
    ),

    'Xi_c_plus': Particle(
        name='Xi_c+', symbol='Ξc⁺', latex_symbol=r'\Xi_c^+',
        mass_exp=2467.71, node_id='Xc_plus',
        c5=15, c4=2, c3=1, c2=1,
        correction_func=xi_c_p_corr,
        correction_latex=r'\frac{7\pi}{5} - \frac{6}{5}',
        spin='1/2', charge=1, strangeness=-1, multiplet='charm-octet', quarks='usc'
    ),

    'Xi_c_zero': Particle(
        name='Xi_c0', symbol='Ξc⁰', latex_symbol=r'\Xi_c^0',
        mass_exp=2470.44, node_id='Xc_zero',
        c5=15, c4=2, c3=1, c2=2,
        correction_func=xi_c_0_corr,
        correction_latex=r'-\pi + \frac{9}{5}',
        spin='1/2', charge=0, strangeness=-1, multiplet='charm-octet', quarks='dsc'
    ),

    'Omega_c': Particle(
        name='Omega_c0', symbol='Ωc⁰', latex_symbol=r'\Omega_c^0',
        mass_exp=2695.2, node_id='Oc_zero',
        c5=16, c4=4, c2=-1,
        correction_func=omega_c_corr,
        correction_latex=r'-\frac{4\pi}{5} + \frac{4}{5}',
        spin='1/2', charge=0, strangeness=-2, multiplet='charm-octet', quarks='ssc'
    ),

    # --- CHARM DECUPLET-LIKE (spin-3/2, c4=6) ---

    'Sigma_c_star_pp': Particle(
        name='Sigma_c*++', symbol='Σc*⁺⁺', latex_symbol=r'\Sigma_c^{*++}',
        mass_exp=2518.41, node_id='Scs_pp',
        c5=14, c4=6, c3=2,
        correction_func=sigma_c_star_pp_corr,
        correction_latex=r'-\pi + \frac{4}{5}',
        spin='3/2', charge=2, strangeness=0, multiplet='charm-decuplet', quarks='uuc'
    ),

    'Sigma_c_star_plus': Particle(
        name='Sigma_c*+', symbol='Σc*⁺', latex_symbol=r'\Sigma_c^{*+}',
        mass_exp=2517.5, node_id='Scs_plus',
        c5=14, c4=6, c3=2,
        correction_func=sigma_c_star_p_corr,
        correction_latex=r'-\frac{4\pi}{5} - \frac{8}{5}',
        spin='3/2', charge=1, strangeness=0, multiplet='charm-decuplet', quarks='udc'
    ),

    'Sigma_c_star_zero': Particle(
        name='Sigma_c*0', symbol='Σc*⁰', latex_symbol=r'\Sigma_c^{*0}',
        mass_exp=2518.48, node_id='Scs_zero',
        c5=14, c4=6, c3=2,
        correction_func=sigma_c_star_0_corr,
        correction_latex=r'-\frac{11}{5}',
        spin='3/2', charge=0, strangeness=0, multiplet='charm-decuplet', quarks='ddc'
    ),

    'Xi_c_star_plus': Particle(
        name='Xi_c*+', symbol='Ξc*⁺', latex_symbol=r'\Xi_c^{*+}',
        mass_exp=2645.57, node_id='Xcs_plus',
        c5=15, c4=6,
        correction_func=xi_c_star_p_corr,
        correction_latex=r'\frac{4\pi}{5}',
        spin='3/2', charge=1, strangeness=-1, multiplet='charm-decuplet', quarks='usc'
    ),

    'Xi_c_star_zero': Particle(
        name='Xi_c*0', symbol='Ξc*⁰', latex_symbol=r'\Xi_c^{*0}',
        mass_exp=2646.38, node_id='Xcs_zero',
        c5=15, c4=6,
        correction_func=xi_c_star_0_corr,
        correction_latex=r'\frac{13\pi}{10}',
        spin='3/2', charge=0, strangeness=-1, multiplet='charm-decuplet', quarks='dsc'
    ),

    'Omega_c_star': Particle(
        name='Omega_c*0', symbol='Ωc*⁰', latex_symbol=r'\Omega_c^{*0}',
        mass_exp=2765.9, node_id='Ocs_zero',
        c5=16, c4=5, c3=1,
        correction_func=omega_c_star_corr,
        correction_latex=r'-\ln\pi - \frac{1}{2}',
        spin='3/2', charge=0, strangeness=-2, multiplet='charm-decuplet', quarks='ssc'
    ),
}


# =============================================================================
# DOUBLE-CHARM BARYON DATABASE
# =============================================================================

DOUBLE_CHARM_PARTICLES = {
    'Xi_cc_pp': Particle(
        name='Xi_cc++', symbol='Ξcc⁺⁺', latex_symbol=r'\Xi_{cc}^{++}',
        mass_exp=3621.55, node_id='Xcc',
        c5=22, c4=3, c3=2,
        correction_func=xi_cc_pp_corr,
        correction_latex=r'\frac{\pi}{6}',
        spin='1/2', charge=2, strangeness=0, multiplet='double-charm', quarks='ucc'
    ),
}


# =============================================================================
# BOTTOM BARYON DATABASE
# =============================================================================

BOTTOM_PARTICLES = {
    # --- BOTTOM OCTET-LIKE (spin-1/2) ---
    # c5 = 36 + |S|, mirroring strange cycle with +29 offset

    'Lambda_b': Particle(
        name='Lambda_b0', symbol='Λb⁰', latex_symbol=r'\Lambda_b^0',
        mass_exp=5619.60, node_id='Lb',
        c5=36, c2=-2,
        correction_func=lambda_b_corr,
        correction_latex=r'\frac{\pi}{10}',
        spin='1/2', charge=0, strangeness=0, multiplet='bottom-octet', quarks='udb'
    ),

    'Sigma_b_plus': Particle(
        name='Sigma_b+', symbol='Σb⁺', latex_symbol=r'\Sigma_b^+',
        mass_exp=5810.56, node_id='Sb_plus',
        c5=36, c4=3, c3=2,
        correction_func=sigma_b_plus_corr,
        correction_latex=r'\frac{1}{30}',
        spin='1/2', charge=1, strangeness=0, multiplet='bottom-octet', quarks='uub'
    ),

    'Sigma_b_minus': Particle(
        name='Sigma_b-', symbol='Σb⁻', latex_symbol=r'\Sigma_b^-',
        mass_exp=5815.64, node_id='Sb_minus',
        c5=36, c4=4, c3=-1,
        correction_func=sigma_b_minus_corr,
        correction_latex=r'\frac{28}{5}',
        spin='1/2', charge=-1, strangeness=0, multiplet='bottom-octet', quarks='ddb'
    ),

    # --- BOTTOM DECUPLET-LIKE (spin-3/2) ---
    'Sigma_b_star_plus': Particle(
        name='Sigma_b*+', symbol='Σb*⁺', latex_symbol=r'\Sigma_b^{*+}',
        mass_exp=5830.32, node_id='Sbs_plus',
        c5=36, c4=3, c3=2, c2=4,
        correction_func=sigma_b_star_plus_corr,
        correction_latex=r'-\frac{7}{9}',
        spin='3/2', charge=1, strangeness=0, multiplet='bottom-decuplet', quarks='uub'
    ),

    'Sigma_b_star_minus': Particle(
        name='Sigma_b*-', symbol='Σb*⁻', latex_symbol=r'\Sigma_b^{*-}',
        mass_exp=5834.74, node_id='Sbs_minus',
        c5=36, c4=4, c2=1,
        correction_func=sigma_b_star_minus_corr,
        correction_latex=r'\frac{21}{10}',
        spin='3/2', charge=-1, strangeness=0, multiplet='bottom-decuplet', quarks='ddb'
    ),

    'Xi_b_zero': Particle(
        name='Xi_b0', symbol='Ξb⁰', latex_symbol=r'\Xi_b^0',
        mass_exp=5791.9, node_id='Xb_zero',
        c5=37, c2=1,
        correction_func=xi_b_zero_corr,
        correction_latex=r'\frac{19}{10}',
        spin='1/2', charge=0, strangeness=-1, multiplet='bottom-octet', quarks='usb'
    ),

    'Xi_b_minus': Particle(
        name='Xi_b-', symbol='Ξb⁻', latex_symbol=r'\Xi_b^-',
        mass_exp=5797.0, node_id='Xb_minus',
        c5=37, c2=2,
        correction_func=xi_b_minus_corr,
        correction_latex=r'2',
        spin='1/2', charge=-1, strangeness=-1, multiplet='bottom-octet', quarks='dsb'
    ),

    'Omega_b': Particle(
        name='Omega_b-', symbol='Ωb⁻', latex_symbol=r'\Omega_b^-',
        mass_exp=6046.1, node_id='Ob',
        c5=38, c4=2, c2=1,
        correction_func=omega_b_corr,
        correction_latex=r'-\frac{3}{2}',
        spin='1/2', charge=-1, strangeness=-2, multiplet='bottom-octet', quarks='ssb'
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_octet() -> List[Particle]:
    """Get octet baryons sorted by mass."""
    return sorted(
        [p for p in PARTICLES.values() if p.multiplet == 'octet'],
        key=lambda p: p.mass_exp
    )

def get_decuplet() -> List[Particle]:
    """Get decuplet baryons sorted by mass."""
    return sorted(
        [p for p in PARTICLES.values() if p.multiplet == 'decuplet'],
        key=lambda p: p.mass_exp
    )

def get_by_strangeness(s: int) -> List[Particle]:
    """Get particles by strangeness."""
    return [p for p in PARTICLES.values() if p.strangeness == s]


def get_charm_octet() -> List[Particle]:
    """Get charm octet-like baryons sorted by mass."""
    return sorted(
        [p for p in CHARM_PARTICLES.values() if p.multiplet == 'charm-octet'],
        key=lambda p: p.mass_exp
    )

def get_charm_decuplet() -> List[Particle]:
    """Get charm decuplet-like baryons sorted by mass."""
    return sorted(
        [p for p in CHARM_PARTICLES.values() if p.multiplet == 'charm-decuplet'],
        key=lambda p: p.mass_exp
    )

def get_double_charm() -> List[Particle]:
    """Get double-charm baryons sorted by mass."""
    return sorted(
        DOUBLE_CHARM_PARTICLES.values(),
        key=lambda p: p.mass_exp
    )

def get_bottom() -> List[Particle]:
    """Get bottom baryons sorted by mass."""
    return sorted(
        BOTTOM_PARTICLES.values(),
        key=lambda p: p.mass_exp
    )


# =============================================================================
# BARYON CYCLE DATA
# =============================================================================

BARYON_CYCLE = {
    'levels': [
        {
            'c5': 9,
            'pi5': r'9\pi^5',
            'strangeness': -3,
            'angle': '324\u00b0',
            'angle_latex': r'\frac{9\pi}{5}',
            'particles': ['Omega'],  # Uses new key names
            'charges': [-1],
            'charge_display': 'Q = -1 only',
            'decuplet_term': r'6\pi^4 - 2\pi^3',
            'octet_term': None,
            'mu_family': '4\u00d75 = 20',
            'mu_formula': r'\mu = \frac{20}{\pi^2}',
            'description': 'The apex. Single particle, maximum strangeness.',
        },
        {
            'c5': 8,
            'pi5': r'8\pi^5',
            'strangeness': -2,
            'angle': '288\u00b0',
            'angle_latex': r'\frac{8\pi}{5}',
            'particles': ['Xi_star_zero', 'Xi_star_minus', 'Xi_zero', 'Xi_minus'],
            'charges': [0, -1],
            'charge_display': 'Q = 0, -1',
            'decuplet_term': r'6\pi^4 - \pi^3',
            'octet_term': r'\pi^4 + \pi^3',
            'mu_family': '4\u00d75 = 20',
            'mu_formula': r'\mu_{\Xi^0} = \frac{4}{\pi}, \quad \mu_{\Xi^-} = \frac{20}{\pi^3}',
            'description': 'First split. The -2\u03c0\u00b3 from Omega splits to \u00b1\u03c0\u00b3.',
        },
        {
            'c5': 7,
            'pi5': r'7\pi^5',
            'strangeness': -1,
            'angle': '252\u00b0',
            'angle_latex': r'\frac{7\pi}{5}',
            'particles': ['Sigma_star_plus', 'Sigma_star_zero', 'Sigma_star_minus', 'Lambda', 'Sigma_plus', 'Sigma_zero', 'Sigma_minus'],
            'charges': [1, 0, -1],
            'charge_display': 'Q = +1, 0, -1',
            'decuplet_term': r'6\pi^4 - 2\pi^2',
            'octet_term': r'\pi^3 + \pi^2 \text{ (}\Lambda\text{)}, \quad 6\pi^3 + \pi^2 \text{ (}\Sigma\text{)}',
            'mu_family': 'Transition',
            'mu_formula': r'\mu_\Lambda = \frac{6}{\pi^2}, \quad \mu_{\Sigma^-} = \frac{36}{\pi^3}',
            'description': 'Transition zone. The "6" migrates: 6\u03c0\u2074 (decuplet) \u2192 6\u03c0\u00b3 (Sigma octet). Lambda bridges families.',
        },
        {
            'c5': 6,
            'pi5': r'6\pi^5',
            'strangeness': 0,
            'angle': '216\u00b0',
            'angle_latex': r'\frac{6\pi}{5}',
            'particles': ['Delta', 'proton', 'neutron'],
            'charges': [2, 1, 0, -1],
            'charge_display': 'Q = +2, +1, 0, -1',
            'decuplet_term': r'6\pi^4 - \pi^2',
            'octet_term': r'\text{pure } 6\pi^5',
            'mu_family': '2\u00d73 = 6',
            'mu_formula': r'\mu_p = \frac{8\pi}{9}, \quad \mu_n = \frac{6}{\pi}',
            'description': 'The base. Cycle completes. Double charge (+2) appears. Proton/Omega cross-reference.',
        },
    ],

    'symmetries': {
        'splitting': r'-2\pi^3 \text{ (}\Omega\text{)} \to -\pi^3 \text{ (}\Xi^*\text{)} + \pi^3 \text{ (}\Xi\text{)}',
        'migration': r'6\pi^4 \text{ (decuplet)} \to 6\pi^3 \text{ (}\Sigma\text{ octet)}',
        'cross_reference': r'\text{Proton uses } \frac{4}{5} \text{ from } 4\times 5; \quad \Omega \text{ uses } \frac{6}{5} \text{ from } 2\times 3',
    },
}


# =============================================================================
# CHARM BARYON CYCLE DATA
# =============================================================================

CHARM_CYCLE = {
    'base_info': {
        'base_coefficient': 14,
        'q_integer': r'[3]_\pi = \pi^2 + \pi + 1 \approx 14.01',
        'description': 'The charm cycle begins at c₅ = 14, the third q-integer at base π.',
        'comparison': 'Compare: strange cycle uses c₅ = 6 = ⌊2π⌋',
    },

    'levels': [
        {
            'c5': 16,
            'pi5': r'16\pi^5',
            'strangeness': -2,
            'charm': 1,
            'particles': ['Omega_c', 'Omega_c_star'],
            'charges': [0],
            'charge_display': 'Q = 0 only',
            'decuplet_term': r'5\pi^4 + \pi^3',
            'octet_term': r'4\pi^4 - \pi^2',
            'description': 'Double-strange charm. Ωc* breaks c₄=6 pattern (has c₄=5). Apex of charm cycle.',
        },
        {
            'c5': 15,
            'pi5': r'15\pi^5',
            'strangeness': -1,
            'charm': 1,
            'particles': ['Xi_c_plus', 'Xi_c_zero', 'Xi_c_star_plus', 'Xi_c_star_zero'],
            'charges': [1, 0],
            'charge_display': 'Q = +1, 0',
            'decuplet_term': r'6\pi^4',
            'octet_term': r'2\pi^4 + \pi^3 + \pi^2/2\pi^2',
            'description': 'Single-strange charm. Decuplet maintains c₄=6 marker.',
        },
        {
            'c5': 14,
            'pi5': r'14\pi^5',
            'strangeness': 0,
            'charm': 1,
            'particles': ['Lambda_c', 'Sigma_c_pp', 'Sigma_c_plus', 'Sigma_c_zero', 'Sigma_c_star_pp', 'Sigma_c_star_plus', 'Sigma_c_star_zero'],
            'charges': [2, 1, 0],
            'charge_display': 'Q = +2, +1, 0',
            'decuplet_term': r'6\pi^4 + 2\pi^3',
            'octet_term': r'2\pi^4 \text{ (}\Lambda_c\text{)}, \quad 5\pi^4 + \pi^3 \text{ (}\Sigma_c\text{)}',
            'description': 'Base level. c₅ = 14 = [3]π. Σc* preserves c₄=6 decuplet marker.',
        },
    ],

    'patterns': {
        'strangeness_rule': r'c_5 = 14 + |S|',
        'decuplet_marker': r'c_4 = 6 \text{ (except } \Omega_c^* \text{ with } c_4 = 5\text{)}',
        'corrections': r'\text{All use } \frac{k}{5} \text{ pattern}',
        'q_integer': r'14 = [3]_\pi = \pi^2 + \pi + 1',
    },

    'comparison': {
        'strange_base': r'c_5 = 6 = \lfloor 2\pi \rfloor',
        'charm_base': r'c_5 = 14 = [3]_\pi',
        'ratio': r'\frac{14}{6} = \frac{7}{3} \approx 2.33',
    },
}


# =============================================================================
# BOTTOM BARYON CYCLE DATA
# =============================================================================

BOTTOM_CYCLE = {
    'base_info': {
        'base_coefficient': 36,
        'relation': r'36 = 6^2',
        'description': 'The bottom cycle begins at c₅ = 36 = 6² (proton coefficient squared).',
    },

    'levels': [
        {
            'c5': 38,
            'pi5': r'38\pi^5',
            'strangeness': -2,
            'bottom': -1,
            'particles': ['Omega_b'],
            'charges': [-1],
            'charge_display': 'Q = -1 only',
            'term': r'2\pi^4 - \pi^2',
            'description': 'Apex. Mirrors Ω⁻ with c₄ = 2 (= 6/3). Same charge window as strange Ω.',
        },
        {
            'c5': 37,
            'pi5': r'37\pi^5',
            'strangeness': -1,
            'bottom': -1,
            'particles': ['Xi_b_zero', 'Xi_b_minus'],
            'charges': [0, -1],
            'charge_display': 'Q = 0, -1',
            'term': r'\pi^4 + \text{corrections}',
            'description': 'Strange-bottom. Maintains c₄ = 1 like strange Ξ octet.',
        },
        {
            'c5': 36,
            'pi5': r'36\pi^5',
            'strangeness': 0,
            'bottom': -1,
            'particles': ['Lambda_b', 'Sigma_b_plus', 'Sigma_b_minus'],
            'charges': [1, 0, -1],
            'charge_display': 'Q = +1, 0, -1',
            'term': r'\text{Various}',
            'description': 'Base level. c₅ = 36 = 6². Same charge window as strange S=-1 level.',
        },
    ],

    'patterns': {
        'strangeness_rule': r'c_5 = 36 + |S|',
        'c4_scaling': r'c_4^{(b)} = c_4^{(s)} / 3 \text{ (approximately)}',
        'corrections': r'\text{All use } \frac{k}{5}\pi \text{ pattern}',
    },

    'comparison': {
        'strange_base': r'c_5 = 7',
        'bottom_base': r'c_5 = 36',
        'c5_squared': r'36 = 6^2 \text{ (proton coefficient squared)}',
    },
}


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Lambda7 Baryon Data")
    print("=" * 60)

    for p in sorted(PARTICLES.values(), key=lambda x: x.mass_exp):
        err = p.error_ev()
        unit = 'eV' if abs(err) < 1000 else 'keV'
        val = err if unit == 'eV' else err/1000
        print(f"{p.symbol:6} {p.full_latex():60} {val:+8.2f} {unit}")
