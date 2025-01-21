from btclib.ec import Point # , S256Point
import pytest 


def test_generic_elliptic_curve_real_field_point_comparison():
    p1 = Point(18, 77, 5, 7)
    p2 = Point(-1, -1, 5, 7)
    assert p1 != p2 

def test_generic_elliptic_curve_real_field_addition():    
    p_inf = Point(None, None, 5, 7)
    p1 = Point(18, 77, 5, 7)
    p2 = Point(-1, -1, 5, 7)
    p12 = Point(-0.14681440443213134,-2.5025513923312417, 5,7)
    assert p1+p_inf==p1, "Infinity point did not act zero-like. Supposed to act like the additive identity"
    assert p1+p2==p12
    assert p2+p2==2*p2, "Point addition did not equate to point  multiplication"

