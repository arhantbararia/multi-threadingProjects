import importlib

import yaml
from multiprocessing import Queue



class YamlPipelineExecutor():
    def __init__(self , yaml_file_location):
        self._pipeline_location = yaml_file_location
        self._queues = {}
        self._workers = {}



    def _load_pipeline(self ):
        with open(self._pipeline_location , 'r') as inFile:
            self._yaml_data = yaml.safe_load(inFile)


    
    def _initialize_queues(self):
        for queue in self._yaml_data['queues']:
            queue_name = queue['name']
            self._queues[queue_name] = Queue()


    def _initialize_workers(self):
        for worker in self._yaml_data['workers']:
            worker_name = worker['name']
            
            worker_class = getattr(importlib.import_module(worker['location']) , worker['class'])     ## this is very interesing piece of code
            input_values = worker.get('input_values')
            input_queue = worker.get('input_queue')
            output_queues = worker.get('output_queues')
            num_instances = worker.get('instances' , 1)

            init_params = {
                'input_queue' : self._queues[input_queue] if input_queue is not None else None,
                'output_queue' : [self._queues[output_queue] for output_queue in output_queues ] if output_queues is not None else None
            }

            if input_values is not None:
                init_params['input_values'] = input_values
                
            
            self._workers[worker_name] = []
            for i in range(num_instances):

                self._workers[worker_name].append(worker_class(**init_params))

    
    def _join_workers(self):
        for worker_name in self._workers:
            for worker_thread in self._workers[worker_name]:
                worker_thread.join()




    def process_pipeline(self):
        self._load_pipeline()
        self._initialize_queues()
        self._initialize_workers()
        self._join_workers()


