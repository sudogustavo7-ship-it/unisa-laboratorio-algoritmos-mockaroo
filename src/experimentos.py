"""Executa os 10 experimentos do enunciado atualizado.
Modo rápido (padrão): 5 repetições, ordenações quadráticas limitadas a 1000.
Modo completo: --repeticoes 30 (atenção ao custo computacional).
Os dados e a metodologia registram integralmente os limites usados.
"""
from pathlib import Path
import csv,sys,time,statistics,random,platform,argparse
from algoritmos import BUSCAS,ORDENACOES,busca_linear,busca_binaria,merge,quick
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resultados';OUT.mkdir(exist_ok=True)

def carregar(n,ordem):
    with (ROOT/'dados'/f'base_{n}_{ordem}.csv').open(encoding='utf-8',newline='') as f:
        return [int(r['id_cliente']) for r in csv.DictReader(f)]

def save(name,rows):
    if not rows:return
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def medir(fn,reps):
    times=[];values=[]
    for _ in range(reps):
        t=time.perf_counter();v=fn();times.append((time.perf_counter()-t)*1000);values.append(v)
    return {'media_ms':statistics.mean(times),'mediana_ms':statistics.median(times),'desvio_ms':statistics.stdev(times) if reps>1 else 0},values[0]

def rowbase(exp,scenario,algo,n,r,extra=None):
    return {'experimento':exp,'cenario':scenario,'algoritmo':algo,'n':n,'repeticoes':r,**(extra or {})}

def executar(reps=5):
    random.seed(2026);result=[]
    print('Experimentos 1-4: buscas',flush=True)
    for n in [1000,10000,100000]:
        u=carregar(n,'desordenada');s=sorted(u)
        for pos in ['inicio','25%','50%','75%','fim','ausente']:
            idx={'inicio':0,'25%':n//4,'50%':n//2,'75%':3*n//4,'fim':n-1,'ausente':None}[pos]
            for algo,fn in BUSCAS.items():
                a=s if 'binaria' in algo else u
                target=a[idx] if idx is not None else max(a)+1
                if algo=='linear_recursiva' and n>1000:
                    result.append({**rowbase('1-4',pos,algo,n,0), 'media_ms':'','mediana_ms':'','desvio_ms':'','comparacoes':'','indice':'','status':'omitido: limite seguro de recursao'})
                    continue
                try:
                    stats,(found,comps)=medir(lambda:fn(a,target),reps)
                    assert (found!=-1)==(idx is not None)
                    result.append({**rowbase('1-4',pos,algo,n,reps),**stats,'comparacoes':comps,'indice':found,'status':'medido'})
                except RecursionError:
                    result.append({**rowbase('1-4',pos,algo,n,0),'status':'omitido: RecursionError'})
    save('buscas.csv',result)
    print('Experimentos 5-6: ordenações',flush=True)
    sorts=[]
    for n in [1000,10000,100000]:
        base=carregar(n,'desordenada')
        for estado,values in [('aleatorio',base),('ordenado',sorted(base)),('inverso',sorted(base,reverse=True))]:
            for algo,fn in ORDENACOES.items():
                if algo in ('bubble','selection','insertion') and n>1000:
                    sorts.append({**rowbase('5-6',estado,algo,n,0),'status':'omitido: limite quadratico de 1000 registros'});continue
                rr=reps if n<=10000 else min(reps,3)
                def job():
                    a=list(values);c,m=fn(a);assert a==sorted(values),(algo,n,estado);return c,m
                stats,(c,m)=medir(job,rr)
                sorts.append({**rowbase('5-6',estado,algo,n,rr),**stats,'comparacoes':c,'movimentacoes':m,'status':'medido'})
    save('ordenacoes.csv',sorts)
    print('Experimento 7: inserção',flush=True)
    inserts=[];a=sorted(carregar(10000,'desordenada'))
    for p in [0,.25,.5,.75,1]:
        ix=min(int(p*len(a)),len(a)-1);key=a[0]-1 if p==0 else a[-1]+1 if p==1 else (a[ix-1]+a[ix])//2
        def reorder():
            v=a.copy();v.append(key);merge(v);assert v==sorted(a+[key]);return None
        def maintain():
            v=a.copy();lo=0;hi=len(v)
            while lo<hi:
                md=(lo+hi)//2
                if v[md]<key:lo=md+1
                else:hi=md
            v.insert(lo,key);assert v==sorted(a+[key]);return None
        for label,fn in [('acrescentar_e_ordenar',reorder),('inserir_ordenado',maintain)]:
            stats,_=medir(fn,reps)
            inserts.append({**rowbase('7',f'{int(p*100)}%',label,len(a),reps),**stats})
    save('insercoes.csv',inserts)
    print('Experimento 8: remoção',flush=True)
    removes=[]
    for label,index in [('inicio',0),('meio',5000),('fim',9999)]:
        loc=[];rem=[]
        for _ in range(reps):
            v=a.copy();target=v[index];t=time.perf_counter();pos,_=busca_binaria(v,target);loc.append((time.perf_counter()-t)*1000)
            t=time.perf_counter();v.pop(pos);rem.append((time.perf_counter()-t)*1000)
        removes.append({**rowbase('8',label,'busca_binaria+pop',len(a),reps),'localizacao_media_ms':statistics.mean(loc),'remocao_media_ms':statistics.mean(rem),'total_media_ms':statistics.mean(loc)+statistics.mean(rem)})
    save('remocoes.csv',removes)
    print('Experimento 9: consultas em lote',flush=True)
    big=carregar(100000,'desordenada');ordered=sorted(big);queries=[big[random.randrange(len(big))] for _ in range(10000)]
    bulk=[]
    for count in [1,10,100,1000]:
        qs=queries[:count]
        t=time.perf_counter()
        for q in qs:busca_linear(big,q)
        ta=(time.perf_counter()-t)*1000
        t=time.perf_counter();v=big.copy();merge(v)
        for q in qs:busca_binaria(v,q)
        tb=(time.perf_counter()-t)*1000
        bulk.extend([{'quantidade_buscas':count,'sistema':'A_linear','tempo_total_ms':ta,'repeticoes':1}, {'quantidade_buscas':count,'sistema':'B_merge_binaria','tempo_total_ms':tb,'repeticoes':1}])
    for sistema in ['A_linear','B_merge_binaria']:
        val_1000=next(v['tempo_total_ms'] for v in bulk if v['quantidade_buscas']==1000 and v['sistema']==sistema)
        val_100=next(v['tempo_total_ms'] for v in bulk if v['quantidade_buscas']==100 and v['sistema']==sistema)
        estimate=val_1000+(10000-1000)*(val_1000-val_100)/(1000-100)
        bulk.append({'quantidade_buscas':10000,'sistema':sistema,'tempo_total_ms':estimate,'repeticoes':0,'status':'PROJECAO_NAO_MEDIDA'})
    for r in bulk:r.setdefault('status','MEDIDO')
    save('muitas_consultas.csv',bulk)
    print('Experimento 10: inserção contínua',flush=True)
    continuous=[]
    for count in [100,500,1000]:
        vals=[random.randint(10000000,20000000) for _ in range(count)]
        def each():
            v=a.copy()
            for x in vals:
                lo,hi=0,len(v)
                while lo<hi:
                    m=(lo+hi)//2
                    if v[m]<x:lo=m+1
                    else:hi=m
                v.insert(lo,x)
            assert v==sorted(a+vals)
        def batch():
            v=a.copy();v.extend(vals);merge(v);assert v==sorted(a+vals)
        for label,fn in [('manter_ordenada',each),('ordenar_em_lote',batch)]:
            stats,_=medir(fn,reps)
            continuous.append({**rowbase('10',str(count)+' insercoes',label,len(a),reps),**stats})
    save('insercao_continua.csv',continuous)
    with (OUT/'ambiente.txt').open('w') as f:
        f.write(f'Plataforma: {platform.platform()}\nProcessador: {platform.processor()}\nPython: {platform.python_version()}\nRepeticoes padrão: {reps}\n')
    print('Concluído',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repeticoes',type=int,default=5);args=p.parse_args();executar(args.repeticoes)
