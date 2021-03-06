# Autogenerated with SMOP version 0.23
# main.py ../t_tide1.3/t_getconsts.m -o ../t_tide_py/t_getconsts.py
from __future__ import division
import numpy as np
from scipy.io import loadmat,savemat
import os
from t_astron import t_astron

def t_getconsts(ctime):
    """T_GETCONSTS Gets constituent data structures
     [CONST,SAT,SHALLOW]=T_GETCONSTS returns data structures holding
     information for tidal analyses.

     Variables are loaded from 't_constituents.mat', otherwise the
     ascii files 'tide3.dat' (provided with the IOS analysis package)
     and 't_equilib.dat' are read, and the results stored in
     't_constituents.mat' for future use.

     [...]=T_GETCONSTS(TIME) recomputes the frequencies from the
     rates-of-change of astronomical parameters at the matlab TIME given.
     R. Pawlowicz 11/8/99
     Version 1.0
    """

    base_dir = os.path.join(os.path.dirname(__file__), 'data')
    if os.path.exists(os.path.join(base_dir,'t_constituents_const.npy')) & os.path.exists(os.path.join(base_dir,'t_constituents_sat.npy')) & os.path.exists(os.path.join(base_dir,'t_constituents_shallow.npy')):
        const=np.load(os.path.join(base_dir,'t_constituents_const.npy'))
        const=const[()]
        sat=np.load(os.path.join(base_dir,'t_constituents_sat.npy'))
        sat=sat[()]
        shallow=np.load(os.path.join(base_dir,'t_constituents_shallow.npy'))
        shallow=shallow[()]
    else:
        print "You do not have t_constituents_*.npy saved from t_constituents.mat, to much work to convert code get them for now."
        const=[]
        sat=[]
        shallow=[]
        #old code to generate t_constituents.mat, just the csv saved instead less work.
        """nc = 146
        empvec = np.zeros(shape=(nc, 1), dtype='float64') + NaN
        const = type('struct', (), {})()
        nsat = 162
        sat = type('struct', (), {})()
        nshl = 251
        shallow = type('struct', (), {})()
        fid = open('tide3.dat')
        if fid == - 1:
            error("Can't find constituent input file 'tide3.dat'!")
        l = fgetl(fid)
        k = 0
        while max(l.shape) > 24:

            k = k + 1
            const.name(k, :) = l[4:8]
            const.freq(k) = sscanf(l[13:25], '\n %f')
            nm = l[29:l.shape[0]] + '    '
            const.kmpr(k, :) = nm[0:4]
            l = fgetl(fid)

        # Coefficients without comparison constituent are not used
        # in the present configuration.
        const.df = np.zeros(shape=(max(const.freq.shape), 1), dtype='float64')
        for k in np.flatnonzero(any(const.kmpr.T != ' ')):
            j1 = strmatch(const.kmpr(k, :), const.name)
            const.ikmpr(k) = j1
            const.df(k) = abs(const.freq(j1) - const.freq(k))
        const.df(1) = 0
        # Leave df(1)=0 to remove z0 from this list
        # Skip blank lines.
        l = fgetl(fid)
        l = fgetl(fid)
        l = fgetl(fid)
        # Now decode the doodson# and satellite information.
        k = 0
        while max(l.shape) > 10:

            kon = l[6:10]
            j1 = strmatch(kon, const.name)
            vals = sscanf(l[10:l.shape[0]], '\n %f')
            const.doodson(j1, :) = vals[0:6]
            const.semi(j1) = vals[6]
            if vals[7] != 0:
                # Satellite data follows
                const.nsat(j1) = vals[7]
                m = vals[7]
                sats = np.array([])
                while m > 0:

                    l = fgetl(fid)
                    l = l + ' 0'
                    for n in range(1, (np.min(m, 3) +1)):
                        if l[(np.dot(n, 23) + 10 -1)] == ' ':
                            l[(np.dot(n, 23) + 10 -1)] = '0'
                        sats = sats + l[(np.dot(n, 23) + np.array([range(- 11, 9)]).reshape(1, -1) -1)] + ' ' + l[(np.dot(n, 23) + 10 -1)] + ' '
                        m = m - 1

                vals = sscanf(sats, '\n %f', np.array([6, np.inf]).reshape(1, -1)).T
                nst = vals.shape[0]
                if nst != const.nsat(j1):
                    error('# of satellites does not match input')
                sat.deldood(k + np.array([range(1, (nst +1))]).reshape(1, -1), :) = vals[:, 0:3]
                sat.phcorr(k + np.array([range(1, (nst +1))]).reshape(1, -1)) = vals[:, 3]
                sat.amprat(k + np.array([range(1, (nst +1))]).reshape(1, -1)) = vals[:, 4]
                sat.ilatfac(k + np.array([range(1, (nst +1))]).reshape(1, -1)) = vals[:, 5]
                sat.iconst(k + np.array([range(1, (nst +1))]).reshape(1, -1)) = j1
                const.isat(j1) = k + 1
                k = k + nst
            l = fgetl(fid)

        # Shallow water constituents - we need to get these in terms
        # of their original!
        l = fgetl(fid)
        k = 0
        while max(l.shape) > 3:

            kon = l[6:10]
            j1 = strmatch(kon, const.name)
            nsh = sscanf(l[10:12], '\n %d')
            const.nshallow(j1) = nsh
            shallow.iconst(k + np.array([range(1, (nsh +1))]).reshape(1, -1)) = j1
            for m in range(1, (nsh +1)):
                shallow.coef(k + m) = sscanf(l[(np.dot(m, 15) + np.array([range(0, 4)]).reshape(1, -1) -1)], '\n %f')
                shallow.iname(k + m) = strmatch(l[(np.dot(m, 15) + np.array([range(5, 7)]).reshape(1, -1) -1)], const.name)
            const.ishallow(j1) = k + 1
            k = k + nsh
            l = fgetl(fid)

        # Get the equilibrium amplitudes from Doodson's development.
        fid = open('t_equilib.dat')
        if fid == - 1:
            error("Can't find equilibrium amplitude dataset")
        # Now parse file, which is in format Name species A B.
        l = fgetl(fid)
        while l[0] == '\n %':

            l = fgetl(fid)

        while max(l.shape) > 1:

            j1 = strmatch(l[0:4], const.name)
            vals = sscanf(l[4:l.shape[0]], '\n %f')
            if vals[1] != 0:
                const.doodsonamp(j1) = vals[1] / 100000.0
                const.doodsonspecies(j1) = vals[0]
            else:
                const.doodsonamp(j1) = vals[2] / 100000.0
                const.doodsonspecies(j1) = - vals[0]
            l = fgetl(fid)

        savemat('t_constituents', 'const', 'sat', 'shallow')"""
    if ctime.size!=0:
        # If no time, just take the "standard" frequencies,
        # otherwise compute them from derivatives of astro
        astro, ader = t_astron(ctime) # nargout=2
        # parameters. This is probably a real overkill - the
        ii=np.isfinite(const['ishallow']).flatten()
        # diffs are in the 10th decimal place (9th sig fig).
        const['freq'][~ii] = (np.dot(const['doodson'][~ii, :], ader)) / (24)
        for k in np.flatnonzero(ii):
            ik = ( const['ishallow'][k]-1 + np.array( range(0,const['nshallow'][k]) ) ).astype(np.int16)
            const['freq'][k] = np.sum(np.multiply(np.squeeze(const['freq'][shallow['iname'][ik]-1]), np.squeeze(shallow['coef'][ik])))

    return const, sat, shallow
