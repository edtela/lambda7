#!/usr/bin/env python3
"""
Lambda7 Cycle Data

Declarative structure for baryon family trees.
Virtual nodes group particles by shared polynomial coefficients.
Resonances are linked via virtual_node field.
"""

# =============================================================================
# LIGHT BARYON CYCLE (S=0 to S=-3)
# =============================================================================

LIGHT_CYCLE = {
    'name': 'Light Baryons',
    'root': 'root6',

    'nodes': {
        # === S=0 Level (6π⁵) ===
        'root6': {
            'label': '6π⁵',
            'sublabel': 'S=0',
            'formula': '6π⁵',
            'c5': 6,
            'strangeness': 0,
            'description': 'Light baryon base (S=0)',
            'parent': None,
            'particles': ['proton', 'neutron'],
            'resonances': [],
        },

        'vD6pi4': {
            'label': '+6π⁴',
            'sublabel': 'Δ base',
            'formula': '6π⁵ + 6π⁴',
            'c5': 6, 'c4': 6,
            'strangeness': 0,
            'description': 'Delta decuplet base (6π⁴)',
            'parent': 'root6',
            'particles': ['Delta'],
            'resonances': ['Delta_1700'],  # 9π⁵+6π⁴ mirrors this
        },

        # === S=-1 Level (7π⁵) ===
        'v7': {
            'label': '+π⁵',
            'sublabel': 'S=-1',
            'formula': '7π⁵',
            'c5': 7,
            'strangeness': -1,
            'description': 'Strangeness -1 level',
            'parent': 'root6',
            'particles': ['Lambda'],
            'resonances': ['Lambda_1405'],  # λ-type mirror
        },

        'vS6pi3': {
            'label': '+6π³',
            'sublabel': 'Σ base',
            'formula': '7π⁵ + 6π³',
            'c5': 7, 'c3': 6,
            'strangeness': -1,
            'description': 'Sigma octet base (6π³)',
            'parent': 'v7',
            'particles': ['Sigma_plus', 'Sigma_zero', 'Sigma_minus'],
            'resonances': ['Roper'],  # σ-type mirror (N not Σ, but mirrors Σ structure)
        },

        'vSs6pi4': {
            'label': '+6π⁴',
            'sublabel': 'Σ* base',
            'formula': '7π⁵ + 6π⁴',
            'c5': 7, 'c4': 6,
            'strangeness': -1,
            'description': 'Sigma* decuplet base (6π⁴)',
            'parent': 'v7',
            'particles': ['Sigma_star_plus', 'Sigma_star_zero', 'Sigma_star_minus'],
            'resonances': ['N_1535'],  # η-type mirror
        },

        # === S=-2 Level (8π⁵) ===
        'v8': {
            'label': '+π⁵',
            'sublabel': 'S=-2',
            'formula': '8π⁵',
            'c5': 8,
            'strangeness': -2,
            'description': 'Strangeness -2 level (Xi)',
            'parent': 'v7',
            'particles': [],
            'resonances': [],
        },

        'vXpi4pi3': {
            'label': '+π⁴+π³',
            'sublabel': 'Ξ base',
            'formula': '8π⁵ + π⁴ + π³',
            'c5': 8, 'c4': 1, 'c3': 1,
            'strangeness': -2,
            'description': 'Xi octet base',
            'parent': 'v8',
            'particles': ['Xi_zero', 'Xi_minus'],
            'resonances': [],
        },

        'vXs6pi4': {
            'label': '+6π⁴-π³',
            'sublabel': 'Ξ* base',
            'formula': '8π⁵ + 6π⁴ - π³',
            'c5': 8, 'c4': 6, 'c3': -1,
            'strangeness': -2,
            'description': 'Xi* decuplet base',
            'parent': 'v8',
            'particles': ['Xi_star_zero', 'Xi_star_minus'],
            'resonances': ['Lambda_1520'],  # η'-type mirror
        },

        # === S=-3 Level (9π⁵) ===
        'v9': {
            'label': '+π⁵',
            'sublabel': 'S=-3',
            'formula': '9π⁵',
            'c5': 9,
            'strangeness': -3,
            'description': 'Strangeness -3 level (Omega)',
            'parent': 'v8',
            'particles': [],
            'resonances': [],
        },

        'vOm6pi4': {
            'label': '+6π⁴-2π³',
            'sublabel': 'Ω base',
            'formula': '9π⁵ + 6π⁴ - 2π³',
            'c5': 9, 'c4': 6, 'c3': -2,
            'strangeness': -3,
            'description': 'Omega decuplet apex',
            'parent': 'v9',
            'particles': ['Omega'],
            'resonances': ['N_1680', 'Delta_1700'],  # 9π⁵+6π⁴ family
        },
    },

    # Edge list (can be derived from parent field, but explicit for clarity)
    'edges': [
        ('root6', 'vD6pi4'),
        ('root6', 'v7'),
        ('v7', 'vS6pi3'),
        ('v7', 'vSs6pi4'),
        ('v7', 'v8'),
        ('v8', 'vXpi4pi3'),
        ('v8', 'vXs6pi4'),
        ('v8', 'v9'),
        ('v9', 'vOm6pi4'),
    ],
}


# =============================================================================
# CHARM BARYON CYCLE (14π⁵ base)
# =============================================================================

CHARM_CYCLE = {
    'name': 'Charm Baryons',
    'root': 'root14',

    'nodes': {
        'root14': {
            'label': '14π⁵',
            'sublabel': 'C=1',
            'formula': '14π⁵',
            'c5': 14,
            'strangeness': 0,
            'description': 'Charm baryon base (14 = [3]π)',
            'parent': None,
            'particles': ['Lambda_c'],
            'resonances': [],
        },

        'vSc': {
            'label': '+5π⁴+π³',
            'sublabel': 'Σc base',
            'formula': '14π⁵ + 5π⁴ + π³',
            'c5': 14, 'c4': 5, 'c3': 1,
            'strangeness': 0,
            'description': 'Sigma_c octet base',
            'parent': 'root14',
            'particles': ['Sigma_c_pp', 'Sigma_c_plus', 'Sigma_c_zero'],
            'resonances': [],
        },

        'vScs': {
            'label': '+6π⁴+2π³',
            'sublabel': 'Σc* base',
            'formula': '14π⁵ + 6π⁴ + 2π³',
            'c5': 14, 'c4': 6, 'c3': 2,
            'strangeness': 0,
            'description': 'Sigma_c* decuplet base (6π⁴)',
            'parent': 'root14',
            'particles': ['Sigma_c_star_pp', 'Sigma_c_star_plus', 'Sigma_c_star_zero'],
            'resonances': [],
        },

        'v15': {
            'label': '+π⁵',
            'sublabel': 'S=-1',
            'formula': '15π⁵',
            'c5': 15,
            'strangeness': -1,
            'description': 'Charm-strange level',
            'parent': 'root14',
            'particles': [],
            'resonances': [],
        },

        'vXc': {
            'label': '+2π⁴+π³',
            'sublabel': 'Ξc base',
            'formula': '15π⁵ + 2π⁴ + π³',
            'c5': 15, 'c4': 2, 'c3': 1,
            'strangeness': -1,
            'description': 'Xi_c octet base',
            'parent': 'v15',
            'particles': ['Xi_c_plus', 'Xi_c_zero'],
            'resonances': [],
        },

        'vXcs': {
            'label': '+6π⁴',
            'sublabel': 'Ξc* base',
            'formula': '15π⁵ + 6π⁴',
            'c5': 15, 'c4': 6,
            'strangeness': -1,
            'description': 'Xi_c* decuplet base (6π⁴)',
            'parent': 'v15',
            'particles': ['Xi_c_star_plus', 'Xi_c_star_zero'],
            'resonances': [],
        },

        'v16': {
            'label': '+π⁵',
            'sublabel': 'S=-2',
            'formula': '16π⁵',
            'c5': 16,
            'strangeness': -2,
            'description': 'Double-strange charm level',
            'parent': 'v15',
            'particles': ['Omega_c', 'Omega_c_star'],
            'resonances': [],
        },
    },

    'edges': [
        ('root14', 'vSc'),
        ('root14', 'vScs'),
        ('root14', 'v15'),
        ('v15', 'vXc'),
        ('v15', 'vXcs'),
        ('v15', 'v16'),
    ],
}


# =============================================================================
# BOTTOM BARYON CYCLE (36π⁵ base)
# =============================================================================

BOTTOM_CYCLE = {
    'name': 'Bottom Baryons',
    'root': 'root36',

    'nodes': {
        'root36': {
            'label': '36π⁵',
            'sublabel': 'B=-1',
            'formula': '36π⁵',
            'c5': 36,
            'strangeness': 0,
            'description': 'Bottom baryon base (36 = 6²)',
            'parent': None,
            'particles': ['Lambda_b', 'Sigma_b_plus', 'Sigma_b_minus'],
            'resonances': [],
        },

        'v37': {
            'label': '+π⁵',
            'sublabel': 'S=-1',
            'formula': '37π⁵',
            'c5': 37,
            'strangeness': -1,
            'description': 'Bottom-strange level',
            'parent': 'root36',
            'particles': ['Xi_b_zero', 'Xi_b_minus'],
            'resonances': [],
        },

        'v38': {
            'label': '+π⁵',
            'sublabel': 'S=-2',
            'formula': '38π⁵',
            'c5': 38,
            'strangeness': -2,
            'description': 'Double-strange bottom level',
            'parent': 'v37',
            'particles': ['Omega_b'],
            'resonances': [],
        },
    },

    'edges': [
        ('root36', 'v37'),
        ('v37', 'v38'),
    ],
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_cycles():
    """Return all cycles."""
    return [LIGHT_CYCLE, CHARM_CYCLE, BOTTOM_CYCLE]


def get_node(cycle, node_id):
    """Get a node by ID from a cycle."""
    return cycle['nodes'].get(node_id)


def get_particles_for_node(cycle, node_id):
    """Get particle keys for a node."""
    node = get_node(cycle, node_id)
    return node.get('particles', []) if node else []


def get_resonances_for_node(cycle, node_id):
    """Get resonance keys for a node."""
    node = get_node(cycle, node_id)
    return node.get('resonances', []) if node else []


def get_children(cycle, node_id):
    """Get child node IDs for a given node."""
    children = []
    for nid, node in cycle['nodes'].items():
        if node.get('parent') == node_id:
            children.append(nid)
    return children


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Lambda7 Cycle Data")
    print("=" * 60)

    for cycle in get_all_cycles():
        print(f"\n{cycle['name']}:")
        print("-" * 40)
        for node_id, node in cycle['nodes'].items():
            particles = node.get('particles', [])
            resonances = node.get('resonances', [])
            print(f"  {node_id:12} {node['formula']:20} P:{len(particles)} R:{len(resonances)}")
