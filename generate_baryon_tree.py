#!/usr/bin/env python3
"""
Generate interactive baryon tree visualization.

Tree structure based on shared coefficients:
- Light baryons: proton (6π⁵) at root
- Charm baryons: Λc+ (14π⁵) at root
- Bottom baryons: Λb⁰ (36π⁵) at root

Particles sharing coefficients are grouped under virtual nodes.
"""

import math
import json
import re
from data.baryons import (
    PARTICLES, CHARM_PARTICLES, BOTTOM_PARTICLES, DOUBLE_CHARM_PARTICLES,
    PI, PI2, PI3, PI4, PI5, PI6, M_E
)

# Map old keys to particle dicts for easy access
ALL_PARTICLES = {**PARTICLES, **CHARM_PARTICLES, **BOTTOM_PARTICLES, **DOUBLE_CHARM_PARTICLES}

# Experimental uncertainties in MeV (from PDG)
UNCERTAINTIES = {
    'p': 0.00000029e-3,  # proton: ultra-precise
    'n': 0.00000054e-3,  # neutron: ultra-precise
    'Lambda': 0.006,
    'Sigma+': 0.03,
    'Sigma0': 0.03,
    'Sigma-': 0.04,
    'Sigma*+': 0.9,
    'Sigma*0': 0.9,
    'Sigma*-': 0.9,
    'Xi0': 0.08,
    'Xi-': 0.06,
    'Xi*0': 0.8,
    'Xi*-': 0.9,
    'Omega': 0.21,
    'Lc+': 0.14,
    'Sc++': 0.14,
    'Sc+': 0.4,
    'Sc0': 0.14,
    'Sc*++': 0.4,
    'Sc*+': 0.5,
    'Sc*0': 0.4,
    'Xc+': 0.31,
    'Xc0': 0.28,
    'Xc*+': 0.5,
    'Xc*0': 0.5,
    'Oc0': 0.21,
    'Oc*0': 0.5,
    'Xcc++': 0.4,
    'Lb0': 0.06,
    'Sb+': 0.5,
    'Sb-': 0.5,
    'Xb0': 0.4,
    'Xb-': 0.4,
    'Ob-': 0.22,
    'D': 2.0,  # Delta resonance width
}

def latex_to_display(latex):
    """Convert simple LaTeX correction to Unicode display format.

    Returns None for complex formulas (with \\left, \\right).
    """
    if not latex:
        return None

    # Complex formulas - return None
    if '\\left' in latex or '\\right' in latex:
        return None

    s = latex.strip()

    # Handle -π - 1/π pattern (Xi0)
    if s == r'-\pi - \frac{1}{\pi}':
        return '-π - 1/π'

    # Plain numbers: -4, +1, -2
    if re.match(r'^[+-]?\d+$', s):
        return s if s.startswith(('+', '-')) else '+' + s

    # \frac{a}{b} patterns
    m = re.match(r'^([+-])?\\frac\{([^}]+)\}\{([^}]+)\}$', s)
    if m:
        sign = m.group(1) or '+'
        num = m.group(2)
        denom = m.group(3)
        # Handle \pi in numerator
        num = num.replace('\\pi', 'π')
        # Handle \pi in denominator
        denom = denom.replace('\\pi', 'π')
        return f"{sign}{num}/{denom}"

    # \frac{4}{5}e^{-\pi} pattern (proton)
    m = re.match(r'^([+-])?\\frac\{([^}]+)\}\{([^}]+)\}e\^\{-\\pi\}$', s)
    if m:
        sign = m.group(1) or '+'
        num = m.group(2)
        denom = m.group(3)
        return f"{sign}({num}/{denom})e⁻ᵖⁱ"

    return None


def get_correction_display(key):
    """Get correction display string from master data."""
    if key not in ALL_PARTICLES:
        return None
    p = ALL_PARTICLES[key]
    return latex_to_display(p.correction_latex)


def get_correction_value(key):
    """Get correction numerical value from master data (in m_e)."""
    if key not in ALL_PARTICLES:
        return 0.0
    return ALL_PARTICLES[key].correction()


def get_residual_me(p):
    """Get residual (exp - poly) in m_e units."""
    return p.mass_exp / M_E - p.mass_base()

def format_coeff(c, power_str, is_first=False):
    """Format a coefficient, omitting 1 coefficients, with spaces around operators."""
    if c == 0:
        return None
    c_int = int(c)
    if is_first:
        if c_int == 1:
            return power_str
        elif c_int == -1:
            return f"-{power_str}"
        else:
            return f"{c_int}{power_str}"
    else:
        if c_int == 1:
            return f" + {power_str}"
        elif c_int == -1:
            return f" - {power_str}"
        elif c_int > 0:
            return f" + {c_int}{power_str}"
        else:
            return f" - {abs(c_int)}{power_str}"

def format_full_formula(p):
    """Format complete polynomial formula."""
    parts = []
    if p.c6:
        parts.append(format_coeff(p.c6, "π⁶", is_first=len(parts)==0))
    if p.c5:
        parts.append(format_coeff(p.c5, "π⁵", is_first=len(parts)==0))
    if p.c4:
        parts.append(format_coeff(p.c4, "π⁴", is_first=len(parts)==0))
    if p.c3:
        parts.append(format_coeff(p.c3, "π³", is_first=len(parts)==0))
    if p.c2:
        parts.append(format_coeff(p.c2, "π²", is_first=len(parts)==0))
    return "".join(p for p in parts if p) if parts else "0"


def format_remainder(p, base_c5):
    """Format the remainder formula (what's added beyond the base c5)."""
    parts = []
    # c6 term (for double charm)
    if hasattr(p, 'c6') and p.c6:
        parts.append(format_coeff(p.c6, "π⁶", is_first=len(parts)==0))
    # Extra c5 beyond base
    extra_c5 = p.c5 - base_c5
    if extra_c5:
        parts.append(format_coeff(extra_c5, "π⁵", is_first=len(parts)==0))
    if p.c4:
        parts.append(format_coeff(p.c4, "π⁴", is_first=len(parts)==0))
    if p.c3:
        parts.append(format_coeff(p.c3, "π³", is_first=len(parts)==0))
    if p.c2:
        parts.append(format_coeff(p.c2, "π²", is_first=len(parts)==0))
    return "".join(p for p in parts if p) if parts else ""


def format_diff(p, parent_c5=0, parent_c4=0, parent_c3=0, parent_c2=0):
    """Format what this particle adds beyond its parent node."""
    parts = []
    # c6 term (for double charm)
    if hasattr(p, 'c6') and p.c6:
        parts.append(format_coeff(p.c6, "π⁶", is_first=len(parts)==0))
    # Differences from parent
    diff_c5 = p.c5 - parent_c5
    if diff_c5:
        parts.append(format_coeff(diff_c5, "π⁵", is_first=len(parts)==0))
    diff_c4 = p.c4 - parent_c4
    if diff_c4:
        parts.append(format_coeff(diff_c4, "π⁴", is_first=len(parts)==0))
    diff_c3 = p.c3 - parent_c3
    if diff_c3:
        parts.append(format_coeff(diff_c3, "π³", is_first=len(parts)==0))
    diff_c2 = p.c2 - parent_c2
    if diff_c2:
        parts.append(format_coeff(diff_c2, "π²", is_first=len(parts)==0))
    return "".join(p for p in parts if p) if parts else ""


def format_correction(corr, has_poly=True):
    """Format correction with proper spacing."""
    if not corr:
        return ""
    # Add space before + or - only if there's a polynomial part
    if corr.startswith('+'):
        return (" + " if has_poly else "") + corr[1:]
    elif corr.startswith('-'):
        return (" - " if has_poly else "-") + corr[1:]
    else:
        return (" + " if has_poly else "") + corr


def generate_light_baryon_data():
    """Generate nodes and edges for light baryons."""
    nodes = []
    edges = []

    # === ROOT: 6π⁵ (virtual) ===
    nodes.append({
        'id': 'root6',
        'label': '6π⁵',
        'sublabel': 'S=0',
        'type': 'virtual',
        'formula': '6π⁵',
        'description': 'Light baryon base (S=0)'
    })

    # === PROTON (6π⁵) - parent: root6 (6π⁵) ===
    p = ALL_PARTICLES['p']
    corr_p = get_correction_display('p')
    poly_p = format_diff(p, parent_c5=6)
    diff_p = poly_p + format_correction(corr_p, has_poly=bool(poly_p))
    nodes.append({
        'id': 'p',
        'label': 'p',
        'sublabel': diff_p if diff_p else '',
        'type': 'particle',
        'formula': format_full_formula(p),
        'correction': corr_p,
        'mass_me': p.mass_base(),
        'actual_mev': p.mass_exp,
        'residual_me': get_residual_me(p),
        'charge': '+1',
        'spin': '1/2',
        'strangeness': 0
    })
    edges.append({'source': 'root6', 'target': 'p'})

    # === NEUTRON (6π⁵ + 8/π) - parent: root6 (6π⁵) ===
    n = ALL_PARTICLES['n']
    corr_n = get_correction_display('n')
    poly_n = format_diff(n, parent_c5=6)
    diff_n = poly_n + format_correction(corr_n, has_poly=bool(poly_n))
    nodes.append({
        'id': 'n',
        'label': 'n',
        'sublabel': diff_n if diff_n else '',
        'type': 'particle',
        'formula': format_full_formula(n),
        'correction': corr_n,
        'mass_me': n.mass_base(),
        'actual_mev': n.mass_exp,
        'residual_me': get_residual_me(n),
        'charge': '0',
        'spin': '1/2',
        'strangeness': 0
    })
    edges.append({'source': 'root6', 'target': 'n'})

    # === DELTA (6π⁵ + 6π⁴ - π²) - parent: root6 (6π⁵) ===
    class DeltaData:
        c6, c5, c4, c3, c2 = 0, 6, 6, 0, -1
    delta = DeltaData()
    diff_d = format_diff(delta, parent_c5=6)
    nodes.append({
        'id': 'D',
        'label': 'Δ',
        'sublabel': diff_d,
        'type': 'spin32',
        'formula': '6π⁵ + 6π⁴ - π²',
        'correction': None,
        'mass_me': 6*PI5 + 6*PI4 - PI2,
        'actual_mev': 1232.0,
        'residual_me': 1232.0/M_E - (6*PI5 + 6*PI4 - PI2),
        'charge': '++,+,0,-',
        'spin': '3/2',
        'strangeness': 0
    })
    edges.append({'source': 'root6', 'target': 'D'})

    # === 7π⁵ LEVEL (S=-1) ===
    nodes.append({
        'id': 'v7',
        'label': '+π⁵',
        'sublabel': 'S=-1',
        'type': 'virtual',
        'formula': '7π⁵',
        'description': 'Strangeness -1 level'
    })
    edges.append({'source': 'root6', 'target': 'v7'})

    # Lambda: 7π⁵ + π³ + π² - parent: v7 (7π⁵)
    lam = ALL_PARTICLES['Lambda']
    corr_lam = get_correction_display('Lambda')
    poly_lam = format_diff(lam, parent_c5=7)
    diff_lam = poly_lam + format_correction(corr_lam, has_poly=bool(poly_lam))
    nodes.append({
        'id': 'L0',
        'label': 'Λ',
        'sublabel': diff_lam,
        'type': 'particle',
        'formula': format_full_formula(lam),
        'correction': corr_lam,
        'mass_me': lam.mass_base(),
        'actual_mev': lam.mass_exp,
        'residual_me': get_residual_me(lam),
        'charge': '0',
        'spin': '1/2',
        'strangeness': -1
    })
    edges.append({'source': 'v7', 'target': 'L0'})

    # === Sigma octet: share 6π³ ===
    nodes.append({
        'id': 'vS6pi3',
        'label': '+6π³',
        'sublabel': 'Σ base',
        'type': 'virtual',
        'formula': '7π⁵ + 6π³',
        'description': 'Sigma octet base (6π³)'
    })
    edges.append({'source': 'v7', 'target': 'vS6pi3'})

    # Σ+: 7π⁵ + 6π³ (c2=0) - parent: vS6pi3 (c5=7, c3=6)
    sp = ALL_PARTICLES['Sigma+']
    corr_sp = get_correction_display('Sigma+')
    poly_sp = format_diff(sp, parent_c5=7, parent_c3=6)
    diff_sp = poly_sp + format_correction(corr_sp, has_poly=bool(poly_sp))
    nodes.append({
        'id': 'S+',
        'label': 'Σ⁺',
        'sublabel': diff_sp,
        'type': 'particle',
        'formula': format_full_formula(sp),
        'correction': corr_sp,
        'mass_me': sp.mass_base(),
        'actual_mev': sp.mass_exp,
        'residual_me': get_residual_me(sp),
        'charge': '+1',
        'spin': '1/2',
        'strangeness': -1
    })
    edges.append({'source': 'vS6pi3', 'target': 'S+'})

    # Σ0: 7π⁵ + 6π³ + π² - parent: vS6pi3 (c5=7, c3=6)
    s0 = ALL_PARTICLES['Sigma0']
    corr_s0 = get_correction_display('Sigma0')
    poly_s0 = format_diff(s0, parent_c5=7, parent_c3=6)
    diff_s0 = poly_s0 + format_correction(corr_s0, has_poly=bool(poly_s0))
    nodes.append({
        'id': 'S0',
        'label': 'Σ⁰',
        'sublabel': diff_s0,
        'type': 'particle',
        'formula': format_full_formula(s0),
        'correction': corr_s0,
        'mass_me': s0.mass_base(),
        'actual_mev': s0.mass_exp,
        'residual_me': get_residual_me(s0),
        'charge': '0',
        'spin': '1/2',
        'strangeness': -1
    })
    edges.append({'source': 'vS6pi3', 'target': 'S0'})

    # Σ-: 7π⁵ + 6π³ + 2π² - parent: vS6pi3 (c5=7, c3=6)
    sm = ALL_PARTICLES['Sigma-']
    corr_sm = get_correction_display('Sigma-')
    poly_sm = format_diff(sm, parent_c5=7, parent_c3=6)
    diff_sm = poly_sm + format_correction(corr_sm, has_poly=bool(poly_sm))
    nodes.append({
        'id': 'S-',
        'label': 'Σ⁻',
        'sublabel': diff_sm,
        'type': 'particle',
        'formula': format_full_formula(sm),
        'correction': corr_sm,
        'mass_me': sm.mass_base(),
        'actual_mev': sm.mass_exp,
        'residual_me': get_residual_me(sm),
        'charge': '-1',
        'spin': '1/2',
        'strangeness': -1
    })
    edges.append({'source': 'vS6pi3', 'target': 'S-'})

    # === Sigma* decuplet: share 6π⁴ ===
    nodes.append({
        'id': 'vSs6pi4',
        'label': '+6π⁴',
        'sublabel': 'Σ* base',
        'type': 'virtual',
        'formula': '7π⁵ + 6π⁴',
        'description': 'Sigma* decuplet base (6π⁴)'
    })
    edges.append({'source': 'v7', 'target': 'vSs6pi4'})

    # Σ*+: 7π⁵ + 6π⁴ - 2π² - parent: vSs6pi4 (c5=7, c4=6)
    ssp = ALL_PARTICLES['Sigma*+']
    corr_ssp = get_correction_display('Sigma*+')
    poly_ssp = format_diff(ssp, parent_c5=7, parent_c4=6)
    diff_ssp = poly_ssp + format_correction(corr_ssp, has_poly=bool(poly_ssp))
    nodes.append({
        'id': 'Ss+',
        'label': 'Σ*⁺',
        'sublabel': diff_ssp,
        'type': 'spin32',
        'formula': format_full_formula(ssp),
        'correction': corr_ssp,
        'mass_me': ssp.mass_base(),
        'actual_mev': ssp.mass_exp,
        'residual_me': get_residual_me(ssp),
        'charge': '+1',
        'spin': '3/2',
        'strangeness': -1
    })
    edges.append({'source': 'vSs6pi4', 'target': 'Ss+'})

    # Σ*0: 7π⁵ + 6π⁴ - 2π² + 1 - parent: vSs6pi4 (c5=7, c4=6)
    ss0 = ALL_PARTICLES['Sigma*0']
    corr_ss0 = get_correction_display('Sigma*0')
    poly_ss0 = format_diff(ss0, parent_c5=7, parent_c4=6)
    diff_ss0 = poly_ss0 + format_correction(corr_ss0, has_poly=bool(poly_ss0))
    nodes.append({
        'id': 'Ss0',
        'label': 'Σ*⁰',
        'sublabel': diff_ss0,
        'type': 'spin32',
        'formula': format_full_formula(ss0),
        'correction': corr_ss0,
        'mass_me': ss0.mass_base(),
        'actual_mev': ss0.mass_exp,
        'residual_me': get_residual_me(ss0),
        'charge': '0',
        'spin': '3/2',
        'strangeness': -1
    })
    edges.append({'source': 'vSs6pi4', 'target': 'Ss0'})

    # Σ*-: 7π⁵ + 6π⁴ - π² - parent: vSs6pi4 (c5=7, c4=6)
    ssm = ALL_PARTICLES['Sigma*-']
    corr_ssm = get_correction_display('Sigma*-')
    poly_ssm = format_diff(ssm, parent_c5=7, parent_c4=6)
    diff_ssm = poly_ssm + format_correction(corr_ssm, has_poly=bool(poly_ssm))
    nodes.append({
        'id': 'Ss-',
        'label': 'Σ*⁻',
        'sublabel': diff_ssm,
        'type': 'spin32',
        'formula': format_full_formula(ssm),
        'correction': corr_ssm,
        'mass_me': ssm.mass_base(),
        'actual_mev': ssm.mass_exp,
        'residual_me': get_residual_me(ssm),
        'charge': '-1',
        'spin': '3/2',
        'strangeness': -1
    })
    edges.append({'source': 'vSs6pi4', 'target': 'Ss-'})

    # === 8π⁵ LEVEL (S=-2) ===
    nodes.append({
        'id': 'v8',
        'label': '+π⁵',
        'sublabel': 'S=-2',
        'type': 'virtual',
        'formula': '8π⁵',
        'description': 'Strangeness -2 level (Xi)'
    })
    edges.append({'source': 'v7', 'target': 'v8'})

    # === Xi octet: share π⁴ + π³ ===
    nodes.append({
        'id': 'vXpi4pi3',
        'label': '+π⁴+π³',
        'sublabel': 'Ξ base',
        'type': 'virtual',
        'formula': '8π⁵ + π⁴ + π³',
        'description': 'Xi octet base'
    })
    edges.append({'source': 'v8', 'target': 'vXpi4pi3'})

    # Ξ0: 8π⁵ + π⁴ + π³ - parent: vXpi4pi3 (c5=8, c4=1, c3=1)
    x0 = ALL_PARTICLES['Xi0']
    corr_x0 = get_correction_display('Xi0')
    poly_x0 = format_diff(x0, parent_c5=8, parent_c4=1, parent_c3=1)
    diff_x0 = poly_x0 + format_correction(corr_x0, has_poly=bool(poly_x0))
    nodes.append({
        'id': 'X0',
        'label': 'Ξ⁰',
        'sublabel': diff_x0,
        'type': 'particle',
        'formula': format_full_formula(x0),
        'correction': corr_x0,
        'mass_me': x0.mass_base(),
        'actual_mev': x0.mass_exp,
        'residual_me': get_residual_me(x0),
        'charge': '0',
        'spin': '1/2',
        'strangeness': -2
    })
    edges.append({'source': 'vXpi4pi3', 'target': 'X0'})

    # Ξ-: 8π⁵ + π⁴ + π³ + π² (Tier 1) - parent: vXpi4pi3 (c5=8, c4=1, c3=1)
    xm = ALL_PARTICLES['Xi-']
    corr_xm = get_correction_display('Xi-')
    poly_xm = format_diff(xm, parent_c5=8, parent_c4=1, parent_c3=1)
    diff_xm = poly_xm + format_correction(corr_xm, has_poly=bool(poly_xm))
    nodes.append({
        'id': 'X-',
        'label': 'Ξ⁻',
        'sublabel': diff_xm,
        'type': 'particle',
        'formula': format_full_formula(xm),
        'correction': corr_xm,
        'mass_me': xm.mass_base(),
        'actual_mev': xm.mass_exp,
        'residual_me': get_residual_me(xm),
        'charge': '-1',
        'spin': '1/2',
        'strangeness': -2
    })
    edges.append({'source': 'vXpi4pi3', 'target': 'X-'})

    # === Xi* decuplet: share 6π⁴ - π³ ===
    nodes.append({
        'id': 'vXs6pi4',
        'label': '+6π⁴-π³',
        'sublabel': 'Ξ* base',
        'type': 'virtual',
        'formula': '8π⁵ + 6π⁴ - π³',
        'description': 'Xi* decuplet base'
    })
    edges.append({'source': 'v8', 'target': 'vXs6pi4'})

    # Ξ*0: 8π⁵ + 6π⁴ - π³ - parent: vXs6pi4 (c5=8, c4=6, c3=-1)
    xs0 = ALL_PARTICLES['Xi*0']
    corr_xs0 = get_correction_display('Xi*0')
    poly_xs0 = format_diff(xs0, parent_c5=8, parent_c4=6, parent_c3=-1)
    diff_xs0 = poly_xs0 + format_correction(corr_xs0, has_poly=bool(poly_xs0))
    nodes.append({
        'id': 'Xs0',
        'label': 'Ξ*⁰',
        'sublabel': diff_xs0,
        'type': 'spin32',
        'formula': format_full_formula(xs0),
        'correction': corr_xs0,
        'mass_me': xs0.mass_base(),
        'actual_mev': xs0.mass_exp,
        'residual_me': get_residual_me(xs0),
        'charge': '0',
        'spin': '3/2',
        'strangeness': -2
    })
    edges.append({'source': 'vXs6pi4', 'target': 'Xs0'})

    # Ξ*-: 8π⁵ + 6π⁴ - π³ - parent: vXs6pi4 (c5=8, c4=6, c3=-1)
    xsm = ALL_PARTICLES['Xi*-']
    corr_xsm = get_correction_display('Xi*-')
    poly_xsm = format_diff(xsm, parent_c5=8, parent_c4=6, parent_c3=-1)
    diff_xsm = poly_xsm + format_correction(corr_xsm, has_poly=bool(poly_xsm))
    nodes.append({
        'id': 'Xs-',
        'label': 'Ξ*⁻',
        'sublabel': diff_xsm,
        'type': 'spin32',
        'formula': format_full_formula(xsm),
        'correction': corr_xsm,
        'mass_me': xsm.mass_base(),
        'actual_mev': xsm.mass_exp,
        'residual_me': get_residual_me(xsm),
        'charge': '-1',
        'spin': '3/2',
        'strangeness': -2
    })
    edges.append({'source': 'vXs6pi4', 'target': 'Xs-'})

    # === 9π⁵ LEVEL (S=-3) ===
    nodes.append({
        'id': 'v9',
        'label': '+π⁵',
        'sublabel': 'S=-3',
        'type': 'virtual',
        'formula': '9π⁵',
        'description': 'Strangeness -3 level (Omega)'
    })
    edges.append({'source': 'v8', 'target': 'v9'})

    # Ω-: 9π⁵ + 6π⁴ - 2π³ - parent: v9 (c5=9)
    om = ALL_PARTICLES['Omega']
    corr_om = get_correction_display('Omega')
    poly_om = format_diff(om, parent_c5=9)
    diff_om = poly_om + format_correction(corr_om, has_poly=bool(poly_om))
    nodes.append({
        'id': 'Om',
        'label': 'Ω⁻',
        'sublabel': diff_om,
        'type': 'spin32',
        'formula': format_full_formula(om),
        'correction': corr_om,
        'mass_me': om.mass_base(),
        'actual_mev': om.mass_exp,
        'residual_me': get_residual_me(om),
        'charge': '-1',
        'spin': '3/2',
        'strangeness': -3
    })
    edges.append({'source': 'v9', 'target': 'Om'})

    return nodes, edges


def generate_charm_baryon_data():
    """Generate nodes and edges for charm baryons."""
    nodes = []
    edges = []

    # === ROOT: 14π⁵ (virtual) ===
    nodes.append({
        'id': 'root14',
        'label': '14π⁵',
        'sublabel': 'C=1',
        'type': 'virtual',
        'formula': '14π⁵',
        'description': 'Charm baryon base (C=1)'
    })

    # === LAMBDA_C (14π⁵ + 2π⁴) - parent: root14 (c5=14) ===
    lc = ALL_PARTICLES['Lc+']
    corr_lc = get_correction_display('Lc+')
    poly_lc = format_diff(lc, parent_c5=14)
    diff_lc = poly_lc + format_correction(corr_lc, has_poly=bool(poly_lc))
    nodes.append({
        'id': 'Lc',
        'label': 'Λc⁺',
        'sublabel': diff_lc if diff_lc else '(base)',
        'type': 'particle',
        'formula': format_full_formula(lc),
        'correction': corr_lc,
        'mass_me': lc.mass_base(),
        'actual_mev': lc.mass_exp,
        'residual_me': get_residual_me(lc),
        'charge': '+1',
        'spin': '1/2',
        'strangeness': 0
    })
    edges.append({'source': 'root14', 'target': 'Lc'})

    # === Sigma_c: share 5π⁴ + π³ ===
    nodes.append({
        'id': 'vSc',
        'label': '+5π⁴+π³',
        'sublabel': 'Σc base',
        'type': 'virtual',
        'formula': '14π⁵ + 5π⁴ + π³',
        'description': 'Sigma_c base'
    })
    edges.append({'source': 'root14', 'target': 'vSc'})

    # Sigma_c particles - parent: vSc (c5=14, c4=5, c3=1)
    for key, sym in [('Sc++', '⁺⁺'), ('Sc+', '⁺'), ('Sc0', '⁰')]:
        s = ALL_PARTICLES[key]
        corr = get_correction_display(key)
        poly = format_diff(s, parent_c5=14, parent_c4=5, parent_c3=1)
        diff = poly + format_correction(corr, has_poly=bool(poly))
        nodes.append({
            'id': f'Sc{sym}',
            'label': f'Σc{sym}',
            'sublabel': diff,
            'type': 'particle',
            'formula': format_full_formula(s),
            'correction': corr,
            'mass_me': s.mass_base(),
            'actual_mev': s.mass_exp,
            'residual_me': get_residual_me(s),
            'charge': sym,
            'spin': '1/2',
            'strangeness': 0
        })
        edges.append({'source': 'vSc', 'target': f'Sc{sym}'})

    # === Sigma_c*: share 6π⁴ + 2π³ ===
    nodes.append({
        'id': 'vScs',
        'label': '+6π⁴+2π³',
        'sublabel': 'Σc* base',
        'type': 'virtual',
        'formula': '14π⁵ + 6π⁴ + 2π³',
        'description': 'Sigma_c* base'
    })
    edges.append({'source': 'root14', 'target': 'vScs'})

    # Sigma_c* particles - parent: vScs (c5=14, c4=6, c3=2)
    for key, sym in [('Sc*++', '⁺⁺'), ('Sc*+', '⁺'), ('Sc*0', '⁰')]:
        s = ALL_PARTICLES[key]
        corr = get_correction_display(key)
        poly = format_diff(s, parent_c5=14, parent_c4=6, parent_c3=2)
        diff = poly + format_correction(corr, has_poly=bool(poly))
        nodes.append({
            'id': f'Scs{sym}',
            'label': f'Σc*{sym}',
            'sublabel': diff,
            'type': 'spin32',
            'formula': format_full_formula(s),
            'correction': corr,
            'mass_me': s.mass_base(),
            'actual_mev': s.mass_exp,
            'residual_me': get_residual_me(s),
            'charge': sym,
            'spin': '3/2',
            'strangeness': 0
        })
        edges.append({'source': 'vScs', 'target': f'Scs{sym}'})

    # === 15π⁵ LEVEL (charm + strange) ===
    nodes.append({
        'id': 'v15',
        'label': '+π⁵',
        'sublabel': 'S=-1',
        'type': 'virtual',
        'formula': '15π⁵',
        'description': 'Charm + strange'
    })
    edges.append({'source': 'root14', 'target': 'v15'})

    # Xi_c: share 2π⁴ + π³
    nodes.append({
        'id': 'vXc',
        'label': '+2π⁴+π³',
        'sublabel': 'Ξc base',
        'type': 'virtual',
        'formula': '15π⁵ + 2π⁴ + π³',
        'description': 'Xi_c base'
    })
    edges.append({'source': 'v15', 'target': 'vXc'})

    # Ξc⁺ - parent: vXc (c5=15, c4=2, c3=1)
    xcp = ALL_PARTICLES['Xc+']
    corr_xcp = get_correction_display('Xc+')
    poly_xcp = format_diff(xcp, parent_c5=15, parent_c4=2, parent_c3=1)
    diff_xcp = poly_xcp + format_correction(corr_xcp, has_poly=bool(poly_xcp))
    nodes.append({
        'id': 'Xc+',
        'label': 'Ξc⁺',
        'sublabel': diff_xcp,
        'type': 'particle',
        'formula': format_full_formula(xcp),
        'correction': corr_xcp,
        'mass_me': xcp.mass_base(),
        'actual_mev': xcp.mass_exp,
        'residual_me': get_residual_me(xcp),
        'charge': '+1',
        'spin': '1/2',
        'strangeness': -1
    })
    edges.append({'source': 'vXc', 'target': 'Xc+'})

    # Ξc⁰ - parent: vXc (c5=15, c4=2, c3=1)
    xc0 = ALL_PARTICLES['Xc0']
    corr_xc0 = get_correction_display('Xc0')
    poly_xc0 = format_diff(xc0, parent_c5=15, parent_c4=2, parent_c3=1)
    diff_xc0 = poly_xc0 + format_correction(corr_xc0, has_poly=bool(poly_xc0))
    nodes.append({
        'id': 'Xc0',
        'label': 'Ξc⁰',
        'sublabel': diff_xc0,
        'type': 'particle',
        'formula': format_full_formula(xc0),
        'correction': corr_xc0,
        'mass_me': xc0.mass_base(),
        'actual_mev': xc0.mass_exp,
        'residual_me': get_residual_me(xc0),
        'charge': '0',
        'spin': '1/2',
        'strangeness': -1
    })
    edges.append({'source': 'vXc', 'target': 'Xc0'})

    # Xi_c*: share 6π⁴
    nodes.append({
        'id': 'vXcs',
        'label': '+6π⁴',
        'sublabel': 'Ξc* base',
        'type': 'virtual',
        'formula': '15π⁵ + 6π⁴',
        'description': 'Xi_c* base'
    })
    edges.append({'source': 'v15', 'target': 'vXcs'})

    # Xi_c* particles - parent: vXcs (c5=15, c4=6)
    for key, sym in [('Xc*+', '⁺'), ('Xc*0', '⁰')]:
        x = ALL_PARTICLES[key]
        corr = get_correction_display(key)
        poly = format_diff(x, parent_c5=15, parent_c4=6)
        diff = poly + format_correction(corr, has_poly=bool(poly))
        nodes.append({
            'id': f'Xcs{sym}',
            'label': f'Ξc*{sym}',
            'sublabel': diff,
            'type': 'spin32',
            'formula': format_full_formula(x),
            'correction': corr,
            'mass_me': x.mass_base(),
            'actual_mev': x.mass_exp,
            'residual_me': get_residual_me(x),
            'charge': sym,
            'spin': '3/2',
            'strangeness': -1
        })
        edges.append({'source': 'vXcs', 'target': f'Xcs{sym}'})

    # === 16π⁵ LEVEL (charm + 2 strange) ===
    nodes.append({
        'id': 'v16',
        'label': '+π⁵',
        'sublabel': 'S=-2',
        'type': 'virtual',
        'formula': '16π⁵',
        'description': 'Charm + double strange'
    })
    edges.append({'source': 'v15', 'target': 'v16'})

    # Omega_c - parent: v16 (c5=16)
    oc = ALL_PARTICLES['Oc0']
    corr_oc = get_correction_display('Oc0')
    poly_oc = format_diff(oc, parent_c5=16)
    diff_oc = poly_oc + format_correction(corr_oc, has_poly=bool(poly_oc))
    nodes.append({
        'id': 'Oc0',
        'label': 'Ωc⁰',
        'sublabel': diff_oc,
        'type': 'particle',
        'formula': format_full_formula(oc),
        'correction': corr_oc,
        'mass_me': oc.mass_base(),
        'actual_mev': oc.mass_exp,
        'residual_me': get_residual_me(oc),
        'charge': '0',
        'spin': '1/2',
        'strangeness': -2
    })
    edges.append({'source': 'v16', 'target': 'Oc0'})

    # Omega_c* - parent: v16 (c5=16)
    ocs = ALL_PARTICLES['Oc*0']
    corr_ocs = get_correction_display('Oc*0')
    poly_ocs = format_diff(ocs, parent_c5=16)
    diff_ocs = poly_ocs + format_correction(corr_ocs, has_poly=bool(poly_ocs))
    nodes.append({
        'id': 'Ocs0',
        'label': 'Ωc*⁰',
        'sublabel': diff_ocs,
        'type': 'spin32',
        'formula': format_full_formula(ocs),
        'correction': corr_ocs,
        'mass_me': ocs.mass_base(),
        'actual_mev': ocs.mass_exp,
        'residual_me': get_residual_me(ocs),
        'charge': '0',
        'spin': '3/2',
        'strangeness': -2
    })
    edges.append({'source': 'v16', 'target': 'Ocs0'})

    # === Double charm (separate branch) - parent: root14 (c5=14) ===
    xcc = ALL_PARTICLES['Xcc++']
    corr_xcc = get_correction_display('Xcc++')
    poly_xcc = format_diff(xcc, parent_c5=14)
    diff_xcc = poly_xcc + format_correction(corr_xcc, has_poly=bool(poly_xcc))
    nodes.append({
        'id': 'Xcc',
        'label': 'Ξcc⁺⁺',
        'sublabel': diff_xcc,
        'type': 'particle',
        'formula': format_full_formula(xcc),
        'correction': corr_xcc,
        'mass_me': xcc.mass_base(),
        'actual_mev': xcc.mass_exp,
        'residual_me': get_residual_me(xcc),
        'charge': '++',
        'spin': '1/2',
        'strangeness': 0
    })
    edges.append({'source': 'root14', 'target': 'Xcc'})

    return nodes, edges


def generate_bottom_baryon_data():
    """Generate nodes and edges for bottom baryons."""
    nodes = []
    edges = []

    # === ROOT: 36π⁵ (virtual) ===
    nodes.append({
        'id': 'root36',
        'label': '36π⁵',
        'sublabel': 'B=-1',
        'type': 'virtual',
        'formula': '36π⁵',
        'description': 'Bottom baryon base (B=-1)'
    })

    # === LAMBDA_B (36π⁵ - 2π²) - parent: root36 (c5=36) ===
    lb = ALL_PARTICLES['Lb0']
    corr_lb = get_correction_display('Lb0')
    poly_lb = format_diff(lb, parent_c5=36)
    diff_lb = poly_lb + format_correction(corr_lb, has_poly=bool(poly_lb))
    nodes.append({
        'id': 'Lb',
        'label': 'Λb⁰',
        'sublabel': diff_lb if diff_lb else '(base)',
        'type': 'particle',
        'formula': format_full_formula(lb),
        'correction': corr_lb,
        'mass_me': lb.mass_base(),
        'actual_mev': lb.mass_exp,
        'residual_me': get_residual_me(lb),
        'charge': '0',
        'spin': '1/2',
        'strangeness': 0
    })
    edges.append({'source': 'root36', 'target': 'Lb'})

    # Sigma_b+ (Tier 1) - parent: root36 (c5=36)
    sbp = ALL_PARTICLES['Sb+']
    corr_sbp = get_correction_display('Sb+')
    poly_sbp = format_diff(sbp, parent_c5=36)
    diff_sbp = poly_sbp + format_correction(corr_sbp, has_poly=bool(poly_sbp))
    nodes.append({
        'id': 'Sb+',
        'label': 'Σb⁺',
        'sublabel': diff_sbp,
        'type': 'particle',
        'formula': format_full_formula(sbp),
        'correction': corr_sbp,
        'mass_me': sbp.mass_base(),
        'actual_mev': sbp.mass_exp,
        'residual_me': get_residual_me(sbp),
        'charge': '+1',
        'spin': '1/2',
        'strangeness': 0
    })
    edges.append({'source': 'root36', 'target': 'Sb+'})

    # Sigma_b- - parent: root36 (c5=36)
    sbm = ALL_PARTICLES['Sb-']
    corr_sbm = get_correction_display('Sb-')
    poly_sbm = format_diff(sbm, parent_c5=36)
    diff_sbm = poly_sbm + format_correction(corr_sbm, has_poly=bool(poly_sbm))
    nodes.append({
        'id': 'Sb-',
        'label': 'Σb⁻',
        'sublabel': diff_sbm,
        'type': 'particle',
        'formula': format_full_formula(sbm),
        'correction': corr_sbm,
        'mass_me': sbm.mass_base(),
        'actual_mev': sbm.mass_exp,
        'residual_me': get_residual_me(sbm),
        'charge': '-1',
        'spin': '1/2',
        'strangeness': 0
    })
    edges.append({'source': 'root36', 'target': 'Sb-'})

    # === 37π⁵ LEVEL (bottom + strange) ===
    nodes.append({
        'id': 'v37',
        'label': '+π⁵',
        'sublabel': 'S=-1',
        'type': 'virtual',
        'formula': '37π⁵',
        'description': 'Bottom + strange'
    })
    edges.append({'source': 'root36', 'target': 'v37'})

    # Xi_b0 - parent: v37 (c5=37)
    xb0 = ALL_PARTICLES['Xb0']
    corr_xb0 = get_correction_display('Xb0')
    poly_xb0 = format_diff(xb0, parent_c5=37)
    diff_xb0 = poly_xb0 + format_correction(corr_xb0, has_poly=bool(poly_xb0))
    nodes.append({
        'id': 'Xb0',
        'label': 'Ξb⁰',
        'sublabel': diff_xb0,
        'type': 'particle',
        'formula': format_full_formula(xb0),
        'correction': corr_xb0,
        'mass_me': xb0.mass_base(),
        'actual_mev': xb0.mass_exp,
        'residual_me': get_residual_me(xb0),
        'charge': '0',
        'spin': '1/2',
        'strangeness': -1
    })
    edges.append({'source': 'v37', 'target': 'Xb0'})

    # Xi_b- - parent: v37 (c5=37)
    xbm = ALL_PARTICLES['Xb-']
    corr_xbm = get_correction_display('Xb-')
    poly_xbm = format_diff(xbm, parent_c5=37)
    diff_xbm = poly_xbm + format_correction(corr_xbm, has_poly=bool(poly_xbm))
    nodes.append({
        'id': 'Xb-',
        'label': 'Ξb⁻',
        'sublabel': diff_xbm,
        'type': 'particle',
        'formula': format_full_formula(xbm),
        'correction': corr_xbm,
        'mass_me': xbm.mass_base(),
        'actual_mev': xbm.mass_exp,
        'residual_me': get_residual_me(xbm),
        'charge': '-1',
        'spin': '1/2',
        'strangeness': -1
    })
    edges.append({'source': 'v37', 'target': 'Xb-'})

    # === 38π⁵ LEVEL (bottom + 2 strange) ===
    nodes.append({
        'id': 'v38',
        'label': '+π⁵',
        'sublabel': 'S=-2',
        'type': 'virtual',
        'formula': '38π⁵',
        'description': 'Bottom + double strange'
    })
    edges.append({'source': 'v37', 'target': 'v38'})

    # Omega_b - parent: v38 (c5=38)
    ob = ALL_PARTICLES['Ob-']
    corr_ob = get_correction_display('Ob-')
    poly_ob = format_diff(ob, parent_c5=38)
    diff_ob = poly_ob + format_correction(corr_ob, has_poly=bool(poly_ob))
    nodes.append({
        'id': 'Ob',
        'label': 'Ωb⁻',
        'sublabel': diff_ob,
        'type': 'particle',
        'formula': format_full_formula(ob),
        'correction': corr_ob,
        'mass_me': ob.mass_base(),
        'actual_mev': ob.mass_exp,
        'residual_me': get_residual_me(ob),
        'charge': '-1',
        'spin': '1/2',
        'strangeness': -2
    })
    edges.append({'source': 'v38', 'target': 'Ob'})

    return nodes, edges


def generate_html():
    """Generate the complete HTML file."""

    light_nodes, light_edges = generate_light_baryon_data()
    charm_nodes, charm_edges = generate_charm_baryon_data()
    bottom_nodes, bottom_edges = generate_bottom_baryon_data()

    light_nodes_json = json.dumps(light_nodes, indent=8)
    light_edges_json = json.dumps(light_edges, indent=8)
    charm_nodes_json = json.dumps(charm_nodes, indent=8)
    charm_edges_json = json.dumps(charm_edges, indent=8)
    bottom_nodes_json = json.dumps(bottom_nodes, indent=8)
    bottom_edges_json = json.dumps(bottom_edges, indent=8)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baryon π-Algebra Tree</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
    <script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
    <script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; }}
        #container {{ display: flex; height: 100vh; }}
        #graph-area {{ flex: 1; display: flex; flex-direction: column; }}
        #main-tabs {{ display: flex; background: #0f0f23; border-bottom: 2px solid #333; }}
        .main-tab {{
            padding: 12px 24px; cursor: pointer; color: #888; font-size: 1em;
            border: none; background: transparent; border-bottom: 3px solid transparent;
        }}
        .main-tab:hover {{ color: #ccc; background: #16213e; }}
        .main-tab.active {{ color: #00d9ff; border-bottom-color: #00d9ff; background: #16213e; }}
        #cy {{ flex: 1; background: #16213e; }}
        #sidebar {{ width: 380px; padding: 20px; background: #0f0f23; overflow-y: auto; border-left: 1px solid #333; }}
        h1 {{ font-size: 1.3em; margin-bottom: 15px; color: #00d9ff; }}
        h2 {{ font-size: 1em; margin: 15px 0 10px 0; color: #ff6b6b; }}
        #info {{
            background: #1a1a2e; padding: 15px; border-radius: 8px;
            font-family: monospace; font-size: 1.1em; line-height: 1.9;
        }}
        .formula {{ color: #00d9ff; font-size: 1.15em; }}
        .value {{ color: #2ecc71; }}
        .label {{ color: #888; }}
        .pos {{ color: #e74c3c; }}
        .neg {{ color: #3498db; }}
        button {{ background: #16213e; color: #eee; border: 1px solid #444; padding: 8px 12px; margin: 3px; cursor: pointer; border-radius: 4px; }}
        button:hover {{ background: #1f4068; border-color: #00d9ff; }}
        .legend {{ margin-top: 20px; font-size: 0.9em; }}
        .legend-item {{ display: flex; align-items: center; margin: 8px 0; }}
        .legend-color {{ width: 20px; height: 20px; border-radius: 4px; margin-right: 10px; border: 2px solid #fff; }}
        #main-tabs {{ display: flex; justify-content: space-between; align-items: center; }}
        .tab-buttons {{ display: flex; }}
        .zoom-controls {{ display: flex; margin-right: 10px; }}
        .zoom-controls button {{ padding: 6px 12px; margin: 0 2px; }}
        #decays {{
            background: #1a1a2e; padding: 15px; border-radius: 8px;
            margin-top: 15px; font-size: 1.05em; line-height: 1.7;
        }}
        .decay-mode {{
            margin: 8px 0; padding: 8px; background: #16213e;
            border-radius: 4px; border-left: 3px solid #444;
        }}
        .decay-mode.strong {{ border-left-color: #e74c3c; }}
        .decay-mode.weak {{ border-left-color: #f39c12; }}
        .decay-mode.em {{ border-left-color: #9b59b6; }}
        .decay-percent {{ float: right; color: #2ecc71; font-weight: bold; }}
        .decay-type {{ font-size: 0.75em; color: #888; margin-top: 4px; }}
    </style>
</head>
<body>
    <div id="container">
        <div id="graph-area">
            <div id="main-tabs">
                <div class="tab-buttons">
                    <button class="main-tab active" onclick="switchTab('light')">Light (6π⁵)</button>
                    <button class="main-tab" onclick="switchTab('charm')">Charm (14π⁵)</button>
                    <button class="main-tab" onclick="switchTab('bottom')">Bottom (36π⁵)</button>
                </div>
                <div class="zoom-controls">
                    <button onclick="cy.zoom(cy.zoom() / 1.2); cy.center()">−</button>
                    <button onclick="cy.fit(50)">Fit</button>
                    <button onclick="cy.zoom(cy.zoom() * 1.2); cy.center()">+</button>
                </div>
            </div>
            <div id="cy"></div>
        </div>
        <div id="sidebar">
            <h1>Baryon π-Algebra Tree</h1>
            <div id="info"><p style="color: #666;">Click a node to see details</p></div>
            <h2>Decays</h2>
            <div id="decays"><p style="color: #666;">Select a particle to see decay modes</p></div>
            <div class="legend">
                <h2>Legend</h2>
                <div class="legend-item"><div class="legend-color" style="background: #3498db;"></div>Spin-1/2</div>
                <div class="legend-item"><div class="legend-color" style="background: #e74c3c;"></div>Spin-3/2</div>
                <div class="legend-item"><div class="legend-color" style="background: #9b59b6; border-style: dashed;"></div>Virtual (shared coeff)</div>
            </div>
            <div class="legend">
                <h2>Decay Types</h2>
                <div class="legend-item"><div class="legend-color" style="background: transparent; border-color: #e74c3c;"></div>Strong (~10⁻²³ s)</div>
                <div class="legend-item"><div class="legend-color" style="background: transparent; border-color: #f39c12;"></div>Weak (~10⁻¹⁰ s)</div>
                <div class="legend-item"><div class="legend-color" style="background: transparent; border-color: #9b59b6;"></div>EM (~10⁻²⁰ s)</div>
            </div>
        </div>
    </div>
    <script>
        const datasets = {{
            light: {{ nodes: {light_nodes_json}, edges: {light_edges_json} }},
            charm: {{ nodes: {charm_nodes_json}, edges: {charm_edges_json} }},
            bottom: {{ nodes: {bottom_nodes_json}, edges: {bottom_edges_json} }}
        }};
        let cy, currentTab = 'light';

        function buildElements(data) {{
            const elements = [];
            data.nodes.forEach(n => {{
                const lbl = (n.type === 'virtual') ? n.label : (n.sublabel ? n.label + '\\n' + n.sublabel : n.label);
                elements.push({{ data: {{ ...n, id: n.id, label: lbl }} }});
            }});
            data.edges.forEach((e, i) => elements.push({{ data: {{ id: 'e'+i, source: e.source, target: e.target }} }}));
            return elements;
        }}

        function initCy(tab) {{
            const elements = buildElements(datasets[tab]);
            cy = cytoscape({{
                container: document.getElementById('cy'),
                elements: elements,
                style: [
                    {{ selector: 'node[type="particle"]', style: {{
                        'label': 'data(label)', 'text-valign': 'center', 'text-halign': 'center',
                        'font-size': '16px', 'font-weight': 'bold', 'color': '#fff',
                        'text-wrap': 'wrap', 'text-max-width': '150px',
                        'shape': 'round-rectangle', 'width': 120, 'height': 55,
                        'background-color': '#3498db', 'border-width': 2, 'border-color': '#fff'
                    }} }},
                    {{ selector: 'node[type="spin32"]', style: {{
                        'label': 'data(label)', 'text-valign': 'center', 'text-halign': 'center',
                        'font-size': '16px', 'font-weight': 'bold', 'color': '#fff',
                        'text-wrap': 'wrap', 'text-max-width': '150px',
                        'shape': 'round-rectangle', 'width': 120, 'height': 55,
                        'background-color': '#e74c3c', 'border-width': 2, 'border-color': '#fff'
                    }} }},
                    {{ selector: 'node[type="virtual"]', style: {{
                        'label': 'data(label)', 'text-valign': 'center', 'text-halign': 'center',
                        'font-size': '16px', 'color': '#fff', 'text-wrap': 'wrap',
                        'shape': 'ellipse', 'width': 70, 'height': 70, 'background-color': '#9b59b6',
                        'border-width': 2, 'border-style': 'dashed', 'border-color': '#fff'
                    }} }},
                    {{ selector: 'edge', style: {{ 'width': 2, 'line-color': '#555', 'target-arrow-color': '#555', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier' }} }},
                    {{ selector: 'node:selected', style: {{ 'border-color': '#00d9ff', 'border-width': 5 }} }}
                ],
                layout: {{ name: 'dagre', rankDir: 'TB', nodeSep: 60, rankSep: 90, padding: 30 }}
            }});
            cy.on('tap', 'node', e => showInfo(e.target.data()));
            cy.on('tap', e => {{ if(e.target === cy) document.getElementById('info').innerHTML = '<p style="color:#666">Click a node</p>'; }});
        }}

        const PI = Math.PI;
        const M_E = 0.51099895;
        const UNCERTAINTIES = {{
            'p': 0.00000029e-3, 'n': 0.00000054e-3,
            'L0': 0.006, 'S+': 0.03, 'S0': 0.03, 'S-': 0.04,
            'Ss+': 0.9, 'Ss0': 0.9, 'Ss-': 0.9,
            'X0': 0.08, 'X-': 0.06, 'Xs0': 0.8, 'Xs-': 0.9, 'Om': 0.21,
            'Lc': 0.14, 'Sc⁺⁺': 0.14, 'Sc⁺': 0.4, 'Sc⁰': 0.14,
            'Scs⁺⁺': 0.4, 'Scs⁺': 0.5, 'Scs⁰': 0.4,
            'Xc+': 0.31, 'Xc0': 0.28, 'Xcs⁺': 0.5, 'Xcs⁰': 0.5,
            'Oc0': 0.21, 'Ocs0': 0.5, 'Xcc': 0.4,
            'Lb': 0.06, 'Sb+': 0.5, 'Sb-': 0.5, 'Xb0': 0.4, 'Xb-': 0.4, 'Ob': 0.22,
            'D': 2.0
        }};

        function evalCorrection(corr) {{
            if (!corr) return 0;
            let s = corr.trim();
            if (s.startsWith('+')) s = s.slice(1);
            // Handle (k/5)e^(-π) format
            if (s.includes('e⁻ᵖⁱ') || s.includes('e^(-π)')) {{
                const expPart = Math.exp(-PI);
                let coeff = s.replace('e⁻ᵖⁱ', '').replace('e^(-π)', '').trim();
                if (coeff.startsWith('(') && coeff.includes('/5)')) {{
                    const num = parseFloat(coeff.replace('(', '').replace('/5)', ''));
                    return (num / 5.0) * expPart;
                }}
                return (parseFloat(coeff) || 1) * expPart;
            }}
            // Handle -π - 1/π pattern (Xi0)
            if (s === '-π - 1/π') return -PI - 1/PI;
            // Handle k/nπ patterns (like 1/5π)
            const fracPiMatch = s.match(/^([+-]?\d*)\/(\d+)π$/);
            if (fracPiMatch) {{
                const num = parseFloat(fracPiMatch[1] || '1');
                const denom = parseFloat(fracPiMatch[2]);
                return num / (denom * PI);
            }}
            if (s.includes('/π')) return parseFloat(s.replace('/π', '')) / PI;
            if (s.includes('/5')) return parseFloat(s.replace('/5', '')) / 5.0;
            return parseFloat(s) || 0;
        }}

        function getSigmaColor(sigma) {{
            if (sigma < 1) return '#2ecc71';      // green
            if (sigma < 2) return '#3498db';      // blue
            if (sigma < 3) return '#f39c12';      // orange
            return '#e74c3c';                      // red
        }}

        function showInfo(d) {{
            if (d.type === 'virtual') {{
                document.getElementById('info').innerHTML = `
                    <div><span class="label">Level:</span> <span class="formula">${{d.formula}}</span></div>
                    <div style="margin-top:8px">${{d.description || ''}}</div>`;
            }} else {{
                const fullFormula = d.correction ? d.formula + ' ' + d.correction : d.formula;
                const corrVal = evalCorrection(d.correction);
                const calcMe = (d.mass_me || 0) + corrVal;
                const calcMev = calcMe * M_E;
                const expMev = d.actual_mev || 0;
                const errorMev = calcMev - expMev;
                const errorKev = errorMev * 1000;
                const unc = UNCERTAINTIES[d.id] || 1.0;
                const sigma = Math.abs(errorMev) / unc;
                const sigmaColor = getSigmaColor(sigma);
                const sigmaText = sigma < 100 ? sigma.toFixed(2) + 'σ' : '>100σ';
                const errorSign = errorMev >= 0 ? '+' : '';

                document.getElementById('info').innerHTML = `
                    <div style="font-size:1.8em; margin-bottom:5px; color:#fff">${{d.label.split('\\n')[0]}}</div>
                    <div style="font-size:1.3em; margin-bottom:12px"><span class="formula">${{fullFormula}}</span></div>
                    <div><span class="label">Charge:</span> ${{d.charge}}</div>
                    <div><span class="label">Spin:</span> ${{d.spin}}</div>
                    <div><span class="label">Strangeness:</span> ${{d.strangeness !== undefined ? d.strangeness : 'N/A'}}</div>
                    <hr style="border-color:#333; margin:12px 0">
                    <div><span class="label">Calculated:</span> <span class="value">${{calcMev.toFixed(4)}} MeV</span></div>
                    <div><span class="label">Experimental:</span> <span class="value">${{expMev.toFixed(4)}} MeV</span></div>
                    <div><span class="label">Uncertainty:</span> <span class="value">±${{unc < 0.001 ? (unc*1e6).toFixed(2) + ' eV' : unc < 1 ? (unc*1000).toFixed(1) + ' keV' : unc.toFixed(2) + ' MeV'}}</span></div>
                    <hr style="border-color:#333; margin:12px 0">
                    <div><span class="label">Error:</span> <span style="color:${{sigmaColor}}">${{errorSign}}${{Math.abs(errorKev) < 1 ? (errorMev*1e6).toFixed(1) + ' eV' : errorKev.toFixed(2) + ' keV'}}</span></div>
                    <div><span class="label">Deviation:</span> <span style="color:${{sigmaColor}}; font-weight:bold">${{sigmaText}}</span></div>`;

                updateDecays(d.id);
            }}
        }}

        function switchTab(tab) {{
            currentTab = tab;
            document.querySelectorAll('.main-tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            cy.destroy();
            initCy(tab);
            document.getElementById('info').innerHTML = '<p style="color:#666">Click a node</p>';
            document.getElementById('decays').innerHTML = '<p style="color:#666">Select a particle to see decay modes</p>';
        }}

        // Decay database
        const decayData = {{
            'p': {{ stable: true, lifetime: '> 10³⁴ years' }},
            'n': {{
                lifetime: '~879 s (15 min)',
                note: 'Longest weak decay! Tiny Q-value (782 keV).',
                modes: [
                    {{ products: 'p + e⁻ + ν̄ₑ', percent: 100, type: 'weak' }}
                ]
            }},
            'D': {{
                lifetime: '~5×10⁻²⁴ s',
                note: 'Resonance, decays via strong force',
                modes: [
                    {{ products: 'N + π', percent: 99.4, type: 'strong' }},
                    {{ products: 'N + γ', percent: 0.6, type: 'em' }}
                ]
            }},
            'L0': {{
                lifetime: '2.6×10⁻¹⁰ s',
                modes: [
                    {{ products: 'p + π⁻', percent: 63.9, type: 'weak' }},
                    {{ products: 'n + π⁰', percent: 35.8, type: 'weak' }}
                ]
            }},
            'S+': {{
                lifetime: '0.80×10⁻¹⁰ s',
                modes: [
                    {{ products: 'p + π⁰', percent: 51.6, type: 'weak' }},
                    {{ products: 'n + π⁺', percent: 48.3, type: 'weak' }}
                ]
            }},
            'S0': {{
                lifetime: '7.4×10⁻²⁰ s',
                note: 'EM decay! Only ground-state baryon.',
                modes: [
                    {{ products: 'Λ + γ', percent: 100, type: 'em' }}
                ]
            }},
            'S-': {{
                lifetime: '1.48×10⁻¹⁰ s',
                modes: [
                    {{ products: 'n + π⁻', percent: 99.8, type: 'weak' }}
                ]
            }},
            'Ss+': {{
                lifetime: '~1.7×10⁻²³ s',
                modes: [
                    {{ products: 'Λ + π⁺', percent: 87, type: 'strong' }},
                    {{ products: 'Σ + π', percent: 12, type: 'strong' }}
                ]
            }},
            'Ss0': {{
                lifetime: '~1.7×10⁻²³ s',
                modes: [
                    {{ products: 'Λ + π⁰', percent: 87, type: 'strong' }},
                    {{ products: 'Σ + π', percent: 12, type: 'strong' }}
                ]
            }},
            'Ss-': {{
                lifetime: '~1.7×10⁻²³ s',
                modes: [
                    {{ products: 'Λ + π⁻', percent: 87, type: 'strong' }},
                    {{ products: 'Σ + π', percent: 12, type: 'strong' }}
                ]
            }},
            'X0': {{
                lifetime: '2.9×10⁻¹⁰ s',
                modes: [
                    {{ products: 'Λ + π⁰', percent: 99.5, type: 'weak' }}
                ]
            }},
            'X-': {{
                lifetime: '1.6×10⁻¹⁰ s',
                modes: [
                    {{ products: 'Λ + π⁻', percent: 99.9, type: 'weak' }}
                ]
            }},
            'Xs0': {{
                lifetime: '~7×10⁻²³ s',
                modes: [
                    {{ products: 'Ξ + π', percent: 100, type: 'strong' }}
                ]
            }},
            'Xs-': {{
                lifetime: '~7×10⁻²³ s',
                modes: [
                    {{ products: 'Ξ + π', percent: 100, type: 'strong' }}
                ]
            }},
            'Om': {{
                lifetime: '0.82×10⁻¹⁰ s',
                note: 'Spin-3/2 but NO strong decay!',
                modes: [
                    {{ products: 'Λ + K⁻', percent: 67.8, type: 'weak' }},
                    {{ products: 'Ξ⁰ + π⁻', percent: 23.6, type: 'weak' }},
                    {{ products: 'Ξ⁻ + π⁰', percent: 8.6, type: 'weak' }}
                ]
            }},
            'Lc': {{
                lifetime: '2.0×10⁻¹³ s',
                modes: [
                    {{ products: 'Λ + π⁺ + ...', percent: 35, type: 'weak' }},
                    {{ products: 'pK̄⁰', percent: 3.2, type: 'weak' }}
                ]
            }},
            'Lb': {{
                lifetime: '1.5×10⁻¹² s',
                modes: [
                    {{ products: 'Λc⁺ + ...', percent: 60, type: 'weak' }},
                    {{ products: 'p + ...', percent: 30, type: 'weak' }}
                ]
            }}
        }};

        function updateDecays(id) {{
            const decay = decayData[id];
            let html = '';

            if (!decay) {{
                html = '<p style="color: #666;">No decay data for this particle</p>';
            }} else if (decay.stable) {{
                html = `<div style="color: #2ecc71; font-size: 1.1em;">STABLE</div>
                        <div style="color: #888; margin-top: 5px;">τ ${{decay.lifetime}}</div>`;
            }} else {{
                html = `<div style="color: #888; margin-bottom: 10px;">τ = ${{decay.lifetime}}</div>`;
                if (decay.note) {{
                    html += `<div style="color: #f39c12; margin-bottom: 10px; font-size: 0.9em;">${{decay.note}}</div>`;
                }}
                decay.modes.forEach(m => {{
                    const percent = typeof m.percent === 'number' ? m.percent.toFixed(1) + '%' : m.percent;
                    html += `
                        <div class="decay-mode ${{m.type}}">
                            <span class="decay-percent">${{percent}}</span>
                            ${{m.products}}
                        </div>
                    `;
                }});
            }}

            document.getElementById('decays').innerHTML = html;
        }}

        initCy('light');
    </script>
</body>
</html>'''
    return html


if __name__ == '__main__':
    html = generate_html()
    with open('baryon_tree.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated baryon_tree.html")
