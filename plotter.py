from typing import Callable
from PIL import Image
import math
from random import random


global size

def hash(seed: int) -> int:
    # return int(tanh(seed*seed) * randint(0, 255) * random()**0.5)
    result: int = (round(math.gcd(seed, 2)**2 * random()) % 256) * 64 
    return result

def color_pixel() -> list[int]:
    return [round(255 * random()), round(255 * random()), round(255 * random())]

def gradient_pixel(size: list[int], pixel: list[int]) -> list[int]:
    start_color: list[int] = [255, 255, 0]
    end_color: list[int] = [0, 255, 200]
    pixel_color = interpolate_color(start_color, end_color, pixel[0]/size[0]) 

    return pixel_color

def interpolate_color(start_color: list[int], end_color: list[int], parameter: float) -> list[int]:
    result_color: list[int] = [0, 0, 0]
    for channel in range(len(start_color)):
        result_color[channel] = round((end_color[channel] - start_color[channel])*parameter) + start_color[channel]

    return result_color

def gen_has_pixel(seed) -> list[int]:
    r: int = hash(seed)
    g: int = hash(seed)
    b: int = hash(seed)

    return [r, g, b]

def gen_pixel(pixel: list[int], function: Callable) -> list[int] | None:
    tolerance: float = 1
    scale: float = (size+1)**0.5 # 0.5 acquired from trial and error
    center: int = size // 2 + 1
    try:
        return gradient_pixel([size, size], pixel) if math.fabs(pixel[1] - center - scale * function((pixel[0]-center)/scale)) < tolerance else None
    except:
        return None


def create_image(functions: list[Callable], size: int):
    img = Image.new('RGB', (size, size), "black")
    pixels = img.load()

    for function in functions:
        for x in range(img.size[0]):
            for y in range(img.size[0]):
                color = gen_pixel([x, y], function)
                if color != None:
                    pixels[x, size-y-1] = (color[0], color[1], color[2]) # size-y-1 so it iterates from the bottom of the screen instead of the top, holding the desired orientation 

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

# def superimpose(*args: list[FunctionType]):
#     resultant: Callable = lambda x: 0
#     for function in args:
#         resultant += function
#
    # return resultant
    
def main() -> None:
    global size
    size = 2**9 - 1
    functions = [math.sin, math.cos, math.tan]
    # function = superimpose(functions)
    create_image(functions, size)

main() 
