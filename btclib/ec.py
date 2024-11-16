from math import isclose
from ff import S256FiniteElement
from constants import SECP256K1_A, SECP256K1_B, EC_ORDER, Gx, Gy
from ecds import Signature
from hashlib import sha256
import hmac

# elliptic curve point defintion

# want to define properties for points A, B and C to allow for point addition:

# 1) indentity -> I + A = A
#     I is a zero-like point. we consider it (inf,inf)
# 2) commutativity -> A + B = B + A
# 3) associativity -> (A + B) + C =  A + ( B + C)
# 4) invertibility -> A + (- A) = I


# from finite_field import FiniteElement
class Point:

    def __init__(self, x, y, a, b):
        """curve y^2 = x^3 + a*x + b
        curve parameterised by a & b"""

        # infinity point
        if x is None and y is None:
            self.x = None
            self.y = None
            self.a = a
            self.b = b
            return

        try:
            # testing over real numbers
            if not isclose(y**2, x**3 + a * x + b):
                err_msg = f"({x},{y}) does not lie on curve y^2 = x^3 + {a}*x + {b}"
                raise ValueError(err_msg)
        except TypeError:
            # testing over finite field elements
            if y**2 != x**3 + a * x + b:
                err_msg = f"({x},{y}) does not lie on curve y^2 = x^3 + {a}*x + {b}"
                raise ValueError(err_msg)

        self.x = x
        self.y = y
        self.a = a
        self.b = b

    def __repr__(self):
        return f"({self.x},{self.y})_{self.a}_{self.b}"

    def __eq__(self, other):
        return (
            self.x == other.x
            and self.y == other.y
            and self.a == other.a
            and self.b == other.b
        )

    def __neq__(self, other):
        return (
            self.x != other.x
            and self.y != other.y
            and self.a != other.a
            and self.b != other.b
        )

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            err_msg = f"{self} and {other} are not on the same curve"
            raise TypeError(err_msg)
        # self Point is infinite return Point other
        if self.x is None or self.y is None:
            return other
        # other Point is infinite return  Point self
        if other.x is None or other.y is None:
            return self
        # point self and point other produce zero-like point; P + (-P) = I
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        # self addition with Point at x axis intersect
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)
        if self.x != other.x:
            # 2 points with different x coordinates
            s = (other.y - self.y) / (other.x - self.x)
            x_new = s**2 - self.x - other.x
            y_new = s * (self.x - x_new) - self.y
            return self.__class__(x_new, y_new, self.a, self.b)
        if self.x == other.x and self.y == other.y:
            # 2 * point; tagent line to curve
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x_new = s**2 - 2 * self.x
            y_new = s * (self.x - x_new) - self.y
            return self.__class__(x_new, y_new, self.a, self.b)

    def __rmul__(self, value):
        # time-complexity(value)
        # value * self.Point
        # zero-like Point to aggregate result in
        result = self.__class__(None, None, self.a, self.b)
        for _ in range(value):
            result += self
        return result

    def __rmul__(self, value):
        # time-complexity(log_2(value))
        v = value
        p = self
        result = self.__class__(None, None, self.a, self.b)
        # until v is zero; 0b0000...
        while v:
            if v & 1:
                # if least sig bit-position 1, add to result
                result += p
            # double point value to correspond bit-positional value
            p += p
            # bit-wise right shift
            # e.g big-endian    v = 10110
            # then v >>=1 -> v = 1011
            # apply again
            # v >>=1 ->          v= 101
            v >>= 1
        return result

    def sign(self, hashed_doc):
        pass

    def verify(self, signature, r_x):
        pass


class S256Point(Point):

    def __init__(self, x, y, a=None, b=None):
        a = S256FiniteElement(SECP256K1_A)
        b = S256FiniteElement(SECP256K1_B)
        if type(x) == int:
            x = S256FiniteElement(x)
        if type(y) == int:
            y = S256FiniteElement(y)
        super().__init__(x, y, a, b)

    def __rmul__(self, value):
        value = value % EC_ORDER
        return super().__rmul__(value)

    def verify(self, z, sig):
        s_inv = pow(sig.value, EC_ORDER - 2, EC_ORDER)
        u = (z * s_inv) % EC_ORDER
        v = (sig.r_x * s_inv) % EC_ORDER
        total = u * self.__class__(Gx, Gy) + v * self
        return total.x.element == sig.r_x


class SecretKey:

    def __init__(self, sk):
        self.sk = sk
        self.pk = sk * S256Point(Gx, Gy)

    def hex(self):
        return f"{self.sk:x}".zfill(64)

    def deterministic_k(self, z):
        key = b"\x00" * 32
        val = b"\x01" * 32

        if z > EC_ORDER:
            z -= EC_ORDER
        z_bytes = z.to_bytes(32, "big")
        sk_bytes = self.sk.to_bytes(32, "big")

        key = hmac.new(key, val + b"\x00" + sk_bytes + z_bytes, sha256).digest()
        val = hmac.new(key, val, sha256).digest()
        key = hmac.new(key, val + b"\x01" + sk_bytes + z_bytes, sha256)
        val = hmac.new(key, val, sha256).digest()

        while True:
            val = hmac.new(key, val, sha256).digest()
            possible_k = int.from_bytes(val, "big")
            if possible_k >= 1 and possible_k < EC_ORDER:
                return possible_k
            key = hmac.new(key, val + b"\x00", sha256).digest()
            val = hmac.new(key, val, sha256).digest()

    def sign(self, z):
        # need to choose a unique k for each signature otherwise exposing our sk implicitly

        k = self.deterministic_k(z)
        r_x = (k * S256Point(Gx, Gy)).x.element
        k_inv = pow(k, EC_ORDER - 2, EC_ORDER)
        sig_val = (z + r_x * self.sk) * k_inv % EC_ORDER
        # choosing shortest signature given modulo EC_ORDER
        if sig_val > EC_ORDER / 2:
            sig_val = EC_ORDER - sig_val

        return Signature(r_x, sig_val)


def twice_hash256(s):

    return sha256(sha256(s).digest()).digest()


if __name__ == "__main__":

    # test cases
    fmt = 50
    sym = "#"
    print("represent point".center(fmt, sym))
    p1 = Point(18, 77, 5, 7)
    print(p1)
    p2 = Point(-1, -1, 5, 7)
    print(p2)
    print("comparison".center(fmt, sym))
    print(f"are {p1} and {p1} the same?", p1 == p1)
    print(f"are {p1} and {p2} the same?", p1 == p2)

    p_inf = Point(None, None, 5, 7)

    print("addition".center(fmt, sym))
    print(f"{p1}+{p_inf}={p1+ p_inf}")
    print(f"{p1}+{p2}={p1+p2}")
    print(f"{p2}+{p2}={p2+p2}")

    # NOTICE: we have defined
    # P = I + P
    # where I is the additive identity (zero-like element - infinite point)
    # we however have NOT defined
    # subtraction on the Point
    # P + (-P) = I

    # print('#'*fmt,'subtraction', '#'*fmt)
    # print( f'{p2}-{p2}={p2-p2}')
    print("multiplication".center(fmt, sym))
    coefs = [1, 100, 100000]

    for coef in coefs:
        print(f"{coef}*{p1}={coef*p1}")

    print("multiplication secp256k1 point".center(fmt, sym))
    s256p = S256Point(Gx, Gy)
    print(s256p)
    print(
        f"There are roughly {EC_ORDER:.1E} unique public points on the secp256k1 curve for the given generator point"
    )
    print(
        "do we return to zero-like point on secp256k1 curve?",
        EC_ORDER * s256p == S256Point(None, None),
    )
    print(EC_ORDER * s256p)
    # special case for y = 0 coordinate -> x axis intersection point
    # TO DO: find x coordinate of intersection point
    # test addition of point(x,0,5,7) should be infinity

    print("Testing signature verification")
    x = 0x887387E452B8EACC4ACFDE10D9AAF7F6D9A0F975AABB10D006E4DA568744D06C
    y = 0x61DE6D95231CD89026E286DF3B6AE4A894A3378E393E93A0F45B666329A0AE34
    hashed_document = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
    r_x = 0xAC8D1C87E51D0D441BE8B3DD5B05C8795B48875DFFE00B7FFCFAC23010D3A395
    sig_value = 0x68342CEFF8935EDEDD102DD876FFD6BA72D6A427A3EDB13D26EB0781CB423C4
    sig = Signature(r_x, sig_value)
    PK = S256Point(x, y)

    print(
        f"Does the signature correspond to the hashed doccument being signed?",
        PK.verify(hashed_document, sig),
    )

    print("Generating a signature")

    sk = int.from_bytes(twice_hash256(b"This is a test"), "big")
    hashed_document = int.from_bytes(twice_hash256(b"document being signed"), "big")
    # random k
    k = 24544566675677

    SK = SecretKey(sk)

    r_x = (k * S256Point(Gx, Gy)).x.element
    k_inv = pow(k, EC_ORDER - 2, EC_ORDER)
    sig_val = (hashed_document + r_x * SK.sk) * k_inv % EC_ORDER

    PK = SK.sk * S256Point(Gx, Gy)

    print("Public key/point:", PK)
    print("Hex of hashed document:", hex(hashed_document))
    print("Hex of x coord of random point:", hex(r_x))
    print("Signature value:", hex(sig_val))
    print(
        "Does the signature verfiy?:",
        PK.verify(hashed_document, Signature(r_x, sig_val)),
    )
