"""cfbrank -- A college football ranking algorithm

Written by Michael V. DePalatis <depalatis@gmail.com>

cfbrank is distributed under the terms of the GNU GPL.

"""

from __future__ import division
import os
import os.path
import shutil
import json
import tempfile
import urllib
import argparse
import logging
import numpy as np
import pandas as pd
#import formatting

# Load configuration
# =============================================================================

with open('cfbrank.json', 'r') as config_file:
    config = json.load(config_file)

# Classes
# =============================================================================
    
class CFBRank(object):
    """Object for ranking CFB teams."""
    def __init__(self, data, algorithm='AWPMOV', **kwargs):
        """Creates a new CFBRank object with the given data.

        Parameters
        ----------
        data : pd.DataFrame   
            Data table consisting of season team statistics.
        algorithm : str, optional
            Specifies the default ranking algorithm to use.

        """
        assert isinstance(data, pd.DataFrame)
        self.data = data
        assert isinstance(algorithm, (str, unicode))
        assert algorithm in config['algorithms']
        self.algorithm = algorithm

        # Create a dictionary of teams.
        teams = pd.read_csv(config['team_file'])
        team_names = teams.School.values
        self.teams = {}
        for i, team in enumerate(team_names):
            logging.debug('Adding {0}...'.format(team))
            self.teams[team] = Team(
                self.data, team,
                nickname=teams.Nickname[i],
                division=teams.Division[i],
                conference=teams.Conference[i]
            )

    def rank(self, normalize_scores=True):
        """Rank the teams using the specified algorithm.

        Parameters
        ----------
        normalize_scores : bool, optional
            Normalize the ranking scores so that the first place team
            has a score of 1.0. Defaults to True.

        Returns
        -------
        scores : np.ndarray
            ...

        """
        scores = np.zeros(len(self.teams))
        for i, name in enumerate(self.teams):
            scores[i] = self.teams[name].compute_raw_score(algorithm=self.algorithm)
        if normalize_scores:
            scores = scores/scores.max()
        return scores

class Team(object):
    """Team object for performing rankings and computing other
    statistics.

    """
    def __init__(self, data, school, **kwargs):
        """Create a new team.

        Parameters
        ----------
        data : pd.DataFrame
            Season statistics data.
        school : str
            The name of the school as used in the database, e.g.,
            "Texas".

        Keyword arguments
        -----------------
        nickname : str
            Team nickname of the team, e.g., "Longhorns".
        division : str
            String describing what division the team is in. See the
            config file for valid options.
        conference : str
            The name of the conference the team belongs to if
            applicable.

        """
        # Parse arguments and check they are the right types.
        assert isinstance(data, pd.DataFrame)
        self.data = data
        
        assert isinstance(school, (str, unicode))
        self.school = school

        self.nickname = kwargs.get('nickname', '')
        assert isinstance(self.nickname, (str, unicode))

        self.division = kwargs.get('division', 'FBS')
        assert isinstance(self.division, (str, unicode))
        assert self.division in config['divisions']

        self.conference = kwargs.get('conference', None)
        assert isinstance(self.conference, (str, unicode)) or self.conference is None

        # Compute points and win/loss record.
        matches = self.data.TeamName.str.match(r'^{0}$'.format(self.school))
        self._idx = [i for i, match in enumerate(matches) if match]
        self.points_for = self.data.ScoreOff[self._idx].values
        self.points_against = self.data.ScoreDef[self._idx].values
        diff = self.points_for - self.points_against
        self.wins, self.losses = 0, 0
        for game in diff:
            if game > 0:
                self.wins += 1
            else:
                self.losses += 1

    def _get_opponents_winning_percentage(self):
        """Compute the aggregate winning percentage of the team's
        opponents.

        """

    def compute_raw_score(self, algorithm='AWPMOV'):
        """Compute a raw score using the specified algorithm."""
        if algorithm not in config['algorithms']:
            raise RuntimeError("Unrecognized algorithm.")
        logging.debug('Computing raw score for ' + self.school)
        if algorithm == 'AWPMOV':
            w = np.zeros(3)
            weights = config['weights']['AWPMOV']
            try:
                w[0] = self.wins/self.losses
            except ZeroDivisionError:
                w[0] = 1.0
            #w[1] = self._get_opponents_winning_percentage(data)
            w[2] = self.points_for.sum() - self.points_against.sum()
            w = weights*w
        logging.debug('w = ' + str(w))
        return w.sum()

class Conference(object):
    """Conference object for computing conference statistics."""
    def __init__(self, short_name, long_name='', teams=[]):
        """Create a new Conference object.

        Parameters
        ----------
        short_name : str
            The "short" name for the conference, e.g., "SEC".
        long_name : str
            The "long" name for the conference, e.g., "Southeastern
            Conference".
        teams : list
            A list of strings giving the names of teams in the
            conference.

        """
        assert isinstance(short_name, (str, unicode))
        self.short_name = short_name
        assert isinstance(long_name, (str, unicode))
        self.long_name = long_name
        self.team_names = teams

    def get_record(self):
        """Return the overall conference record, i.e., the total
        number of wins and losses of all teams in the conference.

        """

# Main
# =============================================================================

if __name__ == "__main__":
    # Parse command line options
    parser = argparse.ArgumentParser(description="College football ranking")
    parser.add_argument(
        '-u', '--update-database',
        help="Force re-downloading the data file.",
        action='store_true'
    )
    parser.add_argument(
        '--purge',
        help="Remove the database file and backup file prior to doing anything else.",
        action='store_true'
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Show more output. Useful for debugging purposes.",
        action='store_true'
    )
    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Load season statistics data
    conf_file = config['filename']
    backup_file = conf_file + '.bak'
    if args.purge and os.path.exists(conf_file):
        logging.info("Purging database...")
        os.remove(conf_file)
        try:
            os.remove(backup_file)
        except:
            pass
    if not os.path.exists(conf_file) or args.update_database:
        logging.info("Downloading statistics...")
        try:
            shutil.move(conf_file,
                        os.path.join(os.path.dirname(conf_file), backup_file))
        except IOError:
            pass
        with open(config['filename'], 'w') as dfile:
            dfile.write(urllib.urlopen(config['data_url']).read())
    data = pd.read_csv(config['filename'])

    # Perform the rankings
    ranker = CFBRank(data)
    scores = ranker.rank()
    idx = scores.argsort()[::-1]
    print np.array(ranker.teams.keys(), dtype=str)[idx]
