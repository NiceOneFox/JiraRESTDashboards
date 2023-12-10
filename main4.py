import requests
import matplotlib.pyplot as plt

def func4():
    jira_url = "https://issues.apache.org/jira/rest/api/2/search"

    jql_query = 'project = "KAFKA" AND assignee is not EMPTY AND reporter is not EMPTY'

    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "jql": jql_query,
        "maxResults": 1000,
    }

    response = requests.get(jira_url, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON to get the issues
        issues = response.json()["issues"]

        # Initialize a dictionary to store the count for each user
        user_counts = {}

        # Iterate through each issue and count the occurrences for each user
        for issue in issues:
            assignee = issue["fields"]["assignee"]["displayName"]
            reporter = issue["fields"]["reporter"]["displayName"]

            # Consider only issues where the user is both assignee and reporter
            if assignee == reporter:
                user_counts[assignee] = user_counts.get(assignee, 0) + 1

        # Sort users by the number of tasks in descending order
        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)

        # Extract data for plotting (considering only the top 30 users)
        top_users = [user[0] for user in sorted_users[:30]]
        task_counts = [user[1] for user in sorted_users[:30]]

        # Plot the horizontal bar graph
        plt.barh(top_users, task_counts, color='skyblue')
        plt.xlabel("Number of Tasks")
        plt.ylabel("User")
        plt.title("Top 30 Users with the Maximum Number of Tasks")
        plt.show()
    else:
        print(f"Error: {response.status_code}, {response.text}")
