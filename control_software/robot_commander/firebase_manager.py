import firebase_admin, json, threading, time, re
from firebase_admin import db

class database_manager():
	def __init__(self):
		self.__cred_obj = firebase_admin.credentials.Certificate(json.load(open(__file__.replace("firebase_manager.py", "key.json"))))
		self.__default_app = firebase_admin.initialize_app(self.__cred_obj, {
			'databaseURL':'https://ur16-dev-default-rtdb.europe-west1.firebasedatabase.app'
		})
		self.ref = db.reference("/")

	def recreate(self):
		#with open("firebase/current_order.json", "r") as f:
		with open(__file__.replace("firebase_manager.py", "current_order.json")) as f:
			contents = json.load(f)
		print(contents)
		self.ref.child("CurrentOrder").set(contents)

	# Creates json file backup of the database, useful in testing
	def database_back_up_create(self):
		backUpQuery = self.ref.get()
		backUpQuery = re.sub("\'", "\"", str(backUpQuery))
		f = open("databaseBackUp.json", "w")
		f.write(str(backUpQuery))
		f = open("databaseBackUp.json","r")
		print(f.read())

	def create_process_table(self):
		current_order = self.ref.child("CurrentOrder").get()
		db_product_number = 0
		#process each product
		for product in current_order:
			#get the number of items in product
			number_of_items = int(current_order[product]["quantity"])
			#add correct number of products to db/orderList
			for db_product in range(number_of_items):
				update_data = {
					"item": product,
					"gopigo": "0",
					"status": "ordered"
				}
				self.ref.child(f"orderList/product{db_product_number}").update(update_data)
				db_product_number += 1
	
	def listen_callback(self, event):
		if event.data != "0":
			self.create_process_table()
		
	def rpa_callback(self, event) -> int:	#Yo! not used rn.
		'''Return the number of products in orderList table'''
		if event.data != "0":
			num = len(event.data)
			print(num)

	def start_listener(self):
		#TODO explain the line below
		try:
			listen_thread = threading.Thread(self.ref.child("CurrentOrder").listen(self.listen_callback))
		except:
			pass

	def delete_process_table(self):
		#The point is to set the value of the whole Process table to zero
		self.ref.update({"orderList": "0"})

	def return_product_ammount(self):
		#self.ref.child("orderList").listen(self.rpa_callback) #wip
		while True:
			content = self.ref.child("orderList").get()
			if content != "0":
				return int(len(content))
			time.sleep(10)

	def delete_currentOrder_table(self):
		#The point is to set the value of the whole currentOrder table to one
		self.ref.update({"CurrentOrder": "0"})

class Main():
	@staticmethod
	def main():
		c = database_manager()
		# c.ref.update({"CurrentOrder": "0"})
		# c.start_listener()
		# time.sleep(20)
		c.recreate()

if __name__ == "__main__":
	c = Main()
	c.main()