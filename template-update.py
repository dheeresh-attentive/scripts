import requests
import json
import sys
import csv

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


def get_statement_templates(env, headers):
    base_url = get_base_url(env)
    url = f"{base_url}/payments/api/v1/templates/?type=4&page_size=100"
    response = requests.get(url, headers=headers)
    return response.status_code, response.json()


def main():
    env = sys.argv[1]
    csv_file_path = "companies.csv"

    with open("html_text.txt", "r") as file:
        html_text = file.read()

    with open("placeholders.json", "r") as file:
        placeholders = json.load(file)
        
    with open(csv_file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_id = row["id"]
            name = row["name"]
            token = row["token"]
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            print(f"Processing Company: {name} with ID: {company_id}")
            status_code, response_json = get_statement_templates(env, headers)
            results = response_json["results"]
            cnt = 0
            print(f"len of results: {len(results)}")
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
            print(f"Total Templates Updated: {cnt} for company: {name}")


if __name__ == "__main__":
    main()