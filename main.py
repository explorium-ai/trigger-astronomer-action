import json
import os
import string
import sys
import time
import requests

username = os.environ["INPUT_USERNAME"]
password = os.environ["INPUT_PASSWORD"]
payload = os.environ["INPUT_PAYLOAD"]
webserver_id = os.environ["INPUT_WEBSERVER_ID"]
dag_name = os.environ["INPUT_DAG_NAME"]
dag_run_id = os.environ["INPUT_DAG_RUN_ID"]

def main():
    trigger_dag(
        json.loads(payload),
        dag_run_id,
    )
    status_code = "running"
    while status_code not in {'success', 'failed'}:
        status_code = get_dag_status(dag_run_id)
        print(status_code)
        time.sleep(1)
    if status_code != "success":
        print(f"::set-output name=result::Failed")
        sys.exit("Dag Failed")
    else:
        print(f"::set-output name=result::Success")
        sys.exit(0)

def trigger_dag(data: json, dag_run_id: string):
    endpoint = f"api/v1/dags/{dag_name}/dagRuns"
    json_data = {"conf": data, "dag_run_id": dag_run_id}
    webserver_url = "https://" + webserver_id + "/" + endpoint
    make_iap_request_trigger(webserver_url, method="POST", data=json.dumps(json_data))


def get_dag_status(run_id: string) -> string:
    endpoint = f"api/v1/dags/{dag_name}/dagRuns/{run_id}"
    webserver_url = "https://" + webserver_id + "/" + endpoint
    return make_iap_request_poll(run_id, webserver_url, method="GET")


def auth_astronomer(**kwargs: object) -> string:
    if "timeout" not in kwargs:
        kwargs["timeout"] = 90
    resp = requests.request(
        "POST",
        "https://auth.astronomer.io/oauth/token",
        json={'client_id': username,'client_secret': password,'audience': 'astronomer-ee','grant_type': 'client_credentials'}
    )
    data = json.loads(str(resp.text).replace("'", ""))
    return data["access_token"]


def make_iap_request_poll(run_id: string, url: string, method: string = "GET", **kwargs: object) -> string:
    resp = requests.request(
        method,
        url,
        headers={"Authorization": "Bearer " + auth_astronomer(**kwargs),
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"},
    )

    return handle_request(resp, run_id)


def handle_request(resp: requests.request, run_id: string) -> string:
    if resp.status_code != 200:
        raise Exception(
            "Bad response from application: " + str(resp.status_code) + " / " + str(resp.headers) + " / " + str(resp.text)
        )
    else:
        if run_id:
            data = json.loads(str(resp.text).replace("'", ""))
            if data["dag_run_id"] == run_id:
                return data["state"]
            return resp.text
        else:
            return resp.text


def make_iap_request_trigger(url: string, method: string = "GET", **kwargs: object) -> string:
    resp = requests.request(
        method,
        url,
        headers={"Authorization": "Bearer " + auth_astronomer(**kwargs),
            "Content-Type": "application/json"},
        **kwargs)
    return handle_request(resp, False)

if __name__ == "__main__":
    main()