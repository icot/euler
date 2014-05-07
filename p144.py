#!/usr/bin/python

from sympy.geometry import Point, Ray, Segment, Ellipse

def next_origin(origin, targets):
    if len(targets) == 1:
        return targets[0]
    else:
        return origin

def next_angle(ray, tangents):
    alphas = [ray.angle_between(t) for t in tangents]
    return alphas[0]


def main():
    
    p0 = Point(0, 10.1)
    p1 = Point(1.4, -9.6)
    m = p0.midpoint(p1)

    ellipse = Ellipse(Point(0, 0), 5 , 10)
    sortie = Segment(Point(-0.01, 10), Point(0.01, 10))

    ray = Ray(m, p1)

    reflections = 0
    while not sortie.intersection(ray):
        targets = ellipse.intersection(ray)
        print " Targets: ", targets
        origin = next_origin(ray.p1, targets)
        tangents = ellipse.tangent_lines(origin)
        alpha = next_angle(ray, tangents)
        print " Alpha: ", float(alpha)
        reflections += 1
        ray = Ray(origin, angle=alpha)
        print "Reflections :", reflections
        

if __name__ == "__main__":
    main()
