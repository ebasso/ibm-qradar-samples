import requests
from requests.auth import HTTPBasicAuth
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QRadarSiem:
    def __init__(self, host, username, password, verify_ssl=True):
        self.base_url = f"{host.rstrip('/')}/api"
        self.auth = HTTPBasicAuth(username, password)
        self.verify_ssl = verify_ssl
        self.headers = { "Accept": "application/json", "Content-Type": "application/json", "Version": "20.0" }
        
    def get_offense_types(self):
        url = f"{self['base_url']}/siem/offense_types"
        headers = self.headers
        headers["Range"] = "items=0-49"

        res = requests.get(url=url, headers=headers, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        return None

    # https://ibmsecuritydocs.github.io/qradar_api_20.0/20.0--siem-offenses-GET.html
    def get_offenses(self, range='items=0-40', params={}):
        url = f"{self.base_url}/siem/offenses"
        
        headers = self.headers
        headers["Range"] = range

        res = requests.get(url=url, headers=headers, params=params, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        return None
    
    def get_offense(self, offense_id):
        url = f"{self.base_url}/siem/offenses/{offense_id}"
        res = requests.get(url=url, headers=self.headers, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        return None

    # def create_offense(self, data):
    #     url = f"{self.base_url}/siem/offenses"
    #     res = requests.post(url=url, headers=self.headers, json=data, auth=self.auth, verify=self.verify_ssl)
    #     if res.status_code in (200, 201):
    #         return res.json()
    #     return None

    def update_offense(self, offense_id, params):
        url = f"{self.base_url}/siem/offenses/{offense_id}"
        res = requests.post(url=url, headers=self.headers, params=params, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        return None
    
    def create_note_offense(self, offense_id, note_text):
        url = f"{self.base_url}/siem/offenses/{offense_id}/notes"
        params = { "note_text": note_text }
        res = requests.post(url=url, headers=self.headers, params=params, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        return None

    # def delete_offense(self, offense_id):
    #     url = f"{self.base_url}/siem/offenses/{offense_id}"
    #     res = requests.delete(url=url, headers=self.headers, auth=self.auth, verify=self.verify_ssl)
    #     return res.status_code == 204
    
    def get_network_hierarchy(self):
        url = f"{self.base_url}/config/network_hierarchy/staged_networks"

        res = requests.get(url=url, headers=self.headers, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        return None