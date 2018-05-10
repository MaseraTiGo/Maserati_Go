import concurrent.futures

nums = range(10000)

def f(x):
    return x * x

    
def main():
    # Make sure the map and function are working
    #print([val for val in map(f, nums)])

    # Test to make sure concurrent map is working
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futs = [i for i in executor.map(f, nums)]
        #futs = {executor.submit(f, i) for i in range(10)}
        #res = [fut.result() for fut in futs]
        print(futs[-10:])

if __name__ == '__main__':
    import time
    start = time.time()
    #futs = list(map(f, nums))
    #print(futs[-10:])
    main()
    print(time.time()-start)