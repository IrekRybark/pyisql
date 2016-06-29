import os
import pandas as pd
import datetime as dt


class PyISQL:
    """ Quick and dirty wrapper for Sybase isql command line application.
        Loads the resultset into Pandas DataFrame.
    """

    def __init__(self, host, user, pwd, sql_file_name='select.sql', out_file_name='select_out.txt'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.sql_file_name = sql_file_name
        self.out_file_name = out_file_name
        self.exec_beg_time = None
        self.exec_end_time = None
    
#    def __del__(self):
#        os.remove(self.sql_file_name)
#        os.remove(self.out_file_name)

    def exec_query(self, sql):

        self._make_sql_file(sql, self.sql_file_name)

        isql_conn = self._isql_param_connect(self.host, self.user, self.pwd)
        isql_files = self._isql_param_files(self.sql_file_name, self.out_file_name)
        
        self.exec_beg_time = dt.datetime.now()
        self._isql_exec(isql_conn, isql_files)
        self.exec_end_time = dt.datetime.now()
        
        return self._isql_output_to_df(self.out_file_name)

    def _make_sql(self, sql):
        return "\n".join([
            """
set nocount on
go
set proc_return_status off
go
            """, sql, "go"])

    def _make_sql_file(self, sql, sql_file_name):
        lines = self._make_sql(sql)
        with open(sql_file_name, 'w') as sql_file:
            sql_file.write("".join(lines))    

    def _isql_param_connect(self, host, user, pwd):
        return "-S {} -U {} -P {}".format(host, user, pwd)

    def _isql_param_files(self, sql_file, out_file):
        return "-i {} -o {}".format(sql_file, out_file)

    def _isql_exec(self, connect_str, file_str):
        try:
            os.remove(file_str)
        except OSError:  # in case file does not exist
            pass
        return os.system("isql {} -n {}".format(connect_str, file_str))

    def _isql_output_to_df(self, file_name):

        with open(file_name) as txt_file:
            # read only the beginning of the file: column names and dashes corresponding to column widths
            columns = txt_file.readline()
            sizes = txt_file.readline()
            # count the rest of the lines
            row_count = sum(1 for line in txt_file)
            line_count = row_count + 2

        colnames = []
        df = None
        if line_count >= 2:
            # check if we have header and data separator line, which consist of dashes (-) and spaces
            sep = "".join(sizes.split())
            if sep != '-' * len(sep):  # looks like an error message
                err_msg = ''
                with open(file_name) as text_file:
                    for num, line in enumerate(text_file):
                        err_msg += line
                        if num >= 10:
                            break  # don't go crazy with message length
                    raise ValueError(''.join(['Error processing resultset. [', err_msg, ']']))

            colnames = list(filter(None, columns.split(" ")))
            colnames = colnames[0:len(colnames)-1]  # remove last element, which is \n

            s = sizes.split(" ")
            s = s[1:len(s)-1]  # drop the first and the last elements, which are 0 and 1 respectively
            colwidths = list(map(lambda x: len(x) + 1, s))  # +1 to accommodate spaces between the fields
            if row_count > 0:
                with open(file_name) as output_file:
                    df =  pd.read_fwf(output_file, widths=colwidths, skiprows=2, names=colnames)

        if df is not None:
            return df
        else:
            return pd.DataFrame(columns=colnames)  # empty dataframe


def main():
    pass
  
if __name__ == "__main__":
    main()
