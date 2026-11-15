import sys,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from algoritmos import BUSCAS,ORDENACOES
for n in [0,1,2,10,100]:
    a=[random.randint(0,100) for _ in range(n)]
    for name,sort in ORDENACOES.items():
        b=a.copy();sort(b);assert b==sorted(a),(name,n)
    distinct=sorted(set(a))
    for x in [0,5,55,101]+distinct:
        for name,fn in BUSCAS.items():
            pos,c=fn(distinct,x)
            assert (pos!=-1)==(x in distinct),(name,n,x)
            if pos!=-1:assert distinct[pos]==x
print('Todos os testes passaram.')
