from scrape_nfl.web_driver import SeleniumHelper
from scrape_nfl.variables import nfl_injury_links
import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta
from time import sleep

from scrape_nfl.variables import nfl_injury_links

web_driver = SeleniumHelper()

api_url ='http://api.fantasy.nfl.com/v1/players/stats?statType=seasonStats&season={}&week={}&format=json'

TEAM_ABBR = {
    '49ers': 'SF',
    'Bears': 'CHI',
    'Bengals': 'CIN',
    'Bills': 'BUF',
    'Buccaneers': 'TB',
    'Broncos': 'DEN',
    'Browns': 'CLE',
    'Cardinals': 'ARI',
    'Chargers': 'LAC',
    'Chiefs': 'KC',
    'Cowboys': 'DAL',
    'Colts': 'IND',
    'Dolphins': 'MIA',
    'Eagles': 'PHI',
    'Falcons': 'ATL',
    'Giants': 'NYG',
    'Jaguars': 'JAX',
    'Jets': 'NYJ',
    'Lions': 'DET',
    'Packers': 'GB',
    'Panthers': 'CAR',
    'Patriots': 'NE',
    'Raiders': 'OAK',
    'Rams': 'LA',
    'Ravens': 'BAL',
    'Redskins': 'WAS',
    'Saints': 'NO',
    'Seahawks': 'SEA',
    'Steelers': 'PIT',
    'Texans': 'TEX',
    'Titans': 'TEN',
    'Vikings': 'MIN'
}
STATS_ID = {
    1: {'id': 1, 'abbr': 'GP', 'name': 'Games Played', 'shortName': 'GP'},
    2: {'id': 2, 'abbr': 'Att', 'name': 'Passing Attempts', 'shortName': 'Pass Att'},
    3: {'id': 3, 'abbr': 'Comp', 'name': 'Passing Completions', 'shortName': 'Pass Comp'},
    4: {'id': 4, 'abbr': 'Inc', 'name': 'Incomplete Passes', 'shortName': 'Pass Inc'},
    5: {'id': 5, 'abbr': 'Yds', 'name': 'Passing Yards', 'shortName': 'Pass Yds'},
    6: {'id': 6, 'abbr': 'TD', 'name': 'Passing Touchdowns', 'shortName': 'Pass TD'},
    7: {'id': 7, 'abbr': 'Int', 'name': 'Interceptions Thrown', 'shortName': 'Pass Int'},
    8: {'id': 8, 'abbr': 'Sacked', 'name': 'Every Time Sacked', 'shortName': 'Sacked'},
    9: {'id': 9, 'abbr': '300-399', 'name': '300-399 Passing Yards Bonus', 'shortName': '300-399 Pass Yds'},
    10: {'id': 10, 'abbr': '400+', 'name': '400+ Passing Yards Bonus', 'shortName': '400+ Pass Yds'},
    11: {'id': 11, 'abbr': '40+ TD', 'name': '40+ Passing Yard TD Bonus', 'shortName': '40+ Pass TD'},
    12: {'id': 12, 'abbr': '50+ TD', 'name': '50+ Passing Yards TD Bonus', 'shortName': '50+ Pass TD'},
    13: {'id': 13, 'abbr': 'Att', 'name': 'Rushing Attempts', 'shortName': 'Rush Att'},
    14: {'id': 14, 'abbr': 'Yds', 'name': 'Rushing Yards', 'shortName': 'Rush Yds'},
    15: {'id': 15, 'abbr': 'TD', 'name': 'Rushing Touchdowns', 'shortName': 'Rush TD'},
    16: {'id': 16, 'abbr': '40+ TD', 'name': '40+ Rushing Yard TD Bonus', 'shortName': '40+ Rush TD'},
    17: {'id': 17, 'abbr': '50+ TD', 'name': '50+ Rushing Yard TD Bonus', 'shortName': '50+ Rush TD'},
    18: {'id': 18, 'abbr': '100-199', 'name': '100-199 Rushing Yards Bonus', 'shortName': '100-199 Rush Yds'},
    19: {'id': 19, 'abbr': '200+', 'name': '200+ Rushing Yards Bonus', 'shortName': '200+ Rush Yds'},
    20: {'id': 20, 'abbr': 'Rect', 'name': 'Receptions', 'shortName': 'Receptions'},
    21: {'id': 21, 'abbr': 'Yds', 'name': 'Receiving Yards', 'shortName': 'Rec Yds'},
    22: {'id': 22, 'abbr': 'TD', 'name': 'Receiving Touchdowns', 'shortName': 'Rec TD'},
    23: {'id': 23, 'abbr': '40+ TD', 'name': '40+ Receiving Yard TD Bonus', 'shortName': '40+ Rec TD'},
    24: {'id': 24, 'abbr': '50+ TD', 'name': '50+ Receiving Yard TD Bonus', 'shortName': '50+ Rec TD'},
    25: {'id': 25, 'abbr': '100-199', 'name': '100-199 Receiving Yards Bonus', 'shortName': '100-199 Rec Yds'},
    26: {'id': 26, 'abbr': '200+', 'name': '200+ Receiving Yards Bonus', 'shortName': '200+ Rec Yds'},
    27: {'id': 27, 'abbr': 'Yds', 'name': 'Kickoff and Punt Return Yards', 'shortName': 'Return Yds'},
    28: {'id': 28, 'abbr': 'TD', 'name': 'Kickoff and Punt Return Touchdowns', 'shortName': 'Return TD'},
    29: {'id': 29, 'abbr': 'Fum TD', 'name': 'Fumble Recovered for TD', 'shortName': 'Fum TD'},
    30: {'id': 30, 'abbr': 'Lost', 'name': 'Fumbles Lost', 'shortName': 'Fum Lost'},
    31: {'id': 31, 'abbr': 'Fum', 'name': 'Fumble', 'shortName': 'Fum'},
    32: {'id': 32, 'abbr': '2PT', 'name': '2-Point Conversions', 'shortName': '2PT'},
    33: {'id': 33, 'abbr': 'Made', 'name': 'PAT Made', 'shortName': 'PAT Made'},
    34: {'id': 34, 'abbr': 'Miss', 'name': 'PAT Missed', 'shortName': 'PAT Miss'},
    35: {'id': 35, 'abbr': '0-19', 'name': 'FG Made 0-19', 'shortName': 'FG 0-19'},
    36: {'id': 36, 'abbr': '20-29', 'name': 'FG Made 20-29', 'shortName': 'FG 20-29'},
    37: {'id': 37, 'abbr': '30-39', 'name': 'FG Made 30-39', 'shortName': 'FG 30-39'},
    38: {'id': 38, 'abbr': '40-49', 'name': 'FG Made 40-49', 'shortName': 'FG 40-49'},
    39: {'id': 39, 'abbr': '50+', 'name': 'FG Made 50+', 'shortName': 'FG 50+'},
    40: {'id': 40, 'abbr': '0-19', 'name': 'FG Missed 0-19', 'shortName': 'FG Miss 0-19'},
    41: {'id': 41, 'abbr': '20-29', 'name': 'FG Missed 20-29', 'shortName': 'FG Miss 20-29'},
    42: {'id': 42, 'abbr': '30-39', 'name': 'FG Missed 30-39', 'shortName': 'FG Miss 30-39'},
    43: {'id': 43, 'abbr': '40-49', 'name': 'FG Missed 40-49', 'shortName': 'FG Miss 40-49'},
    44: {'id': 44, 'abbr': '50+', 'name': 'FG Missed 50+', 'shortName': 'FG Miss 50+'},
    45: {'id': 45, 'abbr': 'Sack', 'name': 'Sacks', 'shortName': 'Sack'},
    46: {'id': 46, 'abbr': 'Int', 'name': 'Interceptions', 'shortName': 'Int'},
    47: {'id': 47, 'abbr': 'Fum Rec', 'name': 'Fumbles Recovered', 'shortName': 'Fum Rec'},
    48: {'id': 48, 'abbr': 'Fum F', 'name': 'Fumbles Forced', 'shortName': 'Fum Forc'},
    49: {'id': 49, 'abbr': 'Saf', 'name': 'Safeties', 'shortName': 'Saf'},
    50: {'id': 50, 'abbr': 'TD', 'name': 'Touchdowns', 'shortName': 'TD'},
    51: {'id': 51, 'abbr': 'Block', 'name': 'Blocked Kicks', 'shortName': 'Block'},
    52: {'id': 52, 'abbr': 'Yds', 'name': 'Kickoff and Punt Return Yards', 'shortName': 'Return Yds'},
    53: {'id': 53, 'abbr': 'TD', 'name': 'Kickoff and Punt Return Touchdowns', 'shortName': 'Return TD'},
    54: {'id': 54, 'abbr': 'Pts Allow', 'name': 'Points Allowed', 'shortName': 'Pts Allow'},
    55: {'id': 55, 'abbr': 'Pts Allow', 'name': 'Points Allowed 0', 'shortName': 'Pts Allow 0'},
    56: {'id': 56, 'abbr': 'Pts Allow', 'name': 'Points Allowed 1-6', 'shortName': 'Pts Allow 1-6'},
    57: {'id': 57, 'abbr': 'Pts Allow', 'name': 'Points Allowed 7-13', 'shortName': 'Pts Allow 7-13'},
    58: {'id': 58, 'abbr': 'Pts Allow', 'name': 'Points Allowed 14-20', 'shortName': 'Pts Allow 14-20'},
    59: {'id': 59, 'abbr': 'Pts Allow', 'name': 'Points Allowed 21-27', 'shortName': 'Pts Allow 21-27'},
    60: {'id': 60, 'abbr': 'Pts Allow', 'name': 'Points Allowed 28-34', 'shortName': 'Pts Allow 28-34'},
    61: {'id': 61, 'abbr': 'Pts Allowed', 'name': 'Points Allowed 35+', 'shortName': 'Pts Allowed 35+'},
    62: {'id': 62, 'abbr': 'Yds Allow', 'name': 'Yards Allowed', 'shortName': 'Yds Allow'},
    63: {'id': 63, 'abbr': '0-99 Yds', 'name': 'Less than 100 Total Yards Allowed', 'shortName': 'Less 100 Yds Allowed'},
    64: {'id': 64, 'abbr': '100-199 Yds', 'name': '100-199 Yards Allowed', 'shortName': '100-199 Yds Allow'},
    65: {'id': 65, 'abbr': '200-299 Yds', 'name': '200-299 Yards Allowed', 'shortName': '200-299 Yds Allow'},
    66: {'id': 66, 'abbr': '300-399 Yds', 'name': '300-399 Yards Allowed', 'shortName': '300-399 Yds Allow'},
    67: {'id': 67, 'abbr': '400-449 Yds', 'name': '400-449 Yards Allowed', 'shortName': '400-449 Yds Allow'},
    68: {'id': 68, 'abbr': '450-499 Yds', 'name': '450-499 Yards Allowed', 'shortName': '450-499 Yds Allow'},
    69: {'id': 69, 'abbr': '500+ Yds', 'name': '500+ Yards Allowed', 'shortName': '500+ Yds Allow'},
    70: {'id': 70, 'abbr': 'Tot', 'name': 'Tackle', 'shortName': 'Tack'},
    71: {'id': 71, 'abbr': 'Ast', 'name': 'Assisted Tackles', 'shortName': 'Ast'},
    72: {'id': 72, 'abbr': 'Sck', 'name': 'Sack', 'shortName': 'Sack'},
    73: {'id': 73, 'abbr': 'Int', 'name': 'Defense Interception', 'shortName': 'Int'},
    74: {'id': 74, 'abbr': 'Frc Fum', 'name': 'Forced Fumble', 'shortName': 'Frc Fum'},
    75: {'id': 75, 'abbr': 'Fum Rec', 'name': 'Fumbles Recovery', 'shortName': 'Fum Rec'},
    76: {'id': 76, 'abbr': 'Int TD', 'name': 'Touchdown (Interception return)', 'shortName': 'Int TD'},
    77: {'id': 77, 'abbr': 'Fum TD', 'name': 'Touchdown (Fumble return)', 'shortName': 'Fum TD'},
    78: {'id': 78, 'abbr': 'Blk TD', 'name': 'Touchdown (Blocked kick)', 'shortName': 'Blk TD'},
    79: {'id': 79, 'abbr': 'Blk', 'name': 'Blocked Kick (punt, FG, PAT)', 'shortName': 'Blk'},
    80: {'id': 80, 'abbr': 'Saf', 'name': 'Safety', 'shortName': 'Saf'},
    81: {'id': 81, 'abbr': 'PDef', 'name': 'Pass Defended', 'shortName': 'Pass Def'},
    82: {'id': 82, 'abbr': 'Int Yds', 'name': 'Interception Return Yards', 'shortName': 'Int Yds'},
    83: {'id': 83, 'abbr': 'Fum Yds', 'name': 'Fumble Return Yards', 'shortName': 'Fum Yds'},
    84: {'id': 84, 'abbr': 'TFL', 'name': 'Tackles for Loss Bonus', 'shortName': 'TFL'},
    85: {'id': 85, 'abbr': 'QB Hit', 'name': 'QB Hit', 'shortName': 'QB Hit'},
    86: {'id': 86, 'abbr': 'Sck Yds', 'name': 'Sack Yards', 'shortName': 'Sck Yds'},
    87: {'id': 87, 'abbr': '10+ Tackles', 'name': '10+ Tackles Bonus', 'shortName': '10+ Tack'},
    88: {'id': 88, 'abbr': '2+ Sacks', 'name': '2+ Sacks Bonus', 'shortName': '2+ Sck'},
    89: {'id': 89, 'abbr': '3+ Passes Defended', 'name': '3+ Passes Defended Bonus', 'shortName': '3+ Pas Def'},
    90: {'id': 90, 'abbr': '50+ Yard INT Return TD', 'name': '50+ Yard INT Return TD Bonus', 'shortName': '50+ Yard INT TD'},
    91: {'id': 91, 'abbr': '50+ Yard Fumble Return TD', 'name': '50+ Yard Fumble Return TD Bonus', 'shortName': '50+ Yard Fum Ret TD'}
}
NFL_ARCHIVE = {
    2012: 'https://web.archive.org/web/20130131145247/{}',
    2013: 'https://web.archive.org/web/20140720185448/{}',
    2014: 'https://web.archive.org/web/20150113003837/{}',
    2015: 'https://web.archive.org/web/20160224174133/{}',
    2016: 'https://web.archive.org/web/20170117195919/{}',
    2017: 'https://web.archive.org/web/20180123052053/{}'
}


def loop_weeks(dictionary, yr_start=2012):
    for season in range(yr_start, 2018):
        print(season)
        dictionary[season] = {}
        for wk in range(1, 18):
            print(wk)
            dictionary[season][wk] = {}
            yield season, wk, dictionary[season][wk]


def get_data():
    data_dict = {}
    for season in range(2012, 2018):
        print(season)
        data_dict[season] = {}
        for wk in range(1, 18):
            print(wk)
            data_dict[season][wk] = {}
            url = api_url.format(season, wk)
            data = requests.get(url).json()
            for i, player_row in enumerate(data['players']):
                # player_row['stats'] = {STATS_ID[int(k)]['abbr']: v for k, v in player_row['stats'].items()}
                data_dict[season][wk][player_row['id']] = player_row

    return data_dict


def save_json(dictionary, name):
    with open('./data/' + name + '.json', 'w+') as file_obj:
        json.dump(dictionary, file_obj)


def get_json(name):
    with open('./data/' + name + '.json', 'r') as file_obj:
        return json.load(file_obj)


def get_schedule():
    schedule = {}
    base_url = 'http://www.nfl.com/schedules/{}/REG{}'
    for yr, wk, dict_ref in loop_weeks(schedule):
        url = base_url.format(yr, wk)
        web_driver.navigateToUrl(url)
        content = web_driver.getContent()
        soup = BeautifulSoup(content, 'html.parser')
        score_items = soup.find_all('div', {'class': 'schedules-list-hd post'})
        for item in score_items:
            teams = item.find_all('span', {'class': 'team-name'})
            teams = [t.contents[0] for t in teams]
            team_abbr = [TEAM_ABBR[t] for t in teams]
            schedule[yr][wk][team_abbr[0]] = {'opp': team_abbr[1], 'loc': 'A'}
            schedule[yr][wk][team_abbr[1]] = {'opp': team_abbr[0], 'loc': 'H'}
        for team in TEAM_ABBR.values():
            if team not in schedule[yr][wk].keys():
                schedule[yr][wk][team] = {'opp': None, 'loc': None}
            # print(teams, team_abbr)
    return schedule

def get_injuries():
    injury_data = {}
    try_date = None
    base_url = 'https://web.archive.org/web/{}/nfl.com/injuries'
    for yr, wk, dict_ref in loop_weeks(injury_data, yr_start=2014):
        try:
            url = nfl_injury_links[yr][wk]
            web_driver.navigateToUrl(url)
            content = web_driver.getContent()
            soup = BeautifulSoup(content, 'html.parser')
        except:
            page_wk = 0
            start_date = date(yr, 9, 9) if wk == 1 else date(yr, 9, 3)
            try_date = start_date + timedelta(days=7*wk)
            while page_wk != wk:
                try_string = str(try_date.year) + str(try_date.month).zfill(2) + str(try_date.day).zfill(2)
                if yr == 2016:
                    if wk == 1:
                        url = 'https://web.archive.org/web/20151107185909/http://www.nfl.com:80/injuries?week=1'
                    if wk == 12:
                        url = 'https://web.archive.org/web/20180726041344/http://www.nfl.com/injuries?week=12'
                else:
                    url = base_url.format(try_string)

                web_driver.navigateToUrl(url)
                content = web_driver.getContent()
                # sleep(10)
                soup = BeautifulSoup(content, 'html.parser')
                try:
                    page_wk = int(re.search('NFL INJURIES WEEK (\d{1,2})', soup.text, re.IGNORECASE).group(1))
                except:
                    page_wk = 0
                if page_wk > wk:
                    try_date = try_date - timedelta(days=1)
                elif page_wk < wk:
                    try_date = try_date + timedelta(days=1)
                else:
                    print(yr, wk, url)

        wk_data = []
        raw_text = soup.text
        raw_text = re.sub('\n','',raw_text)
        raw_text = re.sub('\s+', ' ', raw_text)
        player_injuries = re.findall('var (?:dataAway|dataHome) = \[.*?\]', raw_text)
        for row in player_injuries:
            json_string = row[15:]
            json_string = re.sub('(?!<\")(\w+)(?=:)', r'"\1"', json_string)
            json_string = re.sub('}, ]', '}]', json_string)
            row_data = json.loads(json_string)
            wk_data.extend(row_data)
        dict_ref['injuries'] = wk_data
    return injury_data





if __name__ == '__main__':
    # save_json(get_data(), 'all_data')
    # save_json(get_schedule(), 'schedule')
    injury_data = get_injuries()
    save_json(injury_data, 'injuries')
