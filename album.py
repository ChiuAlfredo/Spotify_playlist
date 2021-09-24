class Album:
    """Track represents a piece of music."""

    def __init__(self, album_name, id, artist):
        """
        :param name (str): Album name
        :param id (int): Spotify Album id
        :param artist (str): Artist who created the track
        """
        self.album_name = album_name
        self.id = id
        self.artist = artist

    
    def album_id(self):
        return f"{self.id}"

