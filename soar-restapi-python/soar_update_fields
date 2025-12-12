import os
import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========================== PRODUCAO ==========================
SOAR_CONFIG = {
    "host": os.environ.get("SOAR_HOST", "https://soar.company.com"),
    # Ajustes em campos
    "api_key": os.environ.get("SOAR_API_KEY", ""),
    "api_secret": os.environ.get("SOAR_API_SECRET", ""),  
    "org_id": int(os.environ.get("SOAR_ORG_ID", 201))
}

def get_inc_status(id=None):
    """
    return a description
    """
    if id is not None:
        if id == 12345:
            return "Open"
        elif id == 67890:
            return "Closed"
    return "Unknown"


def get_soar_client():
    return {
        "host": SOAR_CONFIG['host'],
        "api_key_id": SOAR_CONFIG['api_key'],
        "api_key_secret": SOAR_CONFIG['api_secret'],
        "org_id": SOAR_CONFIG['org_id'],
        "auth": HTTPBasicAuth(SOAR_CONFIG['api_key'], SOAR_CONFIG['api_secret']),
        "base_url": f"{SOAR_CONFIG['host']}/rest/orgs/{SOAR_CONFIG['org_id']}"
    }
    
def soar_get_incidents(soar_client):
    """
    Get Incidents on SOAR, plan_status = Closed and incident_status is null and incident_type_ids not 1719 
    """
    headers = { "Accept": "application/json", "Content-Type": "application/json" }
    url = f"{soar_client['base_url']}/incidents/query_paged"
    params = {
        "return_level": "normal",
        "field_handle": ["incident_status"],
        "include_records_total": "false"
    }
    json_body = {"filters": [{"conditions": [
        { "field_name":"plan_status","method":"in","value":["C"]},
        { "field_name":"incident_type_ids","method":"not_in","value":[1719]},
        {"field_name":"properties.incident_status","method":"not_has_a_value"}
        ]}]
    }
   # { "field_name": "properties.incident_status","method": "not_in","value": [96609]}
   # { "field_name": "properties.trendmicro_investigation_result","method": "has_a_value"},

    res = requests.post(url=url, headers=headers, json=json_body,
                                params=params, auth=soar_client['auth'], verify=False)
    if res.status_code == 200:
        #print(res.json())
        return res.json()
    else:
        raise Exception(
            f"Failed to fetch incidents: {res.status_code} - {res.text}")

def soar_update_incident(soar_client, incident_id, json_body):
    """
     Update incident on SOAR
    """
    headers = {"Content-Type": "application/json"}
    url = f"{soar_client['base_url']}/incidents/{incident_id}"
    params = { "return_dto": "false" }
    res = requests.patch(url, headers=headers, json=json_body, params=params, auth=soar_client['auth'], verify=False)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to update incident: {res.status_code} - {res.text}")
        return None

def update_fields_on_soar(soar_client):
    """
    Get Incidents from SOAR and update fields
    """
    try:
        print(f"update_fields_on_soar: starting...")
        json_data = soar_get_incidents(soar_client)
        incidents = json_data.get("data", [])

        print(f"  incidents = {len(incidents)}")
        incident_count = 0
        for inc in incidents[:1]:   # for testing, remove [:1] to process all
            soar_id = inc.get('id','')
            soar_properties = inc.get('properties', {})
            src_value01 = soar_properties.get('incident_status', '')
            dst_value01 = get_inc_status(src_value01)
            
            changes = []
            changes.append( {"field": "incident_status", "old_value": {}, "new_value": 12345 } )
            changes.append( {"field": "field_name2", "old_value": {}, "new_value": { "text": "new_value" }} )

            payload = { "changes": changes }
            
            print(f"  soar_id: {soar_id} - {src_value01} - {dst_value01} - {payload}")
            
            result = soar_update_incident(soar_client, soar_id, payload)
            if result and result.get('success', False):
                print(f"      incident {soar_id} altered.")
                incident_count += 1

        print(f"update_fields_on_soar: finished.  updated incidents = {incident_count}")
        print("")
        return "OK"
    except Exception as e:
        print(f"update_fields_on_soar: Error: {e}")
        return "FAIL"
    
if __name__ == "__main__":
    print("main starting ********************************************************")
    soar_client = get_soar_client()

    res1 = update_fields_on_soar(soar_client)
    print("main finished ********************************************************")
    print(f"  update_fields_on_soar:             [{res1}]")
