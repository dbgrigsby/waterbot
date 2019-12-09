
import requests
import datetime
from random import randint

def sanitize_fact(fact):
    # https://rapidapi.com/neutrinoapi/api/bad-word-filter
    fact_sanitization_url = "https://neutrinoapi-bad-word-filter.p.rapidapi.com/bad-word-filter"
    fact_sanitization_payload = u"censor-character=*&content={}".format(fact)
    headers = {
        'x-rapidapi-host': "neutrinoapi-bad-word-filter.p.rapidapi.com",
        'x-rapidapi-key': "aba48f4856msha0c9bc9d4b82f39p1e84b0jsn71481a93f12e",
        'content-type': "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", fact_sanitization_url, data=fact_sanitization_payload.encode('utf-8'), headers=headers)
    return response.json()['censored-content']

def get_fact_mentalfoss():
    facts_url = 'https://www.mentalfloss.com/api/facts?page=1&limit=1'
    facts = requests.get(facts_url).json()
    n = len(facts)
    i = randint(0, n-1)
    fact = facts[i]['shortHeadline']
    return sanitize_fact(fact)

def get_fact_sanitized():    
    fact_url = 'https://uselessfacts.jsph.pl/random.json?language=en'
    fact = requests.get(fact_url).json()['text']
    while "whale" in fact:
        fact = requests.get(fact_url).json()['text']

    return sanitize_fact(fact)

hour = datetime.datetime.now().hour
is_working_hours = hour > 8 and hour < 18
if is_working_hours:
    payload = {
        # "text": "test \n\n>"+get_fact_mentalfoss(),
        "text": "<!here> drink some water, stay hydrated :)\n\n>"+get_fact_mentalfoss(),
        "mrkdwn": "true",
    }

    requests.post('https://slackme.yelpcorp.com/webhook/7105266', json=payload)
