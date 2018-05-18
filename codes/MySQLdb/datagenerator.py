import pymysql
import random

def random_data():
    name = ''
    for _ in range(4):
        name += chr(random.randint(97, 122))
    age = random.randint(14, 34)
    sex = random.choice(['male', 'female', 'midsex'])
    return name, sex, age

if __name__ == '__main__':
    from time import time
    s = time()
    entry = 300
    c = pymysql.connect('localhost', 'root', '123918', 'learn')
    cs = c.cursor()    
    for _ in range(entry):
        sql_src = 'insert into big_data(name, sex, age) values("%s", "%s", %d)'%random_data()
        #print('sql ---', sql_src)
        #break
        try:
            cs.execute(sql_src)
        except Exception as e:
            c.rollback()
    
    c.commit()
    c.close()
    e = time()
    print('all done', e-s)