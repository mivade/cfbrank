"""
cfbrank -- A college football ranking algorithm

conference.py: Defines the Conference class for generating rankings
and other statistical information on an athletic conference as a
whole.

Written by Michael V. DePalatis <depalatis@gmail.com>

cfbrank is distributed under the terms of the GNU GPL.
"""

class Conference:
    """Utility class for doing statistical analysis for conferences."""
    def __init__(self, members=[]):
        self.members = members

    def getWinningPercentage(self, count_FCS=True, FCS_penalty=False):
        """Calculate the conference's winning percentage. If count_FCS
        is True, the result will fully count wins over FCS teams,
        otherwise it will only look at the FBS games played. If
        FCS_penalty is True, count FCS games, but as a win reduced by
        the B factor."""
        # TODO: FCS stuff
        wins, games = 0, 0
        for team in self.members:
            wins += team.wins
            games += team.wins + team.losses
        return wins/float(games)
