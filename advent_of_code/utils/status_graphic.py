"""Create and save the status graphic to track progress of Advent of Code."""
from pathlib import Path
from sys import path
from time import perf_counter_ns

from PIL import Image, ImageDraw, ImageFont

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.solver_status import (
    first_puzzle_date,
    is_solver_implemented,
    last_puzzle_date,
    puzzle_date_generator,
)


def save_status_graphic(filename: str) -> None:
    """Create a status graphic, and save with the given filename.

    Args:
        filename (str): the filename to save
    """
    # prepare for the images
    images = []
    regular_font = ImageFont.truetype(
        "./advent_of_code/utils/SourceCodePro-Regular.ttf", 14
    )
    bold_font = ImageFont.truetype("./advent_of_code/utils/SourceCodePro-Bold.ttf", 14)
    horizontal_spacing = 8
    vertical_spacing = 20
    border = 10

    for frame in puzzle_date_generator():
        print(frame)
        # Generate the lines to print
        lines = []
        for year in range(first_puzzle_date().year, last_puzzle_date().year + 1):
            line = [f"{year}: "]
            count = 0
            for day in range(1, 26):
                if frame.year > year or (frame.year == year and frame.day >= day):
                    if is_solver_implemented(year, day):
                        line.append("**")
                        count += 2
                    else:
                        line.append("--")
                else:
                    line.append("..")
            line.append(f" {count:02}")

            lines.append("".join(line))

        # create a new image for the frame
        image = Image.new(
            "RGB",
            (
                (max(len(line) for line in lines) * horizontal_spacing) + (2 * border),
                (len(lines) * vertical_spacing) + (2 * border),
            ),
            (0, 0, 0),
        )
        draw = ImageDraw.Draw(image)
        # draw each character, selecting colours and font style as required
        for y, row in enumerate(lines):
            for x, character in enumerate(row):
                if character == "*":
                    fill = (255, 255, 0)
                    font = bold_font
                elif character in ".-":
                    fill = (128, 128, 128)
                    font = regular_font
                else:
                    fill = (255, 255, 255)
                    font = regular_font
                draw.text(
                    (
                        border + (x * horizontal_spacing),
                        border + (y * vertical_spacing),
                    ),
                    character,
                    fill=fill,
                    font=font,
                )
        images.append(image)

    # save the image sequence
    start = perf_counter_ns()

    print(f"\nsaving {len(images)} frames")
    images[0].save(
        filename,
        save_all=True,
        append_images=images[1:],
        duration=25,
    )
    stop = perf_counter_ns()

    print(f"\ncomplete in {(stop - start) / 1000000000:.2f}s")


if __name__ == "__main__":  # pragma: no cover
    save_status_graphic("status.gif")
