import datetime

from ContestService import ContestService
from GroupListService import GroupListService
from SubmissionAnalyzer import SubmissionAnalyzer

analyzed_group = 'IHL-111'  # CHANGE IT
contest_id = "68407"  # CHANGE IT
deadline = datetime.datetime(year=2024,
                             month=10,
                             day=2,
                             hour=13,
                             minute=10,
                             second=0)  # CHANGE IT, write your local time

secret_code = 'y0_AgAAAAAW3qH0AAyEuAAAAAESenn_AAC9dsJiYphGR6AcWui1Zg4RPZPSNQ'
path_to_list_of_all_groupes = 'python_interhouse_24.csv'

path_to_save = f'report_graded_{analyzed_group}'

service = ContestService(secret_code)
group_list = GroupListService(path_to_list_of_all_groupes)
analyzer = SubmissionAnalyzer()

stats = analyzer.get_statistics(group_list.get_list_of_group(analyzed_group),
                                service.get_submissions(contest_id),
                                service.get_list_problems(contest_id),
                                deadline)
stats.to_csv(path_to_save + '.csv')
