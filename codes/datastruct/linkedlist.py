#Test Infomation, ignore it

# class Node(object):
    # def __init__(self, data, pnext=None):
        # self.data = date
        # self.pnext = pnext
        

# class LinkedList(object):
    # def __init__(self):
        # self.head = None
        # self.length = 0
    
    # def isEmpty(self):
        # return (self.length == 0)
    
    # def append(self, data):
        # item = None
        # if isinstance(data, Node):
            # item = data
        # else:
            # item = Node(data)
        # if not self.head:
            # self.length += 1
            

# def lengthOfLongestSubstring(s):
        # """
        # :type s: str
        # :rtype: int
        # """
        # length = []
        # for _ in range(len(s)):
            # temp = []
            # for l in s:
                # if l not in temp:
                    # temp.append(l)
                    # length.append(len(temp))
                # else:
                    # length.append(len(temp))
                    # temp = [l]                    
        # longest = max(length)
        # return longest
# a = lengthOfLongestSubstring("dvdf")
# print('fuckyou---', a)


#add two nums
# def twoSum(nums, target):
    # """
        # :type nums: List[int]
        # :type target: int
        # :rtype: List[int]
    # """
    # for i, n in enumerate(nums):
        # nums.pop
        # try:
            # j = nums.index(target-n)
            # if j == i:
                # continue
            # break
        # except ValueError:
            # continue
    # return i, j
# a = twoSum([2,7,11,15], 9)
# print(a)
        