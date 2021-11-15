#test script for developing socket_controller
import socket, time, threading


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("192.168.1.225",1201))
while True:
    s.send(bytes("Test message", "utf-8"))
    message = s.recv(32)
    print(message.decode("utf-8"))
    #time.sleep(3)



# while True:
#     msg = s.recv(8)
#     full_msg += msg.decode("utf-8")
#     if len(msg) == 0:
#         break
# print(full_msg)