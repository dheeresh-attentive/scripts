import requests
import json
import sys


def get_base_url(env):
    if env == "local":
        return "http://127.0.0.1:8000"
    else:
        return f"https://{env}.web.attentive.ai"


def get_branches(env, company_id, headers):
    base_url = get_base_url(env)
    branch_url = f"{base_url}/core/api/v1/branch/?company={company_id}"
    print(f"\nBranch URL: {branch_url}")
    branch_response = requests.get(branch_url, headers=headers)
    print(f"Branch Response: {branch_response.json()}")
    return branch_response.json()


def create_template(env, branch_id, division_id, html_text, headers):
    base_url = get_base_url(env)
    url = f"{base_url}/payments/api/v1/templates/"
    data = {
        "branch_id": branch_id,
        "division_id": division_id,
        "type": 3,
        "html_text": html_text,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()


def update_template(env, template_id, placeholders, headers):
    base_url = get_base_url(env)
    url = f"{base_url}/payments/api/v1/templates/{template_id}/"
    data = {"placeholders": placeholders}
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()


def main():
    env = sys.argv[1]
    token = sys.argv[2]

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    with open("companies.txt", "r") as file:
        companies = file.read().splitlines()
        print(f"Companies: {companies}")

    with open("html_text.txt", "r") as file:
        html_text = file.read()
        # print(f"HTML Text: {html_text}")

    with open("placeholders.json", "r") as file:
        placeholders = json.load(file)
        # print(f"Placeholders: {placeholders}")

    for company_id in companies:
        branches = get_branches(env, company_id, headers)

        for branch in branches:
            for division in branch["divisions"]:
                status_code, response_json = create_template(
                    env, branch["id"], division["id"], html_text, headers
                )
                print(
                    f"-------------------\nStatus Code: {status_code}\nResponse JSON: {json.dumps(response_json, indent=4)}\n-------------------"
                )

                if status_code == 201:  # if template creation was successful
                    template_id = response_json["id"]
                    status_code, response_json = update_template(
                        env, template_id, placeholders, headers
                    )
                    print(
                        f"-------------------\nStatus Code: {status_code}\nResponse JSON: {json.dumps(response_json, indent=4)}\n-------------------"
                    )


if __name__ == "__main__":
    main()
