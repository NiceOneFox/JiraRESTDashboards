import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import main1
from main1 import func1
# Jira API URL for searching issues
jira_url = "https://issues.apache.org/jira/rest/api/2/search"
func1()
print("OTHER")
# JQL query to find closed issues in the project
jql_query = 'project = "KAFKA" AND status = Closed'

# Set up the Jira API request headers and parameters
headers = {
    "Content-Type": "application/json",
}

params = {
    "jql": jql_query,
    "maxResults": 1000,  # Adjust maxResults based on the number of closed issues in your project
    "expand": "changelog",
}

# Make the Jira API request to search for closed issues with anonymous authentication
response = requests.get(
    jira_url,
    headers=headers,
    params=params,
)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON to get the closed issues
    closed_issues = response.json()["issues"]

    # Initialize a dictionary to store the time spent in the "Open" state
    open_time_distribution = {}

    # Iterate through each closed issue
    for issue in closed_issues:
        issue_key = issue["key"]
        issue_url = f"https://issues.apache.org/jira/rest/api/2/issue/{issue_key}?expand=changelog"

        # Make the Jira API request to get the issue details including the expanded changelog
        issue_response = requests.get(issue_url, headers=headers)

        # Check if the request for the issue details was successful (status code 200)
        if issue_response.status_code == 200:
            # Parse the issue details JSON
            issue_details = issue_response.json()

            # Initialize variables to track the time spent in the "Open" state
            open_state_start = None
            time_spent_in_open = timedelta()

            # Access the expanded changelog
            changelog = issue_details.get("changelog", {}).get("histories", [])

            # Iterate through each change in the expanded changelog
            for change in changelog:
                created_date = datetime.strptime(change["created"], "%Y-%m-%dT%H:%M:%S.%f%z")

                # Check if the issue transitioned to the "Open" state
                if any(item["field"] == "status" and item["toString"] == "Open" for item in change["items"]):
                    open_state_start = created_date

                # Check if the issue transitioned out of the "Open" state
                elif open_state_start and any(item["field"] == "status" and item["fromString"] == "Open" for item in change["items"]):
                    time_spent_in_open += created_date - open_state_start
                    open_state_start = None

            # Increment the histogram bins based on the time spent in the "Open" state
            time_spent_seconds = int(time_spent_in_open.total_seconds())
            open_time_distribution[time_spent_seconds] = open_time_distribution.get(time_spent_seconds, 0) + 1

        else:
            print(f"Error fetching issue details for issue {issue_key}: {issue_response.status_code}, {issue_response.text}")

    # Extract data for plotting
    time_intervals = sorted(open_time_distribution.keys())
    task_counts = [open_time_distribution[time_interval] for time_interval in time_intervals]

    # Plot the histogram
    plt.bar(time_intervals, task_counts, width=1000)
    plt.xlabel("Time Spent in Open State (seconds)")
    plt.ylabel("Number of Closed Tasks")
    plt.title("Histogram of Time Spent in Open State for Closed Issues")
    plt.show()

else:
    print(f"Error: {response.status_code}, {response.text}")
