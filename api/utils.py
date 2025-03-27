from api.database import session
from api.models import User
from matplotlib import pyplot as plt
import seaborn as sns


MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def compute_user_statistics(user: User) -> tuple[str, str] | tuple:
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

        for score in user.scores:
            # add subject if not exists
            if score.quiz.subject.name not in by_subject:
                by_subject[score.quiz.subject.name] = {
                    "name": score.quiz.subject.name,
                    **default_subject
                }
            # add user attempt by month
            if score.quiz.date_of_quiz.month not in by_month:
                by_month[score.quiz.date_of_quiz.month] = {
                    "month": score.quiz.date_of_quiz.month, "count": 0}
            # increment user attempt count
            by_month[score.quiz.date_of_quiz.month]["count"] += 1
            # add user attempt by subject
            by_subject[score.quiz.subject.name]["scores"].append({
                "total": score.total_score,
                "correct": score.user_score,
                "date_of_quiz": score.quiz.date_of_quiz,
                "id": score.id,
            })
            # compute total score and user score
            by_subject[score.quiz.subject.name]["total"] += score.total_score
            by_subject[score.quiz.subject.name]["score"] += score.user_score
        # compute average score for each subject
        for subject in by_subject.values():
            subject["average"] = subject["score"] / subject["total"]

        # plot the subject-wise user scores
        fig = plt.figure()
        plt.bar(by_subject.keys(), [subject["average"]
                for subject in by_subject.values()])
        plt.xlabel("Subjects")
        plt.ylabel("Average")
        filename_by_subject = f"by_subject-{hash(user.email)}.png"
        fig.savefig(f"static/images/{filename_by_subject}")
        fig = plt.figure()
        # plot the month-wise user attempts
        plt.pie(
            [month["count"] for month in by_month.values()],
            labels=[
                f'{MONTHS[month-1]} ({by_month[month]["count"]})' for month in by_month],
            labeldistance=1.125)
        filename_by_month = f"by_month-{hash(user.email)}.png"
        fig.savefig(f"static/images/{filename_by_month}")

        return (filename_by_subject, filename_by_month)
    except Exception as error:
        print('CELERY ERROR:', error)
        return tuple()
