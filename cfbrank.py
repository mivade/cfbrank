"""
cfbrank.py

cfbrank -- A college football ranking algorithm

Written by Michael V. DePalatis <depalatis@gmail.com>

cfbrank is distributed under the terms of the GNU GPL.
"""

from numpy import arange
from team import Team
from conference import Conference
from dataparse import parseNCAACSV, parseSunCSV
import format
from params import *

#teamd = parseNCAACSV('data/NCAA_FBS_2013.csv')
teamd = parseSunCSV('data/sun4cast_FBS_2013.csv')

if False:
    print "'original' method:\n"
    weights = (0.5, 2.)
    penalties = 0.9
    rankings = []
    for school in teamd.keys():
        team = teamd[school]
        if team.FBS:
            rankings.append([
                team.getScore(weights, penalties, 'original'),
                team.school])
    rankings = sorted(rankings)[::-1]
    print format.plain(teamd, rankings)

if True:
    print "AWPMOV method:\n"
    weights = (3., 2., 1.)
    penalties = 0.4
    rankings = []
    for school in teamd.keys():
        team = teamd[school]
        if team.FBS:
            rankings.append([
                team.getScore(weights, penalties, 'AWPMOV'),
                team.school])
    rankings = sorted(rankings)[::-1]
    print format.plain(teamd, rankings)
    print format.rCFB(teamd, rankings)

    UT = teamd['Texas']
    print UT.record
    ## tOSU = teamd['Ohio State']
    #print tOSU.record
    #print format.plain(teamd, rankings, 100)

