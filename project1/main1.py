import time
import threading

from Workers import CalcWorker
from Workers import SleepyWorker



def main():
    print("starting program \n\n")
    calc_start_time = time.time()

    current_threads = []

    for i in range(5):
        maximum_value = (i+1)*1000000

        calcworker = CalcWorker(n = maximum_value)

        # t = threading.Thread(target = calculate_sum_squares, args = (maximum_value,), daemon = True)
        # t.start()
        # calculate_sum_squares(maximum_value)
        current_threads.append(calcworker)

    
    for i in range(len(current_threads)):
        current_threads[i].join()

    


    print('Calculating sum of squares took: ', round(time.time()- calc_start_time, 1))

    sleep_start_time = time.time()

    current_threads = []

    for seconds in range(1,6):

        sleepy_worker = SleepyWorker(seconds= seconds, daemon = True)
        
        # t = threading.Thread(target = sleep_a_little, args = (seconds,), daemon = True)
        # t.start()
        # sleep_a_little(seconds)
        current_threads.append(sleepy_worker)

    
    for i in range(len(current_threads)-3):
        current_threads[i].join()
    
    print('Sleeping time: ', round(time.time()- sleep_start_time, 1))


    print("exiting program")




if __name__ == "__main__":
    main()
    



