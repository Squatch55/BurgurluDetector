import praw
import config
import time
import os
from colorama import init, Fore

init(autoreset=True)

#   Discord: squatchx34
#   Discord: squatchx34
#   Discord: squatchx34
#   Discord: squatchx34


def bot_login():
    print(f"{Fore.YELLOW}Giriş yapılıyor...")
    r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent="Bulgur Detector")
    print(f"{Fore.YELLOW}Giriş yapıldı!")

    return r

def get_submissions_to_subreddit(author, subreddit_name):
    author = r.redditor(author)
    submissions = author.submissions.new(limit=None) # Burdan zaman limitini değiştirebilirsinz
    comments = author.comments.new(limit=None) # Burdan zaman limitini değiştirebilirsinz
    submissions_and_comments_to_subreddit = []

    for submission in submissions:
        if submission.subreddit.display_name.lower() == subreddit_name.lower():
            submissions_and_comments_to_subreddit.append(submission)

    for comment in comments:
        if comment.subreddit.display_name.lower() == subreddit_name.lower():
            submissions_and_comments_to_subreddit.append(comment)

    return submissions_and_comments_to_subreddit
  
def run_bot(r, LoggedBurgurlu):
    print(f"{Fore.YELLOW}Bulgurlu aranıyor...")

    bulgurlu_count = 0
    bulgurlu_degil_count = 0

    for comment in r.subreddit('kgbtr').comments(limit=1000): # Burdan kaç kişiyi tarayacağını değiştirebilirsinz
        author = str(comment.author)
        if author not in LoggedBurgurlu:
            submission_or_comment = get_submissions_to_subreddit(author, "burdurland")
            if submission_or_comment:
                submission = submission_or_comment[0]
                permalink = submission.permalink
                LoggedBurgurlu.append(author)
                with open("LoggedBurgurlu.txt", "a+", encoding="utf-8", errors="ignore") as f:
                    f.seek(0)
                    file_content = f.read()
                    if author not in file_content:
                        f.write(f"{author} - Permalink: {permalink}\n")
                        bulgurlu_count += 1
                        print(f"{Fore.GREEN}Bulgurlu bulundu: {author} - {Fore.CYAN}{permalink} - {Fore.GREEN}{bulgurlu_count}:{Fore.RED}{bulgurlu_degil_count}")
            else:
                bulgurlu_degil_count += 1
                print(f"{Fore.RED}Bulgurlu değil: {author} - {Fore.GREEN}{bulgurlu_count}:{Fore.RED}{bulgurlu_degil_count}")
        time.sleep(0.2)

    print("2 dakika bekleniyor...")
    time.sleep(120)

def get_saved_comments():
    if not os.path.isfile("LoggedBurgurlu.txt"):
        LoggedBurgurlu = []
    else:
        with open("LoggedBurgurlu.txt", "r", encoding="latin-1", errors="ignore") as f:
            LoggedBurgurlu = f.read()
            LoggedBurgurlu = LoggedBurgurlu.split("\n")
            LoggedBurgurlu = list(filter(None, LoggedBurgurlu))

    return LoggedBurgurlu

r = bot_login()
LoggedBurgurlu = get_saved_comments()
print(f"{Fore.GREEN}Şuana kadar bulunanlar: {LoggedBurgurlu}")

while True:
    run_bot(r, LoggedBurgurlu)