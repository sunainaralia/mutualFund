from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import base64


@csrf_exempt
def make_payment(request):
    # Replace these with your actual BluePay API key and token
    api_key = "OsApx4QH0a7RFIgyT5FcKDABq8MuIEWVjmX9NGPlf12eYvo6drnzkiStRwbZhLUC3J"
    api_token = "Qk9qdXR3M0FrbjJHaDVIcThBVTE3VVdxakQvNXpRYkFqMnZKQnF1YTlUbW1ZWjNKb3FjTXkxYURnQ0haaWNXa3p5dmxmUmlNNUE9PQ=="

    credentials = base64.b64encode(f"{api_key}:{api_token}".encode("utf-8")).decode(
        "utf-8"
    )
    url = "https://api.suvidhaabnk.com/api/payout/v2/do_txn"
    headers = {
        "Content-Type": "application/json",
        "Token": f"{api_token}",
    }

    payload = {
        "mode": "IMPS",
        "remarks": "Vendor Payout",
        "amount": "500",
        "bene_acc": "919932096277",
        "bene_ifsc": "PYTM0123456",
        "bene_acc_type": "Saving",
        "bene_name": "ARIF",
        "bene_mobile": "9932096277",
        "bene_email": "arif@suvidhaagroup.com",
        "refid": "arif259121242471",
        "bene_bank_name": "PAYTM PAYMENTS BANK",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "").lower()

        if "application/json" in content_type:
            # Parse JSON response
            response_data = response.json()
            # Rest of the code for handling JSON response
        else:
            # Print raw content for non-JSON responses
            print("Non-JSON response content:", response.content)

            # Handle non-JSON response
            return JsonResponse(
                {"status": "error", "message": "Non-JSON response received"}
            )
    elif response.status_code == 401:
        # Log the details for debugging
        print("Authentication failed. Check API key and token.")
        return JsonResponse({"status": "error", "message": "Authentication failed"})
    else:
        # Handle API request error
        return JsonResponse(
            {
                "status": "error",
                "message": f"API Request Failed: {response.status_code}",
            }
        )
