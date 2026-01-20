# Key Mathematical Identities

## Strangeness-Mass Coefficient Pattern

```
c5 = 6 + |S|

Nucleons (S=0):      c5 = 6
Sigma/Lambda (S=-1): c5 = 7
Xi (S=-2):           c5 = 8
Omega (S=-3):        c5 = 9
```

## Core Particle Formulas

### Mesons
```
pi0 = pi^5 - pi^3 - pi^2 - 1
    = pi^3(pi^2 - 1) - (pi^2 + 1)
```

### Octet Baryons (J=1/2)
```
p   = 6pi^5 + (4/5)e^(-pi)
n   = 6pi^5 + 8/pi

Lam = 7pi^5 + pi^3 + pi^2 + 1/pi
Sig+= 7pi^5 + 6pi^3 - 2/pi
Sig0= 7pi^5 + 6pi^3 + pi^2 - 4

Xi0 = 8pi^5 + pi^4 + pi^3 - pi - 1/pi
    = 8pi^5 + pi^4 + pi^3 - (pi^2 + 1)/pi
Xi- = 8pi^5 + pi^4 + pi^3 + pi^2 + 1/(5pi)
```

### Decuplet Baryons (J=3/2)
```
Sig*0 = 7pi^5 + 6pi^4 - 2pi^2 + 1
Xi*0  = 8pi^5 + 6pi^4 - pi^3 - (5pi+4)/5
```

## Decay Mass Differences

### Sigma to Lambda
```
Sig0 - Lam = 5pi^3 - 4 - 1/pi
           = 150.71 m_e = 77.01 MeV

Sig*0 - Lam = 6pi^4 - pi^3 - 3pi^2 + 1 - 1/pi
            = 524.52 m_e = 268.03 MeV
```

### Xi to Lambda
```
Xi0 - Lam = pi^5 + pi^4 - pi^2 - pi - 2/pi
          = pi(pi^2 - 1)[3]_pi - 2/pi
```

## Key Ratios

```
pi0 / (Sig0 - Lam)   = 1.7526  ~  7/4   (0.26% dev)
(Sig*0 - Lam) / pi0  = 1.9857  ~  2     (0.7% dev)
(Sig*0 - Lam)/(Sig0 - Lam) = 3.48 ~ 7/2
(Xi0 - Lam) / pi0    = 1.48   ~  3/2   (2.4% dev)
```

## Quadratic Forms

The factors `(pi^2 - 1)` and `(pi^2 + 1)` appear throughout:

```
pi0 = pi^3(pi^2 - 1) - (pi^2 + 1)

Xi0 correction: -(pi^2 + 1)/pi

Sig*0 - Lam = pi^2(6pi^2 - pi - 3) + (pi-1)/pi
  where: 6pi^2 - pi - 3 = 6(pi^2 - 1) - (pi - 3)

Xi0 - Lam contains: (pi^2 - 1) * [3]_pi
```

### Fine Structure Connection
```
pi^2(pi^2 + 4) = 136.89 ~ 1/alpha = 137
```

## q-Integers

```
[2]_pi = pi + 1     ~ 4.14
[3]_pi = pi^2 + pi + 1 ~ 14.01
```

The charm coefficient (14) equals `[3]_pi`.

## Three Correction Levels

### Level 1: Geometric (pi^n)
Powers of pi in the polynomial base.

### Level 2: Logarithmic (1/pi)
```
d/d(pi)[ln(pi)] = 1/pi

Transformation: pi^2 --L--> ln(pi) --d/dpi--> 1/pi
Coefficient preserved: -2pi^2 --> -2/pi
```

### Level 3: Exponential (e^(-pi))
```
e^(-pi) = 0.0432...
```

### Correction Types
```
e^(-pi) corrections:     1/pi corrections:
  p:  +(4/5)e^(-pi)        n:  +8/pi
  pi+: +6e^(-pi)           Lam: +1/pi
  mu:  -20e^(-pi)          Sig+: -2/pi
                           Xi0: -(pi^2+1)/pi
                           Xi-: +1/(5pi)
```

## Proton-Neutron Mass Difference

```
n - p = 8/pi - (4/5)e^(-pi)
      = 2.546 - 0.035
      = 2.51 m_e = 1.28 MeV

Experimental: 1.293 MeV
```

## Dimensional Transformations

### Muon-Pion Relationship
```
Muon base: pi^5 - pi^4 = pi^4(pi - 1)
Pion base: pi^5 - pi^3 = pi^3(pi^2 - 1)
Difference: pi^4 - pi^3 = pi^3(pi - 1)
```

### Sigma Family Mirror
```
Sig*0: 6pi^4 (muon-like)  -->  Sig0: 6pi^3 (pion-like)
```

The coefficient 6 migrates from pi^4 to pi^3 in decuplet-to-octet decay.

## Xi vs Sigma Structure

```
Sigma octet: 6pi^3 term (pion-like)
Xi octet:    pi^4 term (muon-like)
```

Xi octet sits one level higher on the dimensional ladder.
