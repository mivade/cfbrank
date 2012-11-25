"""
cfbrank -- A college football ranking algorithm

dataparse.py: A module for parsing datafiles containing the relevant
statistics for the cfbrank algorithm. See the readme for full details
on the data formats and sources supported.

Written by Michael V. DePalatis <depalatis@gmail.com>

cfbrank is distributed under the terms of the GNU GPL.
"""

import csv
from team import Team
from conference import Conference

ncaa_names = [x.strip() for x in open('data/NCAANames2012.txt', 'r').readlines()]

def parseNCAACSV(filename, teamd={}):
    """Parse CSV schedule data file downloadable from the NCAA web
    site."""
    if not isinstance(teamd, dict):
        raise RuntimeError("teamd must be a dictionary!")
    datafile = csv.reader(open(filename, 'r'))
    for i, row in enumerate(datafile):
        if i == 0 or row[5] == '':
            continue
        school = row[1]
        if not teamd.has_key(school):
            teamd[school] = Team(school, "", True)
        won = int(row[5]) > int(row[6])
        opp_name = row[4]
        if not teamd.has_key(opp_name):
            FBS = opp_name in ncaa_names
            teamd[opp_name] = Team(opp_name, "", FBS)
        opponent = teamd[opp_name]
        #print opp_name
        teamd[school].addOpponent(opponent, won)
    return teamd

if __name__ == "__main__":
    teamd = {}
    parseNCAACSV('data/NCAA_FBS_2012.csv', teamd)
    ## ND = teamd['Notre Dame']
    ## Texas = teamd['Texas']
    ## Bama = teamd['Alabama']
    ## Akron = teamd['Akron']
    ## print 'Notre Dame: %i-%i' % (ND.wins, ND.losses)
    ## print 'Alabama: %i-%i' % (Bama.wins, Bama.losses)
    ## print 'Akron: %i-%i' % (Akron.wins, Akron.losses)
    ## print 'Texas: %i-%i' % (Texas.wins, Texas.losses)
    ## if True:
    ##     print "opponents:"
    ##     for opp in Texas.opponents:
    ##         print opp.school
    rankings = []
    for school in teamd.keys():
        team = teamd[school]
        if team.FBS:
            rankings.append([team.getScore(), team.school])
    rankings = sorted(rankings)[::-1]
    for i in range(25):
        print i+1, rankings[i][1], rankings[i][0]
