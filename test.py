"""test de prod cruz y magnitud"""

from fractions import Fraction as F
from gauss_bot.models import Vector

u = Vector([F(4), F(1)])
t = Vector([F(-2), F(3)])

v = Vector([F(-3), F(4), F(6)])
w = Vector([F(-1), F(-2), F(3)])

print(v.magnitud())
