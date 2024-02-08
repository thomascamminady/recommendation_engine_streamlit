import logging

import requests
from requests import Response


def post_request(
    wf_user_token: str,
    number_requested_recommendations: int,
    max_availability_seconds: int,
    motivation_score: int,
    fatigue_score: int,
    workout_type_family_id: int,
) -> Response:
    url = "https://www.wahooligan.com/api/v1/plan_recommendations_request"
    headers = {
        "WF-USER-TOKEN": wf_user_token,
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.36.1",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    data = {
        "plan_recommendations_request": {
            "number_requested_recommendations": number_requested_recommendations,
            "max_availability_seconds": max_availability_seconds,
            "motivation_score": motivation_score,
            "fatigue_score": fatigue_score,
            "workout_type_family_id": workout_type_family_id,
        }
    }
    logging.info(url, data, headers)
    return requests.post(url, json=data, headers=headers, timeout=60)
    # print(response.status_code)
    # print(response.json())
