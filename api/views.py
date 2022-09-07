from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from .constants import (
    RIOT_API_KEY_HEADER,
    server_to_region_map,
)

from .use_cases import get_lobby_summoner_stats

class LobbyView(APIView):
    '''
    Returns ranked lobby statistics
    '''
    def get(self, request, *args, **kwargs):
        params = request.query_params
        server = params.get('server')
        summoners = [params.get('summoner1'), params.get('summoner2'), params.get('summoner3'), params.get('summoner4'), params.get('summoner5')]

        summoner_json = {}
        for summoner in summoners:
            # print(server, summoner)
            url = "https://" + server + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner
            res = requests.get(url, headers=RIOT_API_KEY_HEADER)
            if(res.status_code == 200):
                data = res.json()
                summoner_json.update({
                    summoner: get_lobby_summoner_stats(data.get('name'), data.get('puuid'), data.get('id'), server, server_to_region_map.get(server))
                })
            else:
                summoner_json.update({summoner: None})

        return Response(summoner_json, status=status.HTTP_200_OK)

"""
class CreateSummonerView(APIView):
    '''
    Creates a new summoner
    Returns Summoner, RankedSoloStat, ChampionStat(s), (10) MatchStat(s) data for the current season
    '''
    def post(self, request, *args, **kwargs):
        data = request.data
        server = data.get('server')
        name = data.get('name')

        url = "https://" + server + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)
        if(res.status_code == 404):
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = res.json()

        summoner_data = {
            'summoner_id': data.get('id'),
            'account_id': data.get('accountId'),
            'puuid': data.get('puuid'),
            'name': data.get('name'),
            'profile_icon_id': data.get('profileIconId'),
            'revision_date': data.get('revisionDate'),
            'summoner_level': data.get('summonerLevel'),
            'server': server,
        }
        summoner_data['region'] = server_to_region_map.get(summoner_data.get('server'))
        summoner_data['season'] = get_season(summoner_data.get('revision_date'), summoner_data.get('region'))

        summoner_serializer = SummonerSerializer(data=summoner_data)
        
        if not summoner_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        summoner = summoner_serializer.save()

        get_match_history(summoner)

        try:
            ranked_solo_stats = RankedSoloStat.objects.get(summoner_id=summoner.id, season=summoner.season)
            champion_stats = ChampionStat.objects.filter(summoner_id=summoner.id, season=summoner.season).order_by('-games_played')
            match_stats = MatchStat.objects.filter(summoner_id=summoner.id).reverse()[0:10]
            serializer = search_z_rift(summoner, ranked_solo_stats, champion_stats, match_stats)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer, status=status.HTTP_201_CREATED)

class UpdateSummonerView(APIView):
    '''
    Updates a summoner
    Returns Summoner, RankedSoloStat, ChampionStat(s), (10) MatchStat(s) data for the current season
    '''
    def post(self, request, *args, **kwargs):
        data = request.data
        server = data.get('server')
        name = data.get('name')

        url = 'https://' + server + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)
        data = res.json()

        summoner = Summoner.objects.get(
            puuid=data.get('puuid')
        )

        try: 
            ranked_solo_stat = RankedSoloStat.objects.get(
                summoner=summoner,
                season=summoner.season,
            )
        except:
            ranked_solo_stat = None

        summoner_data = {
            'summoner_id': data.get('id'),
            'account_id':data.get('accountId'),
            'puuid': data.get('puuid'),
            'name': data.get('name'),
            'profile_icon_id': data.get('profileIconId'),
            'revision_date': data.get('revisionDate'),
            'summoner_level': data.get('summonerLevel'),
            'server': server,
        }
        summoner_data['region'] = server_to_region_map.get(summoner_data.get('server'))
        summoner_data['season'] = get_season(summoner_data.get('revision_date'), summoner_data.get('region'))

        summoner_serializer = SummonerSerializer(summoner, data=summoner_data)

        if not summoner_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        summoner = summoner_serializer.save()

        get_match_history(summoner, ranked_solo_stat)

        try:
            ranked_solo_stats = RankedSoloStat.objects.get(summoner_id=summoner.id, season=summoner.season)
            champion_stats = ChampionStat.objects.filter(summoner_id=summoner.id, season=summoner.season).order_by('-games_played')
            match_stats = MatchStat.objects.filter(summoner_id=summoner.id).reverse()[0:10]
            serializer = search_z_rift(summoner, ranked_solo_stats, champion_stats, match_stats)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer, status=status.HTTP_200_OK)

class SummonerView(APIView):
    '''
    Returns Summoner
    '''
    def get(self, request, *args, **kwargs):
        try:
            params = request.query_params
            server = params.get('server')
            name = params.get('name')

            summoner = Summoner.objects.get(name__iexact=name, server=server)
            summoner_serializer = SummonerSerializer(summoner)
        except Summoner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(summoner_serializer.data, status=status.HTTP_200_OK)

class RankedSoloStatView(APIView):
    '''
    Returns RankedSoloStats for a summoner's current season
    '''
    def get(self, request, *args, **kwargs):
        try:
            params = request.query_params
            server = params.get('server')
            name = params.get('name')

            summoner = Summoner.objects.get(name__iexact=name, server=server)
            ranked_solo_stat = RankedSoloStat.objects.get(summoner_id=summoner.id, season=summoner.season)
            serializer = RankedSoloStatSerializer(ranked_solo_stat)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ChampionStatView(APIView):
    '''
    Returns ChampionStat(s) for a summoner's current season
    '''
    def get(self, request, *args, **kwargs):
        try:
            params = request.query_params
            server = params.get('server')
            name = params.get('name')

            summoner = Summoner.objects.get(name__iexact=name, server=server)
            champions = ChampionStat.objects.filter(summoner_id=summoner.id, season=summoner.season).order_by('-games_played')
            serializer = ChampionStatSerializer(champions, many=True)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MatchStatView(APIView):
    '''
    Returns MatchStat(s) for a summoner's current season
    '''
    def get(self, request):
        try:
            params = request.query_params
            server = params.get('server')
            name = params.get('name')
            
            summoner = Summoner.objects.get(name__iexact=name, server=server)
            match_stat = MatchStat.objects.filter(summoner_id=summoner.id, season=summoner.season)
            serializer = MatchStatSerializer(match_stat, many=True)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchZRiftView(APIView):
    '''
    Returns Summoner, RankedSoloStat, ChampionStat(s), (10) MatchStat(s) data for the current season
    '''
    def get(self, request, *args, **kwargs):
        try:
            params = request.query_params
            server = params.get('server')
            name = params.get('name')

            summoner = Summoner.objects.get(name__iexact=name, server=server)
            ranked_solo_stat = RankedSoloStat.objects.get(summoner_id=summoner.id, season=summoner.season)
            champion_stats = ChampionStat.objects.filter(summoner_id=summoner.id, season=summoner.season).order_by('-games_played')
            match_stats = MatchStat.objects.filter(summoner_id=summoner.id).reverse()[0:10]
    
            serializer = search_z_rift(summoner, ranked_solo_stat, champion_stats, match_stats)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer, status=status.HTTP_200_OK)     
"""