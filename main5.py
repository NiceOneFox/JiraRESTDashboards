import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def func5():
    # Jira API URL for searching issues
    jira_url = "https://issues.apache.org/jira/rest/api/2/search"

    # JQL query to find closed issues in the project
    jql_query = 'project = "KAFKA" AND status = Closed'

    # Set up the Jira API request headers and parameters
    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "jql": jql_query,
        "maxResults": 1000,  # Adjust maxResults based on the number of closed issues in your project
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

        # Initialize a dictionary to store the count for each time interval
        time_counts = {}

        # Iterate through each closed issue
        for issue in closed_issues:
            issue_key = issue["key"]
            worklog_url = f"https://issues.apache.org/jira/rest/api/2/issue/{issue_key}/worklog"

            # Make the Jira API request to get worklog entries for the issue
            worklog_response = requests.get(worklog_url, headers=headers)

            # Check if the request for worklog was successful (status code 200)
            if worklog_response.status_code == 200:
                # Parse the worklog entries JSON
                worklogs = worklog_response.json()["worklogs"]

                # Iterate through each worklog entry and calculate the logged time
                for worklog in worklogs:
                    author = worklog["author"]["displayName"]
                    time_spent_seconds = worklog["timeSpentSeconds"]
                    logged_time_interval = timedelta(seconds=time_spent_seconds)

                    # Increment the histogram bins based on the logged time interval
                    time_interval_str = str(logged_time_interval)
                    time_counts[(author, time_interval_str)] = time_counts.get((author, time_interval_str), 0) + 1
            else:
                print(f"Error fetching worklog for issue {issue_key}: {worklog_response.status_code}, {worklog_response.text}")

        # Extract data for plotting
        unique_time_intervals = set(interval for (author, interval) in time_counts.keys())
        unique_authors = set(author for (author, interval) in time_counts.keys())
        data = {author: [time_counts.get((author, interval), 0) for interval in unique_time_intervals] for author in unique_authors}

        # Plot the histogram
        for author, counts in data.items():
            plt.bar(range(len(unique_time_intervals)), counts, label=author)

        plt.xlabel("Time Intervals")
        plt.ylabel("Number of Closed Tasks")
        plt.title("Histogram of Logged Time for Closed Issues")
        plt.xticks(range(len(unique_time_intervals)), unique_time_intervals, rotation=45)
        plt.legend()
        plt.show()
    else:
        print(f"Error: {response.status_code}, {response.text}")
