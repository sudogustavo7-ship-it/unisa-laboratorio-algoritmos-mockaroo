"""Normaliza as bases fornecidas: adapta colunas e reatribui IDs duplicados.
Preserva os outros campos e exporta ordem aleatória e crescente de ID.
"""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
COLS=['id_cliente','nome','email','idade','cidade','estado','data_cadastro','numero_compras','valor_total']
MAPPING={'id':'id_cliente','dataCadastro':'data_cadastro','numeroCompras':'numero_compras','valorTotal':'valor_total'}

def preparar():
    for n in [1000,10000,100000]:
        path=ROOT/'dados'/f'base_{n}.csv'
        with path.open(encoding='utf-8-sig',newline='') as f:
            raw=list(csv.DictReader(f,delimiter=';'))
        assert len(raw)==n,(n,len(raw))
        seen=set();maxid=max(int(v['id']) for v in raw);fixed=0
        rows=[]
        for row in raw:
            id_=int(row['id'])
            if id_ in seen:
                maxid+=1;id_=maxid;fixed+=1
            seen.add(id_)
            row['id']=str(id_)
            rows.append({MAPPING.get(k,k):v for k,v in row.items()})
        assert len(seen)==n
        for label, rr in [('desordenada',rows),('ordenada',sorted(rows,key=lambda x:int(x['id_cliente'])))]:
            with (ROOT/'dados'/f'base_{n}_{label}.csv').open('w',encoding='utf-8',newline='') as out:
                w=csv.DictWriter(out,fieldnames=COLS);w.writeheader();w.writerows(rr)
        print(f'{n}: IDs duplicados reparados={fixed}; linhas={n}')
if __name__=='__main__':preparar()
