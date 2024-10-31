import requests
import csv
import sys

# GitHub API token
api_token = "your_token_here"
headers = {"Authorization": f"token {api_token}"}

# API configuration: update location and minimum followers here
pages_to_fetch = 4  # Set the total number of pages to fetch
location_city = "Seattle"
min_followers = 200

base_url = f'https://api.github.com/search/users?q=location:{location_city} followers:>{min_followers}&per_page=100&page=1'

# List to accumulate all users' data
collected_users = []

# Initial request to check the total number of users
response = requests.get(base_url, headers=headers)
if response.status_code != 200:
    print("Encountered an error:", response.status_code, response.json().get("message"))
    sys.exit()

total_users = response.json().get('total_count', 0)
print(f"Total users in {location_city} with over {min_followers} followers:", total_users)

# Loop to gather users page by page
page_index = 1
while len(collected_users) < total_users:
    page_url = f'https://api.github.com/search/users?q=location:{location_city} followers:>{min_followers}&per_page=100&page={page_index}'
    response = requests.get(page_url, headers=headers)
    page_data = response.json()

    if response.status_code != 200:
        print("Error fetching data:", response.status_code, page_data.get("message"))
        sys.exit()

    # Collect users from this page
    collected_users.extend(page_data.get('items', []))
    print(f"Fetched {len(page_data.get('items', []))} users from page {page_index}. Total so far: {len(collected_users)}.")

    # Stop if we’re on the last page
    if len(page_data.get('items', [])) < 100:
        print("Reached last page, stopping fetch.")
        break
    
    page_index += 1

print("Completed pages:", page_index)
print("Total users fetched:", len(collected_users))

# Fetch details for each user
print("Retrieving detailed user data...")

def fetch_user_details(username):
    details_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(details_url, headers=headers)
    return user_response.json()

# Save the user data to CSV
def export_users_to_csv(user_records, filename="users.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        csv_writer = csv.DictWriter(
            file,
            fieldnames=[
                "login",
                "name",
                "company",
                "location",
                "email",
                "hireable",
                "bio",
                "public_repos",
                "followers",
                "following",
                "created_at",
            ],
        )
        csv_writer.writeheader()
        for record in user_records:
            csv_writer.writerow(record)

# Function to clean company names
def format_company_name(company):
    if company:
        return company.strip().lstrip('@').upper()
    return company

user_details_data = []
user_count = 1

for user in collected_users:
    user_details = fetch_user_details(user["login"])
    print(f"Retrieving data for user {user_count}: {user['login']}")
    
    # Append cleaned data for each user
    user_details_data.append(
        {
            "login": user_details["login"],
            "name": user_details.get("name", ""),
            "company": format_company_name(user_details.get("company", "") or ""),
            "location": user_details.get("location", ""),
            "email": user_details.get("email", ""),
            "hireable": "true" if user_details.get("hireable") else "false",
            "bio": user_details.get("bio", ""),
            "public_repos": user_details.get("public_repos", 0),
            "followers": user_details.get("followers", 0),
            "following": user_details.get("following", 0),
            "created_at": user_details.get("created_at", ""),
        }
    )
    user_count += 1

export_users_to_csv(user_details_data)
print("Successfully created users.csv!")
