import requests
from requests.auth import HTTPBasicAuth
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class QRadarSoar:
    def __init__(self, host, api_key_id, api_key_secret, org_id=201, verify_ssl=True):
        self.base_url = f"{host.rstrip('/')}/rest/orgs/{org_id}"
        self.auth = HTTPBasicAuth(api_key_id, api_key_secret)
        self.verify_ssl = verify_ssl
        self.headers = {
            "Content-Type": "application/json"
        }
        
    def get_incidents(self, conditions=None, sorts=[], start=0, limit=10):
        url = f"{self.base_url}/incidents/query_paged"
        params = {
            "return_level": "full",
            "field_handle": "",
            "include_records_total": "false"
        }
        if conditions is None:
            conditions = [
                {
                    "field_name": "plan_status",
                    "method": "in",
                    "value": ["A"]
                }
            ]
        json_body = {
            "filters": [
                {
                    "conditions": conditions
                }
            ],
            "sorts": sorts,
            "start": start,
            "length": limit
        }

        res = requests.post(url=url, headers=self.headers, json=json_body,
                                 params=params, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        else:
            return None

    def create_incident(self, data):
        url = f"{self.base_url}/incidents"
        res = requests.post(url, headers=self.headers, json=data, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        else:
            return None

    def get_incident(self, incident_id):
        url = f"{self.base_url}/incidents/{incident_id}"
        res = requests.get(url, headers=self.headers, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        else:
            return None

    def update_incident(self, incident_id, data):
        url = f"{self.base_url}/incidents/{incident_id}"
        res = requests.put(url, headers=self.headers, json=data, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return res.json()
        else:
            return None

    def delete_incident(self, incident_id):
        url = f"{self.base_url}/incidents/{incident_id}"
        res = requests.delete(url, headers=self.headers, auth=self.auth, verify=self.verify_ssl)
        if res.status_code == 200:
            return {"message": "Incident deleted"}
        else:
            return None