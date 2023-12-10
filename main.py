# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import jira
from jira import JIRA
import matplotlib.pyplot as plt
import datetime
import time


# Press the green button in the gutter to run the script.
def func():
    print('PyCharm')

    # Specify a server key. It should be your
    # domain name link. yourdomainname.atlassian.net
    jiraOptions = {'server': "https://issues.apache.org/jira"}

    # Get a JIRA client instance, pass,
    # Authentication parameters
    # and the Server name.
    # emailID = your emailID
    # token = token you receive after registration
    jira = JIRA(options=jiraOptions)

    #jql = 'project = KAFKA AND (status CHANGED TO "Closed" OR status CHANGED to "Resolved")'
    jql = 'project = KAFKA AND status CHANGED TO "Closed"'

    listDate = []
    listTimeSpent = []
    # Search all issues mentioned against a project name.
    for singleIssue in jira.search_issues(jql_str=jql, maxResults=3000):
        print('{}: {}:{}'.format(singleIssue.key, singleIssue.fields.summary,
                                 singleIssue.fields.reporter.displayName))
        #print("created: {} duedate: {} resolution ".format(singleIssue.fields.created, singleIssue.fields.duedate))
        issues = jira.search_issues('key=' + singleIssue.key, expand='changelog')

        dateEnd = ''
        timeSpentDelta = ''
        timeCreated = ''
        # поиск даты закрытия или разрешения
        for issue in issues:
            timeCreated = issue.fields.created
            print(issue.key)
            for change in issue.changelog.histories:
                #print("== Change id ==", change.id)
                for change_item in change.items:
                    if change_item.field == 'status':
                        if change_item.toString == "Resolved" or change_item.toString == "Closed":
                            #print("  ", change.created, change_item.field, change_item.fromString, change_item.toString)
                            dateEnd = change.created[:19]

                            date_time_obj = datetime.datetime.strptime(dateEnd, '%Y-%m-%dT%H:%M:%S')
                            date_time_obj2 = datetime.datetime.strptime(issue.fields.created[:19], '%Y-%m-%dT%H:%M:%S')
                            timeSpentDelta = date_time_obj - date_time_obj2

        spentTime = time.gmtime(timeSpentDelta.total_seconds())
        dateEndObj = datetime.datetime.strptime(timeCreated[:19], '%Y-%m-%dT%H:%M:%S')
        print(dateEnd)
        print(timeSpentDelta)
        listDate.append(dateEndObj.date())  # время создания день
        listTimeSpent.append(timeSpentDelta.days) #затрачееное время в днях
        #calculate время выполнения.

    from collections import Counter

    time_spent_counts = Counter(listTimeSpent)

    # Convert Counter to dictionary
    counts_dict = dict(time_spent_counts)

    fig = plt.figure()

    # creating the bar plot
    plt.bar(counts_dict.keys(), counts_dict.values(), color='maroon')

    plt.xlabel("время потраченное на задачу в днях")
    plt.ylabel("суммарное количество задач, которое было в открытом виде соответствующее время")
    plt.title("Затраченное время на задачи проекта Kafka")
    plt.show()
