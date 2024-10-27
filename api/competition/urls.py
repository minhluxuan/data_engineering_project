from .views import ResultView
from .views import EventResultView, upload_event_results
from django.contrib import admin
from django.urls import path
from .views import MedalTableView


urlpatterns = [
    path('results/', ResultView.as_view(), name='results'),
    path("medaltally/", MedalTableView.as_view(), name="medal_table_search"),
    path("medaltally/<int:id>/", MedalTableView.as_view(), name="competition"),
    # URL cho EventResultView
    path('upload-results/', upload_event_results, name='upload_event_results'),
    path('eventresult/', EventResultView.as_view(),
         name='event_result_post'),  # POST cho việc tạo event result
    path('eventresult/<int:edition_id>-<str:country_noc>-<int:result_id>-<int:athlete_id>/',
         EventResultView.as_view(), name='event_result_detail'),
    path('eventresult/u/<int:edition_id>-<str:country_noc>-<int:result_id>-<int:athlete_id>/',
         EventResultView.as_view(), name='event_result_update'),
    path('eventresult/d/<int:edition_id>-<str:country_noc>-<int:result_id>-<int:athlete_id>/',
         EventResultView.as_view(), name='event_result_delete'),
    # path('eventresult/<int:athlete_id>/<int:result_id>/<str:country_noc>/<int:edition_id>/',
    #      EventResultView.as_view(), name='event_result_update'),  # PUT để cập nhật kết quả
    # path('eventresults/', EventResultView.as_view(), name='event_result_list'),  # GET cho danh sách kết quả
]
