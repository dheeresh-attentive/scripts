# Invoice Template Update Script

This script is designed to update invoice templates for a company. It performs the following operations:

1. Fetches all group invoice templates.
2. Updates each template with new HTML text and placeholders.

## How to Run

Run the script with the environment and token as command-line arguments: `python template_update.py <env> <token>`

Replace `<env>` with the environment you want to use (e.g., "local", "prod", or any other environment). Replace `<token>` with your authorization token.

## Inputs

The script requires the following inputs:

- `html_text.txt`: A text file containing the new HTML text for the invoice templates.
- `placeholders.json`: A JSON file containing the new placeholders for the invoice templates.
