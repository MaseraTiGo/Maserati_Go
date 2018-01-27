#-*- coding: utf-8 -*-
#author:ds
#date:2018-1-27

#######################
#    BUBBLE-SORT      #
#######################

import random
import time
c = 0
pre_list = []
while c < 10000:
    pre_list.append(random.randint(1,10000))
    c += 1
#print('before sort:',pre_list)
#bubble time
b_start_time = time.time()
for j in range(len(pre_list)-2):
    for i in range(len(pre_list)-1):
        if pre_list[i] > pre_list[i+1]:
            pre_list[i],pre_list[i+1] = pre_list[i+1],pre_list[i]
b_end_time = time.time()
bubble_time = b_end_time - b_start_time
#built-in sort
s_start_time = time.time()
sorted(pre_list)
s_end_time = time.time()
s_time = s_end_time - s_start_time

print('bubble -sort:',bubble_time)
print('ss     -sort:',s_time)
print (bubble_time - s_time)