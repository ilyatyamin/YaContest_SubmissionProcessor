import datetime
import os
import random
import shutil
import sys
import time
from typing import Optional

from YaContestSubmission import YaContestSubmission
from copydetect import CopyDetector
import pandas as pd


class SubmissionAnalyzer:
    def __init__(self):
        self.plagiariam_status = "0 (IG)"
        self.grade_if_plagiat = 2

    def get_statistics(self,
                       group_list: list[str],
                       submissions: list[YaContestSubmission],
                       problem_list: list[str],
                       plagiat_list: list[YaContestSubmission],
                       deadline: Optional[datetime.datetime] = None):
        df = pd.DataFrame(columns=problem_list,
                          index=group_list)
        df = df.fillna(0)

        for submission in submissions:
            if submission.author_name in group_list:
                is_delayed = self.__get_is_delayed_status(deadline, submission)

                if df.loc[submission.author_name, submission.problem_alias] != 1 and not is_delayed:
                    df.loc[submission.author_name, submission.problem_alias] = int(submission.is_submission_correct())
        grades = (df.sum(axis=1) / (len(problem_list))).apply(self.__get_grade_scale)
        df['grades'] = grades
        df['additional_info'] = ''

        # get plagiat list
        for plagiat in plagiat_list:
            if plagiat.author_name in group_list:
                df.loc[plagiat.author_name, 'grades'] = 2
                df.loc[plagiat.author_name, 'additional_info'] = 'plagiat'

        return df

    def plagiat_checker(self, submissions: list[YaContestSubmission],
                        excluded_tasks=None,
                        percent_plagiat=0.8) -> list[YaContestSubmission]:
        folder_name = self.__create_folder_with_submissions(submissions, excluded_tasks)
        plagiat_list = set()

        for dir in os.listdir(folder_name):
            detector = CopyDetector(test_dirs=[f"{folder_name}/{dir}"],
                                    extensions=["py"],
                                    display_t=percent_plagiat,
                                    silent=True)
            print(f"Running plagiat checker...")
            detector.run()
            time.sleep(1)

            for triple in detector.get_copied_code_list():
                print(f"""
\n\n\n
Plagiat was detected. User 1: {triple[2].split('/')[-1].split('.')[0]}
\033[96m{self.__format_code_text(triple[4])}\033[0m\n
User 2: {triple[3].split('/')[-1].split('.')[0]}
\033[96m{self.__format_code_text(triple[5])}\033[0m\n

Percent of plagiarism: {triple[0]} <-> {triple[1]}
Enter 1 if the given attempts should be considered as plagiarism, otherwise any other input
""")

                user_inp = input()
                if user_inp.strip() == "1":
                    id1 = triple[2].split('/')[-1].split('.')[0].split('_')[-1]
                    id2 = triple[3].split('/')[-1].split('.')[0].split('_')[-1]
                    plagiat_list.add(int(id1))
                    plagiat_list.add(int(id2))
                sys.stdout.flush()
        self.__delete_folder_with_submissions(folder_name)
        return [next(subm for subm in submissions if subm.id == plagiat_id) for plagiat_id in plagiat_list]

    @staticmethod
    def __create_folder_with_submissions(submissions: list[YaContestSubmission],
                                         excluded_tasks) -> str:
        dr_repres = str(datetime.datetime.now()).replace(' ', '')
        folder_name = f'plagiat_{dr_repres}_{str(random.randint(0, 10 ** 10))}'
        os.makedirs(folder_name, exist_ok=True)
        for attempt in submissions:
            if ((excluded_tasks is None or attempt.problem_alias not in excluded_tasks)
                    and attempt.verdict.lower() == 'ok'):
                os.makedirs(f"{folder_name}/{attempt.problem_alias}", exist_ok=True)

                file_path = f'{folder_name}/{attempt.problem_alias}/{attempt.author_name}_{attempt.id}.py'
                with open(file_path, 'w+') as attempt_file:
                    attempt_file.write(attempt.code_submission)
        return folder_name

    @staticmethod
    def __delete_folder_with_submissions(path: str) -> None:
        shutil.rmtree(path)

    @staticmethod
    def __format_code_text(code: str):
        return code[(code.find('>') + 1):(code.rfind('<'))]

    @staticmethod
    def __find_user_by_id(submissions: list[YaContestSubmission], submission_id: str):
        for x in submissions:
            if x.id == submission_id:
                return x.author_name
        return None

    @staticmethod
    def __get_is_delayed_status(deadline,
                                submission: YaContestSubmission):
        if deadline is not None:
            return datetime.datetime.fromisoformat(submission.submission_time[:-1]) > deadline
        else:
            return False

    @staticmethod
    def __get_grade_scale(grade) -> int:
        if grade == 'PL':
            return 2
        percent = grade * 100
        if 0 <= percent <= 9:
            return 2
        elif 10 <= percent <= 50:
            return 3
        elif 51 <= percent <= 74:
            return 4
        elif 75 <= percent <= 100:
            return 5
        else:
            raise Exception(f"wrong percent. need to be [0, 100], got {percent}")
