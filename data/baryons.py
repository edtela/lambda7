#!/usr/bin/env python3
"""
Lambda7 Baryon Data

Pi-algebra mass formulas with Lorentz corrections.
All masses expressed in electron mass units (m_e).

Formula structure:
    mass = c5*pi^5 + c4*pi^4 + c3*pi^3 + c2*pi^2 + correction

Key patterns:
    - Octet (spin-1/2):   c4 = 0 (except Xi with c4=1)
    - Decuplet (spin-3/2): c4 = 6 (universal marker)
    - Strangeness: c5 = 6 + |S|
"""

import math
from dataclasses import dataclass, field
from typing import Optional, Callable, List

# Constants
PI = math.pi
M_E = 0.51099895  # Electron mass in MeV
E_NEG_PI = math.exp(-PI)  # e^(-pi) = 0.04321...
Q2_PI = PI + 1  # [2]_pi = pi + 1

# Powers of pi
PI2 = PI ** 2
PI3 = PI ** 3
PI4 = PI ** 4
PI5 = PI ** 5
PI6 = PI ** 6

# q-calculus integers at base pi
Q3_PI = PI2 + PI + 1  # [3]_pi = pi^2 + pi + 1 ≈ 14.01 (charm base)


@dataclass
class Particle:
    """Baryon with pi-algebra mass formula."""
    name: str
    symbol: str
    latex_symbol: str
    mass_exp: float  # Experimental mass in MeV

    # Polynomial coefficients
    c6: float = 0  # For double-charm (7π⁶)
    c5: float = 0
    c4: float = 0
    c3: float = 0
    c2: float = 0

    # Correction
    correction_func: Optional[Callable[[], float]] = None
    correction_latex: str = ""

    # Metadata
    spin: str = ""
    charge: int = 0
    strangeness: int = 0
    multiplet: str = ""

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
            terms.append(f"{int(self.c6)}\\pi^6")
        if self.c5:
            sign = "+" if self.c5 > 0 and terms else ""
            terms.append(f"{sign}{int(self.c5)}\\pi^5")
        if self.c4:
            sign = "+" if self.c4 > 0 else ""
            terms.append(f"{sign}{int(self.c4)}\\pi^4")
        if self.c3:
            sign = "+" if self.c3 > 0 else ""
            if abs(self.c3) == 1:
                terms.append(f"{sign}\\pi^3" if self.c3 > 0 else "-\\pi^3")
            else:
                terms.append(f"{sign}{int(self.c3)}\\pi^3")
        if self.c2:
            sign = "+" if self.c2 > 0 else ""
            if abs(self.c2) == 1:
                terms.append(f"{sign}\\pi^2" if self.c2 > 0 else "-\\pi^2")
            else:
                terms.append(f"{sign}{int(self.c2)}\\pi^2")

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
    return (2/5) * (4 - PI - (5/4) * E_NEG_PI)

def sigma_plus_corr():
    return -(18/5) * PI + 4/5

def sigma_zero_corr():
    return -(4/5) * (PI + 2 - (1/4) * E_NEG_PI)

def sigma_minus_corr():
    return (1/5) * (11 * PI - 8 - E_NEG_PI)

def xi_zero_corr():
    return (3/5) * (E_NEG_PI - PI - 8/3)

def xi_minus_corr():
    return (2/5) * (9 * PI - 4) + 1 / Q2_PI

def delta_corr():
    return (1/5) * (PI - 2 + 4 * E_NEG_PI)

def sigma_star_plus_corr():
    return (1/5) * (PI - 7 - E_NEG_PI)

def sigma_star_zero_corr():
    return (1/5) * (8 - PI + E_NEG_PI)

def sigma_star_minus_corr():
    return (1/5) * (15 * PI - 8)

def xi_star_zero_corr():
    return -(1/5) * (4 + 5*PI)

def xi_star_minus_corr():
    return (1/5) * (4*PI - 1)

def omega_corr():
    return (6/5) * (E_NEG_PI - PI)


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
    return -8/5


# =============================================================================
# DOUBLE-CHARM BARYON CORRECTION FUNCTIONS
# =============================================================================

def xi_cc_pp_corr():
    """Ξcc++ correction: π + 1/10 (from 7π⁶ formula)."""
    return PI + 1/10


# =============================================================================
# BOTTOM BARYON CORRECTION FUNCTIONS
# =============================================================================

def lambda_b_corr():
    """Λb⁰ correction: π/10."""
    return PI / 10

def sigma_b_plus_corr():
    """Σb⁺ correction: 18π/5."""
    return (18/5) * PI

def sigma_b_minus_corr():
    """Σb⁻ correction: -1/5 (from 36π⁵ + 5π⁴ - 3π³ - 3π²)."""
    return -1/5

def xi_b_zero_corr():
    """Ξb⁰ correction: -4π/5."""
    return -(4/5) * PI

def xi_b_minus_corr():
    """Ξb⁻ correction: -24π/5."""
    return -(24/5) * PI

def omega_b_corr():
    """Ωb⁻ correction: 29π/5."""
    return (29/5) * PI


# =============================================================================
# PARTICLE DATABASE
# =============================================================================

PARTICLES = {
    # --- OCTET (spin-1/2) ---

    'p': Particle(
        name='Proton', symbol='p', latex_symbol='p',
        mass_exp=938.27208816,
        c5=6,
        correction_func=proton_corr,
        correction_latex=r'\frac{4}{5}e^{-\pi}',
        spin='1/2', charge=1, strangeness=0, multiplet='octet'
    ),

    'n': Particle(
        name='Neutron', symbol='n', latex_symbol='n',
        mass_exp=939.56542052,
        c5=6,
        correction_func=neutron_corr,
        correction_latex=r'\frac{8}{\pi}',
        spin='1/2', charge=0, strangeness=0, multiplet='octet'
    ),

    'Lambda': Particle(
        name='Lambda', symbol='\u039b', latex_symbol=r'\Lambda',
        mass_exp=1115.683,
        c5=7, c3=1, c2=1,
        correction_func=lambda_corr,
        correction_latex=r'\frac{2}{5}\left(4 - \pi - \frac{5}{4}e^{-\pi}\right)',
        spin='1/2', charge=0, strangeness=-1, multiplet='octet'
    ),

    'Sigma+': Particle(
        name='Sigma+', symbol='\u03a3\u207a', latex_symbol=r'\Sigma^+',
        mass_exp=1189.37,
        c5=7, c3=6, c2=1,
        correction_func=sigma_plus_corr,
        correction_latex=r'-\frac{18}{5}\pi + \frac{4}{5}',
        spin='1/2', charge=1, strangeness=-1, multiplet='octet'
    ),

    'Sigma0': Particle(
        name='Sigma0', symbol='\u03a3\u2070', latex_symbol=r'\Sigma^0',
        mass_exp=1192.642,
        c5=7, c3=6, c2=1,
        correction_func=sigma_zero_corr,
        correction_latex=r'-\frac{4}{5}\left(\pi + 2 - \frac{1}{4}e^{-\pi}\right)',
        spin='1/2', charge=0, strangeness=-1, multiplet='octet'
    ),

    'Sigma-': Particle(
        name='Sigma-', symbol='\u03a3\u207b', latex_symbol=r'\Sigma^-',
        mass_exp=1197.449,
        c5=7, c3=6, c2=1,
        correction_func=sigma_minus_corr,
        correction_latex=r'\frac{1}{5}\left(11\pi - 8 - e^{-\pi}\right)',
        spin='1/2', charge=-1, strangeness=-1, multiplet='octet'
    ),

    'Xi0': Particle(
        name='Xi0', symbol='\u039e\u2070', latex_symbol=r'\Xi^0',
        mass_exp=1314.86,
        c5=8, c4=1, c3=1,
        correction_func=xi_zero_corr,
        correction_latex=r'\frac{3}{5}\left(e^{-\pi} - \pi - \frac{8}{3}\right)',
        spin='1/2', charge=0, strangeness=-2, multiplet='octet'
    ),

    'Xi-': Particle(
        name='Xi-', symbol='\u039e\u207b', latex_symbol=r'\Xi^-',
        mass_exp=1321.71,
        c5=8, c4=1, c3=1,
        correction_func=xi_minus_corr,
        correction_latex=r'\frac{2}{5}(9\pi - 4) + \frac{1}{[2]_\pi}',
        spin='1/2', charge=-1, strangeness=-2, multiplet='octet'
    ),

    # --- DECUPLET (spin-3/2, c4=6) ---

    'Delta++': Particle(
        name='Delta++', symbol='\u0394\u207a\u207a', latex_symbol=r'\Delta^{++}',
        mass_exp=1232.0,
        c5=6, c4=6, c2=-1,
        correction_func=delta_corr,
        correction_latex=r'\frac{1}{5}\left(\pi - 2 + 4e^{-\pi}\right)',
        spin='3/2', charge=2, strangeness=0, multiplet='decuplet'
    ),

    'Delta+': Particle(
        name='Delta+', symbol='\u0394\u207a', latex_symbol=r'\Delta^+',
        mass_exp=1232.0,
        c5=6, c4=6, c2=-1,
        correction_func=delta_corr,
        correction_latex=r'\frac{1}{5}\left(\pi - 2 + 4e^{-\pi}\right)',
        spin='3/2', charge=1, strangeness=0, multiplet='decuplet'
    ),

    'Delta0': Particle(
        name='Delta0', symbol='\u0394\u2070', latex_symbol=r'\Delta^0',
        mass_exp=1232.0,
        c5=6, c4=6, c2=-1,
        correction_func=delta_corr,
        correction_latex=r'\frac{1}{5}\left(\pi - 2 + 4e^{-\pi}\right)',
        spin='3/2', charge=0, strangeness=0, multiplet='decuplet'
    ),

    'Delta-': Particle(
        name='Delta-', symbol='\u0394\u207b', latex_symbol=r'\Delta^-',
        mass_exp=1232.0,
        c5=6, c4=6, c2=-1,
        correction_func=delta_corr,
        correction_latex=r'\frac{1}{5}\left(\pi - 2 + 4e^{-\pi}\right)',
        spin='3/2', charge=-1, strangeness=0, multiplet='decuplet'
    ),

    'Sigma*+': Particle(
        name='Sigma*+', symbol='\u03a3*\u207a', latex_symbol=r'\Sigma^{*+}',
        mass_exp=1382.80,
        c5=7, c4=6, c2=-2,
        correction_func=sigma_star_plus_corr,
        correction_latex=r'\frac{1}{5}\left(\pi - 7 - e^{-\pi}\right)',
        spin='3/2', charge=1, strangeness=-1, multiplet='decuplet'
    ),

    'Sigma*0': Particle(
        name='Sigma*0', symbol='\u03a3*\u2070', latex_symbol=r'\Sigma^{*0}',
        mass_exp=1383.7,
        c5=7, c4=6, c2=-2,
        correction_func=sigma_star_zero_corr,
        correction_latex=r'\frac{1}{5}\left(8 - \pi + e^{-\pi}\right)',
        spin='3/2', charge=0, strangeness=-1, multiplet='decuplet'
    ),

    'Sigma*-': Particle(
        name='Sigma*-', symbol='\u03a3*\u207b', latex_symbol=r'\Sigma^{*-}',
        mass_exp=1387.2,
        c5=7, c4=6, c2=-2,
        correction_func=sigma_star_minus_corr,
        correction_latex=r'\frac{1}{5}(15\pi - 8)',
        spin='3/2', charge=-1, strangeness=-1, multiplet='decuplet'
    ),

    'Xi*0': Particle(
        name='Xi*0', symbol='\u039e*\u2070', latex_symbol=r'\Xi^{*0}',
        mass_exp=1531.80,
        c5=8, c4=6, c3=-1,
        correction_func=xi_star_zero_corr,
        correction_latex=r'-\frac{1}{5}(4 + 5\pi)',
        spin='3/2', charge=0, strangeness=-2, multiplet='decuplet'
    ),

    'Xi*-': Particle(
        name='Xi*-', symbol='\u039e*\u207b', latex_symbol=r'\Xi^{*-}',
        mass_exp=1535.0,
        c5=8, c4=6, c3=-1,
        correction_func=xi_star_minus_corr,
        correction_latex=r'\frac{1}{5}(4\pi - 1)',
        spin='3/2', charge=-1, strangeness=-2, multiplet='decuplet'
    ),

    'Omega': Particle(
        name='Omega', symbol='\u03a9\u207b', latex_symbol=r'\Omega^-',
        mass_exp=1672.45,
        c5=9, c4=6, c3=-2,
        correction_func=omega_corr,
        correction_latex=r'\frac{6}{5}\left(e^{-\pi} - \pi\right)',
        spin='3/2', charge=-1, strangeness=-3, multiplet='decuplet'
    ),
}


# =============================================================================
# CHARM BARYON DATABASE
# =============================================================================

CHARM_PARTICLES = {
    # --- CHARM OCTET-LIKE (spin-1/2) ---

    'Lc+': Particle(
        name='Lambda_c+', symbol='\u039bc\u207a', latex_symbol=r'\Lambda_c^+',
        mass_exp=2286.46,
        c5=14, c4=2,
        correction_func=lambda_c_corr,
        correction_latex=r'-\frac{23}{5}',
        spin='1/2', charge=1, strangeness=0, multiplet='charm-octet'
    ),

    'Sc++': Particle(
        name='Sigma_c++', symbol='\u03a3c\u207a\u207a', latex_symbol=r'\Sigma_c^{++}',
        mass_exp=2453.97,
        c5=14, c4=5, c3=1,
        correction_func=sigma_c_pp_corr,
        correction_latex=r'-\frac{\pi}{5} + \frac{3}{5}',
        spin='1/2', charge=2, strangeness=0, multiplet='charm-octet'
    ),

    'Sc+': Particle(
        name='Sigma_c+', symbol='\u03a3c\u207a', latex_symbol=r'\Sigma_c^+',
        mass_exp=2452.9,
        c5=14, c4=5, c3=1,
        correction_func=sigma_c_p_corr,
        correction_latex=r'\frac{3\pi}{5} - 4',
        spin='1/2', charge=1, strangeness=0, multiplet='charm-octet'
    ),

    'Sc0': Particle(
        name='Sigma_c0', symbol='\u03a3c\u2070', latex_symbol=r'\Sigma_c^0',
        mass_exp=2453.75,
        c5=14, c4=5, c3=1,
        correction_func=sigma_c_0_corr,
        correction_latex=r'\pi - \frac{18}{5}',
        spin='1/2', charge=0, strangeness=0, multiplet='charm-octet'
    ),

    'Xc+': Particle(
        name='Xi_c+', symbol='\u039ec\u207a', latex_symbol=r'\Xi_c^+',
        mass_exp=2467.71,
        c5=15, c4=2, c3=1, c2=1,
        correction_func=xi_c_p_corr,
        correction_latex=r'\frac{7\pi}{5} - \frac{6}{5}',
        spin='1/2', charge=1, strangeness=-1, multiplet='charm-octet'
    ),

    'Xc0': Particle(
        name='Xi_c0', symbol='\u039ec\u2070', latex_symbol=r'\Xi_c^0',
        mass_exp=2470.44,
        c5=15, c4=2, c3=1, c2=2,
        correction_func=xi_c_0_corr,
        correction_latex=r'-\pi + \frac{9}{5}',
        spin='1/2', charge=0, strangeness=-1, multiplet='charm-octet'
    ),

    'Oc0': Particle(
        name='Omega_c0', symbol='\u03a9c\u2070', latex_symbol=r'\Omega_c^0',
        mass_exp=2695.2,
        c5=16, c4=4, c2=-1,
        correction_func=omega_c_corr,
        correction_latex=r'-\frac{4\pi}{5} + \frac{4}{5}',
        spin='1/2', charge=0, strangeness=-2, multiplet='charm-octet'
    ),

    # --- CHARM DECUPLET-LIKE (spin-3/2, c4=6) ---

    'Sc*++': Particle(
        name='Sigma_c*++', symbol='\u03a3c*\u207a\u207a', latex_symbol=r'\Sigma_c^{*++}',
        mass_exp=2518.41,
        c5=14, c4=6, c3=2,
        correction_func=sigma_c_star_pp_corr,
        correction_latex=r'-\pi + \frac{4}{5}',
        spin='3/2', charge=2, strangeness=0, multiplet='charm-decuplet'
    ),

    'Sc*+': Particle(
        name='Sigma_c*+', symbol='\u03a3c*\u207a', latex_symbol=r'\Sigma_c^{*+}',
        mass_exp=2517.5,
        c5=14, c4=6, c3=2,
        correction_func=sigma_c_star_p_corr,
        correction_latex=r'-\frac{4\pi}{5} - \frac{8}{5}',
        spin='3/2', charge=1, strangeness=0, multiplet='charm-decuplet'
    ),

    'Sc*0': Particle(
        name='Sigma_c*0', symbol='\u03a3c*\u2070', latex_symbol=r'\Sigma_c^{*0}',
        mass_exp=2518.48,
        c5=14, c4=6, c3=2,
        correction_func=sigma_c_star_0_corr,
        correction_latex=r'-\frac{11}{5}',
        spin='3/2', charge=0, strangeness=0, multiplet='charm-decuplet'
    ),

    'Xc*+': Particle(
        name='Xi_c*+', symbol='\u039ec*\u207a', latex_symbol=r'\Xi_c^{*+}',
        mass_exp=2645.57,
        c5=15, c4=6,
        correction_func=xi_c_star_p_corr,
        correction_latex=r'\frac{4\pi}{5}',
        spin='3/2', charge=1, strangeness=-1, multiplet='charm-decuplet'
    ),

    'Xc*0': Particle(
        name='Xi_c*0', symbol='\u039ec*\u2070', latex_symbol=r'\Xi_c^{*0}',
        mass_exp=2646.38,
        c5=15, c4=6,
        correction_func=xi_c_star_0_corr,
        correction_latex=r'\frac{13\pi}{10}',
        spin='3/2', charge=0, strangeness=-1, multiplet='charm-decuplet'
    ),

    'Oc*0': Particle(
        name='Omega_c*0', symbol='\u03a9c*\u2070', latex_symbol=r'\Omega_c^{*0}',
        mass_exp=2765.9,
        c5=16, c4=5, c3=1,
        correction_func=omega_c_star_corr,
        correction_latex=r'-\frac{8}{5}',
        spin='3/2', charge=0, strangeness=-2, multiplet='charm-decuplet'
    ),
}


# =============================================================================
# DOUBLE-CHARM BARYON DATABASE
# =============================================================================

DOUBLE_CHARM_PARTICLES = {
    'Xcc++': Particle(
        name='Xi_cc++', symbol='\u039ecc\u207a\u207a', latex_symbol=r'\Xi_{cc}^{++}',
        mass_exp=3621.55,
        c6=7, c4=3, c3=2,
        correction_func=xi_cc_pp_corr,
        correction_latex=r'\pi + \frac{1}{10}',
        spin='1/2', charge=2, strangeness=0, multiplet='double-charm'
    ),
}


# =============================================================================
# BOTTOM BARYON DATABASE
# =============================================================================

BOTTOM_PARTICLES = {
    # --- BOTTOM OCTET-LIKE (spin-1/2) ---
    # c5 = 36 + |S|, mirroring strange cycle with +29 offset

    'Lb0': Particle(
        name='Lambda_b0', symbol='\u039bb\u2070', latex_symbol=r'\Lambda_b^0',
        mass_exp=5619.60,
        c5=36, c2=-2,
        correction_func=lambda_b_corr,
        correction_latex=r'\frac{\pi}{10}',
        spin='1/2', charge=0, strangeness=0, multiplet='bottom-octet'
    ),

    'Sb+': Particle(
        name='Sigma_b+', symbol='\u03a3b\u207a', latex_symbol=r'\Sigma_b^+',
        mass_exp=5810.56,
        c5=36, c4=3, c3=1, c2=2,
        correction_func=sigma_b_plus_corr,
        correction_latex=r'\frac{18\pi}{5}',
        spin='1/2', charge=1, strangeness=0, multiplet='bottom-octet'
    ),

    'Sb-': Particle(
        name='Sigma_b-', symbol='\u03a3b\u207b', latex_symbol=r'\Sigma_b^-',
        mass_exp=5815.64,
        c5=36, c4=5, c3=-3, c2=-3,
        correction_func=sigma_b_minus_corr,
        correction_latex=r'-\frac{1}{5}',
        spin='1/2', charge=-1, strangeness=0, multiplet='bottom-octet'
    ),

    'Xb0': Particle(
        name='Xi_b0', symbol='\u039eb\u2070', latex_symbol=r'\Xi_b^0',
        mass_exp=5791.9,
        c5=37, c4=1, c3=-3, c2=1,
        correction_func=xi_b_zero_corr,
        correction_latex=r'-\frac{4\pi}{5}',
        spin='1/2', charge=0, strangeness=-1, multiplet='bottom-octet'
    ),

    'Xb-': Particle(
        name='Xi_b-', symbol='\u039eb\u207b', latex_symbol=r'\Xi_b^-',
        mass_exp=5797.0,
        c5=37, c4=1, c3=-1, c2=-3,
        correction_func=xi_b_minus_corr,
        correction_latex=r'-\frac{24\pi}{5}',
        spin='1/2', charge=-1, strangeness=-1, multiplet='bottom-octet'
    ),

    'Ob-': Particle(
        name='Omega_b-', symbol='\u03a9b\u207b', latex_symbol=r'\Omega_b^-',
        mass_exp=6046.1,
        c5=38, c4=2, c2=-1,
        correction_func=omega_b_corr,
        correction_latex=r'\frac{29\pi}{5}',
        spin='1/2', charge=-1, strangeness=-2, multiplet='bottom-octet'
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
            'particles': ['Omega'],
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
            'particles': ['Xi*0', 'Xi*-', 'Xi0', 'Xi-'],
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
            'particles': ['Sigma*+', 'Sigma*0', 'Sigma*-', 'Lambda', 'Sigma+', 'Sigma0', 'Sigma-'],
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
            'particles': ['Delta++', 'Delta+', 'Delta0', 'Delta-', 'p', 'n'],
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
            'particles': ['Oc0', 'Oc*0'],
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
            'particles': ['Xc+', 'Xc0', 'Xc*+', 'Xc*0'],
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
            'particles': ['Lc+', 'Sc++', 'Sc+', 'Sc0', 'Sc*++', 'Sc*+', 'Sc*0'],
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
            'particles': ['Ob-'],
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
            'particles': ['Xb0', 'Xb-'],
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
            'particles': ['Lb0', 'Sb+', 'Sb-'],
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
