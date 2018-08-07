#! /usr/bin/env python

import argparse
from datetime import datetime
from launchpadlib.launchpad import Launchpad
import re

TAG_TO_CUSTOMER = {
    'att-aic-contrail': 'AT&T',
    'dt': 'DT',
    'netcracker': 'NETCRACKER',
    'orange': 'ORANGE',
    'ebay': 'EBAY',
    'nttc': 'NTT',
}

def time_type(s, fmt = "%Y-%m-%d"):
    try:
        datetime_obj = datetime.strptime(s, fmt)
    except:
        raise argparse.ArgumentTypeError(
            "Wrong time format e.g. 2018-03-19")
    return s

def get_case_number(tags):
    pattern = "20\d{2}-\d{4}-\d{4}$"
    return [c for c in tags if re.match(pattern, c)]

def get_customer(tags):
    return [TAG_TO_CUSTOMER[t] for t in tags if t in TAG_TO_CUSTOMER]

def get_times(task):
    date_created = task.date_created
    date_last_touch = max(task.bug.date_last_updated,
                          task.bug.date_last_message)
    date_triaged = None
    date_fix_committed = None
    date_assigned = None
    if not len(task.related_tasks):
        date_assigned = task.date_assigned
        date_triaged = task.date_triaged
        date_fix_committed = task.date_fix_committed
    else:
        for related_task in task.related_tasks:
            if related_task.date_assigned:
                if date_assigned:
                    date_assigned = min(date_assigned, related_task.date_assigned)
                else:
                    date_assigned = related_task.date_assigned

            if related_task.date_triaged:
                if date_triaged:
                    date_triaged = min(date_triaged, related_task.date_triaged)
                else:
                    date_triaged = related_task.date_triaged

            if related_task.date_fix_committed:
                if date_fix_committed:
                    date_fix_committed = min(date_fix_committed, related_task.date_fix_committed)
                else:
                    date_fix_committed = related_task.date_fix_committed

    return map(lambda x:x.strftime("%Y-%m-%d") if x is not None else '',
               (date_created,date_assigned,date_triaged,
                date_fix_committed,date_last_touch))

def lp_query(args):

    launchpad = Launchpad.login_with('juniperopenstack', 'production')
    project=launchpad.projects['juniperopenstack']

    open_status = ('New', 'Incomplete', 'Triaged', 'Opinion',
                   'Confirmed', 'In Progress', 'Triaged')

    close_status = ('Invalid', 'Won\'t Fix', 'Expired',
                    'Fix Committed', 'Fix Released')

    status = ()
    if args.open_only and not args.closed_only:
        status = open_status
    elif args.closed_only and not args.open_only:
        status = close_status

    #tag = args.tag if args.tag else '*'

    bugs = project.searchTasks(tags=args.tag,
                               status=status,
                               created_before=args.before,
                               created_since=args.after,
                               order_by='id')

    print ('id,age,customer,importance,status,cases,reporter,'
           'assignee,title,date_created,date_assigned,date_triaged,'
           'date_fix_committed, date_last_touched')
    for task in bugs:
        id = str(task.bug.id)
        owner = task.owner.display_name
        assignee = 'n/a'
        if task.assignee:
            assignee = task.assignee.display_name
        importance = task.importance
        title = '"' + task.bug.title + '"'

        age = (datetime.now(task.date_created.tzinfo) - task.date_created)
        age_str = "%sd%sh%sm" % (str(age.days),
                                 str(age.seconds//3600),
                                 str((age.seconds//60)%60))
        status = task.status
        cases = ' '.join(get_case_number(task.bug.tags))
        customers = ' '.join(get_customer(task.bug.tags))

        print u','.join([id, age_str, customers, importance, status, cases,
                         owner, assignee, title] + get_times(task))

def main():
    parser = argparse.ArgumentParser(
        prog='lpq',
        description='Script to query Contrail related bugs in launchpad ')
    parser.add_argument(
        '-a', '--after', type=time_type,
        default = "2000-01-01",
        help = "List launchpad created since given time " +
               "e.g. 2018-03-19")
    parser.add_argument(
        '-b', '--before', type=time_type,
        default = datetime.utcnow().strftime("%Y-%m-%d"),
        help = "List launchpad created before given time " +
               "e.g. 2018-03-19")
    parser.add_argument(
        'tag', type=str, default='*',
        help = "List launchpad matching given tags")
    parser.add_argument(
        '--open_only', action="store_true",
        help = "Only list LPs in open state")
    parser.add_argument(
        '--closed_only', action="store_true",
        help = "Only list LPs not in open state")

    parser.set_defaults(func=lp_query)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
