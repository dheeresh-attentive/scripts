import requests
import json
import sys

def get_branches(base_url, token, company_id):
    branch_url = f"https://{base_url}.web.attentive.ai/core/api/v1/branch/?company={company_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    branch_response = requests.get(branch_url, headers=headers)
    return branch_response.json()

def create_template(base_url, token, branch_id, division_id):
    url = f"https://{base_url}.web.attentive.ai/payments/api/v1/templates/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "branch_id": branch_id,
        "division_id": division_id,
        "type": 3,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()

def update_template(base_url, token, template_id, placeholders):
    url = f"https://{base_url}.web.attentive.ai/payments/api/v1/templates/{template_id}/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"placeholders": placeholders}
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()

def main():
    base_url = sys.argv[1]
    token = sys.argv[2]
    company_id = sys.argv[3]
    placeholders = json.loads(sys.argv[4])  # placeholders passed as a JSON string

    branches = get_branches(base_url, token, company_id)

    for branch in branches:
        for division in branch["divisions"]:
            status_code, response_json = create_template(
                base_url, token, branch["id"], division["id"]
            )
            print('-------------------')
            print(status_code)
            print(response_json)
            print('-------------------')

            if status_code == 201:  # if template creation was successful
                template_id = response_json['id']
                status_code, response_json = update_template(
                    base_url, token, template_id, placeholders
                )
                print('-------------------')
                print(status_code)
                print(response_json)
                print('-------------------')

if __name__ == "__main__":
    main()
