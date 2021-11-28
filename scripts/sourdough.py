#!/usr/bin/python

# Fraser Cormack, 2018

# All ratio variables are with regards to total flour weight

from enum import Enum
import argparse

def f2c(f):
    return (f - 32) * 5.0/9.0

def c2f(c):
    return (c * 9.0/5.0) + 32

class RATIOS(Enum):
    WHITE = 0.8243
    BROWN = 0.1216
    RYE   = 0.0541
    LEVAIN = 0.2027
    SALT   = 0.0195

class CONSTS(Enum):
    FINAL_DOUGH_TEMP_C = f2c(78)
    LEVAIN_HYDRATION = 1.0

def print_weights(total_flour):
    print(f"individual weights:")
    for r in RATIOS:
        print(f"  {r.name:<6} : {total_flour:.0f}g * "
              f"{r.value} = {r.value * total_flour:>8.0f}g")

def water_temp_c(flour_temp_c, levain_temp_c, room_temp_c):
    return ((CONSTS.FINAL_DOUGH_TEMP_C.value * 4)
            - (flour_temp_c + levain_temp_c + room_temp_c))

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError(f"{x} not in range [0.0, 1.0]")
    return x

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('total_loaves_weight', type=int)
    parser.add_argument('hydration_ratio', type=restricted_float,
                        help='between 0.0 and 1.0')
    parser.add_argument('--ambient-temps', nargs=3,
                        help='ambient, flour, and levain temperatures (degrees '
                             'celsius) in any order')

    args = parser.parse_args()

    print(f"assuming levain hydration: {CONSTS.LEVAIN_HYDRATION.value:.2f}")

    dry_weight = (args.total_loaves_weight / (1 + args.hydration_ratio))
    wet_weight = args.total_loaves_weight - dry_weight

    print(f"total dry weight: {dry_weight:.0f}g")
    print(f"total wet weight: {wet_weight:.0f}g")
    print("---------------------------------")

    levain_flour_weight_ratio = (
        1 + (RATIOS.LEVAIN.value * CONSTS.LEVAIN_HYDRATION.value)
    )
    levain_weight = (
        RATIOS.LEVAIN.value * (dry_weight / levain_flour_weight_ratio)
    )

    levain_flour_weight = levain_weight / (CONSTS.LEVAIN_HYDRATION.value + 1)
    levain_water_weight = levain_weight - levain_flour_weight

    flour_weight = dry_weight - levain_flour_weight
    water_weight = (args.hydration_ratio * dry_weight) - levain_water_weight

    print(f"total flour weight: {flour_weight:.0f}g")
    print_weights(flour_weight)
    print(f"additional water weight: {water_weight:.0f}g")
    if args.ambient_temps:
        temps_as_floats = map(float, args.ambient_temps)
        print(f"water temperature: {water_temp_c(*temps_as_floats):.0f}C")
