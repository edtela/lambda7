# Lambda7 Project Index

**π-algebra: Particle masses as polynomials in π**

## Overview

Lambda7 expresses particle masses as polynomials in π with Lorentz corrections. The proton mass formula `m_p = 6π⁵ + (4/5)e^(-π)` matches experiment to 3 eV.

---

## Project Structure

```
lambda7/
├── build.py              # Jinja2 build system
├── data/
│   ├── baryons.py        # 18 baryons + charm + bottom data
│   ├── mesons.py         # 17 mesons + muon data
│   └── magnetic.py       # 8 magnetic moment formulas
├── templates/
│   ├── base.html         # Base template with nav
│   ├── index.html        # Home page with derivative framework
│   ├── formulas.html     # All baryon formulas (octet + decuplet)
│   ├── baryon_cycle.html # Strange baryon cycle (6→7→8→9)
│   ├── charm_cycle.html  # Charm baryons (c₅ = 14 = [3]_π)
│   ├── bottom_cycle.html # Bottom baryons (c₅ = 36 = 6²)
│   ├── mesons.html       # Mesons & muon formulas
│   ├── magnetic.html     # Magnetic moments as π-fractions
│   ├── framework.html    # Mathematical framework overview
│   ├── lorentz.html      # e^(-π) derivation (quantum tax)
│   ├── q_calculus.html   # q-integers with q = π
│   └── seven.html        # Why 7 = ⌈2π⌉ = ⌊π!⌋
├── docs/
│   └── pi_space_motivation.md  # Deep motivation document
├── static/
│   └── style.css         # Styling
├── README.md             # Project overview
└── TODO.md               # Task tracking
```

---

## Key Formulas

### Nucleons (Derivative Framework)
| Particle | Source | Derivative | Correction |
|----------|--------|------------|------------|
| Proton | π⁶ | 6π⁵ | +(4/5)e^(-π) |
| Neutron | π⁶ + 8ln(π) | 6π⁵ + 8/π | built-in |
| Omega | (3/2)π⁶ | 9π⁵ | +(6/5)e^(-π) |

### Baryon Pattern
```
m = c₅π⁵ + c₄π⁴ + c₃π³ + c₂π² + correction
```
- **c₅ = 6 + |S|** (strangeness rule)
- **c₄ = 6** for decuplet, **c₄ = 0** for octet

### Magnetic Moments
- **Q > 0**: μ = Nπ/9 (proton: 8π/9)
- **Q ≤ 0**: μ = N/π^k (neutron: -6/π)

---

## Mathematical Framework

### 1. The Lorentz Correction (lorentz.html)
- Discrete sum: `8π × e^π` (quantum)
- Continuous integral: `16π sinh(π)` (classical)
- Difference: `8π × e^(-π)` = **quantum tax**

### 2. q-Calculus (q_calculus.html)
- `[n]_π = (π^n - 1)/(π - 1)`
- `[2]_π = π + 1 ≈ 4.14` → strange quarks
- `[3]_π = π² + π + 1 ≈ 14.01` → charm coefficient

### 3. The Seven Connection (seven.html)
- `⌈2π⌉ = 7` (ceiling)
- `⌊π!⌋ = 7` (π-factorial)
- `⌊π² + π - 6⌋ = 7` (quadratic)

### 4. Floor/Ceiling Quantization
| Expression | Value | Floor | Ceiling | Meaning |
|------------|-------|-------|---------|---------|
| 2π | 6.28 | 6 | 7 | Proton vs strange |
| π + 1 | 4.14 | 4 | 5 | Magnetic moments |
| π² | 9.87 | 9 | 10 | Omega coefficient |

---

## Deep Motivation (docs/pi_space_motivation.md)

### The Singularity Seed
- Start with 3D sphere: `V = (4/3)πr³`
- Take derivatives down to singularity
- At n=0: only **8π** remains (Einstein's constant)

### π as Variable
- At singularity, π is both constant and variable
- `π × r^n` where r = π gives π^(n+1)
- Proton = d/dπ[π⁶] = 6π⁵ = "surface of 6D π-sphere"

### Neutron in ln(π) Space
- Source: π⁶ + 8ln(π)
- Derivative: 6π⁵ + 8/π
- Coefficient 8 = (4/5) × 10 = (4/5) × ⌈π²⌉

---

## Data Files

### baryons.py
- `Particle` dataclass with c5, c4, c3, c2 coefficients
- 8 octet baryons (p, n, Λ, Σ±⁰, Ξ⁰⁻)
- 10 decuplet baryons (Δ, Σ*, Ξ*, Ω)
- 13 charm baryons (Λc, Σc, Ξc, Ωc)
- 6 bottom baryons (Λb, Σb, Ξb, Ωb)
- 1 double-charm (Ξcc)

### mesons.py
- `Meson` dataclass with c5, c4, c3, c2, c1, c0 coefficients
- Light: π±, π⁰, ρ, ω
- Strange: K±, K⁰, η, η', φ
- Charm: D±, D⁰, Ds, J/ψ
- Bottom: B±, B⁰, Bs, Υ
- Lepton: muon

### magnetic.py
- `MagneticMoment` dataclass with numerator, pi_power, denominator
- 8 baryons: p, n, Λ, Σ±, Ξ⁰⁻, Ω⁻

---

## Key Numbers

| Value | Expression | Appears in |
|-------|------------|------------|
| 4 | ⌊π + 1⌋ | Proton correction 4/5 |
| 5 | ⌈π + 1⌉ | Denominator in corrections |
| 6 | ⌊2π⌋ | Proton coefficient, neutron μ |
| 7 | ⌈2π⌉ | Strange baryon coefficient |
| 8 | ⌊2π⌋ + 2 | Proton μ numerator, neutron 8/π |
| 9 | ⌊π²⌋ | Omega c₅, denominator for Q>0 μ |
| 10 | ⌈π²⌉ | Hidden in neutron 8 = (4/5)×10 |
| 14 | [3]_π | Charm coefficient |
| 20 | 4×5 | Muon correction, Ω⁻ μ |
| 36 | 6² | Bottom c₅, Σ⁻ μ |

---

## Build & Run

```bash
pip install jinja2
python build.py
open dist/index.html
```

Watch mode: `python build.py --watch`

---

## Status

### Completed
- [x] All 18 ground-state strange baryons
- [x] 13 charm baryons
- [x] 6 bottom baryons
- [x] 1 double-charm baryon
- [x] 17 mesons + muon
- [x] 8 magnetic moments
- [x] Framework pages (Lorentz, q-calculus, Seven)
- [x] Derivative framework (proton/neutron/omega sources)
- [x] Data-driven templates

### Not Yet on Site
- [ ] pi_space_motivation.md content (deep motivation)
- [ ] Fine structure constant: 1/α = π²(π² + 4) ≈ 136.888
- [ ] Angular structure: θ = c₅ × π/5
- [ ] Charge radius predictions
- [ ] Decay path visualizations
