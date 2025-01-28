from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import (
    pipeline,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    PretrainedConfig,
)
import os

CATEGORIES = {
    0: "Utilities",
    1: "Health",
    2: "Dining",
    3: "Travel",
    4: "Education",
    5: "Subscription",
    6: "Family",
    7: "Food",
    8: "Festivals",
    9: "Culture",
    10: "Apparel",
    11: "Transportation",
    12: "Investment",
    13: "Shopping",
    14: "Groceries",
    15: "Documents",
    16: "Grooming",
    17: "Entertainment",
    18: "Social Life",
    19: "Beauty",
    20: "Rent",
    21: "Money transfer",
    22: "Salary",
    23: "Tourism",
    24: "Household",
}

model_path = "kuro-08/bert-transaction-categorization"


def label_to_category(label: str) -> str:
    label = int(label.removeprefix("LABEL_"))
    return CATEGORIES.get(label, "Other")


def retrieve_model() -> str:
    local_path = "./bert-transaction-model"
    try:
        # Attempt to load the model and tokenizer
        model = AutoModelForSequenceClassification.from_pretrained(local_path)
        tokenizer = AutoTokenizer.from_pretrained(local_path)
        PretrainedConfig.from_pretrained(local_path)
    except Exception as e:
        print("Downloading and saving the model : " + model_path)

        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Save locally
        model.save_pretrained(local_path)
        tokenizer.save_pretrained(local_path)

    return local_path


model_path = retrieve_model()

# Load your fine-tuned model and tokenizer
classifier = pipeline("text-classification", model=model_path, tokenizer=model_path)

# Define the FastAPI app
app = FastAPI()


# Define a request schema
class TransactionRequest(BaseModel):
    id: str | None = None
    description: str
    t_type: str


# Root endpoint (optional for health check)
@app.get("/api/v1/")
def read_root():
    return {"message": "Transaction Categorization API is running"}


# Endpoint to categorize a transaction
@app.post("/api/v1/categorize/bulk/")
def categorize_transactions(requests: List[TransactionRequest], multiple: bool = False):
    try:
        results = []
        for request in requests:
            # Get the transaction description from the request
            description = request.description
            t_type = request.t_type
            # Use the fine-tuned model to classify
            k = 1
            if multiple:
                k = 2

            result = classifier(f"Transaction: {description} - Type: {t_type}", top_k=k)
            categories = [
                {
                    "label": label_to_category(res["label"]),
                    "score": "{:.2%}".format(res["score"]),
                }
                for res in result
            ]

            if multiple:
                results.append(
                    {
                        "id": request.id,
                        "categories": categories,
                    }
                )
            else:
                results.append({"id": request.id, "label": categories[0]["label"]})

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/categorize/")
def categorize_transaction(request: TransactionRequest, multiple: bool = False):
    try:
        # Get the transaction description from the request
        description = request.description
        t_type = request.t_type

        k = 1
        if multiple:
            k = 2

        result = classifier(f"Transaction: {description} - Type: {t_type}", top_k=k)

        categories = [
            {
                "label": label_to_category(res["label"]),
                "score": "{:.2%}".format(res["score"]),
            }
            for res in result
        ]

        if multiple:
            return {
                "categories": categories,
            }

        else:
            return {"label": categories[0]["label"]}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
