#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

from configurator import configurator as cfgr
SIGMA, BETA, RHO, DT = cfgr('chaos.cfg')

def lorenz(x, y, z):
    """
    Test usage:
    lorenz(x_position, y_position, z_position)
    """
    sigma=SIGMA
    beta=BETA
    rho=RHO

    x_dot = sigma*(y-x)
    y_dot = x*(rho-z)-y
    z_dot = x*y-beta*z

    return x_dot, y_dot, z_dot
