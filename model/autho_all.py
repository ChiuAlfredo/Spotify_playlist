'''
    input client_id,client_secret
    
    output ouath token
    
    code by Coding For Entrepreneurs
        30days of python-19day
        
    9/9-v~variable has to re set
        v~choice how to store data
            1.return
            2.txt
            --final.json
        v~variable name has to be renamed according to website
        x~use time to detect to reget redirct or refresh code
    
    9/10 v~not import in createplaylist
         ~improve comment
         
    
        
    Obtaining Authorization:
        1.get_authorizes_access(return (code))
        
        2.post:
            token
            {
                url = {token_url},
                data = {get_token_data()},
                headers = {get_token_headers() - get_client_credentials()}
            }
            
            fresh_token
            {
                url = {token_url}
                data = {get_fresh_token_data()}
                headers = {get_token_headers() - get_client_credentials()}
            }
            
        3.gain_access_token() - read_upload_data()
            or
        gain_refresh_token() - read_upload_data()
        
        4.get_access_token()
        
        
'''

import requests
import datetime
from urllib.parse import urlencode
import base64
import json
import os 

class Auth():
    client_id = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_secret = None
    authorize_url = 'https://accounts.spotify.com/authorize'
    token_url = "https://accounts.spotify.com/api/token"
    redirect_uri = 'http://localhost:8888/callback/'
    scope = 'playlist-modify-public%20playlist-modify-private%20user-read-recently-played'
    code = None
    access_token = None
    refresh_token = None
    choice = 0
    auth_path = os.path.join('.', 'data', 'auth_token.json')
    def __init__(self,client_id,client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        
        current_dir = os.getcwd()
        print(current_dir)
        with open(self.auth_path) as f:
            data = json.load(f)
            try:
                refresh_token = data['refresh_token']
                self.refresh_token = refresh_token
            except:
                self.print_out('no fresh_token can use')
        

        
    def get_authorizes_access(self):
        '''
        

        Returns code 
        -------
        code : str
            this code can gain access token

        '''
        authorize_url = self.authorize_url
        client_id = self.client_id
        response_type = 'code'
        redirect_uri = self.redirect_uri
        scope = self.scope
        r=requests.get(f'{authorize_url}?client_id={client_id}&response_type={response_type}&redirect_uri={redirect_uri}&scope={scope}')
        self.print_out('please copy this url on your browse and copy the code on the url:',r.url)
        code =str(input('code : '))
            
        #update the variable
        self.code = code
        return code
    
    def get_client_credentials(self):
        '''
        return a base64 encoded string
        '''
        
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id ==None:
            raise Exception(self.print_out(' you must set client_id and client_secret'))
        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        
        
        return client_creds_b64.decode()

    def get_token_headers(self):
        '''
        return headers
        '''
        
        client_creds_b64 = self.get_client_credentials()
        token_headers = {
            "Authorization": f"Basic {client_creds_b64}"
        }
        return token_headers
        
    def get_token_data(self):
        '''
        return data
        '''
        code= self.get_authorizes_access()
        redirect_uri = self.redirect_uri
        token_data = {
            "grant_type": "authorization_code",
            "code": f"{code}",
            "redirect_uri":f"{redirect_uri}"
        } 
        return token_data
    
    def get_refresh_token_data(self):
        '''
        return refresh data
        '''
        refresh_token = self.refresh_token
        refresh_token_data={
            "grant_type": "refresh_token",
            "refresh_token": f"{refresh_token}",
        } 
        self.print_out('refresh_token_data :  ',str(refresh_token_data))
        return refresh_token_data
    
    def gain_access_token(self):
        '''
        

        Returns True
        -------
        upload access variable

        '''
        
        #set variable
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        
        r = requests.post(token_url, data=token_data, headers=token_headers)
        
        if r.status_code not in range(200, 299):
            #IS  fresh_token have time
            raise(self.print_out('access_token can\'t get , you can try fresh_token'))
            
            # return False
        
        #read data
        data = r.json()
        
        self.read_upload_data(data)
        
        return True
    
    def gain_refresh_token(self):
        '''
        

        Raises can't authenticate client'
        ------
        Exception
            DESCRIPTION.

        Returns True
        -------
        bool
            DESCRIPTION.

        '''
        #read datat
        with open(self.auth_path) as f:
            data = json.load(f)
            try:
                refresh_token = data['refresh_token']
                self.refresh_token = refresh_token
                refresh_token = self.refresh_token
                self.print_out('refresh_token',str(refresh_token))
            except:
                self.print_out('refresh_token can\'t get')
        
        
        token_url=self.token_url
        token_data=self.get_refresh_token_data()
        token_headers =self.get_token_headers()

        #post
        r = requests.post(token_url, data=token_data, headers=token_headers)
        
        self.print_out('gain_refresh_token\'s response',r)
        if r.status_code not in range(200, 299):
            self.print_out('no fresh_token')
            self.choice = 0
            
            # return False
        else:

            self.print_out('access_token by fresh_token')

            
            self.choice =1
            data = r.json()
        
            self.read_upload_data(data)

        return True
    
    def read_upload_data(self,data):
        '''
        

        Parameters
        ----------
        data : (json)
            import data

        Returns True
        -------
        None.

        '''
        data = data
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        try:
            refresh_token = data['refresh_token']
            self.print_out('refresh_token',refresh_token)
        except:
            self.print_out('second refresh_token')
        expires = now + datetime.timedelta(seconds=expires_in)
        
        
        self.print_out("access_token :  ",access_token)
        self.print_out('expires :  ',str(expires))
        
        #write data
        with open(self.auth_path,'w')as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
            
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        
        return True
        
    def get_access_token(self):
        '''
        

        Returns access_token
        -------
        access_token : str
            DESCRIPTION.

        '''
        self.gain_refresh_token()
        if self.choice !=1:
            self.gain_access_token()
        
        access_token = self.access_token
        
        return access_token
    
    def print_out(self,*args):
        print('')
        print('###############################################################')
        print('')
        for arg in args:
            print(arg)
            print('')
        
        
    

