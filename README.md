# Transaction Categorization API

This API categorizes financial transactions using a fine-tuned BERT model. It provides endpoints to categorize single or multiple transactions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Request Schema](#request-schema)
- [Response Schema](#response-schema)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    fastapi dev src/main.py
    ```

## Usage

Once the application is running, you can access the API at `http://127.0.0.1:8000`.

## Endpoints

### Root Endpoint

- **GET** `/api/v1/`
    - **Description**: Health check endpoint.
    - **Response**: `{ "message": "Transaction Categorization API is running" }`

### Categorize Single Transaction

- **POST** `/api/v1/categorize/`
    - **Description**: Categorizes a single transaction.
    - **Request Body**: [TransactionRequest](http://_vscodecontentref_/1)
    - **Response**: `TransactionResponse`

### Categorize Multiple Transactions

- **POST** `/api/v1/categorize/bulk/`
    - **Description**: Categorizes multiple transactions.
    - **Request Body**: List of [TransactionRequest](http://_vscodecontentref_/2)
    - **Response**: List of `TransactionResponse`

## Request Schema

### TransactionRequest

```json
{
    "id": "string (optional)",
    "description": "string",
    "t_type": "string"
}
```

## Response Schema

For single transaction categorization:

```json
{
    "id": "string",
    "label": "string"
}
```
For multiple transactions categorization:


```json
[
    {
        "id": "string",
        "categories": [
            {
                "label": "string",
                "score": "string"
            }
        ]
    }
]
```