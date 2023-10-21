import time
import threading

from Workers import WikiWorker
from Workers import YahooFinanceWorker
from Workers import YahooFinananceScheduler
from Workers import MySqlMasterScheduler

from multiprocessing import Queue




def main():
    print("starting program \n\n")
    p = 1
    
    symbol_queue = Queue()
    insertion_queue = Queue()


    worker = WikiWorker()

    yahoo_finance_schedular_threads = []

    num_yahoo_workers = 4

    for i in range(num_yahoo_workers):
        yahooFinananceScheduler = YahooFinananceScheduler(input_queue= symbol_queue , output_queue=insertion_queue)
        yahoo_finance_schedular_threads.append(yahooFinananceScheduler)
    
    
    mysql_scheduler_threads = []

    num_mysql_workers = 4

    for i in range(num_mysql_workers):
        mysqlMasterScheduler = MySqlMasterScheduler(input_queue= insertion_queue)
        mysql_scheduler_threads.append(mysqlMasterScheduler)
    
    
    scrapper_time_start = time.time()
    

    for symbol in worker.get_sp_500_companies():
        symbol_queue.put(symbol)
            
    
    

        # yahoo_worker = YahooFinanceWorker(symbol=symbol)
        # current_threads.append(yahoo_worker)
    for i in range(len(yahoo_finance_schedular_threads)):
        symbol_queue.put("DONE")

    
    for i in range(len(yahoo_finance_schedular_threads)):
        yahoo_finance_schedular_threads[i].join()

    for i in range(len(mysql_scheduler_threads)):
        mysql_scheduler_threads[i].join()

    
    print('Extractime time took ', round(time.time()- scrapper_time_start, 1))

    print()

    print("exiting program")




if __name__ == "__main__":
    main()
    



