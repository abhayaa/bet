import pandas as pd

from nba_api.stats.endpoints import playerdashboardbylastngames, teamvsplayer, scoreboard
from nba_api.stats.endpoints import leaguegamefinder,playercareerstats
from nba_api.stats.static import teams, players


pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 10000)

playerNames = players.get_players()
teamNames = teams.get_teams()

def get_player_id(playerName):
    playerIdByName = [player for player in playerNames
                        if player['full_name'] == playerName][0]

    return playerIdByName['id']
   

def get_team_id(teamName):
    teamIdByName = [team for team in teamNames
                    if team['abbreviation'] == teamName][0]
    return teamIdByName['id']


def get_stats_player_vs_team(playerName, playerTeam, oppTeamName, seasonval):
    opp_team_id = get_team_id(oppTeamName)
    player_id = get_player_id(playerName)
    player_team_id = get_team_id(playerTeam)

    tvp = teamvsplayer.TeamVsPlayer(season = seasonval, opponent_team_id = opp_team_id , vs_player_id = player_id, team_id = player_team_id)
    
    df = tvp.get_data_frames()[1]

    for(columnName, columnData) in df.items():
        print(columnName, columnData.values)

    return tvp.get_data_frames()[1]


def get_games_played(team_abbvr, opp_abbvr, season):
    team_id = get_team_id(team_abbvr)
    opp_team_id = get_team_id(opp_abbvr)

    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    games = gamefinder.get_data_frames()[0]
    games_in_given_season = games[games.SEASON_ID.str[-4:] == season]

    games_vs_opp_in_season = games_in_given_season[games_in_given_season.MATCHUP.str.contains(opp_abbvr)]

    for(columnName, columnData) in games_vs_opp_in_season.items():
        print(columnName, columnData.values)

    return games_vs_opp_in_season

gids = get_games_played('GSW', 'LAL', '2022').GAME_ID

print(gids)