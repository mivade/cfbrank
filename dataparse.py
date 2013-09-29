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
sun_names = [x.strip() for x in open('data/SunNames2013.txt', 'r').readlines()]

def parseNCAACSV(filename, teamd={}):
    """Parse CSV schedule data file downloadable from the NCAA web
    site. Unfortunately, as of week 4 of the 2013 season, the NCAA
    schedules do not include scores, so this won't work."""
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

def parseSunCSV(filename, teamd={}):
    """Prase Sunshine Forecast data file."""
    if not isinstance(teamd, dict):
        raise RuntimeError("teamd must be a dictionary!")
    datafile = csv.reader(open(filename, 'r'))
    for i, row in enumerate(datafile):
        if i == 0 or len(row[2].split()) == 0:
            continue
        home, away = row[3], row[1]
        home_score, away_score = int(row[4]), int(row[2])
        ## if home == 'Texas' or away == 'Texas':
        ##     print home_score, home, "--", away, away_score
        ##     if home == 'Texas':
        ##         print home_score > away_score
        ##     else:
        ##         print away_score > home_score
        for school in [home, away]:
            if not teamd.has_key(school):
                FBS = school in sun_names
                teamd[school] = Team(school, "", FBS)
        home_won = home_score > away_score
        teamd[home].addOpponent(teamd[away], home_won)
        teamd[home].points_for += home_score
        teamd[home].points_against += away_score
        teamd[away].addOpponent(teamd[home], not home_won)
        teamd[away].points_for += away_score
        teamd[away].points_against += home_score
    return teamd

if __name__ == "__main__":
    teamd = {}
    parseSunCSV('data/sun4cast_FBS_2013.csv', teamd)
    Texas = teamd['Texas']
    Bama = teamd['Alabama']
    print 'Alabama: %i-%i' % (Bama.wins, Bama.losses)
    print 'Texas: %i-%i' % (Texas.wins, Texas.losses)
    if True:
        print "opponents:"
        for opp in Texas.opponents:
            print opp.school
    rankings = []
    for school in teamd.keys():
        team = teamd[school]
        if team.FBS:
            rankings.append([team.getScore(), team.school])
    rankings = sorted(rankings)[::-1]
    for i in range(25):
        print i+1, rankings[i][1], rankings[i][0]
