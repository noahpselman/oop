

from src.Logging.Logger import Logger
from src.db_conf import db_conf
import psycopg2 as pg
from psycopg2.extras import DictCursor


class SQLDatabase():
    """
    CRUD operations sql db
    """

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SQLDatabase.__instance == None:
            SQLDatabase()
        return SQLDatabase.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SQLDatabase.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SQLDatabase.__instance = self
            self._conn = self.__get_conn()

    @property
    def conn(self):
        return self._conn

    def __get_conn(self):
        print("running get conn")
        db_config = db_conf()

        # def inner(select, tables, on={}, filter={}):
        try:
            connection = pg.connect(
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port'],
                cursor_factory=DictCursor
            )
            return connection
            # result = method(select, tables, on, filter)
        except KeyError as e:
            print("Unable to connect to the databse with db_config")
            raise

    def create(self, *, table, values_dict):
        """
        values_dict
        """
        place_holders = ', '.join(values_dict.keys())
        values = ', '.join(['%s']*len(values_dict))
        query = f"""
        INSERT INTO {table} ({place_holders})
        VALUES ({values})
        """
        args = tuple(values_dict.values())
        cur = self.conn.cursor()
        try:
            cur.execute(query, args)
            result = True
        except Exception as e:
            # logger = Logger.getInstance()
            # logger.log(context=self.__class__.__name__,
            #            method="create",
            #            msg=f"query: {query}; Excpetion {e}")
            print(e)
            result = False
        finally:
            cur.close()
            self.conn.commit()
            return result

    def delete(self, *, table, filter):
        filter_line, args = self.__build_filter(filter)
        query = f"DELETE FROM {table} {filter_line}"
        cur = self.conn.cursor()
        try:
            cur.execute(query, args)
            result = True
        except Exception as e:
            # logger = Logger.getInstance()
            # logger.log(context=self.__class__.__name__,
            #            method="delete",
            #            msg=f"query: {query}; Excpetion {e}")
            print(e)
            result = False
        finally:
            cur.close()
            self.conn.commit()
            return result

    def find_all(self, select, tables, on={}, filter={}):
        query, args = self.__build_find_query(select, tables, on, filter)
        cur = self.conn.cursor()
        try:
            cur.execute(query, args)
            result = cur.fetchall()
        except Exception as e:
            # logger = Logger.getInstance()
            # logger.log(context=self.__class__.__name__,
            #            method="fetch_all",
            #            msg=f"query: {query}; Excpetion {e}")
            print(e)
            result = None

        finally:
            cur.close()
            return result

    def find_one(self, select, tables, on={}, filter={}):
        """
        args is a tuple
        query is a str
        """
        query, args = self.__build_find_query(select, tables, on, filter)

        cur = self.conn.cursor()

        try:
            cur.execute(query, args)
            result = cur.fetchone()
        except Exception as e:
            # logger = Logger.getInstance()
            # logger.log(context=self.__class__.__name__,
            #            method="fetch_all",
            #            msg=f"query: {query}; Excpetion {e}")
            print(e)
            result = None
        finally:
            cur.close()
            return result

    def __build_find_query(self, select, tables, on={}, filter={}):
        '''
        select: dict {
            table: List[colname]
        }
        tables: List[table_name]
        filter: dict {
            "table": {
                "col_name": value
                "other_col": value
                }
            }
        on: dict {
            table1: {
                col_name: {
                    table2: col_name2
                }
            }
            table3: {
                col_name3: {
                    table2: col_name2
                }
            }
        }

        '''
        # build the select part
        select_line = self.__build_select(select)
        # build the from part
        from_line = self.__connect_tables(tables, on)

        filter_line, args_list = self.__build_filter(filter)
        query = ' '.join([select_line, from_line, filter_line])

        return query, args_list

    def __build_select(self, select):
        """
        select: dict {
            table: List[colname]
        }
        """
        select_list = []
        for t, c_list in select.items():
            select_list.extend([f"{t}.{c}" for c in c_list])
        return "SELECT " + ', '.join(select_list)

    def __connect_tables(self, tables, on):
        """
        tables: list of strings
        on: dict {
            table1: {
                col_name: {
                    table2: col_name2
                }
            }
            table3: {
                col_name3: {
                    table2: col_name2
                }
            }
        }
        """
        from_line = "FROM " + " JOIN ".join(tables)
        on_list = []
        for t in tables:
            if t in on:
                t_vars = on[t]
                for var, vals in t_vars.items():
                    for table_name, var_name in vals.items():
                        on_list.append(f"{t}.{var}={table_name}.{var_name}")
        if on_list:
            on_line = "ON " + " AND ".join(on_list)
        else:
            on_line = ""
        return from_line + " " + on_line

    def __build_filter(self, filter):
        '''
        very simple filtering but it fills all the use cases
        will need to be expanded to and many values
        filter: dict {
            "table": {
                "col_name": {value: value, op: str}
                "other_col": {value: value, op: str}
                }
            }
        returns:
            tuple(
                filter_line (str),
                args (tuple)
            )
        '''
        filter_list = []
        args_list = []
        for t, c in filter.items():

            table_filter_list = [f'{t}.{k} {v["op"]} %s' for k, v in c.items()]
            filter_list.extend(table_filter_list)
            args_list.extend([c['value'] for c in c.values()])

        filter_line = "WHERE " + " AND ".join(filter_list)
        args = tuple(args_list)

        return (filter_line, args)

    def __unpack_result(self, columns: list, result):
        """
        creates dictionary from db results
        columns: tuple containing names of columns
        result: result of fetch_one from db class
        """
        # return {col: result[col] for col in columns}
        result_dict = {}
        for col in columns:
            result_dict[col] = result[col]
        return result_dict

    def __unpack_results(self, columns, results):
        return [self.unpack_db_result(columns, r) for r in results]
