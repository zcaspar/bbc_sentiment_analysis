sqoop import --connect jdbc:mysql://localhost/Assignment 
--username root 
-P 
--split-by Accident_Index
--table accients  
--target-dir /Assignment/accidents4
--hive-import 
--create-hive-table 
--hive-table sqoop_workspace.customers