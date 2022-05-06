import statsapi
import tweepy
import json

#SCHEDULE
schedule = json.load(open("./schedule.json", "r"))
games_left = [g for g in schedule if "win_loss_result" not in g]

#CHAPMAN SEASON STATS
chapmanSeasonStats = statsapi.player_stat_data(
		656305, #playerID
		group = "hitting",
		type = "season"
		) 

game_id = statsapi.last_game(141)

#CHAPMAN DAILY STATS
#HOME OR AWAY
if statsapi.boxscore_data(game_id)['homeBatters'][0]['namefield'] == 'Blue Jays Batters':
	batters = 'homeBatters'
elif statsapi.boxscore_data(game_id)['awayBatters'][0]['namefield'] == 'Blue Jays Batters':
	batters = 'awayBatters'

#FIND INDEX
for i in range(len(statsapi.boxscore_data(game_id)[batters])):
	if statsapi.boxscore_data(game_id)[batters][i]['name'] == 'Chapman, M':
		index = i

if index: #if chapman played, get stats from game and season stats
	at_bats = statsapi.boxscore_data(game_id)[batters][index]['ab']
	hits = statsapi.boxscore_data(game_id)[batters][index]['h']

	statline = f"""{hits}/{at_bats}"""

	doubles = int(statsapi.boxscore_data(game_id)[batters][index]['doubles'])
	if doubles > 0:
		statline += f""", {doubles} 2B"""

	triples = int(statsapi.boxscore_data(game_id)[batters][index]['triples'])
	if triples > 0:
		statline += f""", {triples} 3B"""

	home_runs = int(statsapi.boxscore_data(game_id)[batters][index]['hr'])
	if home_runs > 0:
		statline += f""", {home_runs} HR"""

	rbis = int(statsapi.boxscore_data(game_id)[batters][index]['rbi'])
	if rbis > 0:
		statline += f""", {rbis} RBI"""

	strikeouts = int(statsapi.boxscore_data(game_id)[batters][index]['k'])
	if strikeouts > 0:
		statline += f""", {strikeouts} K"""


	message = f"""Today's Stats:
{statline}

Season Stats:
{chapmanSeasonStats['stats'][0]['stats']['avg']}/{chapmanSeasonStats['stats'][0]['stats']['obp']}/{chapmanSeasonStats['stats'][0]['stats']['slg']}

{len(games_left)} games left"""
else: #if chapman did not play, get just season stats
	message = f"""Matt Chapman did not play today

Season Stats:
{chapmanSeasonStats['stats'][0]['stats']['avg']}/{chapmanSeasonStats['stats'][0]['stats']['obp']}/{chapmanSeasonStats['stats'][0]['stats']['slg']}

{len(games_left)} games left"""

#TWITTER VERIFICATION
auth = tweepy.OAuthHandler(CONSUMER_KEY,
                           CONSUMER_KEY_SECRET)

auth.set_access_token(ACCESS_TOKEN_KEY,
                      ACCESS_TOKEN_KEY_SECRET)

api = tweepy.API(auth)

api.update_status(status=message)
