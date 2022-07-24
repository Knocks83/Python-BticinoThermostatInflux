from requests import get, post
from json import loads
from os.path import exists


class Bticino:
    def __init__(self, ClientID: str, ClientSecret: str, Redirect: str, SubscriptionKey: str, PlantID: str, ModuleID: str, AuthEndpoint: str, APIEndpoint: str, RefreshTokenPath: str):
        self.__ClientID = ClientID
        self.__ClientSecret = ClientSecret
        self.__Redirect = Redirect
        self.__SubscriptionKey = SubscriptionKey
        self.__PlantID = PlantID
        self.__ModuleID = ModuleID
        self.__AuthEndpoint = AuthEndpoint
        self.__APIEndpoint = APIEndpoint
        self.__RefreshTokenPath = RefreshTokenPath

        self.__AccessToken = None
        self.__RefreshToken = None

        if exists(self.__RefreshTokenPath):
            with open(self.__RefreshTokenPath, 'r') as f:
                self.__RefreshToken = f.read()


    def __SetRefreshToken(self, refresh_token):
        self.__RefreshToken = refresh_token
        with open(self.__RefreshTokenPath, 'w+') as f:
            f.write(self.__RefreshToken)


    # Unimplemented: an actual internal login page to log onto the LeGrand website.
    """
    def authorize(self):
        get_params = {
            'client_id': self.__ClientID,
            'redirect_uri': self.__Redirect,
            'response_type': 'code'
        }
        res = get(params=get_params, url=self.__AuthEndpoint+'authorize')
        return ''
    """


    def __authorize(self):
        if self.__RefreshToken is not None:
            return

        # Generate a string to send to the user and ask for the code
        url = self.__AuthEndpoint+f"authorize?client_id={self.__ClientID}&response_type=code&redirect_uri={self.__Redirect}"
        code = input(url+"\nType the code: ").strip()

        # Send the code to the backend, ask for updated access token and the refresh token
        post_data = {
            'client_id': self.__ClientID,
            'grant_type': 'authorization_code',
            'code': code,
            'client_secret': self.__ClientSecret
        }
        res = post(data=post_data, url=self.__AuthEndpoint+'token')

        # Parse the result and save both the access tokena nd the refresh token
        parsed = loads(res.content)
        self.__AccessToken = parsed['access_token']
        self.__SetRefreshToken(parsed['refresh_token'])


    # Refresh the token flow
    def __token(self):
        post_data = {
            'client_id': self.__ClientID,
            'grant_type': 'refresh_token',
            'refresh_token': self.__RefreshToken,
            'client_secret': self.__ClientSecret
        }
        res = post(data=post_data, url=self.__AuthEndpoint+'token')
        
        parsed = loads(res.content)
        # If there's an error, authorize again.
        if 'error' in parsed:
            # Clear variables
            self.__RefreshToken = None
            self.__AccessToken = None

            self.login()

        self.__AccessToken = parsed['access_token']
        self.__SetRefreshToken(parsed['refresh_token'])


    def login(self):
        self.__authorize()
        self.__token()


    def measures(self):
        url = self.__APIEndpoint+f"chronothermostat/thermoregulation/addressLocation/plants/{self.__PlantID}/modules/parameter/id/value/{self.__ModuleID}"
        headers = {
            'Ocp-Apim-Subscription-Key': self.__SubscriptionKey,
            'Authorization': f"Bearer {self.__AccessToken}"
        }

        res = get(headers=headers, url=url)
        parsed = loads(res.content)
        
        if 'code' in parsed:
            self.login()
            self.measures()

        # Return a dictionary, the last element is a boolean.
        return {
            'temperature': parsed['chronothermostats'][0]['thermometer']['measures'][0]['value'],
            'humidity': parsed['chronothermostats'][0]['hygrometer']['measures'][0]['value'],
            'status': parsed['chronothermostats'][0]['loadState'] == 'ACTIVE'
        }
