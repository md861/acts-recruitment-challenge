#!/usr/bin/env python3
## @file render-terrain-gif.py
#  @brief Render a configurable terrain-backed simulation preview GIF.
#
#  Generates a deterministic review artifact from the same terrain map and
#  model defaults used by the live simulation. `SIM_GIF_TICKS` or `--ticks`
#  controls the frame count; the default remains 100 ticks.

"""Render the first terrain-map simulation ticks to a GIF.

The script uses only the Python standard library. It mirrors the frontend
terrain-map visual language closely enough to create a portable review artifact
without depending on a browser, ffmpeg, or ImageMagick.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "model-python"))

from population_model.config import ModelConfig
from population_model.model import PopulationModel
from population_model.terrain import _read_png_rgb


MAP_SIZE = (640, 443)
LEGEND_WIDTH = 220
OUTPUT_SIZE = (MAP_SIZE[0] + LEGEND_WIDTH, MAP_SIZE[1])
DEFAULT_TICKS = 100
FRAME_DELAY_CENTISECONDS = 6

NORMAL = 0
BLACK = 1
RED = 2
ORANGE = 3
GREEN = 4
BLUE = 5
PINK = 6
CIVILIAN = 7
STAFF = 8
PATROL = 9
AGENT_OUTLINE = 10
BROWN = 11
TEXT = 12
LINE = 13
PANEL = 14
LIGHT = 15

PALETTE_RGB = [
    (255, 255, 255),
    (0, 0, 0),
    (237, 28, 36),
    (255, 127, 39),
    (34, 177, 76),
    (63, 72, 204),
    (255, 174, 201),
    (45, 122, 70),
    (111, 90, 168),
    (177, 86, 40),
    (255, 255, 255),
    (136, 0, 21),
    (28, 36, 32),
    (184, 195, 187),
    (243, 244, 241),
    (248, 250, 247),
]

CELL_COLORS = {
    (255, 255, 255): NORMAL,
    (0, 0, 0): BLACK,
    (136, 0, 21): BROWN,
    (185, 122, 87): BROWN,
    (237, 28, 36): RED,
    (255, 127, 39): ORANGE,
    (34, 177, 76): GREEN,
    (63, 72, 204): BLUE,
    (255, 174, 201): PINK,
}

AGENT_COLORS = {
    "civilian": CIVILIAN,
    "staff": STAFF,
    "patrol": PATROL,
}

LEGEND_ITEMS = [
    ("NORMAL", NORMAL, False),
    ("OUTER BOUNDARY", BLACK, False),
    ("DENSITY ZERO", BROWN, True),
    ("RESTRICTED", RED, True),
    ("GATE", ORANGE, True),
    ("EXIT", GREEN, True),
    ("TYPE 1 PENALTY", BLUE, True),
    ("TYPE 2 PENALTY", PINK, True),
    ("CIVILIAN", CIVILIAN, False),
    ("STAFF", STAFF, False),
    ("PATROL", PATROL, False),
]

FONT = {
    " ": ["000", "000", "000", "000", "000", "000", "000"],
    "0": ["111", "101", "101", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "010", "010", "111"],
    "2": ["111", "001", "001", "111", "100", "100", "111"],
    "3": ["111", "001", "001", "111", "001", "001", "111"],
    "4": ["101", "101", "101", "111", "001", "001", "001"],
    "5": ["111", "100", "100", "111", "001", "001", "111"],
    "6": ["111", "100", "100", "111", "101", "101", "111"],
    "7": ["111", "001", "001", "010", "010", "010", "010"],
    "8": ["111", "101", "101", "111", "101", "101", "111"],
    "9": ["111", "101", "101", "111", "001", "001", "111"],
    "A": ["010", "101", "101", "111", "101", "101", "101"],
    "B": ["110", "101", "101", "110", "101", "101", "110"],
    "C": ["111", "100", "100", "100", "100", "100", "111"],
    "D": ["110", "101", "101", "101", "101", "101", "110"],
    "E": ["111", "100", "100", "110", "100", "100", "111"],
    "F": ["111", "100", "100", "110", "100", "100", "100"],
    "G": ["111", "100", "100", "101", "101", "101", "111"],
    "H": ["101", "101", "101", "111", "101", "101", "101"],
    "I": ["111", "010", "010", "010", "010", "010", "111"],
    "L": ["100", "100", "100", "100", "100", "100", "111"],
    "M": ["101", "111", "111", "101", "101", "101", "101"],
    "N": ["101", "111", "111", "111", "101", "101", "101"],
    "O": ["111", "101", "101", "101", "101", "101", "111"],
    "P": ["110", "101", "101", "110", "100", "100", "100"],
    "R": ["110", "101", "101", "110", "101", "101", "101"],
    "S": ["111", "100", "100", "111", "001", "001", "111"],
    "T": ["111", "010", "010", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "101", "101", "111"],
    "X": ["101", "101", "101", "010", "101", "101", "101"],
    "Y": ["101", "101", "101", "010", "010", "010", "010"],
    "Z": ["111", "001", "001", "010", "100", "100", "111"],
    ":": ["000", "010", "010", "000", "010", "010", "000"],
}


def main() -> None:
    args = parse_args()
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)

    config = ModelConfig.from_env()
    model = PopulationModel(config)
    terrain_path = ROOT / config.terrain_map_path
    terrain_width, terrain_height, terrain_pixels = _read_png_rgb(terrain_path)
    base_frame = render_base_frame(terrain_width, terrain_height, terrain_pixels)

    frames = []
    for tick in range(1, args.ticks + 1):
        model.step()
        frames.append(
            draw_frame(base_frame, model, terrain_width, terrain_height, tick)
        )

    write_gif(output, OUTPUT_SIZE[0], OUTPUT_SIZE[1], frames)
    print(output)


def parse_args() -> argparse.Namespace:
    ## @brief Parse configurable GIF tick count and output path.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ticks",
        type=_positive_int,
        default=_env_positive_int("SIM_GIF_TICKS", DEFAULT_TICKS),
        help="Number of simulation ticks to render. Defaults to 100.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output GIF path.",
    )
    args = parser.parse_args()
    if args.output is None:
        args.output = Path(
            os.getenv(
                "SIM_GIF_OUTPUT",
                str(ROOT / "artifacts" / f"terrain1_first_{args.ticks}_ticks.gif"),
            )
        )
    return args


def _env_positive_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return _positive_int(raw)
    except argparse.ArgumentTypeError:
        return default


def _positive_int(raw: str) -> int:
    value = int(raw)
    if value < 1:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return value


def render_base_frame(
    terrain_width: int, terrain_height: int, terrain_pixels: list[tuple[int, int, int]]
) -> bytearray:
    width, height = OUTPUT_SIZE
    frame = bytearray([PANEL] * (width * height))
    map_width, map_height = MAP_SIZE

    for y in range(map_height):
        source_y = min(terrain_height - 1, (y * terrain_height) // map_height)
        source_row = source_y * terrain_width
        for x in range(map_width):
            source_x = min(terrain_width - 1, (x * terrain_width) // map_width)
            rgb = terrain_pixels[source_row + source_x]
            color = CELL_COLORS[rgb]
            frame[y * width + x] = patterned_color(color, x, y)

    draw_rect(frame, width, MAP_SIZE[0], 0, 2, MAP_SIZE[1], LINE)
    draw_legend(frame, width)
    return frame


def patterned_color(color: int, x: int, y: int) -> int:
    if color in (NORMAL, BLACK):
        return color
    if color == BROWN:
        return BROWN if (x + y) % 8 < 3 else LIGHT
    if color == RED:
        return RED if (x + y) % 10 < 3 else LIGHT
    if color == ORANGE:
        return ORANGE if y % 8 < 3 else LIGHT
    if color == GREEN:
        return GREEN if x % 8 < 3 else LIGHT
    if color == BLUE:
        return BLUE if (x - y) % 10 < 3 else LIGHT
    if color == PINK:
        return PINK if (x + y) % 12 < 4 else LIGHT
    return color


def draw_frame(
    base_frame: bytearray,
    model: PopulationModel,
    terrain_width: int,
    terrain_height: int,
    tick: int,
) -> bytes:
    width, height = OUTPUT_SIZE
    frame = bytearray(base_frame)
    draw_text(frame, width, MAP_SIZE[0] + 14, 14, f"TICK:{tick:03d}", TEXT)
    for agent in model.agents:
        x = round(agent.position.x * (MAP_SIZE[0] - 1) / max(1, terrain_width - 1))
        y = round(agent.position.y * (MAP_SIZE[1] - 1) / max(1, terrain_height - 1))
        color = AGENT_COLORS.get(agent.role, TEXT)
        draw_disc(frame, width, height, x, y, radius=4, color=AGENT_OUTLINE)
        draw_disc(frame, width, height, x, y, radius=2, color=color)
    return bytes(frame)


def draw_legend(frame: bytearray, width: int) -> None:
    x = MAP_SIZE[0] + 14
    y = 40
    draw_text(frame, width, x, y, "LEGEND", TEXT)
    y += 22
    for label, color, striped in LEGEND_ITEMS:
        draw_swatch(frame, width, x, y, color, striped)
        draw_text(frame, width, x + 24, y + 2, label, TEXT)
        y += 28


def draw_swatch(
    frame: bytearray, width: int, x: int, y: int, color: int, striped: bool
) -> None:
    for yy in range(y, y + 16):
        for xx in range(x, x + 16):
            frame[yy * width + xx] = patterned_color(color, xx, yy) if striped else color
    draw_rect(frame, width, x, y, 16, 1, TEXT)
    draw_rect(frame, width, x, y + 15, 16, 1, TEXT)
    draw_rect(frame, width, x, y, 1, 16, TEXT)
    draw_rect(frame, width, x + 15, y, 1, 16, TEXT)


def draw_text(
    frame: bytearray, width: int, x: int, y: int, text: str, color: int
) -> None:
    cursor = x
    for char in text.upper():
        glyph = FONT.get(char, FONT[" "])
        for gy, row in enumerate(glyph):
            for gx, pixel in enumerate(row):
                if pixel == "1":
                    frame[(y + gy) * width + cursor + gx] = color
        cursor += 5


def draw_rect(
    frame: bytearray, width: int, x: int, y: int, rect_width: int, rect_height: int, color: int
) -> None:
    height = OUTPUT_SIZE[1]
    for yy in range(max(0, y), min(height, y + rect_height)):
        for xx in range(max(0, x), min(width, x + rect_width)):
            frame[yy * width + xx] = color


def draw_disc(
    frame: bytearray,
    width: int,
    height: int,
    center_x: int,
    center_y: int,
    radius: int,
    color: int,
) -> None:
    radius_squared = radius * radius
    for y in range(max(0, center_y - radius), min(height, center_y + radius + 1)):
        for x in range(max(0, center_x - radius), min(width, center_x + radius + 1)):
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius_squared:
                frame[y * width + x] = color


def write_gif(path: Path, width: int, height: int, frames: list[bytes]) -> None:
    color_table = bytes(channel for rgb in PALETTE_RGB for channel in rgb)
    with path.open("wb") as gif:
        gif.write(b"GIF89a")
        gif.write(width.to_bytes(2, "little"))
        gif.write(height.to_bytes(2, "little"))
        gif.write(bytes([0b10000011, 0, 0]))
        gif.write(color_table)
        gif.write(b"!\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00")

        for frame in frames:
            gif.write(b"!\xf9\x04\x04")
            gif.write(FRAME_DELAY_CENTISECONDS.to_bytes(2, "little"))
            gif.write(b"\x00\x00")
            gif.write(b",")
            gif.write((0).to_bytes(2, "little"))
            gif.write((0).to_bytes(2, "little"))
            gif.write(width.to_bytes(2, "little"))
            gif.write(height.to_bytes(2, "little"))
            gif.write(b"\x00")
            gif.write(bytes([4]))
            encoded = lzw_encode(frame, min_code_size=4)
            for index in range(0, len(encoded), 255):
                block = encoded[index : index + 255]
                gif.write(bytes([len(block)]))
                gif.write(block)
            gif.write(b"\x00")

        gif.write(b";")


def lzw_encode(indices: bytes, min_code_size: int) -> bytes:
    clear_code = 1 << min_code_size
    end_code = clear_code + 1
    code_size = min_code_size + 1
    writer = BitWriter()
    writer.write(clear_code, code_size)
    codes_since_clear = 0

    for index in indices:
        writer.write(index, code_size)
        codes_since_clear += 1
        if codes_since_clear >= 10:
            writer.write(clear_code, code_size)
            codes_since_clear = 0

    writer.write(end_code, code_size)
    return writer.finish()


class BitWriter:
    def __init__(self) -> None:
        self.buffer = bytearray()
        self.accumulator = 0
        self.bit_count = 0

    def write(self, code: int, size: int) -> None:
        self.accumulator |= code << self.bit_count
        self.bit_count += size
        while self.bit_count >= 8:
            self.buffer.append(self.accumulator & 0xFF)
            self.accumulator >>= 8
            self.bit_count -= 8

    def finish(self) -> bytes:
        if self.bit_count:
            self.buffer.append(self.accumulator & 0xFF)
        return bytes(self.buffer)


if __name__ == "__main__":
    main()
