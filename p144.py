#!/usr/bin/python

import cmath
import math
import fractions
import itertools
import time

from pylab import *
import matplotlib
import numpy as np

def slope(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return fractions.Fraction((y1-y0)/(x1-x0))

def perpendicular_slope(m):
    if m > 1000:
        return fractions.Fraction(0)
    elif m < 0.001:
        return fractions.Fraction(1e6)
    else:
        return fractions.Fraction(-m.denominator, m.numerator)

def angle(slope, degrees = False):
    if degrees:
        return (180/math.pi) * math.atan2(slope.numerator, slope.denominator)
    else:
        return math.atan2(slope.numerator, slope.denominator)

def test_ellipse(p):
    return (4*pow(p[0], 2) + pow(p[1], 2)) == 100

def solve_quadratic(a,b,c):
    arr = np.array([a,b,c])
    return np.roots(arr)

def cross_point(m,b):
    a2 = 4 + pow(m, 2)
    a1 = 2 * m * b
    a0 = pow(b,2) - 100
    xs = solve_quadratic(a2, a1, a0)
    ys = [m*x +b for x in xs]
    return zip(xs,ys)

def plot_point(p):
    plot(p[0], p[1], 'sb')

def plot_line(p0, p1, fmt):
    if type(p1) == type(()):
        # Point, Point
        m = slope(p0,p1)
        xs = arange(p0[0], p1[0], 0.01)
    else:
        # Point, slope
        m = p1
        xs = arange(p0[0] - 2, p0[0] + 2, 0.01)
    b = p0[1] - m * p0[0]
    ys = map(lambda x: m*x +b, xs)
    plot(xs, ys, fmt)

def plot_ellipse(rx, ry):
    ts = arange(0.0, 2*math.pi, 0.001)
    xs = [rx * math.cos(t) for t in ts]
    ys = [ry * math.sin(t) for t in ts]
    plot(xs, ys,'k')
    ylim([-12, 12])
    xlim([-12, 12])

def step(p0, p1):
    m_inc = slope(p0, p1)
    m_tangent = fractions.Fraction(-4*p1[0] / p1[1])
    m_perp = perpendicular_slope(m_tangent)
    alpha_inc = angle(m_inc)
    alpha_tangent = angle(m_tangent)
    alpha_perp = angle(m_perp) 
    alpha_ref = alpha_perp + abs(alpha_perp - alpha_inc)
    m_ref = math.tan(alpha_ref)
    b = p1[1] - m_ref * p1[0]
    sols = cross_point(m_ref, b)
    for sol in sols:
        if sol != p1:
            p2 = sol
    
    plot_line(p0, p1, 'r')
    plot_line(p1, m_tangent, 'b')
    plot_line(p1, m_perp, 'g')

    return p2

def main():
    
    O = (0, 0)
    A = (-2, 2)
    p0 = (0, 10.1)
    p1 = (1.4, -9.6)

    #plot ellipse
    clf()
    grid(True)
    plot_ellipse(4, 10)
    plot_point(p0)
    plot_point(p1)
    matplotlib.interactive(True)
    
    a = p0
    b = p1
    for n in range(4):
        print ">>", (a,b)
        sig =  step(a, b)
        a = b
        b = sig 
        draw()
        time.sleep(1)
    show()

if __name__ == "__main__":
    main()
