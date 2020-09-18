from django.urls import path
from .views.artist_views import Artists, ArtistDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.track_views import Tracks, TrackDetail

urlpatterns = [
  	# Restful routing
    path('artists/', Artists.as_view(), name='artists'),
    path('artists/<int:pk>/', ArtistDetail.as_view(), name='artist_detail'),
    path('new-artist/', Artists.as_view(), name='new-artist'),
    path('tracks/<int:artist_id>', Tracks.as_view(), name='tracks'),
    path('tracks/track/<int:track_id>', TrackDetail.as_view(), name='update-track'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
