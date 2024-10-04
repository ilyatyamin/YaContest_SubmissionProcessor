class YaContestSubmission:
    def __init__(self,
                 id: int,
                 compiler: str,
                 submission_time: str,
                 author_name: str,
                 author_id: int,
                 problem_id: str,
                 problem_alias: str,
                 time_consumption: int,
                 memory_consumption: int,
                 verdict: str,
                 falled_test: str,
                 score: int,
                 code: str,
                 other_info):
        self.id = id
        self.compiler = compiler
        self.submission_time = submission_time
        self.author_name = author_name
        self.author_id = author_id
        self.problem_id = problem_id
        self.problem_alias = problem_alias
        self.time_consumption = time_consumption
        self.memory_consumption = memory_consumption
        self.verdict = verdict
        self.falled_test = falled_test
        self.score = score
        self.code_submission = code
        self.other_info = other_info

    def is_submission_correct(self):
        return self.verdict == 'OK'
