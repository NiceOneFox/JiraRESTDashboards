import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

def func2():
    list_open = []
    list_in_progress = []
    list_resolved = []
    list_resolved_day = []
    list_reopened = []
    list_patch_available = []
    list_patch_available_day = []

    payload = {'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
               'expand': 'changelog',
               'fields': 'created'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    graph2_data = json.loads(response.text)

    for elem in graph2_data["issues"]:
        t_open, t_in_prog, t_res, t_reo, t_patch = status_statistic(elem)

        if t_open != timedelta(0):
            list_open.append(timedelta_to_days(t_open))
        if t_in_prog != timedelta(0):
            list_in_progress.append(timedelta_to_days(t_in_prog))
        if t_res != timedelta(0):
            list_resolved.append(timedelta_to_sec(t_res))
            list_resolved_day.append(timedelta_to_days(t_res))
        if t_reo != timedelta(0):
            list_reopened.append(timedelta_to_days(t_reo))
        if t_patch != timedelta(0):
            list_patch_available_day.append(timedelta_to_days(t_patch))
            list_patch_available.append(timedelta_to_hours(t_patch))

    plt.hist(list_open, color='blue', edgecolor='black', bins=30)
    plt.title('Диаграмма Open')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    '''list_open.sort()
    middle_index = int(len(list_open) / 1.2)
    first_patr = list_open[:middle_index]
    plt.hist(first_patr, color='blue', edgecolor='black', bins=80)
    plt.title('2. Диаграмма Open 2')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()'''

    ###### Resolved
    plt.hist(list_resolved_day, color='green', edgecolor='black', bins=30)
    plt.title('Диаграмма Resolved')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    '''list_resolved.sort()
    middle_index = int(len(list_resolved) / 1.6)
    first_patr = list_resolved[:middle_index]
    plt.hist(first_patr, color='green', edgecolor='black', bins=80)
    plt.title('2. Диаграмма Resolved 2')
    plt.xlabel('Время решения (секунды)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    middle_index = int(len(list_resolved) / 1.8)
    second_patr = list_resolved[:middle_index]
    plt.hist(second_patr, color='green', edgecolor='black', bins=80)
    plt.title('2. Диаграмма Resolved 3')
    plt.xlabel('Время решения (секунды)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()'''

    ###### Reopened
    plt.hist(list_reopened, color='yellow', edgecolor='black', bins=175)
    plt.title('Диаграмма Reopened')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    #### In Progress
    plt.hist(list_in_progress, color='purple', edgecolor='black', bins=50)
    plt.title('Диаграмма In Progress')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    '''list_in_progress.sort()
    second_patr = list_in_progress[:len(list_in_progress) - 4]
    plt.hist(second_patr, color='purple', edgecolor='black', bins=80)
    plt.title('2. Диаграмма In Progress 2')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()'''

    ###### Patch Available
    plt.hist(list_patch_available_day, color='orange', edgecolor='black', bins=30)
    plt.title('Диаграмма Patch Available')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    '''list_patch_available.sort()
    middle_index = int(len(list_patch_available) / 1.3)
    second_patr = list_patch_available[:middle_index]
    plt.hist(second_patr, color='orange', edgecolor='black', bins=40)
    plt.title('2. Диаграмма Patch Available 2')
    plt.xlabel('Время решения (часы)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()'''


def status_statistic(issue):
    sum_time_open = timedelta(0)
    sum_time_in_progress = timedelta(0)
    sum_time_resolved = timedelta(0)
    sum_time_reopened = timedelta(0)
    sum_time_patch_available = timedelta(0)

    time_start = get_issue_created_time(issue)
    for history in issue['changelog']['histories']:
        for item in history['items']:
            if item['field'] == 'status':
                time_stop = convert_time(history['created'])
                time = time_stop - time_start
                status = item['fromString']
                if status == 'Open':
                    sum_time_open = sum_time_open + time
                elif status == 'In Progress':
                    sum_time_in_progress = sum_time_in_progress + time
                elif status == 'Resolved':
                    sum_time_resolved = sum_time_resolved + time
                elif status == 'Reopened':
                    sum_time_reopened = sum_time_reopened + time
                elif status == 'Patch Available':
                    sum_time_patch_available = sum_time_patch_available + time
                time_start = time_stop

    return sum_time_open, sum_time_in_progress, sum_time_resolved, sum_time_reopened, sum_time_patch_available


def status_statistic(issue):
        sum_time_open = timedelta(0)
        sum_time_in_progress = timedelta(0)
        sum_time_resolved = timedelta(0)
        sum_time_reopened = timedelta(0)
        sum_time_patch_available = timedelta(0)

        time_start = get_issue_created_time(issue)
        for history in issue['changelog']['histories']:
            for item in history['items']:
                if item['field'] == 'status':
                    time_stop = convert_time(history['created'])
                    time = time_stop - time_start
                    status = item['fromString']
                    if status == 'Open':
                        sum_time_open = sum_time_open + time
                    elif status == 'In Progress':
                        sum_time_in_progress = sum_time_in_progress + time
                    elif status == 'Resolved':
                        sum_time_resolved = sum_time_resolved + time
                    elif status == 'Reopened':
                        sum_time_reopened = sum_time_reopened + time
                    elif status == 'Patch Available':
                        sum_time_patch_available = sum_time_patch_available + time
                    time_start = time_stop

        return sum_time_open, sum_time_in_progress, sum_time_resolved, sum_time_reopened, sum_time_patch_available


def get_issue_created_time(issue):
    time_str = issue['fields']['created']
    time = convert_time(time_str)
    return time


def convert_time(time_str):
    time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    return time


def timedelta_to_sec(time):
    return time.total_seconds()


def timedelta_to_days(time):
    return time.total_seconds() / (3600 * 24)


def timedelta_to_hours(time):
    return time.total_seconds() / 3600
