from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.artist import Artist
from ..serializers import ArtistSerializer, UserSerializer

# Create your views here.
class Artists(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ArtistSerializer
    def get(self, request):
        """Index request"""
        # Get all the artists:
        # artists = Artist.objects.all()
        # Filter the artists by owner, so you can only see your owned artists
        artists = Artist.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ArtistSerializer(artists, many=True).data
        return Response({ 'artists': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['artist']['owner'] = request.user.id
        # Serialize/create artist
        artist = ArtistSerializer(data=request.data['artist'])
        # If the artist data is valid according to our serializer...
        if artist.is_valid():
            # Save the created artist & send a response
            artist.save()
            return Response({ 'artist': artist.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(artist.errors, status=status.HTTP_400_BAD_REQUEST)

class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the artist to show
        artist = get_object_or_404(Artist, pk=pk)
        # Only want to show owned artists?
        if not request.user.id == artist.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this artist')

        # Run the data through the serializer so it's formatted
        data = ArtistSerializer(artist).data
        return Response({ 'artist': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate artist to delete
        artist = get_object_or_404(Artist, pk=pk)
        # Check the artist's owner agains the user making this request
        if not request.user.id == artist.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this artist')
        # Only delete if the user owns the  artist
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['artist'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['artist'].get('owner', False):
            del request.data['artist']['owner']

        # Locate Artist
        # get_object_or_404 returns a object representation of our Artist
        artist = get_object_or_404(Artist, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == artist.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this artist')

        # Add owner to data object now that we know this user owns the resource
        request.data['artist']['owner'] = request.user.id
        # Validate updates with serializer
        data = ArtistSerializer(artist, data=request.data['artist'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
