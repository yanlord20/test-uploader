import time
import pymysql
from const.staram.appcfg import *
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB


class Mysql(object):
    __pool = None

    def __init__(self, custom_db=''):
        self._dbname = DBNAME if custom_db == '' else custom_db
        self._conn = Mysql.__getConn(self._dbname)
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn(dbname):
        __pool = Mysql.__pool
        if Mysql.__pool is None:
            success = False
            count = 0
            while not success:
                try:
                    __pool = PooledDB(creator=pymysql, mincached=1, maxcached=50,
                                      host=DBHOST, port=DBPORT,
                                      user=DBUSER, passwd=DBPWD, db=dbname,
                                      use_unicode=True, charset=DBCHARSET, cursorclass=DictCursor)
                    if __pool is not None:
                        success = True
                except pymysql.OperationalError as e:
                    if e.args[0] in (2006, 2013, 2003, 2006):
                        print("DB-CONNECTION ERROR: ", str(e.args[0]) + "-" + str(e.args[1]))
                    else:
                        print("UNKNOWN DB ERROR: ", str(e.args[0]) + "-" + str(e.args[1]))
                    success = False
                    time.sleep(2)
                    if count > 3:
                        raise
                count += 1
        return __pool.connection()

    """
    @:return dictionary of fetched data (IF fetch one), LIST of Dictionary of fetched data (IF Fetch all/many)
    Fetching data from mysql db,

    example usage:

    1. Fetch all:
        mysql.fetch_rows(sql = "SELECT * FROM user where id=%s", 
                        values=(1,), 
                        many=1)

    2. Fetch one:
        mysql.fetch_rows(sql = "SELECT * FROM user where id=%s", 
                         values=(1,))
    """

    def fetch_rows(self, sql, values, many=0, ck="", ttl=TTLDAY):
        if ck == "":
            self._cursor.execute(sql, values)
            retval = self._cursor.fetchone() if many == 0 else self._cursor.fetchall()
        return retval

    """
    @:return integer - last row id 
    Insert new data to mysql db,

    example usage:   
    1. Insert Many

        data1 = dict(msisdn="08129938848",username='you',
                    fullname="my fullname", socmed_id='899928843994',
                    email='mymail@hotmama.com', access_token="jsdhfsd99938393")

        data2 = dict(msisdn="08129932248",username='you 2',
                    fullname="my fullname 2", socmed_id='899922243994',
                    email='mymail2@hotmama.com', access_token="sdfiiibkjeed")

        listdict = [data1, data2]
        mysql.insert_rows("user", listdict)
        mysql.dispose()


    2. Insert One

        data3 = dict(msisdn="081299222248",username='you 4',
                        fullname="my fullname 4", socmed_id='899922243994',
                        email='mymail2@hotmama.com', access_token="sdfiiibkjeed")

        mysql.insert_rows("user", data3)
        mysql.dispose()
    """

    def insert_rows(self, tbl, param, on_duplicate_key_update=False, on_duplicate_key_update_condition=""):
        ct = 0
        setcol = ""
        lv = ""
        isMany = False
        if isinstance(param, list) or isinstance(param, tuple):
            isMany = True
            listtuple = list()
            for p in param:
                cts = 0
                vals = list()
                for key, val in p.items():
                    key = self.__sanitize_column(key)
                    vals.append(val)
                    if ct == 0:
                        sep = "" if cts == (len(p.items()) - 1) else ","
                        setcol += key + sep
                        lv += "%s" + sep
                    cts += 1
                listtuple.append(tuple(vals))
                ct += 1
        elif isinstance(param, dict):
            vals = list()
            for key, val in param.items():
                key = self.__sanitize_column(key)
                vals.append(val)
                sep = "" if ct == (len(param.items()) - 1) else ","
                setcol += key + sep
                lv += "%s" + sep
                ct += 1
            listtuple = tuple(vals)
        else:
            raise Exception('SQL INSERT err: Wrong data type set in SECOND parameter')

        sql = "INSERT into " + tbl + " " + "(" + setcol + ")" + " VALUES " + "(" + lv + ")"
        if on_duplicate_key_update and on_duplicate_key_update_condition:
            sql += " " + "ON DUPLICATE KEY UPDATE" + " " + on_duplicate_key_update_condition
        if isMany:
            count = self._cursor.executemany(sql, listtuple)
        else:
            count = self._cursor.execute(sql, listtuple)

        try:
            res = self._cursor.lastrowid
        except:
            res = self._conn.insert_id()
        return res

    """
    @:return integer - number of row updated (1)
    Update data to mysql db,

    example usage:

        dictset = dict(username='THIS you 4', fullname="THIS my fullname 4")
        dictwhere = dict(email='mymail4@hotmama.com', msisdn="08129932248")

        mysql.update_rows("user", dictset, dictwhere)

    """

    def update_rows(self, tbl, dictset, dictwhere):
        setval = ""
        lv = ""
        if isinstance(dictset, dict):
            ct = 0
            vals = list()
            for key, val in dictset.items():
                key = self.__sanitize_column(key)
                vals.append(val)
                sep = " " if ct == (len(dictset.items()) - 1) else ", "
                setval += key + "=%s" + sep
                ct += 1
            listtuple_ds = tuple(vals)
        else:
            raise Exception('SQL UPDATE err: Wrong data type set in FIRST parameter')

        if isinstance(dictwhere, dict):
            ct = 0
            vals = list()
            for key, val in dictwhere.items():
                key = self.__sanitize_column(key)
                vals.append(val)
                sep = " " if ct == (len(dictwhere.items()) - 1) else " AND "
                lv += key + "=%s" + sep
                ct += 1
            listtuple_dw = tuple(vals)
        else:
            raise Exception('SQL UPDATE err: Wrong data type set in SECOND parameter')

        thistuple = listtuple_ds + listtuple_dw
        sql = "UPDATE " + tbl + " SET " + setval + " WHERE " + lv
        return self.__query(sql, thistuple)

    def custom_update(self, sql, param=None):
        count = self._cursor.execute(sql, param)
        return count

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def __getInsertId(self):
        """
        :
        :return:
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def begin(self):
        """
        :keyword: Open a transaction
        :return: None
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        :keyword: Closing a transaction
        :param option: commit or rollback
        :return:
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        :keyword: Release connection pool resource
        :param isEnd: 1 or 0
        :return:
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')

    def closing(self):
        """
        Closing a transaction
        :return:
        """
        self._cursor.close()
        self._conn.close()

    def __sanitize_column(self, key):
        if key == "to":
            ret = "`to`"
        elif key == "status":
            ret = "`status`"
        elif key == "type":
            ret = "`type`"
        elif key == "comment":
            ret = "`comment`"
        else:
            ret = key
        return ret
