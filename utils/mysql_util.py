#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
"""
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""

import pymysql
from pymysql import IntegrityError, DatabaseError
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB

import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MySQL:
    """
    MYSQL数据库对象，负责产生数据库连接，此类中的连接采用连接池实现
    """
    __pool = None

    def __init__(self, host, port, user, password, db="lps"):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

        # 使用连接池
        self.__pool = PooledDB(creator=pymysql,
                               mincached=5, maxcached=50,
                               host=self.host, port=self.port,
                               user=self.user, passwd=self.password,
                               db=self.db, charset='utf8mb4',
                               cursorclass=DictCursor,
                               autocommit=True)  # 设置自动提交模式为True

    def get_conn(self):
        """
        从连接池中获取连接对象
        """
        return self.__pool.connection()

    def get_all(self, sql, param=None):
        """
        执行查询，并取出所有结果集
        """
        conn = None
        cursor = None
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            if param is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, param)
            result = cursor.fetchall()
            return result if result else False
        except Exception as e:
            logger.error(f"数据库查询错误: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def select_one(self, condition):
        """
        @summary: 执行查询，并取出第一条
        @return: result dict 查询到的结果字典
        :param condition: 查询条件
        """
        conn = None
        cursor = None
        result = {}
        try:
            conn = self.get_conn()
            cursor = conn.cursor()

            cursor.execute(condition)
            row = cursor.fetchone()

            if row:
                result = {'code': '0', 'message': '执行单条查询操作成功', 'data': row}
            else:
                result = {'code': '0', 'message': '查询结果为空', 'data': None}

        except DatabaseError as e:
            conn.rollback()
            result = {'code': '1002', 'message': '数据库操作异常', 'data': str(e)}
        except Exception as e:
            conn.rollback()
            result = {'code': '9999', 'message': '执行单条查询异常', 'data': str(e)}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result

    def exe_multi(self, sql_list):
        print(f"exe_multi===={sql_list}")
        res_list = []
        conn = None
        cursor = None
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            for sql in sql_list:
                print(f"exe_multi::sql::\n{sql}")
                res = cursor.execute(sql)
                if res > 0:
                    res_list.append(res)
            conn.commit()
            result = {'code': '0', 'message': '执行批操作成功', 'data': res_list}
        except Exception as e:
            if conn:
                conn.rollback()
            result = {'code': '9999', 'message': '执行批量操作异常', 'data': res_list}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result

    def exec_one(self, sql, params=None):
        logger.info(f"exec_one SQL: {sql} - Params: {params}")

        conn = None
        cursor = None
        result = {}
        try:
            conn = self.get_conn()
            cursor = conn.cursor()

            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

            conn.commit()
            result = {'code': '0', 'message': '执行操作成功'}
        except IntegrityError as e:
            conn.rollback()
            result = {'code': '1001', 'message': '违反唯一约束，无法执行操作'}
            logger.error(f"IntegrityError: {e}")
        except DatabaseError as e:
            conn.rollback()
            result = {'code': '1002', 'message': '数据库操作异常', 'data': str(e)}
            logger.error(f"DatabaseError: {e}")
        except Exception as e:
            conn.rollback()
            result = {'code': '9999', 'message': '执行操作异常', 'data': str(e)}
            logger.error(f"Exception: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        logger.info(f"exec_one Result: {result}")
        return result

    def insert_many(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()
