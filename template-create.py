import requests
import json
import sys
from typing import Dict, Any, Tuple


def get_branches(
    base_url: str, company_id: str, headers: Dict[str, str]
) -> Dict[str, Any]:
    branch_url = (
        f"{base_url}/core/api/v1/branch/?company={company_id}"
    )
    branch_response = requests.get(branch_url, headers=headers)
    return branch_response.json()


def create_template(
    base_url: str,
    branch_id: str,
    division_id: str,
    html_text: str,
    headers: Dict[str, str],
) -> Tuple[int, Dict[str, Any]]:
    url = f"{base_url}/payments/api/v1/templates/"
    data = {
        "branch_id": branch_id,
        "division_id": division_id,
        "type": 3,
        "html_text": html_text,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()


def update_template(
    base_url: str,
    template_id: str,
    placeholders: Dict[str, str],
    headers: Dict[str, str],
) -> Tuple[int, Dict[str, Any]]:
    url = (
        f"{base_url}/payments/api/v1/templates/{template_id}/"
    )
    data = {"placeholders": placeholders}
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()


def main():
    base_url = str(sys.argv[1])
    token = str(sys.argv[2])
    company_id = str(sys.argv[3])
    html_text = str(sys.argv[4])
    placeholders = json.loads(str(sys.argv[5]))  # placeholders passed as a JSON string

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    branches = get_branches(base_url, token, company_id, headers)

    for branch in branches:
        for division in branch["divisions"]:
            status_code, response_json = create_template(
                base_url, branch["id"], division["id"], html_text, headers
            )
            print(
                f"-------------------\nStatus Code: {status_code}\nResponse JSON: {json.dumps(response_json, indent=4)}\n-------------------"
            )

            if status_code == 201:  # if template creation was successful
                template_id = response_json["id"]
                status_code, response_json = update_template(
                    base_url, template_id, placeholders, headers
                )
                print(
                    f"-------------------\nStatus Code: {status_code}\nResponse JSON: {json.dumps(response_json, indent=4)}\n-------------------"
                )


if __name__ == "__main__":
    main()

#0dec7e3a-23c6-44b0-afdf-f705bd3d7da3
