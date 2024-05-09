# Invoice Template Management Script

This script is designed to manage invoice templates for different branches and divisions of a company. It performs the following operations:

1. Fetches all branches of a company.
2. Creates an invoice template for each division in each branch.
3. Updates the created invoice template with placeholders.

## How to Run

Run the script with the environment and token as command-line arguments: `python script_name.py <env> <token>`

Replace `<env>` with the environment you want to use (e.g., "local", "prod", or any other environment). Replace `<token>` with your authorization token.

## Inputs

The script requires the following inputs:

- `company.txt`: A text file containing the company ID.
- `html_text.txt`: A text file containing the HTML text for the invoice template.
- `placeholders.json`: A JSON file containing the placeholders for the invoice template.
