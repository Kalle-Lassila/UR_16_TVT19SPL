from RobotConnectionManager import RobotConnectionManager
from firebase_manager import database_manager
import socket, threading, time, firebase_admin, json
from firebase_admin import db

class ur5_control():
    def __init__(self):
        #takes robots ip, port number and buffer size as inputs for init
        self.__robot_con_man = RobotConnectionManager(ip="192.168.100.10",port=1201,buffer=4096)   
        self.__db_man = database_manager()

        # DEBUG create back up of current database
        #self.__db_man.database_back_up_create()
        
        # Start connection with the robot in server mode
        #self.__robot_con_man.robot_address = "192.168.100.10" # not required 
        self.__robot_con_man.begin("server")

    def work(self):
        # get amount of products to unload for the current order from the database
        self.__packetCount = self.__db_man.return_product_ammount()
        __delivery_increment = 0

        #if there are workable orders initiate the robot, otherwise wait a while and check the database again
        if self.__packetCount != 0:
            # Tell UR5 to keep working until delivery is completed
            for __delivery_increment in range(self.__packetCount):
                self.__robot_con_man.send_str("work")
                #TODO REMOVE debug print below
                print("DEBUG work")
                # Wait for robot to indicate it has completed one move cycle
                if self.__robot_con_man.blockking_get_recv_byte_buffer() == "1":
                    __delivery_increment = __delivery_increment + 1
                    #TODO REMOVE debug print below
                    print("DEBUG delivery_increment value PROCESS:"+str(__delivery_increment))
                    time.sleep(1) #TODO sleep here might not be necessary delete this line if so
        
            # Tell robot that the order is complete
            # (necessary so robot knows to when to start stacking process over from the beginning)
            time.sleep(1) #wait a sec so robot is ready in listening mode, maybe not necessary
            self.__robot_con_man.send_str("ready")

            #TODO commented out for testing purposes, remember to UNCOMMENT below
            # When robot is done with the current order set orderList table from database to indicate order being complete
            # Also do the same for "currentOrder" table
            #self.__db_man.delete_process_table()
            #self.__db_man.delete_currentOrder_table()
        
            #TODO REMOVE debug print below    
            print("DEBUG database remove")
            print("DEBUG delivery_increment value END:"+str(__delivery_increment))
        else:
            time.sleep(5)

if __name__ == "__main__":
    def main():
        desdi = ur5_control()
        while True:
            desdi.work()
    main()
    

