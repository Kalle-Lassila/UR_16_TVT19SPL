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
        self.__robot_con_man.begin(mode="server")

    def work(self):
        while True:    
            # get amount of products to unload for the current order from the database
            self.__packetCount = self.__db_man.return_product_ammount()
            print(self.__packetCount)
            __delivery_increment = 0

            #if there are workable orders initiate the robot, otherwise wait a while and check the database again
            if self.__packetCount != 0:
                # Tell UR5 to keep working until delivery is completed
                while __delivery_increment <= self.__packetCount:
                    time.sleep(2) #TODO sleep before sending
                    if __delivery_increment == 0:
                        # Tell robot that the order is complete
                        self.__robot_con_man.send_str("first")
                        print("DEBUG first")
                    else:
                        self.__robot_con_man.send_str("work")
                        print("DEBUG work")

                     #Wait for robot to indicate it has completed one packet move cycle
                    if self.__robot_con_man.blockking_get_recv_byte_buffer() == "1":
                        __delivery_increment = __delivery_increment + 1
                        #TODO REMOVE debug print below
                        print("DEBUG delivery completed, progress:"+str(__delivery_increment))
                    else:
                        #TODO change for the software to lock up in this if statement if the robot end goes haywire
                        print("DEBUG delivery not completed, progress:"+str(__delivery_increment))
        
                # When robot is done with the current order set orderList table from database to indicate order being complete
                # Also do the same for "currentOrder" table
                self.__db_man.delete_process_table()
                self.__db_man.delete_currentOrder_table()    
                print("DEBUG database remove")
        
            else:
                print("DEBUG orderList empty")
                time.sleep(10)
            
if __name__ == "__main__":
    def main():
        desdi = ur5_control()
        desdi.work()
    main()
    

