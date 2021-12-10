from RobotConnectionManager import RobotConnectionManager
from firebase_manager import database_manager
import socket, threading, time, firebase_admin, json
from firebase_admin import db

if __name__ == "__main__":
    robot_con_man = RobotConnectionManager(1201,4096)   #takes port number and buffer size as inputs for init
    db_man = database_manager()
    
    # Start connection with the robot in server mode
    robot_con_man.robot_address = "192.168.100.10"
    robot_con_man.begin("server")
    
    while True:
        # Send amount of ordered packets to UR10
        robot_con_man.send_str(db_man.return_product_ammount())

        # When robot reports being ready delete "process" table from database to indicate order being complete
        # Also do the same for "currentOrder" table
        if robot_con_man.blockking_get_recv_byte_buffer() == 1:
            db_man.delete_process_table()
            db_man.delete_currentOrder_table()
    

