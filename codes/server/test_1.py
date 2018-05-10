import socket
import time
from concurrent import futures
def blocking_way():
    sock = socket.socket()
    sock.connect(('www.baidu.com', 80))
    request = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    reponse = b''
    chunk = sock.recv(4096)
    while chunk:
        reponse += chunk
        chunk = sock.recv(4096)
    #print(reponse)
    #with open(r'd:\baidu.html', 'wb') as f:
        #f.write(chunk)
    return reponse
ss = 0
def tt():
    global ss
    ss += 1
    return 'caonima'
    
def sync_way():
    res = []
    for i in range(10):
        res.append(blocking_way())
    return len(res)
    

def process_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as executor:
            res = {executor.submit(blocking_way) for i in range(10)}
    return len([rr.result() for rr in res])
s = time.time()
process_way()#sync_way()
print(time.time()-s)

