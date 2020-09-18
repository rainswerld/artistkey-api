from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.track import Track
from ..serializers import TrackSerializer, UserSerializer

# Create your views here.
class Tracks(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = TrackSerializer
    def get(self, request, artist_id):
        """Index request"""
        # Get all the tracks:
        # tracks = Track.objects.all()
        # Filter the tracks by artist, so you can only see your owned tracks
        artist_tracks = Track.objects.filter(artist=artist_id)

        # # Run the data through the serializer
        data = TrackSerializer(artist_tracks, many=True).data
        return Response({ 'tracks': data })

    def post(self, request, artist_id):
        """Create request"""
        print(request.data)
        # Add track to specific artist
        # request.data['track'] = request.track.owner.id
        # Serialize/create track
        track = TrackSerializer(data=request.data['track'])
        # If the track data is valid according to our serializer...
        if track.is_valid():
            # Save the created artist & send a response
            track.save()
            return Response({ 'track': track.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(track.errors, status=status.HTTP_400_BAD_REQUEST)

class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, track_id):
        """Show request"""
        # Locate the track to show
        track = get_object_or_404(Track, id=track_id)
        # Only want to show owned tracks?
        # if not request.artist.owner.id == artist.owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own the artist this track is attached to')

        # Run the data through the serializer so it's formatted
        print(track)
        data = TrackSerializer(track).data
        return Response({ 'track': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate artist to delete
        track = get_object_or_404(Track, pk=pk)
        # Check the artist's owner agains the user making this request
        # if not request.user.id == track.artist.id:
        #     raise PermissionDenied('Unauthorized, you do not own this artist')
        # Only delete if the user owns the  artist
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, track_id):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['artist'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        # if request.data['track'].get('owner', False):
        #     del request.data['track']['owner']
        # Locate Track
        # get_object_or_404 returns a object representation of our Artist
        track = get_object_or_404(Track, id=track_id)
        # Check if user is the same as the request.user.id
        # if not request.user.id == artist.owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own this artist')

        # Add owner to data object now that we know this user owns the resource
        # request.data['track']['artist']['owner'] = request.artist.owner.id
        # Validate updates with serializer
        data = TrackSerializer(track, data=request.data['track'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
