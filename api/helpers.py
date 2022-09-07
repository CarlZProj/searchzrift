from .constants import (
    region_to_season_12_start_time_map,
    # team_position_to_match_rating_ratios_map,
)

def get_season(epooch_time, region):
    if epooch_time >= 1000 * region_to_season_12_start_time_map.get(region):
        return 12

def get_main_role(top, jungle, mid, bot, sup):
    role_list = [top, jungle, mid, bot, sup]
    role = max(role_list)

    if role == top:
        return "TOP"
    elif role == jungle:
        return "JUNGLE"
    elif role == mid:
        return "MIDDLE"
    elif role == bot:
        return "BOTTOM"
    elif role == sup:
        return "SUPPORT"

def get_lobby_match_rating(match_data) -> int:
    match_rating = 0
    match_rating += match_data.get('win_rate') * 5 / 0.7                                        # 5 - 70% win rate

    if match_data.get('main_role') == "TOP":
        match_rating += match_data.get('damage_participation') * 15 / 0.25                      # 15 - 25% damage participation
        match_rating += match_data.get('kill_participation') * 10 / 0.5                         # 10 - 50% kill participation
        match_rating += match_data.get('kda') * 10 / 3                                          # 10 - 3 kda

        match_rating += match_data.get('avg_gold_per_min') * 10 / 500                           # 10 - 500 gold / min
        match_rating += match_data.get('avg_cs_per_min') * 10 / 8                               # 10 - 8 cs / min

        match_rating += match_data.get('total_damage_dealt_to_champions_per_min') * 15 / 800    # 15 - 800 dmg / min
        match_rating += match_data.get('damage_self_mitigated_per_min') * 10 / 1000             # 10 - 1000 dmg mitigated / min
        match_rating += match_data.get('damage_dealt_to_buildings_per_min') * 5 / 200           # 5 - 200 dmg to buildings / min

        # match_rating += match_data.get('total_damage_shielded_on_teammates_per_min')          #
        # match_rating += match_data.get('total_heals_on_teammates_per_min')                    #
        match_rating += match_data.get('time_ccing_others_per_min') * 5                         # 5 - 1 cc score / min
        match_rating += match_data.get('vision_score_per_min') * 5                              # 5 - 1 vision score / min

    # -----------------------------------------------------------------------------------------------------------------------------

    elif match_data.get('main_role') == "JUNGLE":
        match_rating += match_data.get('damage_participation') * 10 / 0.25                      # 10 - 25% damage participation
        match_rating += match_data.get('kill_participation') * 20 / 0.65                        # 20 - 65% kill participation
        match_rating += match_data.get('kda') * 10 / 4                                          # 10 - 4 kda

        match_rating += match_data.get('avg_gold_per_min') * 10 / 500                           # 10 - 500 gold / min
        match_rating += match_data.get('avg_cs_per_min') * 5 / 6                                # 5 - 6 cs / min

        match_rating += match_data.get('total_damage_dealt_to_champions_per_min') * 15 / 700    # 15 - 700 dmg / min
        match_rating += match_data.get('damage_self_mitigated_per_min') * 5 / 1000              # 5 - 1000 dmg mitigated / min
        # match_rating += match_data.get('damage_dealt_to_buildings_per_min')                   #

        # match_rating += match_data.get('total_damage_shielded_on_teammates_per_min')          #
        # match_rating += match_data.get('total_heals_on_teammates_per_min')                    #
        match_rating += match_data.get('time_ccing_others_per_min') * 10                        # 10 - 1 cc score / min
        match_rating += match_data.get('vision_score_per_min') * 10                             # 10 - 1 vision score / min

    # -----------------------------------------------------------------------------------------------------------------------------

    elif match_data.get('main_role') == "MIDDLE":
        match_rating += match_data.get('damage_participation') * 15 / 0.30                      # 15 - 30% damage participation
        match_rating += match_data.get('kill_participation') * 20 / 0.55                        # 20 - 55% kill participation
        match_rating += match_data.get('kda') * 10 / 3.5                                        # 10 - 3.5 kda

        match_rating += match_data.get('avg_gold_per_min') * 10 / 500                           # 10 - 500 gold / min
        match_rating += match_data.get('avg_cs_per_min') * 5 / 7                                # 5 - 7 cs / min

        match_rating += match_data.get('total_damage_dealt_to_champions_per_min') * 20 / 1000   # 20 - 900 dmg / min
        # match_rating += match_data.get('damage_self_mitigated_per_min')                       #
        # match_rating += match_data.get('damage_dealt_to_buildings_per_min')                   #
         
        # match_rating += match_data.get('total_damage_shielded_on_teammates_per_min')          #
        # match_rating += match_data.get('total_heals_on_teammates_per_min')                    #
        match_rating += match_data.get('time_ccing_others_per_min') * 5                         # 5 - 1 cc score / min
        match_rating += match_data.get('vision_score_per_min') * 10                             # 10 - 1 vision score / min

    # -----------------------------------------------------------------------------------------------------------------------------

    elif match_data.get('main_role') == "BOTTOM":
        match_rating += match_data.get('damage_participation') * 15 / 0.30                      # 15 - 30% damage participation
        match_rating += match_data.get('kill_participation') * 15 / 0.6                         # 15 - 60% kill participation
        match_rating += match_data.get('kda') * 10 / 3.5                                        # 10 - 3.5 kda

        match_rating += match_data.get('avg_gold_per_min') * 10 / 500                           # 10 - 500 gold / min
        match_rating += match_data.get('avg_cs_per_min') * 10 / 8                               # 10 - 8 cs / min

        match_rating += match_data.get('total_damage_dealt_to_champions_per_min') * 20 / 1000   # 20 - 1000 dmg / min
        # match_rating += match_data.get('damage_self_mitigated_per_min')                       #
        # match_rating += match_data.get('damage_dealt_to_buildings_per_min')                   #

        # match_rating += match_data.get('total_damage_shielded_on_teammates_per_min')          #
        # match_rating += match_data.get('total_heals_on_teammates_per_min')                    #
        match_rating += match_data.get('time_ccing_others_per_min') * 5 / 0.5                   # 5 - 0.5 cc score / min
        match_rating += match_data.get('vision_score_per_min') * 10                             # 10 - 1 vision score / min

    # -----------------------------------------------------------------------------------------------------------------------------

    elif match_data.get('main_role') == "SUPPORT":
        match_rating += match_data.get('damage_participation') * 5 / 0.1                        # 5 - 10% damage participation
        match_rating += match_data.get('kill_participation') * 25 / 0.65                        # 25 - 65% kill participation
        match_rating += match_data.get('kda') * 5 / 3.5                                         # 5 - 3.5 kda

        # match_rating += match_data.get('avg_gold_per_min')                                    #
        # match_rating += match_data.get('avg_cs_per_min')                                      #

        match_rating += match_data.get('total_damage_dealt_to_champions_per_min') * 5 / 500     # 5 - 500 dmg / min
        match_rating += match_data.get('damage_self_mitigated_per_min') * 10 / 300              # 10 - 300 dmg mitigated / min
        # match_rating += match_data.get('damage_dealt_to_buildings_per_min')                   #

        match_rating += match_data.get('total_damage_shielded_on_teammates_per_min') * 10 / 75  # 10 - 75 shield / min
        match_rating += match_data.get('total_heals_on_teammates_per_min') * 10 / 150           # 10 - 150 heal / min
        match_rating += match_data.get('time_ccing_others_per_min') * 10 / 1.5                  # 10 - 1.5 cc score / min
        match_rating += match_data.get('vision_score_per_min') * 15 / 2.5                       # 15 - 2.5 vision score / min

    # filter inters
    if match_data.get('avg_deaths') > 10:
        match_rating -= 20
    elif match_data.get('avg_deaths') > 9:
        match_rating -= 15
    elif match_data.get('avg_deaths') > 8:
        match_rating -= 10

    # filter inters/low kp
    if match_data.get('kda') < 1:
        match_rating -= 15
    if match_data.get('kda') < 1.5:
        match_rating -= 5

    # time factor (longer games more stats)
    match_rating -= match_data.get('duration_of_games_in_min_per_game') - 20

    return match_rating

    """
    def get_match_rating(match_data) -> int:
    overall, participation, offense, defense, objectives_and_turrets, income, vision, utility = (0, 0, 0, 0, 0, 0, 0, 0)

    # OVERALL
    overall += 10 if match_data.get('win') else 0                                                                                       # 10%   : win
    if match_data.get('deaths') == 0:
        overall += 100
    else:
        overall += 18 * (match_data.get('kills') + match_data.get('assists')) / match_data.get('deaths')                                # 90%   : 5 kda            

    # PARTCIPATION
    if match_data.get('ally_tower_kills') == 0:
        participation += 200 * (match_data.get('kills') / match_data.get('ally_champion_kills'))     
    else:
        # participation += 10 * (match_data.get('baron_kills') / match_data.get('ally_baron_kills'))
        participation += 140 * (match_data.get('kills') / match_data.get('ally_champion_kills'))                                        # 70%   : 0.5 kill particpation
        # participation += 10 * (match_data.get('dragon_kills') / match_data.get('ally_dragon_kills'))
        # participation += 20 * (match_data.get('inhibitor_kills') / match_data.get('ally_inhibitor_kills')) / 0.3
        # participation += 10 * (match_data.get('rift_herald_kills') / match_data.get('ally_rift_herald_kills'))
        participation += 30 * (match_data.get('turret_takedowns') / match_data.get('ally_tower_kills')) / 0.4                           # 30%   : 0.4 kill particpation

    # OFFENSE
    # offense += match_data.get('bounty_level')
    offense += 5 if match_data.get('first_blood_assist') else 0                                                                         #       
    offense += 5 if match_data.get('first_blood_kill') else 0                                                                           # 
    # offense += match_data.get('largest_killing_spree')
    # offense += match_data.get('largest_multi_kill')

    # offense += match_data.get('magic_damage_dealt_to_champions')
    # offense += match_data.get('physical_damage_dealt_to_champions')
    # offense += match_data.get('true_damage_dealt_to_champions')
    offense += 90 * match_data.get('total_damage_dealt_to_champions') / 30000                                                           # 90%   : 30k 
    
    offense += 2 * match_data.get('double_kills')                                                                                       #                                    
    offense += 3 * match_data.get('triple_kills')                                                                                       # 
    offense += 4 * match_data.get('quadra_kills')                                                                                       # 
    offense += 5 * match_data.get('penta_kills')                                                                                        # 
    offense += 10 * match_data.get('unreal_kills') # hexa_kills+                                                                        # 
    
    # DEFENSE
    defense += 50 * match_data.get('damage_self_mitigated') / 1e5                                                                       # 50%    : 100k
    # defense += match_data.get('longest_time_spent_living')
    # defense += match_data.get('magic_damage_taken')
    # defense += match_data.get('physical_damage_taken')
    # defense += match_data.get('true_damage_taken')
    defense += 50 * match_data.get('total_damage_taken') / 1e5                                                                          # 50%   : 100k
    
    # UTILITY
    utility += 0.5 * match_data.get('time_ccing_others')                                                                                # 25%   : 50
    # utility += match_data.get('total_time_cc_dealt')
    utility += 25 * (match_data.get('total_heal') - match_data.get('total_heals_on_teammates')) / 20000                                 # 25%   : 20k
    utility += 25 * match_data.get('total_heals_on_teammates') / 30000                                                                  # 25%   : 30k
    utility += 25 * match_data.get('total_damage_shielded_on_teammates') / 15000                                                        # 25%   : 15k
    
    # VISION
    vision += match_data.get('detector_wards_placed')                                                                                   # 10%   : 10
    vision += 0.5 * match_data.get('vision_score')                                                                                      # 50%   : 100
    vision += 4 * match_data.get('wards_killed')                                                                                        # 20%   : 5
    vision += 20 * match_data.get('wards_placed') / 3                                                                                        # 20%   : 30
    
    # OBJECTIVES + TURRETS
    objectives_and_turrets += 5 if match_data.get('first_tower_assist') else 0                                                          #
    objectives_and_turrets += 5 if match_data.get('first_tower_kill') else 0                                                            #
    objectives_and_turrets += 0.006 * match_data.get('damage_dealt_to_builldings')                                                      # 60%   : 10k
    objectives_and_turrets += 0.0006 * match_data.get('damage_dealt_to_objectvies')                                                     # 30%   : 50k
    objectives_and_turrets += 5 * match_data.get('inhibitor_takedowns')                                                                 #
    objectives_and_turrets += 5 * match_data.get('objectives_stolen')                                                                   # 

    # INCOME
    income += 4 * (match_data.get('total_minions_killed') + match_data.get('neutral_minions_killed')) / match_data.get('time_played')   # 40%   : 10 cs/min                                                           #                                                     # 
    income += 7.5 * match_data.get('gold_earned') / match_data.get('time_played')                                                       # 60%   : 8 g/sec

    # match rating
    match_rating_ratios = team_position_to_match_rating_ratios_map.get(match_data.get('team_position'))

    # print('overall', overall)
    # print('particpation', participation)
    # print('offense', offense)
    # print('defense', defense)
    # print('utility', utility)
    # print('vision', vision)
    # print('objectives_and_turrets', objectives_and_turrets)
    # print('income', income)

    # print(match_rating_ratios.get('overall') * overall)
    # print(match_rating_ratios.get('participation') * participation)
    # print(match_rating_ratios.get('offense') * offense)
    # print(match_rating_ratios.get('defense') * defense)
    # print(match_rating_ratios.get('objectives_and_turrets') * objectives_and_turrets)
    # print(match_rating_ratios.get('income') * income)
    # print(match_rating_ratios.get('vision') * vision)
    # print(match_rating_ratios.get('utility') * utility)

    match_rating = match_rating_ratios.get('overall') * overall \
        + match_rating_ratios.get('participation') * participation \
        + match_rating_ratios.get('offense') * offense \
        + match_rating_ratios.get('defense') * defense \
        + match_rating_ratios.get('objectives_and_turrets') * objectives_and_turrets \
        + match_rating_ratios.get('income') * income \
        + match_rating_ratios.get('vision') * vision \
        + match_rating_ratios.get('utility') * utility

    return match_rating
"""