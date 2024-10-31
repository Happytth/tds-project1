# tds-project1
- Used python's library `requests`, scraped the data by first querying the GitHub API endpoint `/search/users?q=location:Seattle followers:>200` to retrieve users in Seattle with over 200 followers, then retrieving each user’s details from `/users/{username}` and their repositories from `/users/{username}/repos` with parameter `sort=pushed`.

- Interesting fact discovered: Among Seattle users, those who are "hireable" follow fewer people on average than non-hireable users, though both groups maintain strong follower counts.

- Actionable recommendation:Developers seeking visibility on GitHub may benefit from marking themselves "hireable" and adding a public email address, as this may help attract connections and collaborators.
  
## Usage

1. Run the Python script `get_users_csv.py` first.
- It will generate the `users.csv` for users in `Seattle` with more than `200` followers.

2. Next, after getting the users run the `get_repos_csv.py` to get the top 500 repositories of each users in `users.csv` file.
- this will generate the `repositories.csv` file.

# Ensure you have a valid GitHub API `token` and install the python's `requests` library.
