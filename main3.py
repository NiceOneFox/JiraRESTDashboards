import requests
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def func3():
    # Jira API URL for searching issues
    jira_url = "https://issues.apache.org/jira/rest/api/2/search"

    # JQL query to find all issues in the project
    jql_query = 'project = "KAFKA"'

    # Set up the Jira API request headers and parameters
    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "jql": jql_query,
        "maxResults": 1000,  # Adjust maxResults based on the number of issues in your project
    }

    # Make the Jira API request to search for issues
    response = requests.get(
        jira_url,
        headers=headers,
        params=params,
    )

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON to get the issues
        issues = response.json()["issues"]

        # Initialize dictionaries to store daily counts and cumulative totals
        opened_count_per_day = {}
        closed_count_per_day = {}
        cumulative_opened_count = 0
        cumulative_closed_count = 0

        # Iterate through each issue and update counts
        for issue in issues:
            created_date = issue["fields"]["created"]
            closed_date = issue["fields"]["resolutiondate"]

            # Parse dates and truncate to only keep date (ignoring time)
            created_date = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S.%f%z").date()
            closed_date = (
                datetime.strptime(closed_date, "%Y-%m-%dT%H:%M:%S.%f%z").date() if closed_date else None
            )

            # Update opened count for the created date
            opened_count_per_day[created_date] = opened_count_per_day.get(created_date, 0) + 1
            cumulative_opened_count += 1

            # Update closed count for the closed date
            if closed_date:
                closed_count_per_day[closed_date] = closed_count_per_day.get(closed_date, 0) + 1
                cumulative_closed_count += 1

        # Generate lists for plotting
        dates = sorted(set(opened_count_per_day.keys()) | set(closed_count_per_day.keys()))
        cumulative_opened = [cumulative_opened_count] * len(dates)  # Ensure both lists have the same length
        cumulative_closed = [cumulative_closed_count] * len(dates)

        for i, date in enumerate(dates):
            cumulative_opened_count += opened_count_per_day.get(date, 0)
            cumulative_closed_count += closed_count_per_day.get(date, 0)
            cumulative_opened[i] = cumulative_opened_count
            cumulative_closed[i] = cumulative_closed_count

        # Plot the graph
        plt.plot(dates, cumulative_opened, label="Cumulative Opened", marker="o")
        plt.plot(dates, cumulative_closed, label="Cumulative Closed", marker="o")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Number of Tasks")
        plt.title("Cumulative Opened and Closed Tasks per Day")
        plt.legend()
        plt.show()

    else:
        print(f"Error: {response.status_code}, {response.text}")
