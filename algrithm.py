#交换排序
#1. 冒泡排序
def bubbleSort(l):
    for i in range(len(l)):
        for j in range(0,len(l)-i-1):
            print(i,j)
            if l[j]>l[j+1]:
                temp=l[j+1]
                l[j+1]=l[j]
                l[j]=temp
    return print(l)

#2. 快速排序
def quickSort(l):
    return

def partition(l):
    return

#插入排序
#1.直接插入
def insertionSort(l):
    for i in range(1,len(l)):
        temp=l[i]
        j=i-1
        while j>=0 and temp<l[j]:
            l[j+1]=l[j]
            j-=1
        l[j+1]=temp
    return print(l)

def insertSortRecursively(l,m,n):
    if n == len(l):
        return
    if m == 0:
        return
    if l[m]>l[m-1] and m>=1:
        l[m], l[m - 1] = l[m - 1], l[m]
        insertSortRecursively(l,n,m - 1)
    if l[n]<= l[m]:
        insertSortRecursively(l,n+1,n+1)

#2.shell排序
def shellSort(l):
    k=[5,3,1]
    print(l)
    for i in k:
        shell(l,i)

def shell(l, gap):
    for i in range(len(l)):
        temp=l[i]
        j=i-gap
        while j>=0:
            if l[j]>temp:
                l[j+gap]=l[j]
            else:
                break
            j -= gap
        l[j+gap]=temp

#选择排序
#1.直接选择
def selectSort(l):
    for i in range(len(l)-1):
        min=i
        j=i
        while j<len(l):
            if l[min]>l[j]:
                min=j
            j += 1
        temp=l[i]
        l[i]=l[min]
        l[min]=temp

def quickSelect(l,lo,hi,k):
    s=LomutoPartition(l)
    if s-lo==k-1:
        return l[s]
    if s-lo>k-1:
        quickSelect(l,lo,s-1,k)
    else:
        quickSelect(l,s+1,hi,(k-1)-(s-lo))

def LomutoPartition(l):
    p = l[0]
    s = 0
    for i in range(1,len(l)):
        if l[i]<p:
            s+=1
            temp=l[s]
            l[s]=l[i]
            l[i]=temp
    l[0], l[s] = l[s], l[0]
    return s

#2.堆排序
def heapSort(l):
    for i in range(len(l)/2-1,-1):
        adjustHeap(l)
    for i in range(len(l)-1,-1):
        l[0],l[i]=l[i],l[0]
        adjustHeap(l)
    return

def adjustHeap(l):
    for i in range(len(l)):
        if l[i]<l[2*i+1]:
            temp=l[i]
            l[i]=l[2*i+1]
            l[2*i+1]=temp
        if l[i]<l[2*i+2]:
            temp = l[i]
            l[i] = l[2 * i + 2]
            l[2 * i + 2] = temp

test=[2,9,4,3,6,0,5,8]
# bubbleSort(test)
# insertionSort(test)
# insertSortRecursively(test,1,1)
# shellSort(test)
# print(quickSelect(test,0,len(test)-1,3))
selectSort(test)
heapSort(test)
print(test)
