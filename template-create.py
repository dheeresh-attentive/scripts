import requests
import json
import sys


def get_base_url(env):
    if env == "local":
        return "http://127.0.0.1:8000"
    elif env == "prod":
        return "https://web.attentive.ai"
    else:
        return f"https://{env}.web.attentive.ai"


def update_template(env, template_id, placeholders, headers, html_text):
    base_url = get_base_url(env)
    url = f"{base_url}/payments/api/v1/templates/{template_id}/"
    data = {
        "placeholders": placeholders["placeholders"],
        "html_text": html_text,
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()


def get_group_invoice_templates(env, headers):
    base_url = get_base_url(env)
    url = f"{base_url}/payments/api/v1/templates/?type=3&page_size=100"
    response = requests.get(url, headers=headers)
    return response.status_code, response.json()


def main():
    env = sys.argv[1]
    token = sys.argv[2]

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    with open("company.txt", "r") as file:
        company_id = file.read().strip()
        print(f"Company: {company_id}")

    with open("html_text.txt", "r") as file:
        html_text = file.read()

    with open("placeholders.json", "r") as file:
        placeholders = json.load(file)

    status_code, response_json = get_group_invoice_templates(env, headers)
    results = response_json["results"]
    cnt = 0
    for template in results:
        template_id = template["id"]
        print(f"Template ID: {template_id}")
        status_code, response_json = update_template(
            env, template_id, placeholders, headers, html_text
        )
        print(
            f"-------------------\nTemplate Update Status Code: {status_code}\n-------------------"
        )
        cnt += 1
    print(f"Total Templates Updated: {cnt}")


if __name__ == "__main__":
    main()
