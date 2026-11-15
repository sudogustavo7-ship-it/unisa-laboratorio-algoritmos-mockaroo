"""Algoritmos didáticos instrumentados: comparações de chaves e movimentações.
Cada comparação de chave conta uma vez; movimentação conta escrita em vetor.
"""

def busca_linear(a, x):
    c=0
    for i,v in enumerate(a):
        c+=1
        if v==x:return i,c
    return -1,c

def busca_linear_recursiva(a,x):
    # índice explícito; Python possui limite de pilha, ampliado no programa de testes
    def visita(i):
        if i==len(a):return -1,0
        if a[i]==x:return i,1
        pos,c=visita(i+1)
        return pos,c+1
    return visita(0)

def busca_binaria(a,x):
    lo,hi,c=0,len(a)-1,0
    while lo<=hi:
        m=(lo+hi)//2;c+=1
        if a[m]==x:return m,c
        if a[m]<x:lo=m+1
        else:hi=m-1
    return -1,c

def busca_binaria_recursiva(a,x):
    def visita(lo,hi):
        if lo>hi:return -1,0
        m=(lo+hi)//2
        if a[m]==x:return m,1
        if a[m]<x:p,c=visita(m+1,hi)
        else:p,c=visita(lo,m-1)
        return p,c+1
    return visita(0,len(a)-1)

def bubble(a):
    c=m=0;n=len(a)
    for end in range(n-1,0,-1):
        mudou=False
        for j in range(end):
            c+=1
            if a[j]>a[j+1]:a[j],a[j+1]=a[j+1],a[j];m+=2;mudou=True
        if not mudou:break
    return c,m

def selection(a):
    c=m=0
    for i in range(len(a)-1):
        k=i
        for j in range(i+1,len(a)):
            c+=1
            if a[j]<a[k]:k=j
        if k!=i:a[i],a[k]=a[k],a[i];m+=2
    return c,m

def insertion(a):
    c=m=0
    for i in range(1,len(a)):
        key=a[i];j=i-1
        while j>=0:
            c+=1
            if a[j]<=key:break
            a[j+1]=a[j];m+=1;j-=1
        a[j+1]=key;m+=1
    return c,m

def shell(a):
    c=m=0;gap=len(a)//2
    while gap:
        for i in range(gap,len(a)):
            x=a[i];j=i
            while j>=gap:
                c+=1
                if a[j-gap]<=x:break
                a[j]=a[j-gap];m+=1;j-=gap
            a[j]=x;m+=1
        gap//=2
    return c,m

def merge(a):
    def rec(lo,hi):
        if hi-lo<2:return 0,0
        md=(lo+hi)//2;c1,m1=rec(lo,md);c2,m2=rec(md,hi)
        left=a[lo:md];right=a[md:hi];i=j=0;c=m=0;k=lo
        while i<len(left) and j<len(right):
            c+=1
            if left[i]<=right[j]:a[k]=left[i];i+=1
            else:a[k]=right[j];j+=1
            k+=1;m+=1
        while i<len(left):a[k]=left[i];i+=1;k+=1;m+=1
        while j<len(right):a[k]=right[j];j+=1;k+=1;m+=1
        return c+c1+c2,m+m1+m2
    return rec(0,len(a))

def quick(a):
    # quicksort iterativo com pivô central e partição Hoare
    c=m=0;stack=[(0,len(a)-1)]
    while stack:
        lo,hi=stack.pop()
        if lo>=hi:continue
        pivot=a[(lo+hi)//2];i=lo;j=hi
        while i<=j:
            while True:
                c+=1
                if not a[i]<pivot:break
                i+=1
            while True:
                c+=1
                if not a[j]>pivot:break
                j-=1
            if i<=j:
                if i!=j:a[i],a[j]=a[j],a[i];m+=2
                i+=1;j-=1
        if lo<j:stack.append((lo,j))
        if i<hi:stack.append((i,hi))
    return c,m

def heap(a):
    c=m=0;n=len(a)
    def sink(i,end):
        nonlocal c,m
        while 2*i+1<end:
            child=2*i+1
            if child+1<end:
                c+=1
                if a[child]<a[child+1]:child+=1
            c+=1
            if a[i]>=a[child]:break
            a[i],a[child]=a[child],a[i];m+=2;i=child
    for i in range(n//2-1,-1,-1):sink(i,n)
    for end in range(n-1,0,-1):a[0],a[end]=a[end],a[0];m+=2;sink(0,end)
    return c,m

BUSCAS={'linear':busca_linear,'linear_recursiva':busca_linear_recursiva,'binaria':busca_binaria,'binaria_recursiva':busca_binaria_recursiva}
ORDENACOES={'bubble':bubble,'selection':selection,'insertion':insertion,'shell':shell,'merge':merge,'quick':quick,'heap':heap}
