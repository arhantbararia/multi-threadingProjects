import time
import threading

from Workers import WikiWorker
from Workers import YahooFinanceScheduler
from Workers import MySqlMasterScheduler
from yaml_reader import YamlPipelineExecutor

from multiprocessing import Queue




def main():

    pipelinelocation = 'pipelines/wiki_yahoo_scraper_pipeline.yaml'
    yamlpipelineexecutor = YamlPipelineExecutor(yaml_file_location = pipelinelocation)
    yamlpipelineexecutor.process_pipeline()


    print("starting program \n\n")


    
    # symbol_queue = Queue()
    # MySQLUploading = Queue()


    worker = WikiWorker()

    # yahoo_finance_schedular_threads = []

    # num_yahoo_workers = 4

    # for i in range(num_yahoo_workers):
    #     yahooFinananceScheduler = YahooFinanceScheduler(input_queue= symbol_queue , output_queue=MySQLUploading)
    #     yahoo_finance_schedular_threads.append(yahooFinananceScheduler)
    
    
    # mysql_scheduler_threads = []

    # num_mysql_workers = 4

    # for i in range(num_mysql_workers):
    #     mysqlMasterScheduler = MySqlMasterScheduler(input_queue= MySQLUploading)
    #     mysql_scheduler_threads.append(mysqlMasterScheduler)
    
    
    scrapper_time_start = time.time()

    p = 0

    for symbol in worker.get_sp_500_companies():
        if p < 10:
            yamlpipelineexecutor._queues['symbol_queue'].put(symbol)
            p += 1
        else:
            break

            
    
    

        # yahoo_worker = YahooFinanceWorker(symbol=symbol)
        # current_threads.append(yahoo_worker)

    for i in range(5):
        yamlpipelineexecutor._queues['symbol_queue'].put("DONE")

    
    yamlpipelineexecutor._join_workers()

    # for i in range(len(yahoo_finance_schedular_threads)):
    #     yahoo_finance_schedular_threads[i].join()

    # for i in range(len(mysql_scheduler_threads)):
    #     mysql_scheduler_threads[i].join()

    
    print('Extractime time took ', round(time.time()- scrapper_time_start, 1))

    print()

    print("exiting program")




if __name__ == "__main__":
    main()
    



