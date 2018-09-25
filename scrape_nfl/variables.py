nfl_injury_links = {
    2014:{
        1: 'https://web.archive.org/web/20140910/nfl.com/injuries',
        2: 'https://web.archive.org/web/20140916/nfl.com/injuries',
        3: 'https://web.archive.org/web/20140923/nfl.com/injuries',
        4: 'https://web.archive.org/web/20140930/nfl.com/injuries',
        5: 'https://web.archive.org/web/20141008/nfl.com/injuries',
        6: 'https://web.archive.org/web/20141014/nfl.com/injuries',
        7: 'https://web.archive.org/web/20141021/nfl.com/injuries',
        8: 'https://web.archive.org/web/20141028/nfl.com/injuries',
        9: 'https://web.archive.org/web/20141103/nfl.com/injuries',
        10: 'https://web.archive.org/web/20141111/nfl.com/injuries',
        11: 'https://web.archive.org/web/20141119/nfl.com/injuries',
        12: 'https://web.archive.org/web/20141125/nfl.com/injuries',
        13: 'https://web.archive.org/web/20141202/nfl.com/injuries',
        14: 'https://web.archive.org/web/20141208/nfl.com/injuries',
        15: 'https://web.archive.org/web/20141216/nfl.com/injuries',
        16: 'https://web.archive.org/web/20141223/nfl.com/injuries',
        17: 'https://web.archive.org/web/20141231/nfl.com/injuries'
    },
    2015: {
        1: 'https://web.archive.org/web/20150916/nfl.com/injuries',
        2: 'https://web.archive.org/web/20150917/nfl.com/injuries',
        3: 'https://web.archive.org/web/20150924/nfl.com/injuries',
        4: 'https://web.archive.org/web/20151003/nfl.com/injuries',
        5: 'https://web.archive.org/web/20151011/nfl.com/injuries',
        6: 'https://web.archive.org/web/20151015/nfl.com/injuries',
        7: 'https://web.archive.org/web/20151022/nfl.com/injuries',
        8: 'https://web.archive.org/web/20151029/nfl.com/injurie',
        9: 'https://web.archive.org/web/20151105/nfl.com/injuries',
        10: 'https://web.archive.org/web/20151112/nfl.com/injuries',
        11: 'https://web.archive.org/web/20151119/nfl.com/injuries',
        12: 'https://web.archive.org/web/20151126/nfl.com/injuries',
        13: 'https://web.archive.org/web/20151203/nfl.com/injuries',
        14: 'https://web.archive.org/web/20151210/nfl.com/injuries',
        15: 'https://web.archive.org/web/20151217/nfl.com/injuries',
        16: 'https://web.archive.org/web/20151224/nfl.com/injuries',
        17: 'https://web.archive.org/web/20151231/nfl.com/injuries'
    },
    2016 : {
        1: 'https://web.archive.org/web/20151107185909/http://www.nfl.com:80/injuries?week=1:',
        2: 'https://web.archive.org/web/20160917/nfl.com/injuries',
        3: 'https://web.archive.org/web/20160924/nfl.com/injuries',
        4: 'https://web.archive.org/web/20161001/nfl.com/injuries',
        5: 'https://web.archive.org/web/20161008/nfl.com/injuries',
        6: 'https://web.archive.org/web/20161015/nfl.com/injuries',
        7: 'https://web.archive.org/web/20161022/nfl.com/injuries',
        8: 'https://web.archive.org/web/20161029/nfl.com/injuries',
        9: 'https://web.archive.org/web/20161105/nfl.com/injuries',
        10: 'https://web.archive.org/web/20161112/nfl.com/injuries',
        11: 'https://web.archive.org/web/20161119/nfl.com/injuries',
        12: 'https://web.archive.org/web/20170512232035/http://www.nfl.com/injuries?week=12',
        13: 'https://web.archive.org/web/20170421074058/http://www.nfl.com/injuries?week=13',
        14: 'https://web.archive.org/web/20170512232038/http://www.nfl.com/injuries?week=14',
        15: 'https://web.archive.org/web/20170602235619/http://www.nfl.com/injuries?week=15',
        16: 'https://web.archive.org/web/20170428223831/http://www.nfl.com/injuries?week=16',
        17: 'https://web.archive.org/web/20170428223833/http://www.nfl.com/injuries?week=17'
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
