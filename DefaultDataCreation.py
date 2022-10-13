#sample data
import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",passwd="root",database="hospital_mgmt_sys")
mycursor=mydb.cursor()

#Table Creation:

# Table 1
mycursor.execute("CREATE TABLE IF NOT EXISTS PAT_REG(UID char(6) NOT NULL, DOB date, NAME char(20) NOT NULL, SEX char(1), PH_NO bigint, PWD char(15) NOT NULL);")

# Table 2
mycursor.execute("CREATE TABLE IF NOT EXISTS VACCINATION(V_NAME char(20), QTY int);")

# Table 3
mycursor.execute("CREATE TABLE IF NOT EXISTS ADMIN(UID_D char(6), NAME char(20), DEPT char(20), AVAIL varchar(60), PWD char(15));")

#Table 4
mycursor.execute("CREATE TABLE IF NOT EXISTS CONSULTATION(DOC_VAC char(15), UID_P char(6), CONSUL_DATETIME datetime, DIAGNOSIS varchar(100), PRESCRIPTION varchar(200));")

#PAT_REG
sql1 = "INSERT INTO PAT_REG(UID, DOB, NAME, SEX, PH_NO, PWD) VALUES (%s,%s,%s,%s,%s,%s)"
val1 = [('P00001','2000-01-01','Aditya Sharma','M','8713340238','Asharma2000'),
        ('P00002','1998-04-02','Ved Agarwal','M','9440682601','vedA98'),
        ('P00003','2003-07-18','Bhavya Kumar','F','9885748735','Bha'),
        ('P00004','1985-10-27','Manoj Pandey','M','9617316394','j@me$2'),
        ('P00005','1977-05-04','Adya Jain','F','9782246217','$S217')]
mycursor.executemany(sql1,val1)
mydb.commit()

#VACCINATION
sql2 = "INSERT INTO VACCINATION(V_NAME, QTY) VALUES (%s,%s)"
val2 = [('BCG','110'),
        ('Tetanus','111'),
        ('Covaxin','120'),
        ('Covishield','163'),
        ('MMR','149')]
mycursor.executemany(sql2,val2)
mydb.commit()

#ADMIN
sql3 = "INSERT INTO ADMIN(UID_D, Name, DEPT, AVAIL, PWD) VALUES (%s,%s,%s,%s,%s)"
val3 = [('A00001', 'admin1', None, None, 'root'),
        ('D00001','Arush Kumar','Oncology','Monday,Tuesday','JohnW602'),
        ('D00002','Varun Khanna','Orthopaedics','Monday,Friday','$Jack442'),
        ('D00003','Stuti Verma','Neurology','Tuesday,Thursday,Saturday','JillDavis103'),
        ('D00004','Raj Bishnoi','Pulmonology','Monday,Wednesday,Friday','bobStokes402'),
        ('D00005','Meena Rathi','Pediatrics','Sunday,Monday,Tuesday,Thursday','Benjamin6029')]
mycursor.executemany(sql3,val3)
mydb.commit()

#consultation
sql4 = "INSERT INTO CONSULTATION(DOC_VAC, UID_P, CONSUL_DATETIME, DIAGNOSIS, PRESCRIPTION) VALUES (%s,%s,%s,%s,%s)"
val4 = [('BCG', 'P00001', '2022-02-01 12:00:00', 'N/A', 'N/A'),
        ('D00002','P00002','2022-02-02 13:00:00','Minor injury to the ligament','Painkiller-Dolo, advised bed rest till recovery', ),
        ('D00003','P00003','2022-02-03 14:00:00','Irregular heartrate, palpitations, showing signs of stroke','Patient admitted to ICU'),
        ('D00005','P00003','2022-02-04 11:00:00','Mild fever with cold and cough, tonsils inflammed','Fluticone CT nasal spray, Honitus cough syrup, Dolo 350')]
mycursor.executemany(sql4,val4)
mydb.commit()

# After executing this file, start executing main.py directly
