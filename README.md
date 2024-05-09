# Purchase Order Template Management Script

This script is designed to manage purchase order templates for different branches and divisions of a company. It performs the following operations:

1. Fetches all branches of a company.
2. Creates a purchase order template for each division in each branch.
3. Updates the created purchase order template with placeholders.

## How to Run

Run the script with the environment and token as command-line arguments: `python template_create.py <env> <token>`

Replace `<env>` with the environment you want to use (e.g., "local", "prod", or any other environment). Replace `<token>` with your authorization token.

## Inputs

The script requires the following inputs:

- `company.txt`: A text file containing the company ID.
- `html_text.txt`: A text file containing the HTML text for the purchase order template.
- `placeholders.json`: A JSON file containing the placeholders for the purchase order template.
