class mode:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client
        
    def from_recent_playlist_create_playlist(self,spotify_client):
            # get last played tracks
        num_tracks_to_visualise = int(input("How many tracks would you like to visualise? "))
        last_played_tracks = spotify_client.get_last_played_tracks(num_tracks_to_visualise)
    
        print(f"\nHere are the last {num_tracks_to_visualise} tracks you listened to on Spotify:")
        for index, track in enumerate(last_played_tracks):
            print(f"{index+1}- {track}")
    
        # choose which tracks to use as a seed to generate a playlist
        indexes = input("\nEnter a list of up to 5 tracks you'd like to use as seeds. Use indexes separated by a space: ")
        indexes = indexes.split()
        seed_tracks = [last_played_tracks[int(index)-1] for index in indexes]
    
        # get recommended tracks based off seed tracks
        recommended_tracks = spotify_client.get_track_recommendations(seed_tracks)
        print("\nHere are the recommended tracks which will be included in your new playlist:")
        for index, track in enumerate(recommended_tracks):
            print(f"{index+1}- {track}")
    
        # get playlist name from user and create playlist
        playlist_name = input("\nWhat's the playlist name? ")
        playlist = spotify_client.create_playlist(playlist_name)
        print(f"\nPlaylist '{playlist.name}' was created successfully.")
    
        # populate playlist with recommended tracks
        spotify_client.populate_playlist(playlist, recommended_tracks)
        print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")
        
        
    def from_artist_create_playlist(self,spotify_client):
        #show artist name
        print("""
              *******************************************
              you can use a artist as a seed
              
              
              """)
        while 1:
            seed_artist = str(input("which artist you want to listen(enter id): "))
            print("\'"+spotify_client.show_artist_name(seed_artist)+"\'"+" is the artist which you want to be seed")
            choose = str(input("y/n:"))
            if choose == 'y' or choose == 'Y':
                break
        #get recommand playlist
        recommended_tracks = spotify_client.get_artist_recommendations(seed_artist)
        print("\nHere are the recommended tracks which will be included in your new playlist:")
        for index, track in enumerate(recommended_tracks):
            print(f"{index+1}- {track}")
            
        # get playlist name from user and create playlist
        playlist_name = input("\nWhat's the playlist name? ")
        playlist = spotify_client.create_playlist(playlist_name)
        print(f"\nPlaylist '{playlist.name}' was created successfully.")
        
        
        # populate playlist with recommended tracks
        spotify_client.populate_playlist(playlist, recommended_tracks)
        print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")

    def from_url_create_playlist(self,spotify_client):
        #input href
        print("""
              *******************************************
              you can paste the complete web api address here
              
              """)
        href = str(input("Please paste your href:  "))
        
        #get response
        response = spotify_client._place_get_api_request(href)
        response_json = response.json()
        #get track
        tracks = spotify_client.process_tracks_list(response_json)
        print("\nHere are the tracks which will be included in your new playlist:")
        for index, track in enumerate(tracks):
            print(f"{index+1}- {track}")    
        
        #create playlist  
        playlist_name = input("\nWhat's the playlist name? ")
        playlist = spotify_client.create_playlist(playlist_name)
        print(f"\nPlaylist '{playlist.name}' was created successfully.")
        
        
        # populate playlist with recommended tracks
        spotify_client.populate_playlist(playlist,tracks)
        print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")