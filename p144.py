#!/usr/bin/python

from sympy.geometry import Point, Ray, Segment, Ellipse, Line
from math import pi

def next_origin(origin, targets):
    if len(targets) == 1:
        return targets[0]
    else:
        return origin

def next_angle(ray, tangent, axis):
    X, Y = axis
    alpha = ray.angle_between(tangent)
    beta = tangent.angle_between(X)
    # angle_between returns an angle between 0 (paralell) and
    # pi/2 (normal)
    print(" Alpha: %f" % alpha)
    return -(pi - beta -alpha)


def main():

    O = Point(0, 0)
    p0 = Point(0, 10.1)
    p1 = Point(1.4, -9.6)
    m = p0.midpoint(p1)
    X = Line(O, Point(10, 0))
    Y = Line(O, Point(0, 10))

    ellipse = Ellipse(Point(0, 0), 5 , 10)
    sortie = Segment(Point(-0.01, 10), Point(0.01, 10))

    ray = Ray(m, p1)

    reflections = 0
    
    while not sortie.intersection(ray) and reflections < 5:
        targets = ellipse.intersection(ray)
        print " Targets: ", targets
        origin = next_origin(ray.p1, targets)
        tangents = ellipse.tangent_lines(origin)
        if len(tangents) > 1:
            print("Error computing intersection")
            break
        tangent = tangents.pop()
        alpha = next_angle(ray, tangent, (X, Y))
        reflections += 1
        ray = Ray(origin, angle=alpha)
        print "Reflections :", reflections
        

if __name__ == "__main__":
    main()
