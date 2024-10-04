import requests as req
import json

from YaContestSubmission import YaContestSubmission


class ContestService:
    def __init__(self,
                 secret_code: str):
        self.__secret_code = secret_code
        self.__headers = {
            "Authorization": f"OAuth {secret_code}"
        }

    def get_submissions(self,
                        contest_id: str,
                        page_size=10 ** 5) -> list[YaContestSubmission]:
        api_url = self.__get_all_submissions_url(contest_id, page_size)
        request = req.get(api_url, headers=self.__headers)

        if request.status_code != 200:
            raise Exception(request.text)
        else:
            info = json.loads(request.text)
            result = []
            for submission in info['submissions']:
                code = self.__get_code_text(contest_id, submission['id'])

                result.append(YaContestSubmission(submission['id'],
                                                  submission['compiler'],
                                                  submission['submissionTime'],
                                                  submission['author'],
                                                  submission['authorId'],
                                                  submission['problemId'],
                                                  submission['problemAlias'],
                                                  submission['time'],
                                                  submission['memory'],
                                                  submission['verdict'],
                                                  submission['test'],
                                                  submission['score'],
                                                  code,
                                                  submission))
            return result

    def __get_code_text(self, contest_id, submission_id):
        api_url_code = self.__get_code_submission_url(contest_id, submission_id)
        response = req.get(api_url_code, headers=self.__headers)
        if response.status_code != 200:
            raise Exception('error in getting code text')
        return response.text

    def get_list_problems(self,
                          contest_id: str) -> list[str]:
        api_url = self.__get_list_problems_url(contest_id)
        request = req.get(api_url, headers=self.__headers)

        if request.status_code != 200:
            raise Exception(request.text)
        else:
            info = json.loads(request.text)
            return sorted([task['alias'] for task in info['problems']])

    def __get_all_submissions_url(self, contest_id, page_size):
        return f'https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/submissions?page=1&pageSize={page_size}'

    def __get_list_problems_url(self, contest_id, locale='ru'):
        return f'https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/problems?locale={locale}'

    def __get_code_submission_url(self, contest_id, submission_id):
        return f'https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/submissions/{submission_id}/source'

    def __str__(self):
        string_presentation = ''
        for obj in self.__dir__():
            string_presentation += f'#{obj}'
        return string_presentation
