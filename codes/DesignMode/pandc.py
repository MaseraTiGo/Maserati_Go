import time
def customer():
    r = ""
    while True:
        n = yield r
        print('customer cost:', n)
        time.sleep(1)
        r = "cost success!!!"

def productor(c):
    next(c)
    n = 0
    while n < 5:
        print('product Goods:', n)
        r = c.send(n)
        time.sleep(1)
        n += 1
        print('status:', r)
c = customer()
productor(c)        