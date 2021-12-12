from RobotConnectionManager import RobotConnectionManager
from firebase_manager import database_manager
import socket, threading, time, firebase_admin, json
from firebase_admin import db

class ur5_control():
    def __init__(self):
        #takes port number and buffer size as inputs for init
        #TODO UNCOMMENT below
        #self.__robot_con_man = RobotConnectionManager(ip="192.168.100.10",port=1201,buffer=4096)   
        self.__db_man = database_manager()
        #self.__db_man.database_back_up_create()
        # Start connection with the robot in server mode
        #self.__robot_con_man.robot_address = "192.168.100.10" # not required
        #TODO UNCOMMENT below 
        #self.__robot_con_man.begin("server")

    def work(self):
        time.sleep(5)
        # get amount of products to unload for the current order from the database
        self.__packetCount = self.__db_man.return_product_ammount()
        __delivery_increment = 0
        for __delivery_increment in range(self.__packetCount):
            # Tell UR5 to keep working until delivery is completed
            #TODO UNCOMMENT below
            #self.__robot_con_man.send_str("more")
            print("DEBUG more")
            if 1:#self.__robot_con_man.blockking_get_recv_byte_buffer() == "1":
                __delivery_increment = __delivery_increment + 1
                print("DEBUG delivery_increment value PROCESS:"+str(__delivery_increment))
        #TODO UNCOMMENT below
        # Tell robot that the order is complete
        # (necessary so robot knows to when to start stacking process over from the beginning)
        #self.__robot_con_man.send_str("ready")

        # When robot is done with the current order set orderList table from database to indicate order being complete
        # Also do the same for "currentOrder" table
        #TODO commented out for testing purposes, remember to UNCOMMENT below
        #self.__db_man.delete_process_table()
        #self.__db_man.delete_currentOrder_table()    
        print("DEBUG database remove")
        print("DEBUG delivery_increment value END:"+str(__delivery_increment))

if __name__ == "__main__":
    def main():
        desdi = ur5_control()
        desdi.work()
    main()
    

