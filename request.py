import requests
import json
import csv

# Base URL and headers for the API request
URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Keywords list
KEYWORDS = [
    #elastic,
    # "digital ocean",
    # "jfrog",
    # "Grafana",
    # "Prometheus",
    # "Mongodb",
    # "Terraform",
    # "vault"
    # "Gitlab",
    # "Apache",
    # "Spark",
    # "Atlassian",
    # "Snowflake",
    # "Informatica",
    # "Dynatrace",
    # "Couchbase",
    # "Adobe",
    # "Salesforce",
    # "Intl Business Machines",
    # "IBM",
    # "Intuit",
    # "Microsoft",
    # "Servicenow",
    # "Oracle",
    # "SAP SE-Sponsored ADR",
    # "Amplitude",
    # "Avid Technology",
    # "Alteryx",
    # "Blackbaud",
    # "Braze",
    # "Sprinklr",
    # "Docusign",
    # "Domo",
    # "Freshworks",
    # "Hubspot",
    # "Microstrategy",
    # "Sprout Social",
    # "Twilio",
    # "Qualtrics International",
    # "Yext",
    # "Zoominfo Technologies",
    # "Palantir Technologies",
    # "Appian",
    # "Bill Holdings",
    # "Blackline",
    # "Ceridian HCM Holding",
    # "Paycom Software",
    # "Oracle Japan",
    # "Uipath",
    # "Pegasystems",
    # "Workday",
    # "Workiva",
    # "Zuora",
    # "Akamai Technologies",
    # "Check Point Software Tech",
    # "CrowdStrike Holdings",
    # "CyberArk Software Ltd/Israel",
    # "Fastly",
    # "Fortinet",
    # "Cloudflare",
    # "Nutanix",
    # "Okta",
    # "Palo Alto Networks",
    # "Qualys",
    # "Rapid7",
    # "SentinelOne",
    # "Tenable Holdings",
    # "VMware",
    # "Varonis Systems",
    # "Zscaler",
    # "Autodesk",
    # "C3.AI",
    # "Altair Engineering",
    # "Ansys",
    # "Bentley Systems",
    # "Cadence Design Sys",
    # "Everbridge",
    # "Samsara",
    # "Manhattan Associates",
    # "Procore Technologies",
    # "Porch Group",
    # "PTC",
    # "Synopsys",
    # "SPS Commerce",
    # "Tyler Technologies",
    # "Veeva Systems",
    # "Clear Secure",
    # "Asana",
    # "Bandwidth",
    # "Box",
    "Dropbox",
    # "8x8",
    "Jamf Holding",
    "Five9",
    "Monday.com",
    "RingCentral",
    "Sinch AB",
    "Smartsheet",
    "Zoom Video Communications",
    "Couchbase",
    "Confluent",
    "Datadog",
    "DigitalOcean Holdings",
    "Dynatrace"
]

def is_valid_response(response_data):
    """Check if the response contains valid data and has a valid start date."""
    valid_years = ['2020', '2021', '2022', '2023', '2024']

    # Check for the existence of results
    results = response_data.get('results')
    if not results:
        return False

    # Check if any of the results have a start date in the valid years
    for result in results:
        start_date = result.get("Start Date")
        if start_date and start_date.split('-')[0] in valid_years:
            return True

    return False

def fetch_data_for_keyword(keyword):
    print(f"Fetching data for keyword: {keyword}")
    BODY = {
        "filters": {
            "keywords": [keyword],
            "award_type_codes": ["A", "B", "C", "D"],
            "date_range": {
                "start_date": "2019-01-01",
                "end_date": "2023-12-31"
            }
        },
        "fields": [
            "Award ID", "Recipient Name", "Start Date", "End Date", 
            "Award Amount", "Description", "Award Type"
        ],
        "page": 1,
        "limit": 50,
        "sort": "Start Date",
        "order": "desc"
    }
    all_data = []  # List to accumulate all data
    page_num = 1

    while True:
        try:
            response = requests.post(URL, data=json.dumps(BODY), headers=HEADERS)
            response_data = response.json()
            
            if not is_valid_response(response_data):
                print("Response not valid")
                break
            
            # Accumulate data
            all_data.extend(response_data.get('results', []))

            page_num += 1
            BODY['page'] = page_num

        except Exception as e:
            print("Response not valid", e)
            break

    # Write all data to a single JSON file
    with open(f'output_{keyword}.json', 'w') as jsonfile:
        json.dump(all_data, jsonfile, indent=4)

    print(f"Data fetching for keyword: {keyword} completed.")

# Process each keyword serially
for keyword in KEYWORDS:
    fetch_data_for_keyword(keyword)

print("All requests completed.")