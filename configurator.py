#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

def configurator(file_name='setup.cfg'):
    """
    Usage:
    CHANNEL, PLANE, SCOPE, BUFFER = cfgr('setup.cfg')
    SIGMA, BETA, RHO, DT = cfgr('chaos.cfg')
    """

    configure = []
    configuration = open(file_name, 'r').readlines()
    for line in configuration:
        if "Channel:" in line:
            channel = str(line[:].split(":", 1)[1])
            channel = channel.replace('\n', '').replace('\0', '').replace(' ', '')
            configure.append(channel)

        if "Plane:" in line:
            plane = str(line[:].split(":", 1)[1])
            plane = plane.replace('\n', '').replace('\0', '').replace(' ', '')
            plane = abs(int(plane))
            configure.append(plane)

        if "Scope:" in line:
            scope = str(line[:].split(":", 1)[1])
            scope = scope.replace('\n', '').replace('\0', '').replace(' ', '')
            scope = abs(int(scope))
            configure.append(scope)

        if "Buffer:" in line:
            BUFFER = str(line[:].split(":", 1)[1])
            BUFFER = BUFFER.replace('\n', '').replace('\0', '').replace(' ', '')
            BUFFER = abs(int(BUFFER))
            configure.append(BUFFER)

        if "Sigma:" in line:
            sigma = str(line[:].split(":", 1)[1])
            sigma = sigma.replace('\n', '').replace('\0', '').replace(' ', '')
            sigma = float(sigma)
            configure.append(sigma)

        if "Beta:" in line:
            beta = str(line[:].split(":", 1)[1])
            beta = beta.replace('\n', '').replace('\0', '').replace(' ', '')
            beta = float(beta)
            configure.append(beta)

        if "Rho:" in line:
            rho = str(line[:].split(":", 1)[1])
            rho = rho.replace('\n', '').replace('\0', '').replace(' ', '')
            rho = float(rho)
            configure.append(rho)

        if "Gamma:" in line:
            gamma = str(line[:].split(":", 1)[1])
            gamma = gamma.replace('\n', '').replace('\0', '').replace(' ', '')
            gamma = float(gamma)
            configure.append(gamma)

        if "Alpha:" in line:
            alpha = str(line[:].split(":", 1)[1])
            alpha = rho.replace('\n', '').replace('\0', '').replace(' ', '')
            alpha = float(alpha)
            configure.append(alpha)

        if "dt:" in line:
            dt = str(line[:].split(":", 1)[1])
            dt = dt.replace('\n', '').replace('\0', '').replace(' ', '')
            dt = float(dt)
            configure.append(dt)
    return configure



def reconfigure(file_name='config.cfg', keyword="Plane",value='0'):

    filein = open(file_name,'r+b')
    file_read = filein.read()

    indexofKeyword = file_read.index(str(keyword))
    size = len(keyword)

    filein.seek(indexofKeyword + size + 2)
    filein.write(str(value))
    filein.close()



if __name__ == '__main__':
    configurator()
