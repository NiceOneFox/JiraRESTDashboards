import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Jira API URL for searching issues
jira_url = "https://your-jira-instance/rest/api/2/search"

# JQL query to find all issues in the project
jql_query = 'project = "Your Project"'

# Set up the Jira API request headers and parameters
headers = {
    "Content-Type": "application/json",
}

params = {
    "jql": jql_query,
    "maxResults": 1000,  # Adjust maxResults based on the number of issues in your project
}

# Make the Jira API request to search for issues with anonymous authentication
response = requests.get(
    jira_url,
    headers=headers,
    params=params,
)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON to get the issues
    issues = response.json()["issues"]

    # Initialize dictionaries to store opened and closed tasks per day
    opened_tasks_per_day = {}
    closed_tasks_per_day = {}

    # Iterate through each issue and extract creation and resolution dates
    for issue in issues:
        created_date = issue["fields"]["created"]
        resolved_date = issue["fields"]["resolutiondate"]

        # Parse dates and count tasks per day
        created_date = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S.%f%z").date()
        resolved_date = (
            datetime.strptime(resolved_date, "%Y-%m-%dT%H:%M:%S.%f%z").date()
            if resolved_date
            else None
        )

        # Count opened tasks per day
        opened_tasks_per_day[created_date] = opened_tasks_per_day.get(created_date, 0) + 1

        # Count closed tasks per day
        if resolved_date:
            closed_tasks_per_day[resolved_date] = closed_tasks_per_day.get(resolved_date, 0) + 1

    # Prepare data for plotting
    dates = sorted(set(opened_tasks_per_day.keys()) | set(closed_tasks_per_day.keys()))
    cumulative_opened_tasks = [opened_tasks_per_day.get(date, 0) for date in dates]
    cumulative_closed_tasks = [closed_tasks_per_day.get(date, 0) for date in dates]

    # Calculate cumulative totals
    cumulative_opened_total = 0
    cumulative_closed_total = 0
    cumulative_totals = []
    for opened, closed in zip(cumulative_opened_tasks, cumulative_closed_tasks):
        cumulative_opened_total += opened
        cumulative_closed_total += closed
        cumulative_totals.append(cumulative_opened_total - cumulative_closed_total)

    # Plot the graph
    plt.plot(dates, cumulative_opened_tasks, label="Opened Tasks")
    plt.plot(dates, cumulative_closed_tasks, label="Closed Tasks")
    plt.plot(dates, cumulative_totals, label="Cumulative Total")
    plt.xlabel("Dates")
    plt.ylabel("Number of Tasks")
    plt.title("Opened and Closed Tasks per Day with Cumulative Total")
    plt.legend()
    plt.show()

else:
    print(f"Error: {response.status_code}, {response.text}")
