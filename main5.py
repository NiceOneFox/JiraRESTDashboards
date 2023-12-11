import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def func5():

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

    selectedIssues = response.json()["issues"]

    inp = "Philip Nee"

    data_user = {
        "project-ID":[],
        "created":[],
        "resolution":[],
        "estimated":[]
    }

    time_format = "%Y-%m-%d %H:%M:%S"

    for issue in selectedIssues:
        try:
            if (issue["fields"]["assignee"]["displayName"] is not None) and \
                (issue["fields"]["status"]["name"] == "Resolved") and \
                (issue["fields"]["assignee"]["displayName"] == inp):

                data_user["project-ID"].append(issue["key"])
                data_user["created"].append((issue["fields"]["created"])[0:10]+" "+(issue["fields"]["resolutiondate"])[11:19])
                data_user["resolution"].append((issue["fields"]["resolutiondate"])[0:10]+" "+(issue["fields"]["resolutiondate"])[11:19])
        except TypeError:
            continue

    for i in range(len(data_user["project-ID"])):
        start_datetime = datetime.strptime(data_user["created"][i], time_format)
        end_datetime = datetime.strptime(data_user["resolution"][i], time_format)

        difference = round(((end_datetime - start_datetime).total_seconds() / 3600) / 24)
        data_user["estimated"].append(difference)
    print(data_user)

    y = {
       "10":0,
        "50": 0,
        "100": 0,
        "250": 0,
        "500": 0,
        "1000":0
    }

    for i in range(len(data_user["estimated"])):
        if (int(data_user["estimated"][i]) >= 0) and (int(data_user["estimated"][i]) <= 10):
            y["10"] +=1
        if (int(data_user["estimated"][i]) > 10) and (int(data_user["estimated"][i]) <= 50):
            y["50"] +=1
        if (int(data_user["estimated"][i]) > 50) and (int(data_user["estimated"][i]) <= 100):
            y["100"] +=1
        if (int(data_user["estimated"][i]) > 100) and (int(data_user["estimated"][i]) <= 250):
            y["250"] +=1
        if (int(data_user["estimated"][i]) > 250) and (int(data_user["estimated"][i]) <= 500):
            y["500"] +=1
        if (int(data_user["estimated"][i]) > 500) and (int(data_user["estimated"][i]) <= 1000):
            y["1000"] +=1

    print(y.keys())
    print(y.values())
    print(len(data_user["project-ID"]))

    plt.bar(y.keys(),y.values())
    plt.xlabel('Затраченных дней')
    plt.ylabel('Количество задач')
    plt.title('Диаграмма кол-ва задач по затраченному времени')
    plt.show()

    val=list(y.values())
    return val