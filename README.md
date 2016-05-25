# PyISQL

Quick and dirty wrapper for Sybase isql command line application.
The current implementation loads the resultset into Pandas DataFrame

## 1. Purpose

The class purpose is to provide a wrapper for Sybase isql command line tool.

## 2. How it works

The class assembles a command by providing database connection parameters (host, user, password) and executes provided
SQL script.  The text output is then parsed and loaded into Pandas DataFrame.
To achieve consistent format of the output, several Sybase-specific 'set' directives are added to SQL. 

## 3. Example

`import pandas as pd`  
`from pyisql import PyISQL`   
   
`sql =  # assemble SQL query`  
`"""`  
`SELECT year, model, color, sum(sales)`     
`FROM sales_tab`  
`GROUP BY ROLLUP (year, model, color);`  
`"""`
    
`pyisql = PyISQL('db_host', 'db_user', 'db_pwd')  # replace parameters accordingly`    
`sales_df = pyisql.exec_query(sql)`  
`sales_df.describe()`  
  
## 4. Configuration

### 4.1 Requirements

Sybase OpenClient with isql application.

## 5. Similar work

## 6. Open issues
* P2: the application does not delete temporary SQL file and the temporary isql output text file  
* P2: the application does not handle multiple resultsets  