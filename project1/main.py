import time
import threading

from Workers import WikiWorker
from Workers import YahooFinanceScheduler
from Workers import MySqlMasterScheduler
from yaml_reader import YamlPipelineExecutor

from multiprocessing import Queue




def main():
    
    print("starting program \n\n")

    pipelinelocation = 'pipelines/wiki_yahoo_scraper_pipeline.yaml'
    yamlpipelineexecutor = YamlPipelineExecutor(yaml_file_location = pipelinelocation)
    yamlpipelineexecutor.process_pipeline()


    
    print("Pipelined Processed \n\n")


    scrapper_time_start = time.time()


    print('Extractime time took ', round(time.time()- scrapper_time_start, 1))

    print()

    print("exiting program")




if __name__ == "__main__":
    main()
    



