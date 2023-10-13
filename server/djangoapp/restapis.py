import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
# from watson_developer_cloud import NaturalLanguageUnderstandingV1
# from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    try:
        # Call get method of requests library with URL and parameters
        params = {
            "text": kwargs["text"],
            "version": kwargs["version"],
            "features": kwargs["features"],
            "return_analyzed_text": kwargs["return_analyzed_text"]
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for unsuccessful responses
    except Exception as e:
        # Handle exceptions and print error details
        print("Network exception occurred:", str(e))
        return None  # Return None in case of an exception
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = response.json()
    return json_data






# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url, **kwargs):
    results = []

    # Call get_request with a URL parameter
    json_results = get_request(url)

    for json_result in json_results:
        # Assuming each item in the list is a dealer object
        dealer_doc = json_result.get("doc", {})
        
        dealer_obj = CarDealer(
            address=dealer_doc.get("address", ""),
            city=dealer_doc.get("city", ""),
            full_name=dealer_doc.get("full_name", ""),
            id=dealer_doc.get("id", ""),
            lat=dealer_doc.get("lat", ""),
            long=dealer_doc.get("long", ""),
            short_name=dealer_doc.get("short_name", ""),
            st=dealer_doc.get("st", ""),
            zip=dealer_doc.get("zip", "")
        )

        results.append(dealer_obj)

    return results

def get_dealer_by_id(dealer_id, **kwargs):
    # Construct the URL with the dealer_id as a parameter
    url = f"{url}/dealerships/get?id={dealer_id}"
    dealer_doc = get_request(url, **kwargs)
    
    if dealer_doc:
        dealer_obj = CarDealer(
            address=dealer_doc.get("address", ""),
            city=dealer_doc.get("city", ""),
            full_name=dealer_doc.get("full_name", ""),
            id=dealer_doc.get("id", ""),
            lat=dealer_doc.get("lat", ""),
            long=dealer_doc.get("long", ""),
            short_name=dealer_doc.get("short_name", ""),
            st=dealer_doc.get("st", ""),
            zip=dealer_doc.get("zip", "")
        )
        return dealer_obj
    else:
        return None

# Deleted get_dealer_reviews_by_cf because its obsolete. done inside of views.py now


# moved to views.py now
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# moved to views.py now



