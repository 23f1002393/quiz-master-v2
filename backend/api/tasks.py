from sqlalchemy import select
from celery import shared_task
from api.database import session
from api.models import Score, User
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime


MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


@shared_task(name="compute_user_statistics", ignore_results=False)
def compute_user_statistics(user: dict) -> tuple[str, str] | tuple:
    sns.set_theme(style="whitegrid")

    try:
        by_month = {}
        by_subject = {}

        default_subject = {
            "scores": [],
            "average": 0,
            "total": 0,
            "score": 0,
        }

        for score in user["scores"]:
            # add subject if not exists
            if score["subject"] not in by_subject:
                by_subject[score["subject"]] = {
                    "name": score["subject"],
                    **default_subject
                }
            # add user attempt by month
            if score["date_of_quiz"].month not in by_month:
                by_month[score["date_of_quiz"].month] = {
                    "month": score["date_of_quiz"].month, "count": 0}
            # increment user attempt count
            by_month[score["date_of_quiz"].month]["count"] += 1
            # add user attempt by subject
            by_subject[score["subject"]]["scores"].append({
                "total": score["total_score"],
                "correct": score["user_score"],
                "date_of_quiz": score["date_of_quiz"],
            })
            # compute total score and user score
            by_subject[score["subject"]]["total"] += score["total_score"]
            by_subject[score["subject"]]["score"] += score["user_score"]
        # compute average score for each subject
        for subject in by_subject.values():
            subject["average"] = subject["score"] / subject["total"]

        # plot the subject-wise user scores
        fig = plt.figure()
        plt.bar(by_subject.keys(), [subject["score"]
                for subject in by_subject.values()])
        plt.xlabel("Subjects")
        plt.ylabel("Total score by subject")
        filename_by_subject = f"by_subject-{hash(user["email"])}.png"
        fig.savefig(f"static/images/{filename_by_subject}")
        fig = plt.figure()
        # plot the month-wise user attempts
        plt.pie(
            [month["count"] for month in by_month.values()],
            labels=[
                f'{MONTHS[month-1]} ({by_month[month]["count"]})' for month in by_month],
            labeldistance=1.125)
        plt.xlabel("Month wise quiz attempts")
        filename_by_month = f"by_month-{hash(user["email"])}.png"
        fig.savefig(f"static/images/{filename_by_month}")

        return (filename_by_subject, filename_by_month)
    except Exception as error:
        print('CELERY ERROR:', error)
        return tuple()


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
