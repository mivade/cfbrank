"""
cfbrank.py

cfbrank -- A college football ranking algorithm

Written by Michael V. DePalatis <depalatis@gmail.com>

cfbrank is distributed under the terms of the GNU GPL.
"""

from numpy import arange
from team import Team
from conference import Conference
from dataparse import parseNCAACSV
import format
from params import *

teamd = parseNCAACSV('data/NCAA_FBS_2012.csv')

if True:
    print "'original' method:\n"
    weights = 0.5, 2.
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
    print "'adjusted winning percentage' method:\n"
    weights = 1., 1.
    penalties = 0.5
    rankings = []
    for school in teamd.keys():
        team = teamd[school]
        if team.FBS:
            rankings.append([
                team.getScore(weights, penalties, 'adjusted winning percentage'),
                team.school])
    rankings = sorted(rankings)[::-1]
    print format.plain(teamd, rankings)
