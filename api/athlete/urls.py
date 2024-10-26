from django.urls import path

from .views import uploadFile, AthleteBioView

urlpatterns = [
    path("upload_athleteBio/", uploadFile, name='upload_athleteBio'),
    # path('upload-country-profiles/', upload_country_profiles, name='upload-country-profiles'),
    path('athlete_bio/', AthleteBioView.as_view(), name='athletes'),
    path('athlete_bio/<int:id>/', AthleteBioView.as_view(), name='update_delete_athlete'),
]