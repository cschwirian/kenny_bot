import requests
import json

API_KEY = ""
with open( "config/league_api_key.txt", "r" ) as config:
    API_KEY = config.readline().replace( "\n", "" )

CURRENT_SEASON = "9"
INVALID_CHAMPION = 1
INVALID_SUMMONER = 2


QUEUE_IDS = { "ranked": 420, "draft": 400, "blind": 430, "flex": 440 }

CHAMPION_IDS = { 'aatrox': 266, 'thresh': 412, 'tryndamere': 23, 'gragas': 79, 'cassiopeia': 69, 'aurelion sol': 136, 'ryze': 13, 'poppy': 78, 'sion': 14, 'annie': 1, 'jhin': 202, 'karma': 43, 'nautilus': 111, 'kled': 240, 'lux': 99, 'ahri': 103, 'olaf': 2, 'viktor': 112, 'anivia': 34, 'singed': 27, 'garen': 86, 'lissandra': 127, 'maokai': 57, 'morgana': 25, 'evelynn': 28, 'fizz': 105, 'heimerdinger': 74, 'zed': 238, 'rumble': 68, 'mordekaiser': 82, 'sona': 37, "kog'maw": 96, 'katarina': 55, 'lulu': 117, 'ashe': 22, 'karthus': 30, 'alistar': 12, 'darius': 122, 'vayne': 67, 'varus': 110, 'udyr': 77, 'leona': 89, 'jayce': 126, 'syndra': 134, 'pantheon': 80, 'riven': 92, "kha'zix": 121, 'corki': 42, 'azir': 268, 'caitlyn': 51, 'nidalee': 76, 'kennen': 85, 'galio': 3, 'veigar': 45, 'bard': 432, 'gnar': 150, 'malzahar': 90, 'graves': 104, 'vi': 254, 'kayle': 10, 'irelia': 39, 'lee sin': 64, 'illaoi': 420, 'elise': 60, 'volibear': 106, 'nunu': 20, 'twisted fate': 4, 'jax': 24, 'shyvana': 102, 'kalista': 429, 'dr. mundo': 36, 'ivern': 427, 'diana': 131, 'tahm kench': 223, 'brand': 63, 'sejuani': 113, 'vladimir': 8, 'zac': 154, "rek'sai": 421, 'quinn': 133, 'akali': 84, 'taliyah': 163, 'tristana': 18, 'hecarim': 120, 'sivir': 15, 'lucian': 236, 'rengar': 107, 'warwick': 19, 'skarner': 72, 'malphite': 54, 'yasuo': 157, 'xerath': 101, 'teemo': 17, 'nasus': 75, 'renekton': 58, 'draven': 119, 'shaco': 35, 'swain': 50, 'talon': 91, 'janna': 40, 'ziggs': 115, 'ekko': 245, 'orianna': 61, 'fiora': 114, 'fiddlesticks': 9, "cho'gath": 31, 'rammus': 33, 'leblanc': 7, 'soraka': 16, 'zilean': 26, 'nocturne': 56, 'jinx': 222, 'yorick': 83, 'urgot': 6, 'kindred': 203, 'miss fortune': 21, 'wukong': 62, 'blitzcrank': 53, 'shen': 98, 'braum': 201, 'xin zhao': 5, 'twitch': 29, 'master yi': 11, 'taric': 44, 'amumu': 32, 'gangplank': 41, 'trundle': 48, 'kassadin': 38, "vel'koz": 161, 'zyra': 143, 'nami': 267, 'jarvan iv': 59, 'ezreal': 81 }

SEASON_IDS = { "9": 13, "8": 11, "7": 9, "6": 7, "5": 5, "4": 3, "3": 1 }


def get_current_ranked_winrate( summoner_name, champion ):

    try:
        champion_id = CHAMPION_IDS[champion.lower()]
    except:
        return INVALID_CHAMPION

    season_id = SEASON_IDS[CURRENT_SEASON]
    queue_id = QUEUE_IDS["ranked"]

    summoner_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s?api_key=%s"
    summoner_response = requests.get( summoner_url % (summoner_name, API_KEY) )
    summoner = summoner_response.text

    if( not "200" in str(summoner_response) ):
        return INVALID_SUMMONER

    summoner_json = json.loads( summoner )
    account_id = summoner_json["accountId"]

    # Grabs the first up to 100 matches played by the player to ensure the
    # players has played the specified champion.
    matches_url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/%s?api_key=%s&beginIndex=%d&endIndex=%d&queue=%d&champion=%d&season=%d"
    matches_response = requests.get( matches_url % (account_id, API_KEY, 0, 100, queue_id, champion_id, season_id) )
    matches = matches_response.text

    if( not "200" in str( matches_response ) ):
        return "%s has not played %s this season." % (summoner_name, champion.title())

    matches_json = json.loads( matches )
    match_list = matches_json["matches"]

    index = 100

    while( True ):
        matches = requests.get( matches_url % (account_id, API_KEY, index, index + 100, queue_id, champion_id, season_id) ).text
        matches_json = json.loads( matches )
        match_list += matches_json["matches"]

        if( len( matches_json["matches"] ) < 100 ):
            break

        index += 100

    if( len( match_list ) == 0 ):
        return "%s has not played %s this season." % (summoner_name, champion.title())


    win_counter = 0
    match_url = "https://na1.api.riotgames.com/lol/match/v4/matches/%d?api_key=%s"

    for match in match_list:
        game_id = match["gameId"]
        match = requests.get( match_url % (game_id, API_KEY) ).text
        match_json = json.loads( match )

        for participant in match_json["participantIdentities"]:
            if( participant["player"]["summonerName"] == summoner_name ):
                participant_id = participant["participantId"]
                break

        for participant in match_json["participants"]:
            if( participant["participantId"] == participant_id ):
                if( participant["stats"]["win"] ):
                    win_counter += 1

    return "%s has a %.2f%% winrate with %s out of %d games." % (summoner_name, (win_counter / len( match_list ) * 100), champion.title(), len( match_list ))


if( __name__ == "__main__" ):
    print( get_current_ranked_winrate( "MagicalMarvin", "Morgana" ) )
