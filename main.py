import datetime

from ApiContestService import ApiContestService
from GroupListService import GroupListService
from SubmissionAnalyzer import SubmissionAnalyzer

# --------------------- SETTINGS, CHANGE IT --------------------------
analyzed_group = 'IHL-111'  # CHANGE IT
contest_id = "69172"  # CHANGE IT
deadline = datetime.datetime(year=2024,
                             month=10,
                             day=21,
                             hour=20,
                             minute=00,
                             second=00)  # CHANGE IT, write your local time
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
tasks_to_be_checked = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
# service.fill_submission_list_by_code(submissions, contest_id, tasks_to_checked=tasks_to_be_checked)
# pl_list = analyzer.plagiat_checker(submissions,
#                                    percent_plagiat=0.9,
#                                    tasks_to_check=tasks_to_be_checked)

stats = analyzer.get_statistics(group_list=group_list.get_list_of_group(analyzed_group),
                                submissions=submissions,
                                obligatory_problems=[pr for pr in service.get_list_problems(contest_id) if
                                                     '*' not in pr],
                                plagiat_list=pl_list,
                                deadline=deadline,
                                extra_problems=[pr for pr in service.get_list_problems(contest_id) if '*' in pr])
print(pl_list)
stats.to_csv(path_to_save + '.csv')
