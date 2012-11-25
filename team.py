"""
cfbrank -- A college football ranking algorithm

team.py: Defines the Team class representing a CFB Division I team.

Written by Michael V. DePalatis <depalatis@gmail.com>

cfbrank is distributed under the terms of the GNU GPL.
"""

from params import *

class Team:
    """Class representing a CFB team."""
    def __init__(self, school, nickname, FBS=True):
        """Create a new team for the school given."""
        if not isinstance(school, str):
            raise TypeError("school must be a string.")
        if not isinstance(nickname, str):
            raise TypeError("nickname must be a string.")
        if not isinstance(FBS, bool):
            raise TypeError("FBS must be a bool.")
        self.school = school
        self.nickname = nickname
        self.FBS = FBS
        self.wins = 0
        self.losses = 0
        self.num_FCS_opponents = 0
        self.opponents = []
        self.record = []

    def addOpponent(self, opponent, won):
        """Adds opponent to this team's opponents list and marks
        whether it was a win (True) or loss (False). If the opponent
        is FCS and the team won, this makes a note of an FCS game. If
        it's a loss, it treats the opponent as though it were an FBS
        team."""
        win = 1
        if type(won) == bool:
            if won:
                self.wins += 1
            else:
                self.losses += 1
                win = 0
            if not opponent.FBS and won:
                self.num_FCS_opponents += 1
        else:
            raise TypeError("won must be a bool.")
        self.opponents.append(opponent)
        self.record.append(win)

    def getWinningPercentage(self):
        """Returns the team's winning percentage."""
        return self.wins/float(self.wins+self.losses)

    def getOpponentsWinningPercentage(self, use_penalties=True):
        """Returns the winning percentage of all opponents taking into
        account the penalties for beating FCS teams if use_penalties
        is True."""
        wins, games = 0, 0
        for opponent in self.opponents:
            wins += opponent.wins
            games += opponent.wins + opponent.losses
            if use_penalties:
                wins -= opponent.num_FCS_opponents*(1 - PENALTIES)
        return wins/float(games)
        
    def getScore(self, weights=WEIGHTS, penalties=PENALTIES,
                 method="original"):
        """Returns the raw score of the team using the scoring method
        provided. Valid options are 'original', 'adjusted winning
        percentage' and 'park-newman'."""

        # Original method. See the readme for details.
        if method == "original":
            games, N = self.wins + self.losses, self.num_FCS_opponents
            w0 = self.getWinningPercentage()
            w0 = w0 - N*(1 - penalties)/float(games)
            w0_oppts = self.getOpponentsWinningPercentage()
            w1 = w0_oppts/float(games)
            return weights[0]*w0 + weights[1]*w1

        # Adjusted winning percentage rankings. See the readme for
        # details.
        elif method == "adjusted winning percentage":
            w0, w1 = 0., 0.
            games = self.wins + self.losses
            for i, opponent in enumerate(self.opponents):
                w0 += self.record[i]
                if opponent.FBS and self.record[i] == 1:
                    w1 += opponent.getWinningPercentage()
                else:
                    w1 += penalties
            return (weights[0]*w0 + weights[1]*w1)/float(games)

        # Park-Newman one-parameter rankings
        # See J. Park and M.E.J. Newman, J. Stat. Mech. 2005, 10014
        # (2005) or arXiv:physics/0505169
        elif method == "park-newman":
            raise NotImplementedError("Park-Newman rankings not yet implemented.")
        else:
            raise ValueError("Unknown scoring method: '%s'." % method)
            
