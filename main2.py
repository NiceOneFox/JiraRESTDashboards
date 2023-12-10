import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def func2():
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

        # Initialize dictionaries to store time distribution for each state
        state_time_distribution = {}

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

                # Iterate through each worklog entry and calculate the logged time for each state
                for worklog in worklogs:
                    created_date = datetime.strptime(worklog["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    time_spent_seconds = worklog["timeSpentSeconds"]

                    # Assume the state transitions are tracked in the history (modify this part based on your Jira configuration)
                    state_transitions = [
                        {"from": "Open", "to": "In Progress", "transition_date": "2023-01-01T12:00:00.000+0000"},
                        {"from": "In Progress", "to": "Resolved", "transition_date": "2023-01-02T12:00:00.000+0000"},
                        {"from": "Resolved", "to": "Closed", "transition_date": "2023-01-03T12:00:00.000+0000"},
                    ]

                    # Iterate through state transitions and calculate the time spent in each state
                    for transition in state_transitions:
                        from_state = transition["from"]
                        to_state = transition["to"]
                        transition_date = datetime.strptime(transition["transition_date"], "%Y-%m-%dT%H:%M:%S.%f%z")

                        if created_date <= transition_date:
                            state_time_distribution.setdefault(from_state, []).append(time_spent_seconds)
                            state_time_distribution.setdefault(to_state, []).append(-time_spent_seconds)
                            break

            else:
                print(f"Error fetching worklog for issue {issue_key}: {worklog_response.status_code}, {worklog_response.text}")

        # Plot diagrams for each state
        for state, time_list in state_time_distribution.items():
            cumulative_time = 0
            cumulative_times = []

            # Sort the time entries by date
            sorted_time_entries = sorted(time_list, key=lambda x: x["date"])

            # Calculate cumulative time for each time entry
            for time_entry in sorted_time_entries:
                cumulative_time += time_entry["time"]
                cumulative_times.append(cumulative_time)

            # Plot the diagram
            plt.plot(sorted_time_entries, cumulative_times, label=state)

        plt.xlabel("Time")
        plt.ylabel("Cumulative Time in State")
        plt.title("Distribution of Time by Task States")
        plt.legend()
        plt.show()

    else:
        print(f"Error: {response.status_code}, {response.text}")