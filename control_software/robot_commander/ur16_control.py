import time, threading
from RobotConnectionManager import RobotConnectionManager
from firebase_manager import database_manager

#TODO handle incoming messages
class ur16_control():
    def __init__(self):
        self.fm = database_manager()
        self.rcm = RobotConnectionManager(ip="192.168.100.10", port=1201, buffer=4069)
        #TODO uncomment self.rcm.begin(mode="server")
    
    def begin(self):
        self.fm.start_listener()
        product_num = self.fm.return_product_ammount()

        while True:
            #Get all products from orderList
            products = self.fm.ref.child("orderList").get()
            #Check status from each Product
            for product in products:
                if products[product]["status"] == "loading":
                    print(f"{product} loading")
                    #Translate packet name for the robot
                    packet_name = self.translate_product_name(products[product]["item"])
                    if packet_name != 0:
                        #Send translated packet name for the robot
                        #TODO uncomment self.rcm.send_str(packet_name)
                        print(f"Load one {packet_name}")  #TODO remove this
            print("Nothing to load yet")
            time.sleep(10)
    
    @staticmethod
    def translate_product_name(db_name) -> str:
        #I did not do this in python 3.10 so no match here
        if db_name == "Banana": return "paketti1"
        elif db_name == "Cheese": return "paketti2"
        elif db_name == "Milk": return "paketti3"
        else: return 1  #error

if __name__ == "__main__":
    def main():
        c = ur16_control()
        c.begin()
    main()
