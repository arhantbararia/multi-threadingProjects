import threading
import requests
from lxml import html
import time
import random
import datetime


class YahooFinanceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue,**kwargs):
        super(YahooFinanceScheduler, self ).__init__(**kwargs)
        self._input_queue = input_queue

        temp_queue = output_queue
        if type(temp_queue) != list:
            temp_queue = [temp_queue]
        

        self._output_queue = temp_queue
        
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get()
            if val == 'DONE':
                if self._output_queue is not None:
                    self._output_queue[0].put('DONE')
                break
            
            yahooFinanceWorker = YahooFinanceWorker(symbol = val)
            price = yahooFinanceWorker.get_price()
            if self._output_queue is not None:
                output = (val , price , str(datetime.datetime.utcnow()).split('.')[0] )
                self._output_queue[0].put(output)
            time.sleep(random.random() * 50 )



class  YahooFinanceWorker():

    

    def __init__(self , symbol , **kwargs):
        
        self._symbol = symbol
        
        base_url = 'https://finance.yahoo.com/quote/'
        self._url = f'{base_url}{self._symbol}'
        
       

    
        

    def get_price(self):
        
        
        try:
            r= requests.get(self._url)
            if r.status_code != 200:
                
                return
            
            
            page_contents= html.fromstring(r.text)

            price = float((page_contents.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[3]/div[1]/div[1]/fin-streamer[1]')[0].text.replace(',', '')))
            return price
        except requests.exceptions.ConnectionError as error:
            print("ERROR:" , error)

            
