"""
cfbrank -- A college football ranking algorithm

format.py: Defines functions for output of rankings in various
formats.

Written by Michael V. DePalatis <depalatis@gmail.com>

cfbrank is distributed under the terms of the GNU GPL.
"""

def rCFB(teamd, rankings, N=25):
    """Format rankings for Reddit tables for posting in
    /r/CFB. Displays the top N teams in the dictionary of teams teamd
    and the rankings array."""
    top = rankings[0][0]
    out = '|Rank|School|Record|Score|\n' + \
          '|---:|:---|:---|:---|---:|\n'
    for i in range(N):
        school = teamd[rankings[i][1]]
        out += '|' + str(i+1) + '|' + school.school + \
               '|%i - %i|' % (school.wins, school.losses) + \
               '%.5f|\n' % (rankings[i][0]/top)
    return out

def plain(teamd, rankings, N=25):
    """Format rankings for plaintext output. Displays the top N teams
    in the dictionary of teams teamd and the rankings array."""
    top = rankings[0][0]
    out = ''
    for i in range(N):
        school = teamd[rankings[i][1]]
        out +=  str(i+1) + ' ' + school.school + \
               ' (%i-%i) ' % (school.wins, school.losses) + \
               '%.5f\n' % (rankings[i][0]/top)
    return out
