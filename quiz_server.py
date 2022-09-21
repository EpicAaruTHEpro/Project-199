import socket
from threading import Thread
import random
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipaddress = "127.0.0.1"
port = 8000
server.bind((ipaddress, port))
server.listen()
clients = []
questions = ["What is the largest state in the USA? \n a.Texas \n b.California \n c.Alaska \n d.Washington"]
answers = ["c"]
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
    index,question,answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if (message) :
                if message.lower() == answer:
                    score+=1
                    conn.send(f"Bravo your score is {score}\n\n".encode("utf-8"))

                else:
                   conn.send(f"Wrong!! Better luck next time!\n\n".encode("utf-8")) 
                remove_question(index)
                index,question,answer = get_random_question_answer(conn)
            else: 
                remove(conn)
        except:
            continue
while True:
    conn, addr = server.accept()
    clients.append(conn)
    print(addr[0] + " connected")
    new_thread = Thread(target = clientThread,args=(conn))
    new_thread.start()