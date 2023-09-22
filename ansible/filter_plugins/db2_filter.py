#!/usr/bin/python3
"""Works as a filter for the output of sql-scripts run with db2 -tvf
   Does not work with select statements  
    Raises:
        AttributeError:  db2_sql_code_filter needs a valid SQLCODE 

    Returns:
        dict: Contains the stripped down output
    
    Usage: 
    
    Can be used as a filter in any ansible-script which uses the "shell"-module and "db2 -tvf" 
    Does not work with SELECT-Statements, but with all kinds of DDL and DML-Errors. 
    """

import re, time


class FilterModule():

    def filters(self):

        return {
            'db2err_filter': self.db2err_filter,
            'sqlcode_filter': self.sqlcode_filter,
            'sqlerrors_list_grouped': self.sqlerrors_list_grouped,
            "sqlerrors_list_flat": self.sqlerrors_list_flat,
            "allerrors_list_grouped": self.allerrors_list_grouped,
            "allerrors_list_flat": self.allerrors_list_flat,
            "ylist2db2": self.ylist2db2,
            "sizeandtime": self.sizeandtime,
            "epoch2ctime": self.epoch2ctime
            
            
            
        }

    def epoch2ctime(self, epochtime):
        return time.strftime(("%Y-%m-%d %H:%M:%S"),time.localtime(epochtime))

    def sizeandtime(self,  ansible_stat, hostname):
        return f"NMCHECK; { hostname };{ ansible_stat['stat']['size'] };{ self.epoch2ctime(ansible_stat['stat']['mtime'])}"
        
    
    def ylist2db2(self, yaml_list ):
        return "(" + ",".join(["'" + x + "'" for x in yaml_list ]) + ")"
        
    def db2err_filter(self, shell_registered_var):
        scanner = DDLScanner(shell_registered_var)
        return scanner.errors

    def sqlcode_filter(self, shell_registered_var, sql_error):
        scanner = DDLScannerFiltered(shell_registered_var, sql_error)
        # print(scanner.failed_list)
        return scanner.filtered_errors

    def sqlerrors_list_grouped(self, shell_registerd_var, sql_error):
        scanner = DDLScannerFiltered(shell_registerd_var, sql_error)
        return scanner.failed_stmts

    def sqlerrors_list_flat(self, shell_registered_var, sql_error):
        scanner = DDLScannerFiltered(shell_registered_var, sql_error)
        return scanner.failed_list

    def allerrors_list_grouped(self, shell_registered_var):
        scanner = DDLScanner(shell_registered_var)
        return scanner.failed_stmts

    def allerrors_list_flat(self, shell_registered_var):
        scanner = DDLScanner(shell_registered_var)
        return scanner.failed_list


class DDLScanner:

    def __init__(self, shell_result):
        self._failed_stmts = dict()
        self._shell_result = shell_result

        # print(shell_result['stdout_lines'])
        # exit()
        # print(type(self._shell_result))
        okpattern = "^DB2.{4}I"
        failpattern = "^DB2.{4}E"
        sqlpattern = "^SQL.{5}."
        ok_count = 0
        fail_count = 0
        Result = {}
        Failed = {}
        stdout = self._shell_result['stdout_lines']

        for index, line in enumerate(stdout):
            okmatch = re.match(okpattern, line)
            failmatch = re.match(failpattern, line)
            if okmatch:
                ok_count += 1
            elif failmatch:
                fail_count += 1
                #start_count = index
                ende = index + 2
                sql_line = stdout[index-1]
                err_line = stdout[ende]
                err_lines = stdout[ende:ende+2]
                sqlmatch = re.match(sqlpattern, err_line)
                sqlerr = sqlmatch.group().strip()

                if sqlerr not in Failed:
                    Failed[sqlerr] = {}
                    sqlerr_count = 1
                   # Failed[sqlerr]["total"] = sqlerr_count

                else:
                    sqlerr_count += 1
                   # Failed[sqlerr]["total"] = sqlerr_count

                if sql_line not in Failed[sqlerr]:
                    Failed[sqlerr][sql_line] = []

                if sqlerr not in self._failed_stmts.keys():
                    self._failed_stmts[sqlerr] = []
                    self._failed_stmts[sqlerr].append(sql_line)
                    # print(self._failed_stmts)
                    # print(type(self._failed_stmts[sqlerr]))
                else:
                    self._failed_stmts[sqlerr].append(sql_line)

                Failed[sqlerr][sql_line].append(err_lines)
        self._failed_list = [value for (
            key, value) in self._failed_stmts.items()]

        Result['ok_count'] = ok_count
        Result['fail_count'] = fail_count
        Result['sqlerrors'] = Failed
        try:
            Result['rc'] = self._shell_result['rc']
        except:
            pass
        self._errors = Result['sqlerrors']

    @property
    def shell_result(self):
        return self._shell_result

    @property
    def errors(self):
        return self._errors

    @property
    def failed_stmts(self):
        return self._failed_stmts

    @property
    def failed_list(self):
        tmplist = []
        for value in self._failed_list:
            tmplist.extend(value)

        return tmplist


class DDLScannerFiltered(DDLScanner):

    def __init__(self, shell_result, sql_error):
        self._sql_error = validateSQLCODE(sql_error)
        super().__init__(shell_result)
        self._filtered_errors = {key: value for (
            key, value) in self.errors.items() if key == sql_error}
        self._failed_list = [value for (
            key, value) in self._filtered_errors.items() if key != 'total']

    @property
    def sql_error(self):
        return self._sql_error

    @property
    def filtered_errors(self):
        return self._filtered_errors

    @property
    def failed_stmts(self):
        self._failed_stmts = [
            key for key in self._filtered_errors[self.sql_error].keys() if key != "total"]
        return self._failed_stmts

    @property
    def failed_list(self):

        tmplist = []
        for value in self._failed_list:
            tmplist.extend(value)
        print(type(tmplist))
        return tmplist


def validateSQLCODE(sql_error):

    sqlpattern = "^SQL.{5}$"
    sql_error = sql_error.strip()

    if not re.match(sqlpattern, sql_error):
        raise AttributeError("Wrong SQLCODE: " + sql_error)
    else:
        return sql_error
