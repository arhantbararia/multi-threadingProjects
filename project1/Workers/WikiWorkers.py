import threading

import requests
from bs4 import BeautifulSoup

class WikiWorkerMasterScheduler(threading.Thread):
    def __init__(self , output_queue ,**kwargs ):
        if 'input_queue' in kwargs:
            kwargs.pop('input_queue')

        
        self._input_values = kwargs.pop('input_values')

        super(WikiWorkerMasterScheduler, self).__init__(**kwargs)
        temp_queue = output_queue
        if type(temp_queue) != list:
            temp_queue = [temp_queue]
        self._output_queues = temp_queue
        
        
        self.start()

    def run(self):
        for entry in self._input_values:
            wikiWorker = WikiWorker(url = entry)
            symbol_counter = 0
            for symbol in wikiWorker.get_sp_500_companies():
                for output_queue in self._output_queues:
                    output_queue.put(symbol)
                symbol_counter += 1
                if symbol_counter >= 5:
                    break
        
        for out_queue in self._output_queues:
            for i in range(20):
                output_queue.put('DONE')


class WikiWorker():
    def __init__(self , url):
        self._url = url


    @staticmethod
    def _extract_companies__symbols_(page_html):
        
        soup = BeautifulSoup(page_html, 'lxml')
        
        table = soup.find(id='constituents')
        
        
        table_rows = table.find_all('tr')
        
        
        
        for table_row in table_rows[1:]:
            symbol = table_row.find('td').text.strip('\n')
            
            yield symbol

    def get_sp_500_companies(self):
        response= requests.get(self._url)

        if response.status_code != 200:
            print("Couldn't get entries")
            return []
      
        yield from self._extract_companies__symbols_(response.text)
        




