"""Small 2D geometry helpers for evaluators and renderers.

Points are (x, y) pairs (any extra z value is ignored). Polygons are lists of
points without a repeated closing point. No dependencies, so every line is readable.
"""
import math


def _edges(poly):
    n = len(poly)
    for i in range(n):
        yield poly[i], poly[(i + 1) % n]


def area(poly):
    """Area of a simple polygon (shoelace formula)."""
    s = sum(a[0] * b[1] - b[0] * a[1] for a, b in _edges(poly))
    return abs(s) / 2.0


def perimeter(poly):
    return sum(math.dist(a[:2], b[:2]) for a, b in _edges(poly))


def shortest_edge(poly):
    return min(math.dist(a[:2], b[:2]) for a, b in _edges(poly))


def convex_hull(points):
    """Smallest convex polygon around the points (Andrew's monotone chain), anticlockwise."""
    pts = sorted({(p[0], p[1]) for p in points})
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def contains(poly, point):
    """True if the point is inside the polygon (ray casting)."""
    x, y = point[0], point[1]
    inside = False
    for a, b in _edges(poly):
        if (a[1] > y) != (b[1] > y):
            x_cross = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x < x_cross:
                inside = not inside
    return inside


def distance_to_segment(point, a, b):
    px, py = point[0], point[1]
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    dx, dy = bx - ax, by - ay
    length_sq = dx * dx + dy * dy
    t = 0.0 if length_sq == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length_sq))
    return math.dist((px, py), (ax + t * dx, ay + t * dy))


def distance_outside(poly, point):
    """How far a point sits outside a polygon (0 if it is inside)."""
    if contains(poly, point):
        return 0.0
    return min(distance_to_segment(point, a, b) for a, b in _edges(poly))


def rectangle(width, depth):
    """A rectangle centred on the origin, corners anticlockwise from the south-west."""
    w, d = width / 2.0, depth / 2.0
    return [(-w, -d), (w, -d), (w, d), (-w, d)]
