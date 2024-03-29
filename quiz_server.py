import socket
from threading import Thread
import random
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipaddress = "127.0.0.1"
port = 8000
server.bind((ipaddress, port))
server.listen()
clients = []
nicknames = []
questions = ["What is the largest state in the USA? \n a.Texas \n b.California \n c.Alaska \n d.Washington", "Which major aircraft manufacturer unveiled its lighter, smoother, more turbulent-resistant 787 Dreamliner in 2007? \n a. Airbus \n b. Northrop Grumman \n c. General Electric \n d. Boeing", "How many sides does a stop sign have? \n a. 5 \n b. 6 \n c. 7 \n d. 8"]
answers = ["c","d","d"]
print("Server is running")
def broadcast(message, connection): 
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode("utf-8"))
            except: 
                remove(client)

def remove(connection) :
    if connection in clients:
        clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

def get_random_question_answer():
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)


def clientThread(conn, nickname) :
    score = 0
    conn.send("Welcome to this quiz game".encode("utf-8"))
    conn.send("Answers to questions are either a, b, c, or d".encode("utf-8"))
    conn.send("Good Luck!!\n\n".encode("utf-8"))
    index,question,answer = get_random_question_answer()
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if (message) :
                print("Message:", message)
                if message.lower().split(":")[1] == answer:
                    score+=1
                    conn.send(f"Bravo your score is {score}\n\n".encode("utf-8"))

                else:
                   conn.send(f"Wrong!! Better luck next time!\n\n".encode("utf-8")) 
                remove_question(index)
                index,question,answer = get_random_question_answer()
            else: 
                remove(conn)
                remove_nickname(nickname)
        except:
            continue
while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    clients.append(conn)
    message = "{} joined!!!!!!!!".format(nickname)
    print(message)
    broadcast(message,conn)
    new_thread = Thread(target = clientThread, args = (conn, addr))
    new_thread.start()