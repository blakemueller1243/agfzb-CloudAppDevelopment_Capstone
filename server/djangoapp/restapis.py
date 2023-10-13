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

# Update the get_dealer_reviews_from_cf method
def get_dealer_reviews_from_cf(url, dealer_id):
    url = f"{url}"
    json_results = get_request(url)
    print(f"Requesting data from {url}")
    
    if json_results is not None:
        results = []
        for json_result in json_results:
            review_data = json_result
            dealer_review = DealerReview(
                dealership=review_data.get("dealership", ""),
                name=review_data.get("name", ""),
                purchase=review_data.get("purchase", ""),
                review=review_data.get("review", ""),
                purchase_date=review_data.get("purchase_date", ""),
                car_make=review_data.get("car_make", ""),
                car_model=review_data.get("car_model", ""),
                car_year=review_data.get("car_year", ""),
                sentiment="",  # Initialize sentiment as empty
                id=review_data.get("id", "")
            )

            # Analyze sentiment and assign it to the DealerReview object
            # dealer_review.sentiment = analyze_review_sentiments(dealer_review.review)

            results.append(dealer_review)
        return results
    else:
        print("Dealer reviews not found or an error occurred.")
        return []




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
#     # Analyze sentiment using Watson NLU
#     response = nlu.analyze(
#         text=text,
#         features=Features(sentiment=SentimentOptions())
#     )

#     # Extract sentiment label from the response
#     sentiment = response['sentiment']['document']['label']

#     return sentiment



