import requests
import matplotlib.pyplot as plt

def func6():
    # Jira API URL for searching issues
    jira_url = "https://issues.apache.org/jira/rest/api/2/search"

    # Jira credentials

    # JQL query to find all issues in your project
    jql_query = 'project = "KAFKA"'

    # Set up the Jira API request headers and parameters
    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "jql": jql_query,
        "maxResults": 10000,  # Adjust maxResults based on the number of issues in your project
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

        # Initialize a dictionary to store the count for each severity
        severity_counts = {}

        # Iterate through each issue and count the occurrences of each severity
        for issue in issues:
            severity = issue["fields"]["priority"]["name"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Extract data for plotting
        severities = list(severity_counts.keys())
        counts = list(severity_counts.values())

        # Plot the bar graph
        plt.bar(severities, counts, color=['red', 'yellow', 'green', 'blue', 'purple'])
        plt.xlabel("Severity")
        plt.ylabel("Number of Issues")
        plt.title("Number of Tasks by Severity")
        plt.show()
    else:
        print(f"Error: {response.status_code}, {response.text}")
