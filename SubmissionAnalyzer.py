import datetime
from typing import Optional

from YaContestSubmission import YaContestSubmission
import pandas as pd


class SubmissionAnalyzer:
    def get_statistics(self,
                       group_list: list[str],
                       submissions: list[YaContestSubmission],
                       problem_list: list[str],
                       deadline: Optional[datetime.datetime] = None):
        df = pd.DataFrame(columns=problem_list,
                          index=group_list)

        for submission in submissions:
            if submission.author_name in group_list:
                if deadline is not None:
                    is_delayed = (datetime.datetime.fromisoformat(submission.submission_time[:-1]) > deadline)
                else:
                    is_delayed = False
                if df.loc[submission.author_name, submission.problem_alias] != 1 and not is_delayed:
                    df.loc[submission.author_name, submission.problem_alias] = int(submission.is_submission_correct())

        df = df.fillna(0)
        grades = (df.sum(axis=1) / len(problem_list)).apply(self.__get_grade_scale)
        df['total_solved'] = df.sum(axis=1)
        df['grades'] = grades
        return df

    def __get_grade_scale(self, grade: float) -> int:
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
