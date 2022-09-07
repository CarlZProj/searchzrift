from django.urls import path, include
from .views import (
    LobbyView,
)

urlpatterns = [
    path('lobby/', LobbyView.as_view(), name="lobby"),
    # path('summoners/create/', CreateSummonerView.as_view(), name='create-summoner'),
    # path('summoners/update/', UpdateSummonerView.as_view(), name='update-summoner'),
    # path('summoners/', SummonerView.as_view(), name='summoner'),
    # path('rankedsolostat/', RankedSoloStatView.as_view(), name="rankedsolostat"),
    # path('championstat/', ChampionStatView.as_view(), name='championstat'),
    # path('matchstat/', MatchStatView.as_view(), name='matchstat'),
    # path('searchzrift/', SearchZRiftView.as_view(), name="searchzrift"),
]
