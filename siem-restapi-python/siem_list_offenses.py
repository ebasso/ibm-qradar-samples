import os
from dotenv import load_dotenv
from helpers.qradar_siem import QRadarSiem
from datetime import datetime
from helpers.utils import get_date_string
import re

load_dotenv()

def get_siem_client() -> QRadarSiem:
    """Get QRadar SIEM client using environment variables."""
    host = os.environ.get('SIEM_HOST')
    username = os.environ.get('SIEM_USERNAME')
    password = os.environ.get('SIEM_PASSWORD')
    return QRadarSiem(
        host=host,
        username=username,
        password=password,
        verify_ssl=False
    )


def print_to_csv(data, append=False):
    print('Print to CSV')

    # Define the CSV file name
    csv_file = "siem_offenses.csv"
    
    if append:
        mode="a"
    else:
        mode="w"

    # Open the file for writing
    with open(csv_file, mode=mode, encoding="utf-8") as file:
        # Write header
        if not append:
            file.write("id;domain_id;description;offense_type;offense_source;status;inactive\n")

        for row in data:
            description=row.get("description", "").replace("\n", "")
            line = '{id};{domain_id};{description};{offense_type};{offense_source};{status};{inactive}\n'.format(
                id=row.get("id", ""),
                domain_id=row.get("domain_id", ""),
                description=description,
                offense_type=row.get("offense_type", ""),
                offense_source=row.get("offense_source", ""),
                status=row.get("status", ""),
                inactive=row.get("inactive", "")
            )
            file.write(line)

    print(f"Data written to {csv_file}")


def main():

    siem = get_siem_client()

    # print("QRadar SIEM - Network Hierarchy")
    # print (siem.get_network_hierarchy())
   
    print("QRadar SIEM - Offenses")

    params = {
        "fields": "id,domain_id,description,offense_type,offense_source,status,inactive",
        "filter": "status=OPEN"
        }
    
    for i in [0, 1000, 2000, 3000, 4000, 5000, 6000]:
        range = "items={start}-{end}".format(start=i, end=(i+1000))
        data = siem.get_offenses(range,params)
        
        if not data or len(data) < 1000:
            print_to_csv(data, append=(i != 0))
            break

        print_to_csv(data, append=(i != 0))
    

# ==========================
if __name__ == "__main__":
    main()
