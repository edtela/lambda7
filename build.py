#!/usr/bin/env python3
"""
Lambda7 Build System

Renders Jinja2 templates with particle data to static HTML.

Usage:
    python build.py          # Build all pages
    python build.py --watch  # Watch for changes and rebuild
"""

import os
import sys
import shutil
from pathlib import Path

# Add data directory to path
sys.path.insert(0, str(Path(__file__).parent / 'data'))

from jinja2 import Environment, FileSystemLoader
from baryons import (
    PARTICLES, BARYON_CYCLE, get_octet, get_decuplet,
    CHARM_PARTICLES, CHARM_CYCLE, get_charm_octet, get_charm_decuplet,
    DOUBLE_CHARM_PARTICLES, get_double_charm,
    BOTTOM_PARTICLES, BOTTOM_CYCLE, get_bottom
)

# Paths
ROOT = Path(__file__).parent
TEMPLATES = ROOT / 'templates'
STATIC = ROOT / 'static'
DIST = ROOT / 'dist'


def build():
    """Build all HTML pages."""
    print("Building lambda7...")

    # Create dist directory
    DIST.mkdir(exist_ok=True)

    # Copy static files
    static_dist = DIST / 'static'
    if static_dist.exists():
        shutil.rmtree(static_dist)
    shutil.copytree(STATIC, static_dist)
    print(f"  Copied static files")

    # Set up Jinja2
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=True
    )

    # Common context for all templates
    context = {
        'particles': PARTICLES,
        'octet': get_octet(),
        'decuplet': get_decuplet(),
        'cycle': BARYON_CYCLE,
        # Charm baryon data
        'charm_particles': CHARM_PARTICLES,
        'charm_octet': get_charm_octet(),
        'charm_decuplet': get_charm_decuplet(),
        'charm_cycle': CHARM_CYCLE,
        # Double-charm baryon data
        'double_charm_particles': DOUBLE_CHARM_PARTICLES,
        'double_charm': get_double_charm(),
        # Bottom baryon data
        'bottom_particles': BOTTOM_PARTICLES,
        'bottom': get_bottom(),
        'bottom_cycle': BOTTOM_CYCLE,
    }

    # Pages to build
    pages = [
        ('index.html', 'index.html'),
        ('baryon_cycle.html', 'baryon_cycle.html'),
        ('charm_cycle.html', 'charm_cycle.html'),
        ('bottom_cycle.html', 'bottom_cycle.html'),
        ('mesons.html', 'mesons.html'),
        ('magnetic.html', 'magnetic.html'),
        ('formulas.html', 'formulas.html'),
        # Framework pages
        ('framework.html', 'framework.html'),
        ('lorentz.html', 'lorentz.html'),
        ('q_calculus.html', 'q_calculus.html'),
        ('seven.html', 'seven.html'),
    ]

    for template_name, output_name in pages:
        template_path = TEMPLATES / template_name
        if not template_path.exists():
            print(f"  Skipping {template_name} (not found)")
            continue

        template = env.get_template(template_name)
        html = template.render(**context)

        output_path = DIST / output_name
        output_path.write_text(html)
        print(f"  Built {output_name}")

    print(f"Done! Open {DIST}/index.html in your browser.")


def watch():
    """Watch for changes and rebuild."""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Install watchdog for --watch: pip install watchdog")
        sys.exit(1)

    class RebuildHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith(('.html', '.css', '.py')):
                print(f"\nChange detected: {event.src_path}")
                build()

    build()

    observer = Observer()
    observer.schedule(RebuildHandler(), str(TEMPLATES), recursive=True)
    observer.schedule(RebuildHandler(), str(STATIC), recursive=True)
    observer.schedule(RebuildHandler(), str(ROOT / 'data'), recursive=True)
    observer.start()

    print("\nWatching for changes... (Ctrl+C to stop)")
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    if '--watch' in sys.argv:
        watch()
    else:
        build()
