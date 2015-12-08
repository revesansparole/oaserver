from math import cos, exp, pi, sin
from numpy import array
from random import random
from scipy.optimize import leastsq

nb = 3
apl = array([random() for i in range(nb)])
ofs = array([random() * pi / 2 for i in range(nb)])

x_data = array([2 * pi * i / (nb * 100.) for i in range(nb * 100)])
y_data = array([sum([apl[i] * sin(v + ofs[i]) for i in range(nb)]) + random() / 10. for v in x_data])

def err(params):
    a = params[:nb]
    b = params[nb:]
    y = array([sum([a[i] * sin(v + b[i]) for i in range(nb)]) for v in x_data])
    e = y - y_data
    return e

guess = array([1.] * nb + [0.] * nb)


def main(a):
    opt = leastsq(err, guess)
    print opt

    print "guess", (err(guess) ** 2).sum()
    print "final", (err(opt[0]) ** 2).sum()

