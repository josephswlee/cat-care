import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from SqliteHelper import *
import os.path

import sqlite3

# Create database
dbTables = []
tableList = ["Choose Table"]
foreignKeys = {}
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('petData.db')

def createDB():
	if not db.open():
		msg = QMessageBox()
		msg.setText("Error occurred during creating Database")
		retval = msg.exec_()
		return False
	query = QSqlQuery()

	query.exec_("PRAGMA foreign_keys = ON;")

	#Creating tables
	#Cat basic information table
	catInfo = """CREATE TABLE Cat_Info (
				 Cat_ID INTEGER PRIMARY KEY AUTOINCREMENT,
				 Cat_Name CHAR(50) NOT NULL UNIQUE,
				 Cat_Age INTEGER,
				 Cat_Weight INTEGER
				)"""
	dbTables.append(["Cat_Info", catInfo])
	tableList.append("Cat_Info")

	#Cat vaccination information table
	catVac = """CREATE TABLE Cat_Vaccine (
				CatVac_ID INTEGER PRIMARY KEY AUTOINCREMENT,
				Cat_Vac_Name CHAR(50) NOT NULL,
				Cat_Vac_Date DATE,
				Cat_Vac_Description TEXT,
				Cat_ID INTEGER,
				FOREIGN KEY (Cat_ID) REFERENCES CatInfo(Cat_ID)
				)"""
	dbTables.append(["Cat_Vaccine", catVac])
	tableList.append("Cat_Vaccine")
	foreignKeys["Cat_Vaccine"] = [[1, "CatInfo", "Cat_ID", "Cat_Name"]]

	#Cat item inventory table
	inventory = """CREATE TABLE Inventory (
				   Inv_ID INTEGER PRIMARY KEY AUTOINCREMENT,
				   Inv_Name TEXT NOT NULL UNIQUE,
				   Inv_Description TEXT,
				   Quantity CHAR(50) NOT NULL,
				   Cat_ID INTEGER,
				   FOREIGN KEY (Cat_ID) REFERENCES CatInfo(Cat_ID)
				   )"""
	dbTables.append(["Inventory", inventory])
	tableList.append("Inventory")
	foreignKeys["Inventory"] = [[1, "CatInfo", "Cat_ID", "Cat_Name"]]

	for i in range(len(dbTables)):
		if dbTables[i][0] not in db.tables():
			query.exec(dbTables[i][1])
	print(query.exec("PRAGMA FOREIGN_KEY_LIST(\"TESTING\")"))
	print("this is pk",db.primaryIndex("catInfo").name())

	return True


#loading welcome screen
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomeScreen.ui", self)
        qpixmap = QPixmap('kittens-bg.jpg')
        self.bgPicLabel.setPixmap(qpixmap)
        
#More features to implement
#1.Update existing row 2.Refresh app once database gets editted (so app doesn't have to be restarted)
#3.Home Screen gets picture and more feature (clock/weather display etc)
#4.Improve database display (not excel formal and include displaying picture of cat)

#Problems noticed
#PK ID number does not come back even after I delete item
#currently adding to Cat_Info will make Cat_ID start from 6 not 4 
class MyCatScreen(QDialog):
	def __init__(self):
		super(MyCatScreen, self).__init__()
		loadUi("myCatScreen.ui", self)

		self.tableWidget.setColumnWidth(0,169)
		self.tableWidget.setColumnWidth(1,169)
		self.tableWidget.setColumnWidth(2,169)
		self.tableWidget.setColumnWidth(3,169)
		self.tableWidget.setHorizontalHeaderLabels(["Cat ID", "Cat Name", "Cat Age", "Cat Weight"])
		self.loaddata()

		self.catAdd.clicked.connect(self.addToDB)
		self.catDelete.clicked.connect(self.deleteFromtDB)

	def loaddata(self):
		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		# global cursor
		# cursor = connection.cursor()
		sqlquery = 'SELECT * FROM Cat_Info'

		#numRow = cur.execute("SELECT count(Cat_ID) FROM Cat_Info")
		#print(numRow)

		#Attention needed!
		#This needs to be changed to allocate dynamically
		self.tableWidget.setRowCount(10)
		tableRow = 0
		for row in cur.execute(sqlquery):
			print(row)
			self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
			self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
			self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
			self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
			tableRow+=1

	def addToDB(self):
		name = self.catName.text()
		age = self.catAge.text()
		weight = self.catWeight.text()
		#newCat = (name, str(age), str(weight))

		print(name + " " + age + " " + weight + " added to the database")

		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		sqlquery = 'INSERT into Cat_Info (Cat_Name, Cat_Age, Cat_Weight) VALUES(?,?,?)'
		cur.execute(sqlquery, (name, age, weight))
		connection.commit()
		self.loaddata()

		#for row in cur.execute('SELECT * FROM Cat_Info'):
		#print(row)

		#cur.execute('INSERT into Cat_Info (Cat_Name) VALUES(?)', (name))
		#cur.execute('INSERT into Cat_Info (Cat_Age) VALUES(?)', (age))
		#cur.execute('INSERT into Cat_Info (Cat_Weight) VALUES(?)', (weight))

	def deleteFromtDB(self):

		rowNum = self.catRow.text()

		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		sqlquery = 'DELETE FROM Cat_Info WHERE Cat_ID in (?)'
		cur.execute(sqlquery, [rowNum])
		connection.commit()
		self.loaddata()

class CatVacScreen(QDialog):
	def __init__(self):
		super(CatVacScreen, self).__init__()
		loadUi("CatVacScreen.ui", self)
		self.tableWidget.setColumnWidth(0,45)
		self.tableWidget.setColumnWidth(1,125)
		self.tableWidget.setColumnWidth(2,80)
		self.tableWidget.setColumnWidth(3,380)
		self.tableWidget.setColumnWidth(4,45)
		#self.tableWidget.setColumnWidth(4,50)
		self.tableWidget.setHorizontalHeaderLabels(["Vac ID", "Vaccine Name", "Date Received", "Description", "Cat ID"])
		self.loaddata()

		self.vacAdd.clicked.connect(self.addToDB)
		self.vacDelete.clicked.connect(self.deleteFromtDB)

	def loaddata(self):
		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		# global cursor
		# cursor = connection.cursor()
		sqlquery = 'SELECT * FROM Cat_Vaccine'

		#numRow = cur.execute("SELECT count(Cat_ID) FROM Cat_Info")
		#print(numRow)

		#Attention needed!
		#This needs to be changed to allocate dynamically
		self.tableWidget.setRowCount(10)
		tableRow = 0
		for row in cur.execute(sqlquery):
			print(row)
			self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
			self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
			self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
			self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
			self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
			tableRow+=1

	def addToDB(self):
		name = self.vacName.text()
		date = self.vacDate.text()
		descript = self.vacDescription.text()
		catID = self.vacCatID.text()
		#newCat = (name, str(age), str(weight))

		print(name + " " + date + " " + descript + " " + catID + " added to the database")

		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		sqlquery = 'INSERT into Cat_Vaccine (Cat_Vac_Name, Cat_Vac_Date, Cat_Vac_Description, Cat_ID) VALUES(?,?,?,?)'
		cur.execute(sqlquery, (name, date, descript, catID))
		connection.commit()

	def deleteFromtDB(self):

		rowNum = self.vacRow.text()

		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		sqlquery = 'DELETE FROM Cat_Vaccine WHERE CatVac_ID in (?)'
		cur.execute(sqlquery, [rowNum])
		connection.commit()


class InventoryScreen(QDialog):
	def __init__(self):
		super(InventoryScreen, self).__init__()
		loadUi("InventoryScreen.ui", self)
		self.tableWidget.setColumnWidth(0,45)
		self.tableWidget.setColumnWidth(1,110)
		self.tableWidget.setColumnWidth(2,405)
		self.tableWidget.setColumnWidth(3,70)
		self.tableWidget.setColumnWidth(4,45)
		#self.tableWidget.setColumnWidth(4,50)
		self.tableWidget.setHorizontalHeaderLabels(["Inv ID", "Inventory Name", "Description", "Quantity", "Cat ID"])
		self.loaddata()

		self.invAdd.clicked.connect(self.addToDB)
		self.invDelete.clicked.connect(self.deleteFromtDB)

	def loaddata(self):
		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		# global cursor
		# cursor = connection.cursor()
		sqlquery = 'SELECT * FROM Inventory'

		#numRow = cur.execute("SELECT count(Cat_ID) FROM Cat_Info")
		#print(numRow)

		#Attention needed!
		#This needs to be changed to allocate dynamically
		self.tableWidget.setRowCount(10)
		tableRow = 0
		for row in cur.execute(sqlquery):
			print(row)
			self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
			self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
			self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
			self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
			self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
			tableRow+=1

	def addToDB(self):
		name = self.invName.text()
		descript = self.invDescription.text()
		quant = self.invQuantity.text()
		catID = self.invCatID.text()
		#newCat = (name, str(age), str(weight))

		print(name + " " + descript + " " + quant + " " + catID + " added to the database")

		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		sqlquery = 'INSERT into Inventory (Inv_Name, Inv_Description, Quantity, Cat_ID) VALUES(?,?,?,?)'
		cur.execute(sqlquery, (name, descript, quant, catID))
		connection.commit()
		#self.loaddata()

	def deleteFromtDB(self):

		rowNum = self.invRow.text()

		connection = sqlite3.connect('petData.db')
		cur = connection.cursor()
		sqlquery = 'DELETE FROM Inventory WHERE Inv_ID in (?)'
		cur.execute(sqlquery, [rowNum])
		connection.commit()
		#self.self.loaddata()

#Backup
class MainWindow(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cat Care Application')
        self.welcome_screen = WelcomeScreen()
        self.cat_screen = MyCatScreen()
        self.vac_screen = CatVacScreen()
        self.inv_screen = InventoryScreen()

        self.addWidget(self.welcome_screen)
        self.addWidget(self.cat_screen)
        self.addWidget(self.vac_screen)
        self.addWidget(self.inv_screen)

        self.setFixedWidth(1120)
        self.setFixedHeight(850)

        self.welcome_screen.MyCatLoad.clicked.connect(self.goto_myCat)
        self.welcome_screen.VaccinationLoad.clicked.connect(self.goto_vac)
        self.welcome_screen.InventoryLoad.clicked.connect(self.goto_inv)

        self.cat_screen.MyCatLoad.clicked.connect(self.goto_myCat)
        self.cat_screen.VaccinationLoad.clicked.connect(self.goto_vac)
        self.cat_screen.InventoryLoad.clicked.connect(self.goto_inv)

        self.vac_screen.MyCatLoad.clicked.connect(self.goto_myCat)
        self.vac_screen.VaccinationLoad.clicked.connect(self.goto_vac)
        self.vac_screen.InventoryLoad.clicked.connect(self.goto_inv)

        self.inv_screen.MyCatLoad.clicked.connect(self.goto_myCat)
        self.inv_screen.VaccinationLoad.clicked.connect(self.goto_vac)
        self.inv_screen.InventoryLoad.clicked.connect(self.goto_inv)

        #self.loadData()
        #self.goto_welcome()

    def goto_myCat(self):
        self.setCurrentIndex(self.indexOf(self.cat_screen))

    def goto_vac(self):
    	self.setCurrentIndex(self.indexOf(self.vac_screen))

    def goto_inv(self):
    	self.setCurrentIndex(self.indexOf(self.inv_screen))

# main
def main():
	# Create instance of QApplication
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    try:
        app.exec_()
        #sys.exit(app_exec())
    except:
        print("Exiting gracefully...")

if __name__=='__main__':
	app = QApplication(sys.argv)
	createDB()
	main()