#test script for developing socket_controller
import socket, time, threading


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("172.16.177.128",30020))
while True:
    send = input()
    msg= 'def qwer():\n popup("hi")\nend\nqwer()\n'
    msg='popup("hi2")\n'
    s.send(bytes(msg, "UTF-8"))
    #message = s.recv(256)
    #print(message.decode("utf-8"))
    #print(message)
    #time.sleep(3)



# while True:
#     msg = s.recv(8)
#     full_msg += msg.decode("utf-8")
#     if len(msg) == 0:
#         break
# print(full_msg)