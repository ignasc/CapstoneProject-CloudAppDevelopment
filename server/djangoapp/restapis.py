import os
import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")# Retrieve api key if it was supplied
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    result = requests.post(url, params=kwargs, json=json_payload["review"])
    return result


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result#["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer#["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_by_id_from_cf method to get dealer details based on dealer ID
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id = dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result#["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer#["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    # https://ignuic-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id=15
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id = dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result#["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer#["doc"]
            # Create a CarDealer object with values in `doc` object
            #def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id)
            dealer_obj = DealerReview(
            dealership=dealer_doc["dealership"],
            name=dealer_doc["name"],
            purchase=dealer_doc["purchase"],
            review=dealer_doc["review"],
            purchase_date=dealer_doc["purchase_date"] if dealer_doc["purchase"] else "N/A",
            car_make=dealer_doc["car_make"] if dealer_doc["purchase"] else "N/A",
            car_model=dealer_doc["car_model"] if dealer_doc["purchase"] else "N/A",
            car_year=dealer_doc["car_year"] if dealer_doc["purchase"] else "N/A",
            #sentiment="implement Watson NLU",
            sentiment=analyze_review_sentiments(dealer_doc["review"]),
            id=dealer_doc["id"])
            results.append(dealer_obj)
    print(results)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(review_text):
    key = "API_KEY_REVIEW_POST"
    api_key_for_review_post = os.getenv(key, default = None)
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/385cb7f7-1bcb-4159-8547-557de27da4cf"

    json_result = get_request(url, apikey = api_key_for_review_post)
    result = "This should be sentiment value from watson NLU (not implemented in analyze_review_sentiments() method"
    return result


