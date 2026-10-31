from kit import geometry as geo

SQUARE = [(0, 0), (10, 0), (10, 10), (0, 10)]


def test_area_and_perimeter():
    assert geo.area(SQUARE) == 100
    assert geo.area(list(reversed(SQUARE))) == 100
    assert geo.perimeter(SQUARE) == 40
    assert geo.shortest_edge([(0, 0), (4, 0), (4, 9), (0, 9)]) == 4


def test_convex_hull_drops_inner_points():
    hull = geo.convex_hull(SQUARE + [(5, 5), (2, 8)])
    assert sorted(hull) == sorted(SQUARE)


def test_contains_and_distance_outside():
    assert geo.contains(SQUARE, (5, 5))
    assert not geo.contains(SQUARE, (15, 5))
    assert geo.distance_outside(SQUARE, (5, 5)) == 0
    assert geo.distance_outside(SQUARE, (13, 5)) == 3
    assert abs(geo.distance_outside(SQUARE, (13, 14)) - 5) < 1e-9


def test_rectangle_is_centred():
    r = geo.rectangle(20, 10)
    assert geo.area(r) == 200
    assert sum(x for x, _ in r) == 0 and sum(y for _, y in r) == 0
