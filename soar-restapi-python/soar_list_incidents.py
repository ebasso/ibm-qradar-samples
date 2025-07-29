from helpers.qradar_soar import QRadarSoar
from helpers.utils import get_date_string
from datetime import datetime
from dotenv import load_dotenv
import re

load_dotenv()

def get_soar_client() -> QRadarSoar:
    """Get QRadar SOAR client."""
    host = os.environ.get('SOAR_HOST')
    api_key = os.environ.get('SOAR_API_KEY')
    api_secret = os.environ.get('SOAR_API_SECRET')
    return QRadarSoar(
        host=host,
        api_key_id=api_key,
        api_key_secret=api_secret,
        org_id=204,
        verify_ssl=False
    )
    
def extract_qradar_and_wb(text):
    """
    Extracts QRadar ID and WB- code from the given string.
    Returns a tuple: (qradar_id, wb_code) or (None, None) if not found.
    """
    match = re.search(r'QRadar ID (\d+)', text)
    qradar_id = match.group(1) if match else ''
    
    wb_match = re.search(r'(WB-\S+)', text)
    wb_code = wb_match.group(1) if wb_match else ''
    
    return qradar_id, wb_code


def print_to_csv(data, append=False):
    print('Print to CSV')

    # Define the CSV file name
    csv_file = "soar_incidents.csv"
    
    if append:
        mode="a"
    else:
        mode="w"

    # Open the file for writing
    with open(csv_file, mode=mode, encoding="utf-8") as file:
        # Write header
        if not append:
            file.write("id;plan_status;incident_type_ids;name;create_date;qradar_id;wb_code;severity_code;phase_id;discovered_date;owner_id;due_date;is_scenario\n")

        for row in data:
            # Use semicolon as separator and f-string formatting
            name=row.get("name", "")
            qradar_id, wb_code = extract_qradar_and_wb(name)
            line = '{id};{plan_status};{incident_type_ids};"{name}";{create_date};{qradar_id};{wb_code};{phase_id};{severity_code};{discovered_date};{owner_id};{due_date};{is_scenario}\n'.format(
                id=row.get("id", ""),
                name=name,
                qradar_id=qradar_id,
                wb_code=wb_code,
                phase_id=row.get("phase_id", ""),
                discovered_date=get_date_string(row.get("discovered_date", 0)),
                due_date=row.get("due_date", ""),
                create_date=get_date_string(row.get("create_date", 0)),
                owner_id=row.get("owner_id", ""),
                severity_code=row.get("severity_code", ""),
                plan_status=row.get("plan_status", ""),
                is_scenario=row.get("is_scenario", ""),
                incident_type_ids=str(row.get("incident_type_ids", ""))
            )
            file.write(line)

    print(f"Data written to {csv_file}")


def main():
    print("List Incidents - start")

    soar = get_soar_client()
    conditions = [
                {
                    "field_name": "plan_status",
                    "method": "in",
                    "value": ["A","C"]
                }
            ]
        
    for i in [0, 1000, 2000, 3000, 4000, 5000, 6000]:
        incidents = soar.get_incidents(conditions=conditions, start=i, limit=1000)
        data = incidents.get('data')
        
        if not data or len(data) < 1000:
            print_to_csv(data, append=(i != 0))
            break

        print_to_csv(data, append=(i != 0))

        
# ==========================
if __name__ == "__main__":
    main()
