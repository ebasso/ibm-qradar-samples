import requests
import json
import logging
import logging.handlers

IBMCLOUD_LOG_URL = "https://xxxxxx-sao.logs.cloud.ibm.com"
IBMCLOUD_API_KEY = "a3ff...6"
SYSLOG_IP = "192.168.1.10"
SYSLOG_PORT = 514  # Port should be an integer

class IBMCloudLogs:
    def __init__(self):
        self.iam_url = "https://iam.cloud.ibm.com/identity/token"
        self.log_url = IBMCLOUD_LOG_URL
        self.api_key = IBMCLOUD_API_KEY
        self.bearer_token = None

    def get_bearer_token(self):
        payload = f'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey={self.api_key}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request(method="POST", url=self.iam_url, headers=headers, data=payload)
        if response.status_code != 200:
            print(f'get_bearer_token: requests.post -> {response.url} = {response}')
            print(response.content)
            return None

        token_response = json.loads(response.text)
        self.bearer_token = token_response.get("access_token")
        if not self.bearer_token:
            print("get_bearer_token: Error retrieving access_token")

    def query_logs(self):
        if not self.bearer_token:
            self.get_bearer_token()

        if self.bearer_token:
            log_url = self.log_url + "/v1/query"
            payload = json.dumps({
                "query": "source logs | limit 1000",
                "metadata": {
                    "tier": "frequent_search",
                    "syntax": "dataprime",
                    "limit": 1000,
                    "strict_fields_validation": False
                }
            })
            headers = {
                'Authorization': f'Bearer {self.bearer_token}',
                'Accept': 'text/event-stream',
                'Content-Type': 'application/json'
            }

            response = requests.request(method="POST", url=log_url, headers=headers, data=payload, stream=True)

            if response.status_code == 200:
                print('query_logs: Streaming logs...')

                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: {"result"'):
                            json_part = line_str[len('data: '):]
                            json_data = json.loads(json_part)
                            return json_data
            else:
                print(f'query_logs: requests.post -> {response.url} = {response}')
                print(response.content)
        return None

    def print_results(self,results_data):
        for result in results_data['result']['results']:
            print(result['user_data'])

            # for metadata in result['metadata']:
            #     print(f"  {metadata['key']}: {metadata['value']}")
            
            # print("\nLabels:")
            # for label in result['labels']:
            #     print(f"  {label['key']}: {label['value']}")

            # print("\nUser Data:")
            # user_data = json.loads(result['user_data'])
            # for key, value in user_data.items():
            #     print(f"  {key}: {value}")
            print("\n")

    def syslog_results(self,results_data):
        for result in results_data['result']['results']:
            #print(result['user_data'])
            json_str = json.dumps(result['user_data'])
            json_str_fixed = json_str.replace("\\", "")
            print(f'syslog_results: message size -> {len(json_str_fixed)}')
            self.send_syslog_message(json_str_fixed)

    def send_syslog_message(self,message):
        try:
            logger = logging.getLogger('SyslogLogger')
            logger.setLevel(logging.INFO)

            syslog_handler = logging.handlers.SysLogHandler(address=(SYSLOG_IP, SYSLOG_PORT))
            formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%b %d %H:%M:%S')
            syslog_handler.setFormatter(formatter)

            logger.addHandler(syslog_handler)
            logger.info(message)
        except Exception as e:
            print(f"Failed to send syslog message: {e}")

if __name__ == "__main__":
    ibmcloud_logs = IBMCloudLogs()
    results_data = ibmcloud_logs.query_logs()
    #ibmcloud_logs.print_results(results_data)
    ibmcloud_logs.syslog_results(results_data)

