import requests

from api.serializers import LobbyStatSerializer

from .constants import (
    region_to_season_12_start_time_map,
    RIOT_API_KEY_HEADER,
)
from .helpers import get_lobby_match_rating, get_main_role


def get_lobby_summoner_stats(summoner_name, puuid, summoner_id, server, region):
    season_start_time = str(region_to_season_12_start_time_map[region])
    # print(region, puuid, season_start_time)
    url = "https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?startTime=" + season_start_time + "&queue=420&type=ranked&start=0&count=10"
    # url = "https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?startTime=" + season_start_time + "&queue=400&type=normal&start=0&count=20"
    res = requests.get(url, headers=RIOT_API_KEY_HEADER)
    match_list = list(res.json())

    # total data
    games_played = 0
    duration_of_games = 0
    wins = 0
    total_team_damage = 0

    ally_champion_kills = 0 
    enemy_champion_kills = 0
    kills = 0
    deaths = 0
    assists = 0

    # champion_level = 0
    gold_earned = 0
    cs = 0

    total_damage_dealt_to_champions = 0
    total_damage_taken = 0
    damage_self_mitigated = 0

    damage_dealt_to_buildings = 0
    damage_dealt_to_objectives = 0
    turret_takedowns = 0
    inhibitor_takedowns = 0

    total_damage_shielded_on_teammates = 0
    total_heals_on_teammates = 0
    time_ccing_others = 0 # cc score 
    vision_score = 0

    # champion_id = 0
    role_top = 0
    role_jungle = 0
    role_mid = 0
    role_bot = 0
    role_sup = 0
    # total data

    for match_id in match_list:
        # print(games_played, match_id)

        url = "https://" + region + ".api.riotgames.com/lol/match/v5/matches/" + match_id
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)
        # print(res.status_code)
        while res.status_code == 429:
            # print(res.status_code, 'Rate limit exceeded. Retrying...')
            # sleep
            res = requests.get(url, headers=RIOT_API_KEY_HEADER)
        data = res.json()

        info_data = data.get('info')
        index = data.get('metadata').get('participants').index(puuid)
        match_stat_data = info_data.get('participants')[index]

        # remaked game (due to afk)
        time_played = match_stat_data.get('timePlayed')
        if time_played <= 270:
            continue

        games_played += 1
        
        team100 = [0, 1, 2, 3, 4]
        team200 = [5, 6, 7, 8, 9]

        if match_stat_data.get('teamId') == 100:
            ally_objective_data = info_data.get('teams')[0].get('objectives')
            enemy_objective_data = info_data.get('teams')[1].get('objectives')

            for x in range(len(team100)):
                total_team_damage += info_data.get('participants')[x].get("totalDamageDealtToChampions")
        else:
            ally_objective_data = info_data.get('teams')[1].get('objectives')
            enemy_objective_data = info_data.get('teams')[0].get('objectives')

            for x in range(len(team200)):
                total_team_damage += info_data.get('participants')[x].get("totalDamageDealtToChampions")

        # match data
        duration_of_games += info_data.get('gameDuration')
        wins += 1 if match_stat_data.get('win') else 0

        ally_champion_kills += ally_objective_data.get('champion').get('kills')
        enemy_champion_kills += enemy_objective_data.get('champion').get('kills')
        kills += match_stat_data.get('kills')
        deaths += match_stat_data.get('deaths')
        assists += match_stat_data.get('assists')

        # champion_level +=  match_stat_data.get('champLevel')
        gold_earned += match_stat_data.get('goldEarned')
        cs += match_stat_data.get('totalMinionsKilled') + match_stat_data.get('neutralMinionsKilled')

        total_damage_dealt_to_champions += match_stat_data.get('totalDamageDealtToChampions')
        total_damage_taken += match_stat_data.get('totalDamageTaken')
        damage_self_mitigated += match_stat_data.get('damageSelfMitigated')

        damage_dealt_to_buildings += match_stat_data.get('damageDealtToBuildings')
        damage_dealt_to_objectives += match_stat_data.get('damageDealtToObjectives')
        turret_takedowns += match_stat_data.get('turretTakedowns')
        inhibitor_takedowns += match_stat_data.get('inhibitorTakedowns')

        total_damage_shielded_on_teammates += match_stat_data.get('totalDamageShieldedOnTeammates')
        total_heals_on_teammates += match_stat_data.get('totalHealsOnTeammates')
        time_ccing_others += match_stat_data.get('timeCCingOthers') # cc score 
        vision_score += match_stat_data.get('visionScore')

        # champion_id = 0
        role = match_stat_data.get('teamPosition') if match_stat_data.get('teamPosition') == '' else match_stat_data.get('individualPosition')
        if role == "TOP": 
            role_top += 1
        elif role == "JUNGLE":
            role_jungle += 1
        elif role == "MIDDLE":
            role_mid += 1
        elif role == "BOTTOM":
            role_bot += 1
        elif role == "UTILITY":
            role_sup += 1
        # match_data

    if games_played == 0:
        # print("No Ranked Games Played")
        return

    duration_of_games_in_min = duration_of_games / 60

    # get rank
    url = 'https://'+ server + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id
    res = requests.get(url, headers=RIOT_API_KEY_HEADER)
    data = res.json()

    ranked_solo_data = None
    for ranked_data in data:
        # print(ranked_data)
        if ranked_data and ranked_data.get('queueType') == 'RANKED_SOLO_5x5':
            ranked_solo_data = ranked_data

    match_data = {
        'summoner_name': summoner_name,
        'tier': None if not ranked_solo_data else ranked_solo_data.get('tier'),
        'rank': None if not ranked_solo_data else ranked_solo_data.get('rank'),
        'games_played': games_played, 
        'duration_of_games_in_min_per_game': duration_of_games_in_min / games_played,
        'win_rate': wins / games_played,

        'damage_participation': total_damage_dealt_to_champions / total_team_damage,
        'kill_participation': (kills + assists) / ally_champion_kills,
        'kda': (kills + assists) / deaths,
        'avg_kills': kills / games_played,
        'avg_deaths': deaths / games_played,
        'avg_assists': assists / games_played,

        'avg_gold_per_min': gold_earned / duration_of_games_in_min,
        'avg_cs_per_min': cs / duration_of_games_in_min,

        'total_damage_dealt_to_champions_per_min': total_damage_dealt_to_champions / duration_of_games_in_min,
        'total_damage_taken_per_min': total_damage_taken / duration_of_games_in_min,
        'damage_self_mitigated_per_min': damage_self_mitigated / duration_of_games_in_min,

        'damage_dealt_to_buildings_per_min': damage_dealt_to_buildings / duration_of_games_in_min,
        'damage_dealt_to_objectives_per_min': damage_dealt_to_objectives / duration_of_games_in_min,
        'turret_takedowns_per_min': turret_takedowns / duration_of_games_in_min,
        'inhibitor_takedowns_per_min': inhibitor_takedowns / duration_of_games_in_min,

        'total_damage_shielded_on_teammates_per_min': total_damage_shielded_on_teammates / duration_of_games_in_min,
        'total_heals_on_teammates_per_min': total_heals_on_teammates / duration_of_games_in_min,
        'time_ccing_others_per_min': time_ccing_others / duration_of_games_in_min,
        'vision_score_per_min': vision_score / duration_of_games_in_min,

        'main_role': get_main_role(role_top, role_jungle, role_mid, role_bot, role_sup)
    }
    match_data['match_rating'] = get_lobby_match_rating(match_data)

    match_data_serializer = LobbyStatSerializer(data=match_data)

    if not match_data_serializer.is_valid():
        # print('Not valid', match_data_serializer.errors)
        return # Response('Error bulk creating match stats', status=status.HTTP_400_BAD_REQUEST)

    return match_data_serializer.data

"""
def get_match_history(summoner, ranked_solo_stat=None):
    season_start_time = str(region_to_season_12_start_time_map[summoner.region])
    games_played = ranked_solo_stat.games_played if ranked_solo_stat else 0

    url = "https://" + summoner.region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + summoner.puuid + "/ids?startTime=" + season_start_time + "&queue=420&type=ranked&start=" + str(games_played) + "&count=100"
    res = requests.get(url, headers=RIOT_API_KEY_HEADER)
    match_list = list(res.json())
    num_matches = len(match_list)

    # get all match_ids
    while num_matches == MAX_MATCH_IDS:
        url = "https://" + summoner.region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + summoner.puuid + "/ids?startTime=" + season_start_time + "&queue=420&type=ranked&start=" + str(games_played + MAX_MATCH_IDS) + "&count=100"
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)
        append_match_list = list(res.json())

        num_matches = len(append_match_list)
        games_played += num_matches
        match_list += append_match_list

    print("Number of new ranked solo games since last update: ", len(match_list))

    if len(match_list) > 0:
        _update_or_create_stats(summoner, ranked_solo_stat, match_list)


def _update_or_create_stats(summoner, ranked_solo_stat, matches):
    # match_stat data
    match_stat_list = []

    # champion_stat data
    create_champion_stat_list = []
    update_champion_stat_list = []
    create_champion_stat_map = {}
    update_champion_stat_map = {}

    played_champions = ChampionStat.objects.filter(summoner=summoner, season=summoner.season)
    for champion in played_champions:
        update_champion_stat_map[champion.champion_name] = {
            'summoner_id': summoner.id,
            'season': summoner.season,
            'champion_name': champion.champion_name,
            # total stats
            'wins': champion.wins,
            'losses': champion.losses,
            'games_played': champion.games_played,
            'time_played': champion.time_played,
            'total_kills': champion.total_kills,
            'total_deaths': champion.total_deaths,
            'total_assists': champion.total_assists,
            'total_cs': champion.total_cs,
            'total_rating': champion.total_rating,
        }
        update_champion_stat_list.append(champion)

    # ranked_solo_stat data
    url = 'https://'+ summoner.server + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner.summoner_id
    res = requests.get(url, headers=RIOT_API_KEY_HEADER)
    data = res.json()

    ranked_solo_data = None
    for ranked_data in data:
        if ranked_data.get('queueType') == 'RANKED_SOLO_5x5':
            ranked_solo_data = ranked_data

    updated_ranked_solo_stat = {
        'summoner_id': summoner.id,
        'season': summoner.season,
        # https://developer.riotgames.com/apis#league-v4/GET_getLeagueEntriesForSummoner
        'league_id': ranked_solo_data.get('leagueId') if ranked_solo_data else None,
        'tier': ranked_solo_data.get('tier') if ranked_solo_data else None,
        'rank': ranked_solo_data.get('rank') if ranked_solo_data else None,
        'league_points': ranked_solo_data.get('leaguePoints') if ranked_solo_data else None,
        'wins': ranked_solo_data.get('wins') if ranked_solo_data else 0,
        'losses': ranked_solo_data.get('losses') if ranked_solo_data else 0,
        # total stats
        'total_kills': ranked_solo_stat.total_kills if ranked_solo_stat else 0,
        'total_deaths': ranked_solo_stat.total_deaths if ranked_solo_stat else 0,
        'total_assists': ranked_solo_stat.total_assists if ranked_solo_stat else 0,
        'total_cs': ranked_solo_stat.total_cs if ranked_solo_stat else 0,
        'time_played': ranked_solo_stat.time_played if ranked_solo_stat else 0,
        'games_played': ranked_solo_stat.games_played + len(matches) if ranked_solo_stat else len(matches),
        'total_rating': ranked_solo_stat.total_rating if ranked_solo_stat else 0,
    }

    count = 0
    for match_id in matches:
        count += 1
        print(count, match_id)

        url = "https://" + summoner.region + ".api.riotgames.com/lol/match/v5/matches/" + match_id
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)
        print(res.status_code)
        while res.status_code == 429:
            print(res.status_code, 'Rate limit exceeded. Retrying...')
            # sleep
            res = requests.get(url, headers=RIOT_API_KEY_HEADER)
        data = res.json()

        info_data = data.get('info')
        index = data.get('metadata').get('participants').index(summoner.puuid)
        match_stat_data = info_data.get('participants')[index]

        # match not played this season
        match_season = int(info_data.get('gameVersion').split('.', 1)[0])
        if match_season != summoner.season:
            continue

        # remaked game (due to afk)
        time_played = match_stat_data.get('timePlayed')
        if time_played <= 270:
            continue

        match_rating = _update_match_stats(
            summoner,
            match_stat_list,
            match_id,
            info_data,
            match_stat_data
        )
        _update_champion_stats(
            update_champion_stat_map,
            create_champion_stat_map,
            match_stat_data,
            match_rating,
        )
        _update_ranked_solo_stat(
            updated_ranked_solo_stat,
            match_stat_data,
            match_rating,
        )

    for champ in create_champion_stat_map:
        new_champion = create_champion_stat_map[champ]
        create_champion_stat_list.append(
            {
                'summoner_id': summoner.id,
                'season': summoner.season,
                'champion_name': champ,
                # total stats
                'wins': new_champion.get('wins'),
                'losses': new_champion.get('losses'),
                'games_played': new_champion.get('games_played'),
                'time_played': new_champion.get('time_played'),
                'total_kills': new_champion.get('total_kills'),
                'total_deaths': new_champion.get('total_deaths'),
                'total_assists': new_champion.get('total_assists'),
                'total_cs': new_champion.get('total_cs'),
                'total_rating': new_champion.get('total_rating'),
            }
        )

    updated_ranked_solo_stat['total_rating'] = updated_ranked_solo_stat.get('total_rating')

    # create match_stats
    match_stat_serializer = MatchStatSerializer(data=match_stat_list, many=True)

    if not match_stat_serializer.is_valid():
        print('Not valid', match_stat_serializer.errors)
        return # Response('Error bulk creating match stats', status=status.HTTP_400_BAD_REQUEST)

    # create champion_stats
    create_champion_stat_serializer = ChampionStatSerializer(data=create_champion_stat_list, many=True)
    if not create_champion_stat_serializer.is_valid():
        print('Not valid create champion stat -', create_champion_stat_serializer.errors)
        return

    # update champion_stats 
    update_champion_stat_serializer = ChampionStatSerializer(update_champion_stat_list, data=list(update_champion_stat_map.values()), many=True)
    if not update_champion_stat_serializer.is_valid():
        print('Not valid update champion stat -', update_champion_stat_serializer.errors)
        return

    # create/update ranked_solo_stats
    if ranked_solo_stat:
        ranked_solo_stat_serializer = RankedSoloStatSerializer(ranked_solo_stat, data=updated_ranked_solo_stat)
    else:
        ranked_solo_stat_serializer = RankedSoloStatSerializer(data=updated_ranked_solo_stat)

    if not ranked_solo_stat_serializer.is_valid():
        print('Not valid ranked_solo_stat -', ranked_solo_stat_serializer.errors)
        return

    try:
        with transaction.atomic():
            match_stat_serializer.save()
            create_champion_stat_serializer.save()
            update_champion_stat_serializer.save()
            ranked_solo_stat_serializer.save()
    except IntegrityError:
        print('Failed to update summoner stats')

def _update_match_stats(
    summoner,
    match_stat_list,
    match_id,
    info_data,
    match_stat_data,
):

    if match_stat_data.get('teamId') == 100:
        ally_objective_data = info_data.get('teams')[0].get('objectives')
        enemy_objective_data = info_data.get('teams')[1].get('objectives')
    else:
        ally_objective_data = info_data.get('teams')[1].get('objectives')
        enemy_objective_data = info_data.get('teams')[0].get('objectives')

    match_data = {
        'summoner_id': summoner.id,
        'season': summoner.season,
        'match_id': match_id,
        #
        'game_creation': info_data.get('gameCreation'),
        'game_duration': info_data.get('gameDuration'),
        'game_start_time_stamp': info_data.get('gameStartTimestamp'),
        'game_end_time_stamp': info_data.get('gameEndTimestamp'),
        'game_version': info_data.get('gameVersion'),
        'platform_id': info_data.get('platformId'),
        # queue_id = 420 (RANKED_SOLO_5x5)
        'queue_id': info_data.get('queueId'),
        # tean stats
        'ally_baron_kills': ally_objective_data.get('baron').get('kills'),
        'ally_champion_kills': ally_objective_data.get('champion').get('kills'),
        'ally_dragon_kills': ally_objective_data.get('dragon').get('kills'),
        'ally_inhibitor_kills': ally_objective_data.get('inhibitor').get('kills'),
        'ally_rift_herald_kills': ally_objective_data.get('riftHerald').get('kills'),
        'ally_tower_kills': ally_objective_data.get('tower').get('kills'),
        'enemy_baron_kills': enemy_objective_data.get('baron').get('kills'),
        'enemy_champion_kills': enemy_objective_data.get('champion').get('kills'),
        'enemy_dragon_kills': enemy_objective_data.get('dragon').get('kills'),
        'enemy_inhibitor_kills': enemy_objective_data.get('inhibitor').get('kills'),
        'enemy_rift_herald_kills': enemy_objective_data.get('riftHerald').get('kills'),
        'enemy_tower_kills': enemy_objective_data.get('tower').get('kills'),
        # stats
        'assists': match_stat_data.get('assists'),
        'baron_kills': match_stat_data.get('baronKills'),
        'bounty_level': match_stat_data.get('bountyLevel'),
        'champ_experience': match_stat_data.get('champExperience'),
        'champ_level': match_stat_data.get('champLevel'),
        'champion_id': match_stat_data.get('championId'),
        'champion_name': match_stat_data.get('championName'),
        'champion_transform': match_stat_data.get('championTransform'),
        'consumables_purchased': match_stat_data.get('consumablesPurchased'),
        'damage_dealt_to_builldings': match_stat_data.get('damageDealtToBuildings'),
        'damage_dealt_to_objectvies': match_stat_data.get('damageDealtToObjectives'),
        'damage_dealt_to_turrets': match_stat_data.get('damageDealtToTurrets'),
        'damage_self_mitigated': match_stat_data.get('damageSelfMitigated'),
        'deaths': match_stat_data.get('deaths'),
        'detector_wards_placed': match_stat_data.get('detectorWardsPlaced'),
        'double_kills': match_stat_data.get('doubleKills'),
        'dragon_kills': match_stat_data.get('dragonKills'),
        'first_blood_assist': match_stat_data.get('firstBloodAssist'),
        'first_blood_kill': match_stat_data.get('firstBloodKill'),
        'first_tower_assist': match_stat_data.get('firstTowerAssist'),
        'first_tower_kill': match_stat_data.get('firstTowerKill'),
        'game_ended_in_early_surrender': match_stat_data.get('gameEndedInEarlySurrender'),
        'game_ended_in_surrender': match_stat_data.get('gameEndedInSurrender'),
        'gold_earned': match_stat_data.get('goldEarned'),
        'gold_spent': match_stat_data.get('goldSpent'),
        'individual_position': match_stat_data.get('individualPosition'),
        'inhibitor_kills': match_stat_data.get('inhibitorKills'),
        'inhibitor_takedowns': match_stat_data.get('inhibitorTakedowns'),
        'inhibitors_lost': match_stat_data.get('inhibitorsLost'),
        'item0': match_stat_data.get('item0'),
        'item1': match_stat_data.get('item1'),
        'item2': match_stat_data.get('item2'),
        'item3': match_stat_data.get('item3'),
        'item4': match_stat_data.get('item4'),
        'item5': match_stat_data.get('item5'),
        'item6': match_stat_data.get('item6'),
        'items_purchased': match_stat_data.get('itemsPurchased'),
        'killing_sprees': match_stat_data.get('killingSprees'),
        'kills': match_stat_data.get('kills'),
        'lane': match_stat_data.get('lane'),
        'largest_critical_strike': match_stat_data.get('largestCriticalStrike'),
        'largest_killing_spree': match_stat_data.get('largestKillingSpree'),
        'largest_multi_kill': match_stat_data.get('largestMultiKill'),
        'longest_time_spent_living': match_stat_data.get('longestTimeSpentLiving'),
        'magic_damage_dealt': match_stat_data.get('magicDamageDealt'),
        'magic_damage_dealt_to_champions': match_stat_data.get('magicDamageDealtToChampions'),
        'magic_damage_taken': match_stat_data.get('magicDamageTaken'),
        'neutral_minions_killed': match_stat_data.get('neutralMinionsKilled'),
        'nexus_kills': match_stat_data.get('nexusKills'),
        'nexus_lost': match_stat_data.get('nexusLost'),
        'nexus_takedowns': match_stat_data.get('nexusTakedowns'),
        'objectives_stolen': match_stat_data.get('objectivesStolen'),
        'objectives_stolen_assists': match_stat_data.get('objectivesStolenAssists'),
        'participant_id': match_stat_data.get('participantId'),
        'penta_kills': match_stat_data.get('pentaKills'),
        'physical_damage_dealt': match_stat_data.get('physicalDamageDealt'),
        'physical_damage_dealt_to_champions': match_stat_data.get('physicalDamageDealtToChampions'),
        'physical_damage_taken': match_stat_data.get('physicalDamageTaken'),
        'profile_icon': match_stat_data.get('profileIcon'),
        'puuid': match_stat_data.get('puuid'),
        'quadra_kills': match_stat_data.get('quadraKills'),
        'riot_id_name': match_stat_data.get('riotIdName'),
        'riot_tag_line': match_stat_data.get('riotIdTagline'),
        'role': match_stat_data.get('role'),
        'sight_wards_bought_in_game': match_stat_data.get('sightWardsBoughtInGame'),
        'spell1_casts': match_stat_data.get('spell1Casts'),
        'spell2_casts': match_stat_data.get('spell2Casts'),
        'spell3_casts': match_stat_data.get('spell3Casts'),
        'spell4_casts': match_stat_data.get('spell4Casts'),
        'summoner1_casts': match_stat_data.get('summoner1Casts'),
        'summoner1_id': match_stat_data.get('summoner1Id'),
        'summoner2_casts': match_stat_data.get('summoner2Casts'),
        'summoner2_id': match_stat_data.get('summoner2Id'),
        'summoner_level': match_stat_data.get('summonerLevel'),
        'team_early_surrender': match_stat_data.get('teamEarlySurrendered'),
        'team_id': match_stat_data.get('teamId'),
        'team_position': match_stat_data.get('teamPosition'),
        'time_ccing_others': match_stat_data.get('timeCCingOthers'),
        'time_played': match_stat_data.get('timePlayed'),
        'total_damage_dealt': match_stat_data.get('totalDamageDealt'),
        'total_damage_dealt_to_champions': match_stat_data.get('totalDamageDealtToChampions'),
        'total_damage_shielded_on_teammates': match_stat_data.get('totalDamageShieldedOnTeammates'),
        'total_damage_taken': match_stat_data.get('totalDamageTaken'),
        'total_heal': match_stat_data.get('totalHeal'),
        'total_heals_on_teammates': match_stat_data.get('totalHealsOnTeammates'),
        'total_minions_killed': match_stat_data.get('totalMinionsKilled'),
        'total_time_cc_dealt': match_stat_data.get('totalTimeCCDealt'),
        'total_time_spent_dead': match_stat_data.get('totalTimeSpentDead'),
        'total_units_healed': match_stat_data.get('totalUnitsHealed'),
        'triple_kills': match_stat_data.get('tripleKills'),
        'true_damage_dealt': match_stat_data.get('trueDamageDealt'),
        'true_damage_dealt_to_champions': match_stat_data.get('trueDamageDealtToChampions'),
        'true_damage_taken': match_stat_data.get('trueDamageTaken'),
        'turret_kills': match_stat_data.get('turretKills'),
        'turret_takedowns': match_stat_data.get('turretTakedowns'),
        'turrets_lost': match_stat_data.get('turretsLost'),
        'unreal_kills': match_stat_data.get('unrealKills'),
        'vision_score': match_stat_data.get('visionScore'),
        'vision_wards_bought_in_game': match_stat_data.get('visionWardsBoughtInGame'),
        'wards_killed': match_stat_data.get('wardsKilled'),
        'wards_placed': match_stat_data.get('wardsPlaced'),
        'win': match_stat_data.get('win'),
    }

    match_data['match_rating'] = get_match_rating(match_data)
    match_stat_list.append(match_data)

    return match_data.get('match_rating')

def _update_champion_stats(
    update_map,
    create_map,
    match_stat_data,
    match_rating
):
    try:
        # existing champion stat
        champion = update_map[match_stat_data.get('championName')]
        champion['wins'] += match_stat_data.get('win')
        champion['losses'] += not match_stat_data.get('win')
        champion['games_played'] += 1
        champion['time_played'] +=  match_stat_data.get('timePlayed')
        champion['total_kills'] +=  match_stat_data.get('kills')
        champion['total_deaths'] += match_stat_data.get('deaths')
        champion['total_assists'] += match_stat_data.get('assists')
        champion['total_cs'] +=  match_stat_data.get('totalMinionsKilled') + match_stat_data.get('neutralMinionsKilled')
        champion['total_rating'] = champion.get('total_rating') + match_rating
    except KeyError:
        try:
            # new champion stat, since last update
            champion = create_map[match_stat_data.get('championName')]
            champion['wins'] += match_stat_data.get('win')
            champion['losses'] += not match_stat_data.get('win')
            champion['games_played'] += 1
            champion['time_played'] +=  match_stat_data.get('timePlayed')
            champion['total_kills'] +=  match_stat_data.get('kills')
            champion['total_deaths'] += match_stat_data.get('deaths')
            champion['total_assists'] += match_stat_data.get('assists')
            champion['total_cs'] +=  match_stat_data.get('totalMinionsKilled') + match_stat_data.get('neutralMinionsKilled')
            champion['total_rating'] += match_rating
        except KeyError:
            # new champion stat
            create_map[match_stat_data.get('championName')] = {
                'wins': int(match_stat_data.get('win')),
                'losses': int(not match_stat_data.get('win')),
                'games_played': 1,
                'time_played': match_stat_data.get('timePlayed'),
                'total_kills': match_stat_data.get('kills'),
                'total_deaths': match_stat_data.get('deaths'),
                'total_assists': match_stat_data.get('assists'),
                'total_cs': match_stat_data.get('totalMinionsKilled') + match_stat_data.get('neutralMinionsKilled'),
                'total_rating': match_rating
            }


def _update_ranked_solo_stat(updated_ranked_solo_stat, match_stat_data, match_rating):
    updated_ranked_solo_stat['total_kills'] += match_stat_data.get('kills')
    updated_ranked_solo_stat['total_deaths'] += match_stat_data.get('deaths')
    updated_ranked_solo_stat['total_assists'] += match_stat_data.get('assists')
    updated_ranked_solo_stat['total_cs'] += match_stat_data.get('totalMinionsKilled') + match_stat_data.get('neutralMinionsKilled')
    updated_ranked_solo_stat['time_played'] += match_stat_data.get('timePlayed')
    updated_ranked_solo_stat['total_rating'] += match_rating


def search_z_rift(summoner, ranked_solo_stat, champion_stats, match_stats):
    summoner_serializer = SummonerSerializer(summoner)
    ranked_solo_stat_serializer = RankedSoloStatSerializer(ranked_solo_stat)
    champion_stat_serializer = ChampionStatSerializer(champion_stats, many=True)
    match_stat_serializer = MatchStatSerializer(match_stats, many=True)

    serializer = {
        'summoner': summoner_serializer.data,
        'ranked_solo_stat': ranked_solo_stat_serializer.data,
        'champion_stat:': champion_stat_serializer.data, 
        'match_stat': match_stat_serializer.data,
    }

    return serializer
"""