import os
import random
import time

import praw
import requests


def main():
    reddit = login_reddit()
    url = 'https://www.reddit.com/r/AskReddit/comments/7zzim3/what_app_is_so_useful_you_cant_believe_its_free/'
    answers_scrape('outoftheloop', reddit)


def comment_loop(subname, reddit):
    print(reddit.auth.limits)
    for comment in reddit.subreddit(subname).stream.comments():
        if any(word in comment.body.lower() for word in list_of_words):
            print(comment.body)


def generate_random(reddit):
    submissions = reddit.subreddit('learnpython').hot(limit=50)
    submission_id = random.sample(list(submissions), 1)
    submission = reddit.submission(id=submission_id[0].id)
    print(submission.author)
    print(submission.selftext)


def picture(reddit):
    sub_list = ['funny', 'earthporn', 'pics']
    submission = reddit.subreddit(random.choice(sub_list)).random()
    if (submission.score < 100):
        print('Not enough updoots')
        print("This has a score of: {}".format(submission.score))
        print("From: {}".format(submission.subreddit))
    else:
        print("This has a score of: {}".format(submission.score))
        print("From: {}".format(submission.subreddit)) 


def generate_markdown(url, reddit):
    submission = reddit.submission(url=url)
    submitter = submission.author.name
    title = submission.author.name
    print(title)
    submission_body = submission.selftext
    filename = ("{}.txt".format(submission.id))
    submission.comments.replace_more(limit=None)
    f = open(filename, 'w+', encoding='utf-8')
    f.write(">{}\n\n".format(submission_body))
    f.write('Question|Answer\n:--|:--\n')
    for comment in submission.comments.list():
        for second_level_comment in comment.replies:
            if second_level_comment.author == submitter:
                question = comment.body.splitlines()
                answer = second_level_comment.body.splitlines()
                question = list(filter(None, question))
                answer = list(filter(None, answer))
                num_quest = len(question)
                num_answer= len(answer)
                if num_quest > num_answer:
                    for i in range(num_answer):
                        string_insert = ("[{0}]({1})|{2}\n".format(question[i], comment.permalink, answer[i]))
                        f.write(string_insert)
                    for j in range(num_answer, num_quest):
                        string_insert ="{0}| Q answered above \n".format(question[j])
                        f.write(string_insert)
                elif num_quest == num_answer:
                    for i in range(num_answer):
                        string_insert = ("[{0}]({1})|{2}\n".format(question[i], comment.permalink, answer[i]))
                        f.write(string_insert)
                elif num_quest < num_answer:
                    for i in range(num_quest):
                        string_insert = ("[{0}]({1})|{2}\n".format(question[i], comment.permalink, answer[i]))
                        f.write(string_insert)
                    for j in range(num_quest, num_answer):
                        string_insert = (" Answer to Q above |{0}\n".format(answer[j]))
                        f.write(string_insert)
                
    f.write("{}".format(url))
    f.close()

def generate_html_ama(url, reddit):   
    reddit = reddit
    submission = reddit.submission(url=url)
    submitter = submission.author.name
    title = submission.title
    submission_body = submission.selftext
    filename = ("{}.txt".format(title))
    submission.comments.replace_more(limit=None, threshold=10)
    f = open(os.path.join('reddit', filename), 'w+', encoding='utf-8')
    f.write("{}\n".format(submission_body))
    f.write('<table style="width:100%;text-align:left;background-color:gold;">')
    for comment in submission.comments.list():
        for second_level_comment in comment.replies:
            if second_level_comment.author == submitter:
                question = comment
                string_insert = ("<tr><td bgcolor='#d3d3d3'>Question: {0}\n</td></tr><tr><td bgcolor='#f5d5d5'>Answer: {1}\n</td></tr>".format(question.body,second_level_comment.body))
                f.write(string_insert)
    f.write("</table>")
    f.close()

def generate_html_thread(url, reddit):
    reddit = reddit
    submission = reddit.submission(url=url)
    title = submission.id + "_html"
    submission_body = submission.selftext
    filename = ("{}.txt".format(title))
    submission.comments.replace_more(limit=None)
    source = ("https://www.reddit.com/{}".format(submission.permalink))
    f = open(filename, 'w', encoding='utf-8')
    f.write("{}\n".format(submission_body))
    f.write("{}\n".format(source))
    f.write('<table style="width:100%;text-align:left;background-color:gold;">')
    for comment in submission.comments.list():
        if comment.score > 10 and comment.depth == 0:
            string_insert = ("<tr><td bgcolor='#d3d3d3'>/u/{0}\n</td></tr><tr><td bgcolor='#f5d5d5'>Answer: {1}\n</td></tr>".format(comment.author,comment.body))
            f.write(string_insert)
    f.write("</table>")
    f.close()

def time_scrape_sub(subname, reddit):
    subreddit = reddit.subreddit(subname)
    f = open(subname, 'w+', encoding='utf-8')
    f.write("User|Title|Score|Date\n")
    f.write(":--|:--|:--|:--\n")
    for submission in subreddit.submissions(start= None, end= 1515326411):
        if "amos yee" in submission.title.lower():
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(submission.created_utc))
            f.write("{0}| [{1}]({2})|{3}|{4}\n".format(submission.author, submission.title, submission.permalink, submission.score, date))
        else:
            continue
    f.close()

def time_scrape_com(subname, reddit):
    subreddit = reddit.subreddit(subname)
    print(reddit.auth.limits)
    f = open(subname, 'w+', encoding='utf-8')
    f.write("User|Comment|Score|Date\n")
    f.write(":--|:--|:--|:--\n")
    for submission in subreddit.submissions(start= 1509408000, end= 1514678400):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if comment.author == "amos-counter-bot" or comment.author == "sg_amos_yee_counter" or comment.author == "rsg-retrivr":
                continue
            elif "amos yee" in comment.body.lower():
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(submission.created_utc))
                answer = comment.body.splitlines()
                comment_text = ' '.join(answer)
                comment_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.created_utc))
                comment_text.strip('|')
                f.write("{0}| [{1}]({2})|{3}|{4}\n".format(comment.author, comment_text, comment.permalink, comment.score, comment_date))
            else:
                continue


def generate_md_thread(url, reddit):
    reddit = reddit
    print(reddit.auth.limits)
    submission = reddit.submission(url=url)
    print(reddit.auth.limits)
    title = submission.title    
    #submission_body = submission.selftext
    filename = ("{}.txt".format(submission.id))
    submission.comments.replace_more(limit = None, threshold = 1)
    print(reddit.auth.limits)
    source = ("https://www.reddit.com/{}".format(submission.permalink))
    f = open(filename, 'w', encoding='utf-8')
    f.write("[Source]({})\n\n".format(source))
    f.write('User| Answer| \n:--|:--\n')
    for comment in submission.comments.list():
        if comment.score > 500 and comment.depth == 0:
            answer = comment.body.splitlines()
            string_insert = ("[{0}]({1})| {2} upvotes\n".format(comment.author, comment.permalink, comment.score))
            f.write(string_insert)
            for line in answer:
                if len(line)>0:
                    string_insert = (" | {}\n".format(line))
                    f.write(string_insert)
    f.close()

def answers_scrape(subname , reddit):
    subreddit = reddit.subreddit(subname)
    i = 0
    print(reddit.auth.limits)
    filename = subname
    f = open(filename, 'w+', encoding='utf-8')
    f.write('Question | Answer| \n:--|:--\n')
    #submission_body = submission.selftext
    for submission in subreddit.top('week'):
        title = submission.title
        top_comment = (submission.comments.list())[0]
        print(top_comment)
        f.write("[{0}]({1}) | {2} - Score {3}\n".format(title, submission.permalink, top_comment.author, top_comment.score))
        for line in top_comment.body.splitlines():
            f.write(" | {}\n".format(line))
        i += 1  
        if i > 5:
            break
        else:
            continue
        


def login_reddit():
    reddit = praw.Reddit('bot1', user_agent='<Python> Test bot')
    return reddit

def process_submissions(submission):
    download_image(submission.url, format(submission.title))
    print("done")

def download_image(image_url, local_file):
    response = requests.get(image_url)
    if response.status_code == 200:
        print('Downloading %s...' % (local_file))
    with open(local_file, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    
def generate_html_ama_test(url, reddit):   
    reddit = reddit
    submission = reddit.submission(url=url)
    submitter = submission.author.name
    title = submission.title
    submission_body = submission.selftext
    filename = ("{}.txt".format(title))
    submission.comments.replace_more(limit= None, threshold= 1)
    f = open(filename, 'w', encoding='utf-8')
    f.write("{}\n".format(submission_body))
    f.write('<table style="width:100%;text-align:left;background-color:gold;">')
    for comment in submission.comments.list():
        if comment.author == submitter and comment.depth== 1:
            question = comment.parent()
            string_insert = ("<tr><td bgcolor='#d3d3d3'>Question: {0}\n</td></tr><tr><td bgcolor='#f5d5d5'>Answer: {1}\n</td></tr>".format(question.body,comment.body))
            f.write(string_insert)
    f.write("</table>")
    f.close()
    

if __name__ == '__main__':
    main()
