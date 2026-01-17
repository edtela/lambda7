# λ7 — Lambda7

**Particle masses as polynomials in π**

## The Proton Mass

```
m_p = 6π⁵ + (4/5)e^(-π)
```

| Term | Calculation | Value |
|------|-------------|-------|
| 6π⁵ | 6 × 306.0197 | 1836.1181 mₑ |
| (4/5)e^(-π) | 0.8 × 0.0432 | 0.0346 mₑ |
| **Total** | | **1836.1527 mₑ** |
| In MeV | × 0.511 MeV | **938.2721 MeV** |
| Experimental | | 938.2720888 MeV |
| **Error** | | **3 eV** |

## Key Results

All 18 ground-state baryons have π-polynomial formulas with sub-5 keV accuracy:

| Particle | Formula | Error |
|----------|---------|-------|
| p | 6π⁵ + (4/5)e^(-π) | 3 eV |
| Σ*⁰ | 7π⁵ + 6π⁴ - 2π² + (1/5)(8 - π + e^(-π)) | 52 eV |
| Ω⁻ | 9π⁵ + 6π⁴ - 2π³ + (6/5)(e^(-π) - π) | 0.97 keV |
| Δ | 6π⁵ + 6π⁴ - π² + (1/5)(π - 2 + 4e^(-π)) | 1.06 keV |

## The Structure

Baryon masses follow:

```
m = c₅π⁵ + c₄π⁴ + c₃π³ + c₂π² + correction
```

Where:
- **c₅ = 6 + |S|** — strangeness determines the leading coefficient
- **c₄ = 6** for decuplet (spin-3/2), **c₄ = 0** for octet (spin-1/2)
- **Corrections** use e^(-π) (Lorentz) and q-calculus terms

## The Baryon Cycle

```
9π⁵  Ω⁻      S=-3   Q=-1 only         4×5 family
  ↓
8π⁵  Ξ       S=-2   Q=0,-1            4×5 family
  ↓
7π⁵  Λ,Σ     S=-1   Q=+1,0,-1         Transition
  ↓
6π⁵  N,Δ     S=0    Q=+2,+1,0,-1      2×3 family
```

The proton and omega cross-reference each other's magnetic moment families in their Lorentz corrections.

## Build

```bash
python build.py
open dist/index.html
```

Requires: Python 3, Jinja2 (`pip install jinja2`)

## License

MIT
