import requests
from bs4 import BeautifulSoup



class WikiWorker():
    def __init__(self):
        self.url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


    @staticmethod
    def _extract_companies__symbols_(page_html):
        
        soup = BeautifulSoup(page_html, 'lxml')
        
        table = soup.find(id='constituents')
        
        
        table_rows = table.find_all('tr')
        
        i = 1
        
        for table_row in table_rows[1:]:
            symbol = table_row.find('td').text.strip('\n')
            
            yield symbol

    def get_sp_500_companies(self):
        response= requests.get(self.url)

        if response.status_code != 200:
            print("Couldn't get entries")
            return []
      
        yield from self._extract_companies__symbols_(response.text)
        



