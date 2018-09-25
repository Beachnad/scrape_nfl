nfl_injury_links = {
    2014: {
        1: 'https://web.archive.org/web/20140908193954/nfl.com/injuries',
        2: 'https://web.archive.org/web/20140915051129/nfl.com/injuries',
        3: 'https://web.archive.org/web/20140915051129/nfl.com/injuries',
        4: 'https://web.archive.org/web/20140929003950/nfl.com/injuries',

    }
}

WEEKDAY = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}

from datetime import date, timedelta

def n_dayofweek(yr, mo, dayofweek, n):
    i, cnt = 0, 0
    while i <= 31:
        i += 1
        d = date(yr, mo, i)
        cnt += 1 if WEEKDAY[d.weekday()].lower() == dayofweek.lower() else 0
        if cnt == n:
            return d

nfl_injury_links = {}
for yr in range(2012, 2018):
    start = n_dayofweek(yr, 9, 'Monday', 1) + timedelta(days=2)
    nfl_injury_links[yr] = {}
    for wk in range(1, 18):
        wk_date = start + timedelta(days=7 * (wk))
        url = 'https://web.archive.org/web/{}{}{}/http://www.nfl.com/injuries'.format(
            str(wk_date.year).zfill(4), str(wk_date.month).zfill(2), str(wk_date.day).zfill(2)
        )
        nfl_injury_links[yr][wk] = url

