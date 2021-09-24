
from spotifyclient import SpotifyClient
from mode import mode
from autho_all import Auth
def main():
    '''
    use 
    $ export SPOTIFY_AUTHORIZATION_TOKEN=value_grabbed_from_spotify

    $ export SPOTIFY_USER_ID=value_grabbed_from_spotify
    '''
    client_id,client_secret,user_name = attain_account()
    print("""
          Welcome To Use Spotify Create Playlist
          """)

    print('                      Client Inf                               ')
    print_out('client_id is : %s'%client_id,
              'client_secret is : %s'%client_secret,
              'user_name is : %s'%user_name)      
    print('                        Choose                                     ')
    print_out(          '1)Use recent play songs as seeds to create a recommand playlist',
          '2)Use a artist as a seed to craete a recommand playlist',
          '3)Use a spotify href to create a playlist')  

    
    choose_mode = int(input("which mode you want to choose: "))

    auth = Auth(client_id,client_secret)    
    autho_token = auth.get_access_token()
    
    spotify_client = SpotifyClient(autho_token ,
                                           user_name )
    mode_choose = mode(spotify_client)
    if choose_mode ==1:
        mode_choose.from_recent_playlist_create_playlist(spotify_client)
    if choose_mode ==2:
        mode_choose.from_artist_create_playlist(spotify_client)
    if choose_mode ==3:
        mode_choose.from_url_create_playlist(spotify_client)
        
    
def print_out(*args):
    print('*******************************************************************')
    print('')
    print('')
    for arg in args:
        print(arg.strip())
        print('')


def divi(line):
    new = line.split(":")
    new_line = new[1].strip()
    
    return new_line

def attain_account():
    account_id=''
    account_secret=''
    account_name = ''
    with open('account.txt','r') as ac:
        account_id = str(divi(ac.readline()))
        account_secret = str(divi(ac.readline()))
        account_name = str(divi(ac.readline()))
        
    return account_id,account_secret,account_name
    


if __name__ == "__main__":
    main()
    
    
