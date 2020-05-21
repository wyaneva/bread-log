#!/usr/bin/python

# Vanya Yaneva, 2020

# A small script to calculate how to build a levain without discard

from enum import Enum
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('target_levain_weight', type=int,
                        help='required amount of levain in recipe')
    parser.add_argument('--steps', type=int,
                        help='number of feeding steps')
    num_steps = 2; # default number of steps

    args = parser.parse_args()
    y = args.target_levain_weight;
    if (args.steps):
        num_steps = args.steps;
    n = num_steps;

    # calculate starting amount; equation is derived as follows:
    # step 1: 3*x
    # step 2: 3*3*x
    # step n: (3**n)*x
    # (3**n)*x = y + x + 10 (adding 10 grams to account for scraps)
    x = (y + 10) / (3**n - 1);

    print()
    print(f"start levain: {x:.1f}g")
    print("---------------------------------")
    while (n > 0):
        n = n - 1;
        print(f"step {num_steps-n}: {x:.1f} {x:.1f} {x:.1f}")
        x = 3*x;
    print("---------------------------------")
    print(f"end levain: {x:.1f}g")
    print(f" - target levain: {y:.1f}g")
    print(f" - remainder: {x-y:.1f}g")
    print()
