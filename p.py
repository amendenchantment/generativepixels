from PIL import Image
import math
from random import random


global square_width

def hash(seed: int) -> int:
    # return int(tanh(seed*seed) * randint(0, 255) * random()**0.5)
    result: int = (round(math.gcd(seed, 2)**2 * random()) % 256) * 64 
    return result

def color_pixel() -> list[int]:
    return [round(255 * random()), round(255 * random()), round(255 * random())]

def gen_has_pixel(seed) -> list[int]:
    r: int = hash(seed)
    g: int = hash(seed)
    b: int = hash(seed)

    return [r, g, b]

def gen_pixel(pixel: list[int]) -> list[int]:
    function = math.sin
    tolerance: float = 2
    scale: float = (square_width+1)**0.5 # 0.75 acquired from trial and error
    center: int = square_width // 2 + 1
    try:
        return color_pixel() if math.fabs(pixel[1] - center - scale * function((pixel[0]-center)/scale)) < tolerance else [0, 0, 0]
    except ValueError:
        return [0, 0, 0]

def create_image():
    global square_width
    square_width = 2**7 - 1 
    img = Image.new('RGB', (square_width, square_width), "white")
    pixels = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[0]):
            color = gen_pixel([x, y])
            pixels[x, square_width-y-1] = (color[0], color[1], color[2]) # square_width-y-1 so it iterates from the bottom of the screen instead of the top, maintaining the orientation desired

    increment_counter()
    current_counter = get_counter()
    file_name: str = f"/Users/anshmendiratta/Code/generativepixels/images/image{current_counter}.png"
    img.save(file_name)

def increment_counter() -> int:
    with open("counter.txt", "r+") as file:
        current_count = int(file.readline().strip('\x00'))
        file.truncate(0)
        file.write(str(current_count + 1))

    return int(current_count + 1)

def get_counter() -> int:
    with open("counter.txt", "r") as file:
        return int(file.readline().strip('\x00'))

def main() -> None:
    create_image()

main() 
