import socket, time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    server.bind(("0.0.0.0", 1201))
    server.listen(5)
    robot_socket, robot_ip = server.accept()

    while robot_socket:
        robot_socket.send(bytes("Hello", "utf-8"))
        time.sleep(1)
