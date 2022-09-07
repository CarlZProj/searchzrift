from datetime import datetime, timezone
from django.core.validators import MinValueValidator

from rest_framework import serializers

class LobbyStatSerializer(serializers.Serializer):
    summoner_name = serializers.CharField(max_length=16)
    tier = serializers.CharField(max_length=11, allow_null=True)
    rank = serializers.CharField(max_length=3, allow_null=True)
    games_played = serializers.IntegerField()
    duration_of_games_in_min_per_game = serializers.FloatField()
    win_rate =  serializers.FloatField()

    damage_participation = serializers.FloatField()
    kill_participation = serializers.FloatField()
    kda = serializers.FloatField()
    avg_kills = serializers.FloatField()
    avg_deaths = serializers.FloatField()
    avg_assists = serializers.FloatField()

    avg_gold_per_min = serializers.FloatField()
    avg_cs_per_min = serializers.FloatField()

    total_damage_dealt_to_champions_per_min = serializers.FloatField()
    total_damage_taken_per_min = serializers.FloatField()
    damage_self_mitigated_per_min = serializers.FloatField()

    damage_dealt_to_buildings_per_min = serializers.FloatField()
    damage_dealt_to_objectives_per_min = serializers.FloatField()
    turret_takedowns_per_min = serializers.FloatField()
    inhibitor_takedowns_per_min = serializers.FloatField()

    total_damage_shielded_on_teammates_per_min = serializers.FloatField()
    total_heals_on_teammates_per_min = serializers.FloatField()
    time_ccing_others_per_min = serializers.FloatField()
    vision_score_per_min = serializers.FloatField()

    main_role = serializers.CharField(max_length=20)

    match_rating = serializers.FloatField()

"""

class SummonerSerializer(serializers.Serializer):
    summoner_id = serializers.CharField(max_length=63, write_only=True)     # unique
    account_id = serializers.CharField(max_length=56, write_only=True)      # unique
    puuid = serializers.CharField(max_length=78, write_only=True)           # unique
    name = serializers.CharField(max_length=16)
    profile_icon_id = serializers.IntegerField()
    revision_date = serializers.IntegerField(write_only=True)
    summoner_level = serializers.IntegerField()
    #  BR1   - Brazil                - AMERICAS
    #  EUN1  - Europe Nordic & East  - EUROPE
    #  EUW1  - Europe West           - EUROPE
    #  LA1   - Latin America North   - AMERICAS
    #  LA2   - Latin America South   - AMERiCAS
    #  NA1   - North America         - AMERICAS
    #  OC1   - Oceania               - AMERICAS
    #  RU    - Russia                - EUROPE
    #  TR1   - Turkey                - EUROPE
    #  JP1   - Japan                 - ASIA
    #  KR    - Republic of Korea     - ASIA
    server = serializers.CharField(max_length=4)
    # AMERICAS, EUROPE, ASIA
    region = serializers.CharField(max_length=8)
    season = serializers.IntegerField()
    last_updated = serializers.SerializerMethodField('get_last_updated')

    class Meta:
        read_only_fields = ['last_updated']

    def get_last_updated(self, obj):
        date = datetime.fromtimestamp(obj.revision_date/1e3, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
        return date 

    def create(self, validated_data):
        return Summoner.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.profile_icon_id = validated_data.get('profile_icon_id', instance.profile_icon_id)
        instance.revision_date = validated_data.get('revision_date', instance.revision_date)
        instance.summoner_level = validated_data.get('summoner_level', instance.summoner_level)
        instance.server = validated_data.get('server', instance.server)
        instance.save()
        return instance


class RankedSoloStatSerializer(serializers.Serializer):
    summoner_id = serializers.IntegerField(write_only=True)
    season = serializers.IntegerField()
    # https://developer.riotgames.com/apisleague-v4/GET_getLeagueEntriesForSummoner
    league_id = serializers.CharField(max_length=36, allow_null=True, write_only=True)
    tier = serializers.CharField(max_length=11, allow_null=True)
    rank = serializers.CharField(max_length=3, allow_null=True)
    league_points = serializers.IntegerField(allow_null=True)
    wins = serializers.IntegerField()
    losses = serializers.IntegerField()
    # total stats
    games_played = serializers.IntegerField()
    time_played = serializers.IntegerField(write_only=True)
    total_kills = serializers.IntegerField(write_only=True)
    total_deaths = serializers.IntegerField(write_only=True)
    total_assists = serializers.IntegerField(write_only=True)
    total_cs = serializers.IntegerField(write_only=True)
    total_rating = serializers.FloatField(
        validators=[MinValueValidator(0)],
        write_only=True,
    )
    # avg stats
    win_rate = serializers.SerializerMethodField('get_win_rate')
    kda = serializers.SerializerMethodField('get_kda')
    kills = serializers.SerializerMethodField('get_kills')
    deaths = serializers.SerializerMethodField('get_deaths')
    assists = serializers.SerializerMethodField('get_assists')
    cs = serializers.SerializerMethodField('get_cs')
    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        read_only_fields = ['win_rate', 'kda', 'kills', 'deaths', 'assists', 'cs', 'rating']

    def get_win_rate(self, obj):
        return round(obj.wins / obj.games_played, 2)

    def get_kda(self, obj):
        return -1 if obj.total_deaths == 0 else round((obj.total_kills + obj.total_assists) / obj.total_deaths, 2)

    def get_kills(self, obj):
        return round(obj.total_kills / obj.games_played, 2)

    def get_deaths(self, obj):
        return round(obj.total_deaths / obj.games_played, 2)

    def get_assists(self, obj):
        return round(obj.total_assists / obj.games_played, 2)

    def get_cs(self, obj):
        return round(obj.total_cs * 60 / obj.time_played, 2)

    def get_rating(self, obj):
        return round(obj.total_rating / obj.games_played, 2)

    def create(self, validated_data):
        return RankedSoloStat.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tier = validated_data.get('tier', instance.tier)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.league_points = validated_data.get('league_points', instance.league_points)
        instance.wins = validated_data.get('wins', instance.wins)
        instance.losses = validated_data.get('losses', instance.losses)
        instance.games_played = validated_data.get("games_played", instance.games_played)
        instance.time_played = validated_data.get('time_played', instance.time_played)
        instance.total_kills = validated_data.get('total_kills', instance.total_kills)
        instance.total_deaths = validated_data.get('total_deaths', instance.total_deaths)
        instance.total_assists = validated_data.get('total_assists', instance.total_assists)
        instance.total_cs = validated_data.get('total_cs', instance.total_cs)
        instance.total_rating = validated_data.get('total_rating', instance.total_rating)
        instance.save()

        return instance


class ChampionStatListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        champion_stat_list = [ChampionStat(**item) for item in validated_data]
        return ChampionStat.objects.bulk_create(champion_stat_list)

    def update(self, instances, validated_data):
        instance_hash = {index: instance for index, instance in enumerate(instances)}

        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]

        writable_fields = [
            x
            for x in self.child.Meta.fields
            if x not in self.child.Meta.read_only_fields
        ]

        try:
            ChampionStat.objects.bulk_update(result, writable_fields)
        except:
            print("bulk update failed")
            
        return result

class ChampionStatSerializer(serializers.Serializer):
    summoner_id = serializers.IntegerField(write_only=True)
    season = serializers.IntegerField()
    champion_name = serializers.CharField(max_length=20)
    # total stats
    wins = serializers.IntegerField()
    losses = serializers.IntegerField()
    games_played = serializers.IntegerField()
    time_played = serializers.IntegerField(write_only=True)
    total_kills = serializers.IntegerField(write_only=True)
    total_deaths = serializers.IntegerField(write_only=True)
    total_assists = serializers.IntegerField(write_only=True)
    total_cs = serializers.IntegerField(write_only=True)
    total_rating = serializers.FloatField(
        validators=[MinValueValidator(0)],
        write_only=True,
    )
    # avg stats
    win_rate = serializers.SerializerMethodField('get_win_rate')
    kda = serializers.SerializerMethodField('get_kda')
    kills = serializers.SerializerMethodField('get_kills')
    deaths = serializers.SerializerMethodField('get_deaths')
    assists = serializers.SerializerMethodField('get_assists')
    cs = serializers.SerializerMethodField('get_cs')
    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        model = ChampionStat
        fields = ['season', 'champion_name', 'wins', 'losses', 'games_played', 'time_played', 'total_kills', 'total_deaths', 'total_assists', 'total_cs', 'total_rating']
        read_only_fields = ['win_rate', 'kda', 'kills', 'deaths', 'assists', 'cs', 'rating']
        list_serializer_class = ChampionStatListSerializer

    def get_win_rate(self, obj):
        return round(obj.wins / obj.games_played, 2)

    def get_kda(self, obj):
        return -1 if obj.total_deaths == 0 else round((obj.total_kills + obj.total_assists) / obj.total_deaths, 2)

    def get_kills(self, obj):
        return round(obj.total_kills / obj.games_played, 2)

    def get_deaths(self, obj):
        return round(obj.total_deaths / obj.games_played, 2)

    def get_assists(self, obj):
        return round(obj.total_assists / obj.games_played, 2)

    def get_cs(self, obj):
        return round(obj.total_cs * 60 / obj.time_played, 2)

    def get_rating(self, obj):
        return round(obj.total_rating / obj.games_played, 2)

    def update(self, instance, validated_data):
        instance.wins = validated_data.get('wins', instance.wins)
        instance.losses = validated_data.get('losses', instance.losses)
        instance.games_played = validated_data.get('games_played', instance.games_played)
        instance.time_played = validated_data.get('time_played', instance.time_played)
        instance.total_kills = validated_data.get('total_kills', instance.total_kills)
        instance.total_deaths = validated_data.get('total_deaths', instance.total_deaths)
        instance.total_assists = validated_data.get('total_assists', instance.total_assists)
        instance.total_cs = validated_data.get('total_cs', instance.total_cs)
        instance.total_rating = validated_data.get('total_rating', instance.total_rating)

        return instance


class MatchStatListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        match_stat_list = [MatchStat(**item) for item in validated_data]
        return MatchStat.objects.bulk_create(match_stat_list)

class MatchStatSerializer(serializers.Serializer):
    summoner_id = serializers.IntegerField(write_only=True)
    season = serializers.IntegerField(write_only=True)
    match_id = serializers.CharField(max_length=20, write_only=True)
    # https://developer.riotgames.com/apismatch-v5/GET_getMatch
    game_creation = serializers.IntegerField(write_only=True)
    game_duration = serializers.IntegerField(write_only=True)
    game_start_time_stamp = serializers.IntegerField(write_only=True)
    game_end_time_stamp = serializers.IntegerField(write_only=True)
    game_version = serializers.CharField(max_length=20, write_only=True)
    platform_id = serializers.CharField(max_length=4, write_only=True)
    # queue_id = 420 (RANKED_SOLO_5x5)
    queue_id = serializers.IntegerField(write_only=True)
    # team stats
    ally_baron_kills = serializers.IntegerField()
    ally_champion_kills = serializers.IntegerField()
    ally_dragon_kills = serializers.IntegerField()
    ally_inhibitor_kills = serializers.IntegerField()
    ally_rift_herald_kills = serializers.IntegerField()
    ally_tower_kills = serializers.IntegerField()
    enemy_baron_kills = serializers.IntegerField()
    enemy_champion_kills = serializers.IntegerField()
    enemy_dragon_kills = serializers.IntegerField()
    enemy_inhibitor_kills = serializers.IntegerField()
    enemy_rift_herald_kills = serializers.IntegerField()
    enemy_tower_kills = serializers.IntegerField()
    # stats
    assists = serializers.IntegerField()
    baron_kills = serializers.IntegerField()
    bounty_level = serializers.IntegerField()
    champ_experience = serializers.IntegerField()
    champ_level = serializers.IntegerField()                                            
    champion_id = serializers.IntegerField()                                            
    champion_name = serializers.CharField(max_length=20)                                     
    champion_transform = serializers.IntegerField()                                         # kayn only  (Legal values: 0 - None, 1 - Slayer, 2 - Assassin)
    consumables_purchased = serializers.IntegerField()
    damage_dealt_to_builldings = serializers.IntegerField()                             
    damage_dealt_to_objectvies = serializers.IntegerField()                              
    damage_dealt_to_turrets = serializers.IntegerField()                                
    damage_self_mitigated = serializers.IntegerField()                                  
    deaths = serializers.IntegerField()                                                 
    detector_wards_placed = serializers.IntegerField()                                  
    double_kills = serializers.IntegerField()
    dragon_kills = serializers.IntegerField()
    first_blood_assist = serializers.BooleanField()
    first_blood_kill = serializers.BooleanField()
    first_tower_assist = serializers.BooleanField()
    first_tower_kill = serializers.BooleanField()
    game_ended_in_early_surrender = serializers.BooleanField()
    game_ended_in_surrender = serializers.BooleanField()
    gold_earned = serializers.IntegerField()                                            
    gold_spent = serializers.IntegerField()
    individual_position = serializers.CharField(max_length=16)
    inhibitor_kills = serializers.IntegerField()
    inhibitor_takedowns = serializers.IntegerField()
    inhibitors_lost = serializers.IntegerField()
    item0 = serializers.IntegerField()
    item1 = serializers.IntegerField()
    item2 = serializers.IntegerField()
    item3 = serializers.IntegerField()
    item4 = serializers.IntegerField()
    item5 = serializers.IntegerField()
    item6 = serializers.IntegerField()
    items_purchased = serializers.IntegerField()
    killing_sprees = serializers.IntegerField()
    kills = serializers.IntegerField()
    lane = serializers.CharField(max_length=16)
    largest_critical_strike = serializers.IntegerField()
    largest_killing_spree = serializers.IntegerField()
    largest_multi_kill = serializers.IntegerField()
    longest_time_spent_living = serializers.IntegerField()
    magic_damage_dealt = serializers.IntegerField()        
    magic_damage_dealt_to_champions = serializers.IntegerField()                         
    magic_damage_taken = serializers.IntegerField()                                      
    neutral_minions_killed = serializers.IntegerField()
    nexus_kills = serializers.IntegerField()
    nexus_lost = serializers.IntegerField()
    nexus_takedowns = serializers.IntegerField()
    objectives_stolen = serializers.IntegerField()
    objectives_stolen_assists = serializers.IntegerField()
    participant_id = serializers.IntegerField()                                          
    penta_kills = serializers.IntegerField()                                             
    physical_damage_dealt = serializers.IntegerField()                                   
    physical_damage_dealt_to_champions = serializers.IntegerField()                      
    physical_damage_taken = serializers.IntegerField()                                   
    profile_icon = serializers.IntegerField()
    puuid = serializers.CharField(max_length=78)
    quadra_kills = serializers.IntegerField()                                            
    riot_id_name = serializers.CharField(allow_blank=True, max_length=16)
    riot_tag_line = serializers.CharField(allow_blank=True, max_length=16)
    role = serializers.CharField(max_length=16)                                                       
    sight_wards_bought_in_game = serializers.IntegerField()                              
    spell1_casts = serializers.IntegerField()
    spell2_casts = serializers.IntegerField()
    spell3_casts = serializers.IntegerField()
    spell4_casts = serializers.IntegerField()
    summoner1_casts = serializers.IntegerField()
    summoner1_id = serializers.IntegerField()
    summoner2_casts = serializers.IntegerField()
    summoner2_id = serializers.IntegerField()
    summoner_level = serializers.IntegerField()
    team_early_surrender = serializers.BooleanField()
    team_id = serializers.IntegerField()
    team_position = serializers.CharField(allow_blank=True, max_length=16)          
    time_ccing_others = serializers.IntegerField()                                       
    time_played = serializers.IntegerField()                                             
    total_damage_dealt = serializers.IntegerField()                                      
    total_damage_dealt_to_champions = serializers.IntegerField()                         
    total_damage_shielded_on_teammates = serializers.IntegerField()                      
    total_damage_taken = serializers.IntegerField()                                      
    total_heal = serializers.IntegerField()                                              
    total_heals_on_teammates = serializers.IntegerField()                                
    total_minions_killed = serializers.IntegerField()                                    
    total_time_cc_dealt = serializers.IntegerField()                                     
    total_time_spent_dead = serializers.IntegerField()                                   
    total_units_healed = serializers.IntegerField()                                      
    triple_kills = serializers.IntegerField()                                            
    true_damage_dealt = serializers.IntegerField()                                       
    true_damage_dealt_to_champions = serializers.IntegerField()                          
    true_damage_taken = serializers.IntegerField()                                       
    turret_kills = serializers.IntegerField()
    turret_takedowns = serializers.IntegerField()
    turrets_lost = serializers.IntegerField()
    unreal_kills = serializers.IntegerField()
    vision_score = serializers.IntegerField()                                            
    vision_wards_bought_in_game = serializers.IntegerField()                             
    wards_killed = serializers.IntegerField()                                            
    wards_placed = serializers.IntegerField()                                            
    win = serializers.BooleanField()
    #
    match_rating = serializers.FloatField(
        validators=[MinValueValidator(0)],
        write_only=True,
    )
    #
    match_time = serializers.SerializerMethodField('get_match_time')

    class Meta:
        list_serializer_class = MatchStatListSerializer
        read_only_fields = ['match_time']

    def get_match_time(self, obj):
        date = datetime.fromtimestamp(obj.game_start_time_stamp/1e3, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
        return date 

"""
