"""Extract all canvas scripts and randomize colors."""
from pathlib import Path
import re
from typing import Tuple
import random


styles = dict()
p = Path('./canvas/')

HEX_RE = re.compile(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', flags=re.IGNORECASE)
RGB_RE = re.compile(r'rgb\((\d{1,3},\s?){2}(\d{1,3}\s?)\)')
CANVAS_RE = re.compile(r'(getElementById\()[\'\"](\w+)[\'\"]\)')
WIDTH_RE = re.compile(r'(.width) = \'?(\d+)(px[\'\"])?')
HEIGHT_RE = re.compile(r'(.height) = [\'\"]?(\d+)(px[\'\"])?')


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert an rgb tuple to a hex code string."""
    return ('#%02x%02x%02x' % rgb).upper()


def get_random_hex_color() -> str:
    """Generate the hex code for a random color"""
    def _rand():
        return random.randint(0, 255)

    rgb = (_rand(), _rand(), _rand())
    return rgb_to_hex(rgb)


def replace_color(match):
    match = match.group()
    color = get_random_hex_color()
    return color


def upscale(match):
    dim = match.group(1)
    val = int(match.group(2))
    px = match.group(3)
    scaled = val * 3
    print(f'Scaling from {val} to {scaled}')
    return f'{dim} = {scaled}' if not px else f"{dim} = '{scaled}px'"


def scale_canvas(code: str) -> str:
    code = HEIGHT_RE.sub(upscale, code, count=2)
    code = WIDTH_RE.sub(upscale, code, count=2)
    return code


def randomize_colors(code: str) -> str:
    """
    Randomize all hex color code references found in a block of code.

    Args:
        code (str): The original code block to be updated.

    Returns:
        str: Code block with all hex code colors replaced with random colors.

    """
    print('Original code is %d lines long' % code.count('\n'))
    randomized_code = HEX_RE.sub(replace_color, code)
    print('Randomized code is %d lines long' % code.count('\n'))
    return randomized_code


def update_canvas_id(code: str, new_id: str = 'randomCanvas') -> str:
    """
    Update the id attribute used to get canvas element on DOM.

    Args:
        code (str): The original code block to be updated.
        new_id (str, optional): The desired ID of the canvas element to target.
                                Defaults to 'randomCanvas'.

    Returns:
        str: Code block with a new id passed into dom selector.

    """
    fixed = CANVAS_RE.sub(rf'\1"{new_id}")', code, count=1)
    return fixed


def process(code: str) -> str:
    """
    Wraps all processing steps in single function call.

    Arguments:
        code (str): The original code block to be updated.

    Returns:
        str: Code block with all processing steps performed.

    """
    randomized = randomize_colors(code)
    tagged = update_canvas_id(randomized)
    scaled = scale_canvas(tagged)
    return scaled


for f in p.glob('*.js'):
    idx = f.stem
    styles[idx] = {'code': f.open().read()}

STYLES = list(styles.keys())
