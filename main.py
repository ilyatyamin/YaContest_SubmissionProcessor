import datetime

from ApiContestService import ApiContestService
from GroupListService import GroupListService
from SubmissionAnalyzer import SubmissionAnalyzer

# --------------------- SETTINGS, CHANGE IT --------------------------
analyzed_group = 'IHL-121'  # CHANGE IT
contest_id = "68815"  # CHANGE IT
deadline = datetime.datetime(year=2024,
                             month=10,
                             day=11,
                             hour=21,
                             minute=59,
                             second=59)  # CHANGE IT, write your local time
# --------------------- SETTINGS, CHANGE IT --------------------------


secret_code = 'y0_AgAAAAAW3qH0AAyEuAAAAAESenn_AAC9dsJiYphGR6AcWui1Zg4RPZPSNQ'
path_to_list_of_all_groupes = 'python_interhouse_24.csv'
path_to_save = f'report_graded'

service = ApiContestService(secret_code)
group_list = GroupListService(path_to_list_of_all_groupes)
analyzer = SubmissionAnalyzer()

submissions = service.get_submissions(contest_id, only_ok=True)
pl_list = []

# decomment if you need plagiat check
# service.fill_submission_list_by_code(submissions, contest_id, tasks_to_checked=['H', 'I'])
# pl_list = analyzer.plagiat_checker(submissions,
#                                    percent_plagiat=0.9,
#                                    tasks_to_check=['H', 'I'])

stats = analyzer.get_statistics(group_list.get_list_of_group(analyzed_group),
                                submissions,
                                service.get_list_problems(contest_id),
                                pl_list,
                                deadline)
stats.to_csv(path_to_save + '.csv')
