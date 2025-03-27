from sqlalchemy import select
from celery import shared_task
from api.database import session
from api.models import Score
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime


MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


@shared_task(name="compute_monthly_statistics", ignore_results=False)
def compute_monthly_statistics() -> tuple[str, str] | tuple:
    sns.set_theme(style="whitegrid")

    try:
        by_subject = {}
        # compute subject-wise max scores and monthly user attempts
        for score in session.execute(select(Score)).scalars():
            if score.quiz.subject.name not in by_subject:
                by_subject[score.quiz.subject.name] = {
                    "max_score": 0,
                    "user_count": 0
                }
            by_subject[score.quiz.subject.name]["max_score"] = max(
                by_subject[score.quiz.subject.name]["max_score"], score.user_score / score.total_score)
            by_subject[score.quiz.subject.name]["user_count"] += 1

        # compute max scores by subject
        fig = plt.figure()
        plt.bar(by_subject.keys(), [subject["max_score"]
                for subject in by_subject.values()])
        plt.xlabel("Subjects")
        plt.ylabel("Max Score")
        filename_subjects = "static/images/admin_subject_wise.png"
        fig.savefig(filename_subjects)
        # compute monthly user attempts by subject
        fig = plt.figure()
        plt.pie(
            [by_subject[subject]["user_count"] for subject in by_subject],
            labels=[f'{subject} ({values["user_count"]})' for subject,
                    values in by_subject.items()],
            rotatelabels=True,
            labeldistance=0.5)
        plt.xlabel(MONTHS[datetime.now().month-1])
        filename_user_count = "static/images/admin_month_wise.png"
        fig.savefig(filename_user_count)

        return (filename_subjects, filename_user_count)
    except Exception as error:
        print('CELERY ERROR:', error)
        return tuple()
