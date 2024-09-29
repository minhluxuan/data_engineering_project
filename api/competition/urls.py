from django.contrib import admin
from django.urls import path

from competition.views import EventResultView

urlpatterns = [
    # URL cho EventResultView
    path('event-result/', EventResultView.as_view(), name='event_result_post'),  # POST cho việc tạo event result
    path('event-result/<int:athlete_id>/<int:result_id>/<str:country_noc>/<int:edition_id>/', 
         EventResultView.as_view(), name='event_result_update'),  # PUT để cập nhật kết quả
    path('event-results/', EventResultView.as_view(), name='event_result_list'),  # GET cho danh sách kết quả
]