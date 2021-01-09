import time
import random

start_time = time.time()
random_time = random.randint(1, 5)

if (time.time() - start_time) > random_time:
    print(1)