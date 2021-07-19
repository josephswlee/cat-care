# Cat Care Application

### Description

Cat record keeping application created to record and track cat's immunization record and medical information.

![image](https://user-images.githubusercontent.com/71230815/126091680-03a5a550-d3c4-4ac8-a580-903e6aa0fae8.png)


### Set up Python Virtual Environment

virtualenv
```
pip install virtualenv
```
Create virtualenv directory
```
virtualenv venv
```
Activate
```
venv\Scripts\activate
```
Deactivate
```
deactivate
```

### Installation

PyQt5
```
pip install PyQt5
```
PyQt5 tools
```
pip install pyqt5-tools
```
Qt Designer
```
pip install PyQt5Designer
```
SQlite3
```
https://www.sqlite.org/download.html
```

### Current implementation

1. Built-in database using SQLite3 

2. Separated Homescreen, Cat Info Screen, Cat Vaccine Screen, Cat Items Inventory Screen using Qt Designer.

3. Displaying database tables to corresponding QTableWidget of the screen.

4. Adding elements to database then refresh the table.

5. Deleting a row of table from database using unique ID number of element.

### Implementation Required

1. Deleting a row does not refresh the Table Widget.

2. Updating a row.

3. Having a history log to see every elements added or deleted previously. (Duplicate a table to replicate all the changes except delete)

4. Better way of deleting a row. (Maybe using a row selected)

5. Make the number of rows shown in the Table Widget dynamically. 

6. Improve database display. (Instead of using excel format)

7. Medical history tracker table and display.
