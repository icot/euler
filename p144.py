#!/usr/bin/python

import cmath
import itertools
import time

from math import pi, atan2, tan, atan
import numpy as np

def sign(a):
    if a >= 0:
        return 1
    else:
        return -1

def slope(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return float((y1-y0))/(x1-x0)

def tangent(p):
    return -4*p[0]/p[1]

def normal(p):
    x, y = p
    mt = tangent(p)
    alpha_tan = angle(mt)
    delta = pi/4
    if sign(x) == sign(y):
        alpha_n = alpha_tan - delta
    else:
        alpha_n = alpha_tan + delta
    return tan(alpha_n)

def angle(slope, degrees = False):
    if degrees:
        return (180/pi) * atan(slope)
    else:
        return atan(slope)

def test_ellipse(p):
    return (4 * pow(p[0], 2) + pow(p[1], 2)) == 100

def solve_quadratic(a,b,c):
    arr = np.array([a,b,c])
    return np.roots(arr)

def cross_point(m,b):
    a2 = 100 + 16 * pow(m, 2)
    a1 = 2 * 16 * m * b
    a0 = pow(b,2) - 100
    xs = solve_quadratic(a2, a1, a0)
    ys = [m*x +b for x in xs]
    return zip(xs,ys)

def step(p0, p1):
    m_inc = slope(p0, p1)
    m_tangent = tangent(p1)
    m_perp = normal(p1)
    
    alpha_inc = angle(m_inc)
    alpha_tangent = angle(m_tangent)
    alpha_perp = angle(m_perp) 
  
    alpha_c = pi - abs(alpha_tangent) - abs(alpha_inc)
    alpha_d = pi/2 - alpha_c
    alpha_ref = alpha_perp + alpha_d
    
    print " inc: %.5f, tan: %.5f, perp: %.5f, ref: %.5f\n" % (alpha_inc, alpha_tangent, alpha_perp, alpha_ref) 
    m_ref = tan(alpha_ref)
    b = p1[1] - m_ref * p1[0]
    sols = cross_point(m_ref, b)
    for sol in sols:
        if sol != p1:
            p2 = sol
    return p2

def main():
    
    O = (0, 0)
    A = (-2, 2)
    p0 = (0, 10.1)
    p1 = (1.4, -9.6)

    a = p0
    b = p1
    for n in range(4):
        print a," to", b, test_ellipse(b)
        sig =  step(a, b)
        a = b
        b = sig 

if __name__ == "__main__":
    main()
