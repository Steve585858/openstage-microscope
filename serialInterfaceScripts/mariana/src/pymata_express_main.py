#https://realpython.com/async-io-python/

import sys
import time
import asyncio
from pymata_express.pymata_express import PymataExpress

from pymata_express_examples import ConcurrentTasks


# Retrieve the asyncio event loop - used by exception
loop = asyncio.get_event_loop()
# Instantiate PyMataExpress
board = PymataExpress()
try:
    id = 11
    if id ==0:
        pass
    elif id ==1:
        s = time.perf_counter()
        worker = ConcurrentTasks(board)
        loop1 = asyncio.get_event_loop()
        loop1.run_until_complete(worker.retrieve_info())
        #asyncio.run(worker.retrieve_info())
        elapsed = time.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    elif id ==10:
        worker = ConcurrentTasks(board, None)
        loop.run_until_complete(worker.async_init_and_run())
    elif id ==11:
        worker = ConcurrentTasks(board, None)
        loop.run_until_complete(worker.blink())
except (KeyboardInterrupt, RuntimeError):
    loop.run_until_complete(board.shutdown())
    print('goodbye-Key')
finally:
    print('goodbye-finally')
    loop.close()
    sys.exit(0)