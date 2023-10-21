import threading
import mysql.connector




class MySqlMasterScheduler(threading.Thread):
    def __init__(self , input_queue , **kwargs):
        super(MySqlMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get()

            if val == "DONE":
                break

            symbol , price , extracted_time = val
            mysqlInsertionWorker = MySqlInsertionWorker(symbol , price , extracted_time)
            mysqlInsertionWorker.db_insert()




class MySqlInsertionWorker():
    def __init__(self, symbol , price , extracted_time ) -> None:
        self._symbol = symbol
        self._price = price
        self._extracted_time= extracted_time

        self._MYSQL_USER = 'arhantbararia'
        self._MYSQL_PASSWORD = 'arh123'
        self._MYSQL_HOST ='localhost'
        self._MYSQL_DB = 'PRICE_DB'

    
    def create_query(self):
        QUERY = f"INSERT INTO sp_500_prices(symbol, price , extracted_time) VALUES('{self._symbol}' , {self._price} , '{self._extracted_time}')"
        return QUERY
    def db_insert(self):
        with mysql.connector.connect(
            host = self._MYSQL_HOST,
            user = self._MYSQL_USER,
            passwd = self._MYSQL_PASSWORD,
            database = self._MYSQL_DB
        ) as connection:
            cursor = connection.cursor(buffered= True )
            cursor.execute(self.create_query())
            connection.commit()
            cursor.close()
            
        
        