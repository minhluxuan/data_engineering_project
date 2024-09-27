from django.urls import path
from api.competition.views.medalTableViews import MedalTableView

urlpatterns = [
    path("medaltally/", MedalTableView.as_view(), name="medal_table_search"),
    # path("medaltally/<int:id>/", MedalTableView.as_view(), name="competition"),
]
