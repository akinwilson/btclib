from btclib.ec import Point, S256Point
from btclib.constants import EC_ORDER,Gx, Gy
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


coefs = [(1,Point(18,77, 5,7)),
         (100,  Point(12.03298143347783,42.53765487429396, 5,7)),
         (100000, Point(3.1937718892639015,7.452912452244291, 5,7))]
@pytest.mark.parametrize("multiplication_coef, point", coefs)

def test_generic_elliptic_curve_over_real_field_point_mulitiplication(multiplication_coef, point):
    p1 = Point(18, 77, 5, 7)
    assert multiplication_coef * p1 == point, f"got: {point}, expected: {multiplication_coef * p1}"

def test_secp256k1_elliptic_curve_over_finite_field_point_order():
    # print(f"There are roughly {EC_ORDER:.1E} unique public points on the secp256k1 curve for the given generator point")
    btc_generator_point = S256Point(Gx, Gy)
    assert EC_ORDER * btc_generator_point == S256Point(None, None), f"Multiplying the generator point by the order of the field does not return infinite point/ zero-like point"


