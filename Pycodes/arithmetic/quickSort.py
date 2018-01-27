#-*- coding: utf-8 -*-
#author:ds
#date:2018-1-27

#######################
#    QUICK-SORT      #
#######################

import random
import time

c = 0
pre_list = []
while c < 10:
    pre_list.append(random.randint(1,100))
    c += 1
print(pre_list)    
def quick_sort(pre_list,start,end):
    if start < end:
        i,j = start,end
        base = pre_list[i]
        while i < j:
            while i < j and pre_list[j] >= base:
                j -= 1
            pre_list[i] = pre_list[j]
            print(j)
            while i < j and pre_list[i] <= base:
                i += 1
            pre_list[j] = pre_list[i]
            print(i)
        print(pre_list)    
        pre_list[i] = base
        quick_sort(pre_list, start, i - 1)
        quick_sort(pre_list, j + 1, end)
    return pre_list
print(quick_sort(pre_list,0,pre_list.__len__()-1))