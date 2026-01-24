def maxsum(lst):
    n=len(lst)
    cursum=0
    maxsum=float('-inf')
    for i in range(n):
        cursum+=lst[i]
        maxsum=max(maxsum,cursum)
        if cursum<0:
            cursum=0
    return maxsum
lst=[-2,7,-3,4]
print(maxsum(lst))