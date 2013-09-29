cfbrank -- A college football ranking algorithm

Overview
========

With a rather small slate of games each year, ranking college football
teams is a rather puzzling challenge. Lots of different metrics can be
used, all with their own advantages and disadvantages. I've set out to
make a simple set of criteria with as few parameters as possible to
(hopefully!) come up with a sensible ranking of all Division I FBS
teams.

My general thoughts on how to determine the ranking of teams are as
follows. First and foremost, overall record matters. With far more
teams than there are slots in any one team's schedule, this is the
best first order metric to use. However, not all schedules are created
equal, and so the overall quality of resume must be considered, as
well.

Ranking schemes
===============

There are a few different ranking schemes that can be utilized, and
they are described individually below. 

Original method
---------------

The following method was the first implemented, and thus carries the
completely non-descriptive name of the "original" method. The general
ranking scheme is as follows. For a given team, :math:`T`, we consider
:math:`T`\'s winning percentage :math:`w_0` (with FCS penalties) and
:math:`T`\'s opponents' winning percentage, :math:`w_1` (with FCS
penalties). Then :math:`T`\'s point total is given by

.. math:: P = A_0 w_0 + A_1 w_1,

where A_i are constants to weight the importance of each
parameter. There is one caveat. Scheduling FCS teams shouldn't be
rewarded [#]_, and therefore a FCS win counts as a fraction of a whole
win, where that fraction is another tunable parameter, B. A loss to an
FCS team counts the same as a loss to an FBS team.

AWPMOV Method
-------------

The AWPMOV method considers a team's wins, opponents' winning
percentage, and margin of victory (actually point differential as
currently implemented). The score is calculated by

.. math:: P = A_0 w_0 + A_1 w_1 + A_2 w_2,

where :math:`w_0` is the winning percentage, :math:`w_1` is the
aggregate winning percentage of opponents that the team has beaten,
and :math:`w_2` is the normalized point differential.

Park-Newman method
------------------

See `J. Park and M.E.J. Newman, J. Stat. Mech. 2005, 10014 (2005)`__
or `arXiv:physics/0505169`__. This method is not yet implemented.

__ http://iopscience.iop.org/1742-5468/2005/10/P10014
__ http://arxiv.org/abs/physics/0505169

Data entry
==========

Perhaps the most daunting thing about developing a CFB ranking
algorithm is entering a season's worth of data (even if only one week
at a time!). Luckily, there are a number of places on the web where
basic data can be downloaded in simple CSV format. Right now, cfbrank
has functionality provided by the dataparse module to parse CSV files
from `Sunshine Forecast`_, the NCAA_ [#]_, and `cfbstats.com`_ (soon).

.. _Sunshine Forecast: http://www.repole.com/sun4cast/data.html
.. _NCAA: http://www.ncaa.org/wps/wcm/connect/public/NCAA/Resources/Stats/Football/index.html
.. _cfbstats.com: http://www.cfbstats.com/blog/college-football-data/

.. [#] One complication is that not all teams play the same number of
       games. The base 12 game schedule is standard, but the "Hawaii
       Rule" allows teams playing at Hawaii to schedule a 13th regular
       season game to help recoup costs associated with travel. Then
       there are conference championship games (CCGs). I am not a big
       fan of the divisional format of deciding who plays in these, as
       it often happens that one division in any given year is much
       stronger than the other. Furthermore, as not all conferences
       are large enough to qualify for a CCG, it seems somewhat unfair
       to provide an extra rankings boost to a team that participates
       in a CCG in a conference where their opponent is of much lower
       quality.

.. [#] As of September 2013, the downloadable NCAA schedules no longer
       include scores, making this data source deprecated.
