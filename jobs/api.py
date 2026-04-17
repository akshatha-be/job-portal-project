import requests

def get_jobs_from_api():

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": "demo",
        "app_key": "demo",
        "results_per_page": 10
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None