"""cfbrank -- A college football ranking algorithm

Written by Michael V. DePalatis <depalatis@gmail.com>

cfbrank is distributed under the terms of the GNU GPL.

"""

import os
import os.path
import shutil
import json
import tempfile
import urllib
import sqlite3
import argparse
import logging
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
    def __init__(self, data, **kwargs):
        """Creates a new CFBRank object with the given data.

        Parameters
        ----------
        data : pd.DataFrame   
            Data table consisting of season team statistics.

        """
        self.data = data

    def rank(self, algorithm='AWPMOV'):
        """Rank the teams using the specified algorithm."""
        assert algorithm in config['algorithms']

    def _rank_original(self):
        """'Original' ranking method."""

    def _rank_awpmov(self):
        """AWPMOV ranking method."""

    def _rank_park_newman(self):
        """Park-Newman ranking method."""
        raise NotImplementedError("Park-Newman not yet implemented.")

class Team(object):
    """Team object for performing rankings and computing other
    statistics.

    """
    def __init__(self, school, nickname='', division='FBS', conference=None):
        """Create a new team.

        Parameters
        ----------
        school : str
            The name of the school as used in the database, e.g.,
            "Texas".
        nickname : str
            Team nickname of the team, e.g., "Longhorns".
        fbs : str
            String describing what division the team is in. See the
            config file for valid options.
        conference : str, optional
            The name of the conference the team belongs to if
            applicable.

        """
        assert isinstance(school, (str, unicode))
        self.school = school
        
        assert isinstance(nickname, (str, unicode))
        self.nickname = nickname
        
        assert isinstance(division, (str, unicode))
        assert division in config['divisions']
        self.division = division
        
        assert isinstance(conference, (str, unicode)) or conference is None
        self.conference = conference

    def get_record(self, data):
        """Determine the team's record.

        Parameters
        ----------
        data : pd.DataFrame
            Database of season statistics.

        Returns
        -------
        wins : int
            Number of wins.
        losses : int
            Number of losses.

        """
        assert isinstance(data, pd.DataFrame)
        matches = data.TeamName.str.match(r'^{0}$'.format(self.school))
        idx = [i for i, match in enumerate(matches) if match]
        points_for = data.ScoreOff[idx].values
        points_against = data.ScoreDef[idx].values
        diff = points_for - points_against
        wins, losses = 0, 0
        for game in diff:
            if game > 0:
                wins += 1
            else:
                losses += 1
        return wins, losses

    def compute_raw_score(self, data, algorithm='AWPMOV'):
        """Compute a raw score using the specified algorithm."""

class Conference(object):
    """Conference object for computing conference statistics."""

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
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Load data
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

    # Testing of records computing
    texas = Team('Texas', 'Longhorns', conference='Big 12')
    print texas.get_record(data)
    tOSU = Team('Ohio State', 'Buckeyes', conference='B1G')
    print tOSU.get_record(data)
