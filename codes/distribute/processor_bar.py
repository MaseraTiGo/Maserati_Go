import sys
import time
def pro(total):
    _output = sys.stdout
    for c in range(total+1):
        time.sleep(0.1)
        _output.write(f'\rcompletepercent:' + '='*c)
    _output.flush()
pro(100)