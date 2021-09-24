import json

import requests

from track import Track
from playlist import Playlist
from album import Album


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._authorization_token = authorization_token
        self._user_id = user_id

    def print_out(*args):
        print('*******************************************************************')
        print('')
        print('')
        for arg in args:
            print(arg)
            print('')
            
    def get_last_played_tracks(self, limit=10):
        """Get the last n tracks played by a user

        :param limit (int): Number of tracks to get. Should be <= 50
        :return tracks (list of Track): List of last played tracks
        """
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        #hard to understand
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for track in response_json["items"]]
             
        return tracks

    def get_track_recommendations(self, seed_tracks, limit=50):
        """Get a list of recommended tracks starting from a number of seed tracks.

        :param seed_tracks (list of Track): Reference tracks to get recommendations. Should be 5 or less.
        :param limit (int): Number of recommended tracks to be returned
        :return tracks (list of Track): List of recommended tracks
        """
        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = self.process_tracks_list(response_json)
        return tracks

    def create_playlist(self, name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        data = json.dumps({
            "name": name,
            "description": "Recommended songs",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        print(response_json)
        # create playlist
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def populate_playlist(self, playlist, tracks):
        """Add tracks to a playlist.

        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        #
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        return response_json

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response
    
    def get_artist_recommendations(self, artist_id, limit=50):
        """Get a list of recommended tracks starting from a number of seed tracks.

        :param seed_artist (artist id): Reference artist to get recommendations. Should be 1.
        :param limit (int): Number of recommended tracks to be returned
        :return tracks (list of Track): List of recommended tracks
        """

        url = f"https://api.spotify.com/v1/recommendations?seed_artists={artist_id}&limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = self.process_tracks_list(response_json)
        return tracks
    def show_artist_name(self,artist_id):
        '''

        Parameters
        ----------
        artist_id : TYPE
            DESCRIPTION.

        Returns
        -------
        artist_name : TYPE
            DESCRIPTION.

        '''
        url=f"https://api.spotify.com/v1/artists/{artist_id}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        artist_name = response_json['name']
        return artist_name
    
    
    def process_tracks_list(self,response_json):
        tracks = []
        response_json = response_json
        try:
            tracks += self.only_tracks(response_json)
        except:
            print('')
            print("no track")
            print('-------------------------------------')
            print('')
            
        try:
            tracks += self.albums_to_tracks(response_json)
        except:
            print('')
            print("no album")
            print('-------------------------------------')
            print('')
            
        return tracks
    
    def only_tracks(self,response_json):
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                  track in response_json["tracks"]]
        return tracks
    
    def albums_to_tracks(self,response_json):
        '''
        
        '''
        repeat_time = len(response_json['albums']['items'] )
        albums = self.read_albums(response_json,repeat_time)
        tracks = self.list_albums_tracks(albums,repeat_time)
        return tracks
    
    def read_albums(self,response_json,repeat_time):
        albums=[]

        for i in range(repeat_time):
            print(response_json['albums']['items'][i]['name'])
            albums+=[Album(response_json['albums']['items'][i]['name'],
                    response_json['albums']['items'][i]['id'],
                    response_json['albums']['items'][i]['artists'][0]['name'])]  
        
        return albums
    
    def list_albums_tracks(self,albums,repeat_time):
        limit = 30
        tracks=[]
        albums_id = [album.album_id() for album in albums]
        for album_id in albums_id:
            print(album_id)
            url = f'https://api.spotify.com/v1/albums/{album_id}/tracks?{limit}'
            response = self._place_get_api_request(url)
            response_json = response.json()
            tracks +=self.album_tracks(response_json)
            
        print('end')
        return tracks
    
    
    def album_tracks(self,response_json):
        tracks = []
        for i in range(response_json['total']):
            try:
                tracks +=[Track(response_json['items'][i]['name'],
                                response_json['items'][i]['id'],
                                response_json['items'][i]['artists'][0]['name'])]
                print((response_json['items'][i]['name'],
                                response_json['items'][i]['id'],
                                response_json['items'][i]['artists'][0]['name']))
            except:
                print(f'{i}:wrong')
            print(i) 
        return tracks