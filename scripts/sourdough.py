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
    WHITE = 82.43
    BROWN = 12.16
    RYE   = 5.41
    LEVAIN = 20.27
    SALT   = 1.95

class CONSTS(Enum):
    FINAL_DOUGH_TEMP_C = f2c(78)

def print_weights(total_flour):
    print(f"individual weights:")
    for r in RATIOS:
        print(f"  {r.name:<6} : {total_flour:.2f}g * "
              f"{r.value / 100} = {r.value * total_flour / 100:>8.4f}g")

def water_weight(total_flour):
    return total_flour * 0.70

def water_temp_c(flour_temp_c, levain_temp_c, room_temp_c):
    return ((CONSTS.FINAL_DOUGH_TEMP_C.value * 4)
            - (flour_temp_c + levain_temp_c + room_temp_c))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('total_loaves_weight', type=int)
    parser.add_argument('hydration_ratio', type=float)
    parser.add_argument('--ambient-temps', nargs=3)

    args = parser.parse_args()

    flour_weight = (args.total_loaves_weight /
                     (1 + args.hydration_ratio
                        + (RATIOS.LEVAIN.value / 100)
                        + (RATIOS.SALT.value / 100)))

    print(f"total flour weight: {flour_weight:.2f}g")
    print_weights(flour_weight)
    print(f"water weight: {water_weight(flour_weight):.2f}g")
    if args.ambient_temps:
        temps_as_floats = map(float, args.ambient_temps)
        print(f"water temperature: {water_temp_c(*temps_as_floats):.2f}C")
