import unittest
import configparser
import pandas as pd
import numpy as np

import pyisql as ps

# config provides database access parameters - replace with your local information
CONFIG_FILE_NAME = "../../../OpenSource.secret/pyisql/db.cfg"

class TestPyISQL(unittest.TestCase):

    def setUp(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(CONFIG_FILE_NAME)
        self.instance = ps.PyISQL(self.cfg['db']['host'], self.cfg['db']['user'], self.cfg['db']['pwd'])

    def test_one_row_one_unnamed_column_query(self):
        sql = "select 1"
        df = self.instance.exec_query(sql)
        self.assertEqual(len(df), 1, 'expected 1 row')
        self.assertEqual(len(df.columns), 1, 'expected 1 column')

    def test_one_row_one_column_query(self):
        sql = "select 1 as col1"
        df = self.instance.exec_query(sql)
        self.assertEqual(len(df), 1, 'expected 1 row')
        self.assertEqual(len(df.columns), 1, 'expected 1 column')
        self.assertEqual(df.columns[0], 'col1', 'expected column name col1')
        self.assertEqual(df['col1'][0], 1, 'expected field value 1')

    def test_zero_rows_one_column_query(self):
        sql = "select 1 as col1 where 1=2"
        df = self.instance.exec_query(sql)
        self.assertEqual(len(df), 0, 'expected 0 rows')
        self.assertEqual(len(df.columns), 1, 'expected 1 column')
        self.assertEqual(df.columns[0], 'col1', 'expected column name col1')

    def test_one_row_two_column_query(self):
        sql = "select 1 as col1, 'a' as col2"
        df = self.instance.exec_query(sql)
        self.assertEqual(len(df), 1, 'expected 1 rows')
        self.assertEqual(len(df.columns), 2, 'expected 2 columns')
        self.assertEqual(df.columns[0], 'col1', 'expected column name col1')
        self.assertEqual(df.columns[1], 'col2', 'expected column name col2')
        self.assertEqual(df['col1'][0], 1, 'expected field value 1')
        self.assertEqual(df['col2'][0], 'a', 'expected field value 1')

    def test_empty_query(self):
        sql = ""
        df = self.instance.exec_query(sql)
        self.assertEqual(len(df), 0, 'expected 0 row')

    def test_syntax_error_query(self):
        sql = "_elect 1"
        with self.assertRaises(ValueError):
            self.instance.exec_query(sql)

    def test_incorrect_host(self):
        sql = "select 1"
        self.instance.host = "non-existent-host"
        with self.assertRaises(ValueError):
            self.instance.exec_query(sql)

    def test_incorrect_user(self):
        sql = "select 1"
        self.instance.user = "non-existent-user"
        with self.assertRaises(ValueError):
            self.instance.exec_query(sql)

    def test_incorrect_password(self):
        sql = "select 1"
        self.instance.pwd = "incorrect-password"
        with self.assertRaises(ValueError):
            self.instance.exec_query(sql)

    def test_three_rows_two_columns(self):
        sql = """
create table #temp (recid int,  name varchar(10))
insert into #temp values(1, 'one')
insert into #temp values(2, 'two')
insert into #temp values(3, 'three')
select * from #temp
            """
        df = self.instance.exec_query(sql)
        self.assertEqual(len(df), 3, 'expected 3 rows')

    def test_three_rows_two_columns_with_nulls(self):
        sql = """
create table #temp (recid int null,  name varchar(10) null)
insert into #temp values(1, null)
insert into #temp values(null, 'two')
insert into #temp values(3, 'three')
select * from #temp
            """
        df = self.instance.exec_query(sql)
        self.assertEqual(len(df), 3, 'expected 3 rows')
        self.assertTrue(np.isnan(df.name[0]), 'expected NaN')
        self.assertTrue(np.isnan(df.recid[1]), 'expected NaN')

if __name__ == "__main__":
    unittest.main()
