import time, threading
from RobotConnectionManager import RobotConnectionManager
from firebase_manager import database_manager

#current flow is:
#first start firebase listener, which also creates the orderList table
#checking for db, robot state messages, and replying to robot are all threaded, so 3 threads
#robot asks for car-> answer when db tells us that we have a car waiting to be loaded

class ur16_control():
    def __init__(self):
        self.car_id = None
        self.packet_id = None
        self.this_car_sent = False
        self.this_pkg_sent = False
        self.waiting_car = False
        self.waiting_pkg = False
        self.fm = database_manager()
        #self.rcm = RobotConnectionManager(ip="192.168.100.10", port=1201, buffer=4069)
        self.rcm = RobotConnectionManager(ip="172.16.140.130", port=1201, buffer=4069)
        #threaded so we can keep track of the state constantly. Not strictly necessary as we also control the other side of the connection.
        self.state_thread = threading.Thread(target=self._robot_state_check)
        self.load_thread = threading.Thread(target=self.__load_product)
        #start the RobotConnectionManager
        self.rcm.begin(mode="server")
    
    def begin(self):
        #start the method that creates orderList table from currentOrder
        self.fm.start_listener()
        self.state_thread.start()
        self.load_thread.start()
        #TODO check and remove 3 lines below
        #wait until something is added to the db table
        #don't think the line below is necessary
        #product_num = self.fm.return_product_ammount()

        while True:
            time.sleep(10)
            #Get all products from orderList
            products = self.fm.ref.child("orderList").get()
            #Check status from each Product
            for product in products:
                if products[product]["status"] == "loading":
                    print(f"{product} loading")
                    #Translate packet name for the robot
                    packet_name = self.translate_product_name(products[product]["item"])
                    if packet_name != 0:
                        print(f"Load one {packet_name}")  #TODO remove this
                        self.current_product = product  #to keep track which productX we are dealing with
                        self.car_id = products[product]["gopigo"]
                        self.packet_id = packet_name
                        #self.this_car_loaded = False
            print("Nothing to load yet")
    
    def __load_product(self):
        '''Threaded to continuously send instructions if needed'''
        while True:
            time.sleep(1)
            if self.waiting_car and self.car_id and not self.this_car_sent:
                self.rcm.send_str(self.car_id)
                self.car_id = None
                self.waiting_car = False
                self.this_car_sent = True
            elif self.waiting_pkg and self.packet_id and not self.this_pkg_sent:
                self.rcm.send_str(self.packet_id)
                self.packet_id = None
                self.waiting_pkg = False
                self.this_pkg_sent = True

    def _robot_state_check(self):
        while True:
            time.sleep(1)   #check message interval
            rcv = self.rcm.get_recv_buffer()
            if "Anna auto" in rcv:
                self.waiting_car = True
                self.waiting_pkg = False
            elif "Anna paketti" in rcv:
                self.waiting_pkg = True
                self.waiting_car = False
            #Lastattu message can come at the same time as "Anna auto" so a separate check needs to be in place
            if "Lastattu" in rcv:
                self.fm.ref.child(f"orderList/{self.current_product}").update({"status": "loaded"})
                self.this_pkg_sent = False
                self.this_car_sent = False
            print(rcv)
   
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
