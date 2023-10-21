import threading


class CalcWorker(threading.Thread):
    def __init__(self , n , **kwargs):
        self._n = n
        super(CalcWorker, self).__init__(**kwargs)
        self.start()

    def _calc_sum_squares(self):
        sum_squares = 0
        for i in range(self._n):
            sum_squares += i **2

        print(sum_squares)

    
    def run(self):
        self._calc_sum_squares()

