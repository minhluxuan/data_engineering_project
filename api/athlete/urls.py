from django.urls import path

from .views import uploadFile, AthleteBioView, AthleteBioUpdateDeleteView

urlpatterns = [
    path("upload_athleteBio/", uploadFile, name='upload_athleteBio'),
    # path('upload-country-profiles/', upload_country_profiles, name='upload-country-profiles'),
    path('athlete_bio/', AthleteBioView.as_view(), name='athletes'),
    path('athlete_bio/<int:option>/', AthleteBioView.as_view(), name='search_athlete'),
    path('athlete_bio_update/<int:id>/', AthleteBioUpdateDeleteView.as_view(), name='update_delete_athlete'),

]