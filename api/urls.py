from django.urls import path
from .views.artist_views import Artists, ArtistDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('artists/', Artists.as_view(), name='artists'),
    path('new-artist/', Artists.as_view(), name='new-artist'),
    path('artists/<int:pk>/', ArtistDetail.as_view(), name='artist_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
