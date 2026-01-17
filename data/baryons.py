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


@dataclass
class Particle:
    """Baryon with pi-algebra mass formula."""
    name: str
    symbol: str
    latex_symbol: str
    mass_exp: float  # Experimental mass in MeV

    # Polynomial coefficients
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
        return self.c5*PI5 + self.c4*PI4 + self.c3*PI3 + self.c2*PI2

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

        if self.c5:
            terms.append(f"{int(self.c5)}\\pi^5")
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
