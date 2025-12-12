import os
import requests
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SOAR_CONFIG = {
    "host": os.environ.get("SOAR_HOST", "https://soar.company.com"),
    # Ajustes em campos
    "api_key": os.environ.get("SOAR_API_KEY", ""),
    "api_secret": os.environ.get("SOAR_API_SECRET", ""),  
    "org_id": int(os.environ.get("SOAR_ORG_ID", 201))
}

LENGTH_LIMIT = 100

def get_soar_client():
    return {
        "host": SOAR_CONFIG['host'],
        "api_key_id": SOAR_CONFIG['api_key'],
        "api_key_secret": SOAR_CONFIG['api_secret'],
        "org_id": SOAR_CONFIG['org_id'],
        "auth": HTTPBasicAuth(SOAR_CONFIG['api_key'], SOAR_CONFIG['api_secret']),
        "base_url": f"{SOAR_CONFIG['host']}/rest/orgs/{SOAR_CONFIG['org_id']}"
    }
    
def soar_artifacts_get_related_incidents(soar_client, artifact_id):
    """
    Get Incidents on SOAR
    """
    headers = { "Accept": "application/json", "Content-Type": "application/json" }
    url = f"{soar_client['base_url']}/artifacts/{artifact_id}/related_incident_artifacts/query_paged"
    json_body = {"start":0,"length":LENGTH_LIMIT,"sorts":[],"filters":[{"conditions":[]}]}
    
    res = requests.post(url=url, headers=headers, json=json_body,
                                auth=soar_client['auth'], verify=False)
    if res.status_code == 200:
        #print(res.json())
        return res.json()
    else:
        raise Exception(
            f"Failed to fetch incidents: {res.status_code} - {res.text}")

def soar_delete_incident_artifact(soar_client, incident_id, artifact_id):
    """
     Delete incident artifact on SOAR
    """
    headers = {"Content-Type": "application/json"}
    url = f"{soar_client['base_url']}/incidents/{incident_id}/artifacts/{artifact_id}"
    
    res = requests.delete(url, headers=headers, auth=soar_client['auth'], verify=False)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to update incident: {res.status_code} - {res.text}")
        return None

def deletes_artifacts_on_soar(soar_client, artifact_id):
    """
    Get Incidents from SOAR and update fields
    """
    try:
        print(f"deletes_artifacts_on_soar: starting...")
        json_data = soar_artifacts_get_related_incidents(soar_client,artifact_id)
        incidents = json_data.get("data", [])

        print(f"  incidents = {len(incidents)}")
        incident_count = 0
        for inc in incidents: #[:1]:
            soar_id = inc.get('inc_id','')
            soar_artifact_id = inc.get('inc_artifact_id','')
            soar_artifact_value = inc.get('inc_artifact_value','')

            print(f"  soar_id: {soar_id} - inc_artifact_id: {soar_artifact_id} - inc_artifact_value: {soar_artifact_value}")

            result = soar_delete_incident_artifact(soar_client, soar_id, soar_artifact_id)
            if result and result.get('success', False):
                print(f"      incident {soar_id} altered.")
                incident_count += 1
            else:
                print(result)

        print(f"deletes_artifacts_on_soar: finished.  updated incidents = {incident_count}")
        print("")
        return "OK"
    except Exception as e:
        print(f"deletes_artifacts_on_soar: Error: {e}")
        return "FAIL"
    
if __name__ == "__main__":
    print("main starting ********************************************************")
    soar_client = get_soar_client()

    artifact_id = '187'
    res1 = deletes_artifacts_on_soar(soar_client, artifact_id)
    print("main finished ********************************************************")
    print(f"  deletes_artifacts_on_soar {artifact_id}:             [{res1}]")
