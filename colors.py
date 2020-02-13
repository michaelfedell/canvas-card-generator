"""Extract all canvas scripts and randomize colors."""
from pathlib import Path
import re
from typing import Tuple
import random


styles = dict()
p = Path('./canvas/')

HEX_RE = re.compile(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', flags=re.IGNORECASE)
RGB_RE = re.compile(r'rgb\((\d{1,3},\s?){2}(\d{1,3}\s?)\)')


for f in p.glob('*.js'):
    idx = f.stem
    styles[idx] = {'code': f.open().read()}


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert an rgb tuple to a hex code string."""
    return ('#%02x%02x%02x' % rgb).upper()


def get_random_hex_color() -> str:
    """Generate the hex code for a random color"""
    def _rand():
        return random.randint(0, 255)

    rgb = (_rand(), _rand(), _rand())
    return rgb_to_hex(rgb)


STYLES = list(styles.keys())
