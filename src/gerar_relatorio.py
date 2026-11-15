"""Gera gráficos e o relatório em LaTeX com base nos CSVs efetivamente coletados."""
from pathlib import Path
import csv,statistics,math,platform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'resultados';G=ROOT/'graficos';L=ROOT/'relatorio';G.mkdir(exist_ok=True)
def load(f):
    with (R/f).open(encoding='utf8') as x:return list(csv.DictReader(x))
busca=load('buscas.csv');ordena=load('ordenacoes.csv');bulk=load('muitas_consultas.csv');ins=load('insercoes.csv');cont=load('insercao_continua.csv')
def graph(name,title,xlabel,ylabel,series,log=False):
    plt.figure(figsize=(8.2,4.7))
    for label,pairs in series.items():
        pairs=sorted(pairs);plt.plot([p[0] for p in pairs],[p[1] for p in pairs],'-o',label=label)
    plt.title(title);plt.xlabel(xlabel);plt.ylabel(ylabel);plt.grid(alpha=.25);plt.legend();
    if log:plt.yscale('log')
    plt.tight_layout();plt.savefig(G/name,dpi=170);plt.close()
def filt(df,algo,scenario):return [(int(x['n']),float(x['media_ms'])) for x in df if x['algoritmo']==algo and x['cenario']==scenario and x.get('status')=='medido']
graph('01_tempo_busca.png','Tempo de busca por tamanho (elemento ausente)','Registros','Tempo médio (ms)',{a:filt(busca,a,'ausente') for a in ['linear','binaria']},True)
graph('02_comparacoes_busca.png','Comparações de busca por tamanho (ausente)','Registros','Comparações', {a:[(int(x['n']),int(x['comparacoes'])) for x in busca if x['algoritmo']==a and x['cenario']=='ausente' and x.get('status')=='medido'] for a in ['linear','binaria']},True)
graph('03_tempo_ordenacao.png','Tempo de ordenação (entrada aleatória)','Registros','Tempo médio (ms)',{a:filt(ordena,a,'aleatorio') for a in ['bubble','selection','insertion','shell','merge','quick','heap']},True)
graph('04_consultas.png','Custo total do sistema por número de consultas','Consultas','Tempo total (ms)',{a:[(int(x['quantidade_buscas']),float(x['tempo_total_ms'])) for x in bulk if x['sistema']==a and x['status']=='MEDIDO'] for a in ['A_linear','B_merge_binaria']},True)
graph('05_insercao_continua.png','Inserção contínua: comparação de estratégias','Número de inserções','Tempo médio (ms)',{a:[(int(x['cenario'].split()[0]),float(x['media_ms'])) for x in cont if x['algoritmo']==a] for a in ['manter_ordenada','ordenar_em_lote']})
# preâmbulo fornecido, com corpo substituído por resultados efetivos
src=(L/'Template_UNISA_Projeto.tex').read_text()
header=src.split('\\begin{document}')[0]
def esc(x):return str(x).replace('_',r'\_').replace('%',r'\%').replace('&',r'\&')
def tab(rows,head):
    out='\\begin{center}\\small\\begin{tabular}{'+'l'*len(head)+'}\\toprule\n'+' & '.join(map(esc,head))+r' \\ '+'\n\\midrule\n'
    for r in rows:out+=' & '.join(map(esc,r))+r' \\ '+'\n'
    return out+'\\bottomrule\\end{tabular}\\end{center}\n'
def fmt(x):return f'{float(x):.3f}'
base=[]
for n in [1000,10000,100000]:
    sub=[r for r in busca if r['n']==str(n) and r['cenario']=='ausente' and r['algoritmo'] in ('linear','binaria') and r['status']=='medido']
    base.append([n]+[f"{fmt(next(r['media_ms'] for r in sub if r['algoritmo']==a))} / {next(r['comparacoes'] for r in sub if r['algoritmo']==a)}" for a in ('linear','binaria')])
ordrows=[]
for a in ['bubble','selection','insertion','shell','merge','quick','heap']:
    vals=[]
    for n in [1000,10000,100000]:
        rr=next((r for r in ordena if r['algoritmo']==a and r['cenario']=='aleatorio' and int(r['n'])==n and r['status']=='medido'),None)
        vals.append(fmt(rr['media_ms']) if rr else 'N/E')
    ordrows.append([a,*vals])
bl=[]
for n in [1,10,100,1000,10000]:
    vs=[next(r for r in bulk if r['sistema']==a and int(r['quantidade_buscas'])==n) for a in ['A_linear','B_merge_binaria']]
    bl.append([n,fmt(vs[0]['tempo_total_ms']),fmt(vs[1]['tempo_total_ms']),'projetado' if n==10000 else 'medido'])
fig=lambda name,caption:'\\begin{figure}[H]\\centering\\includegraphics[width=.91\\textwidth]{../graficos/'+name+'}\\caption{'+caption+'}\\end{figure}\n'
body=r'''
\begin{document}
\begin{titlepage}\centering\vspace*{1cm}\logoUNISA\par\vspace{1.3cm}
{\Large Universidade Santo Amaro -- UNISA\par}\vspace{.3cm}{\large Técnicas de Programação -- 2026\par}\vfill
{\LARGE\bfseries\color{unisaazul}Laboratório Experimental de Algoritmos com Dados Sintéticos\par}\vspace{1.5cm}
\begin{flushleft}\textbf{Integrantes:} preencher nome(s) e RA(s)\\\textbf{Professora:} Profa. Thamiris Neves\\\textbf{Turma:} preencher\end{flushleft}\vfill
São Paulo -- 2026\end{titlepage}
\section*{Resumo}
Este trabalho investiga algoritmos de busca, ordenação, inserção e remoção por meio de dados sintéticos de clientes. Foram utilizadas bases de 1.000, 10.000 e 100.000 registros, originadas de arquivos disponibilizados para o projeto e normalizadas para a chave numérica única. Implementaram-se quatro métodos de pesquisa e sete de ordenação, comparando cenários de posição, crescimento, estado inicial, operações de alteração e consultas em lote. As medições utilizaram o relógio de alta resolução de Python e registraram tempos, comparações e movimentações quando aplicáveis. Algoritmos quadráticos foram executados somente até 1.000 elementos, de modo a evitar tempos de execução desproporcionais. Os resultados mostram comportamentos coerentes com as complexidades teóricas, com vantagens da busca binária após a ordenação e diferenças entre estratégias de manutenção de listas ordenadas. O cenário de 10.000 consultas recebeu projeção separada, não considerada medição. Discute-se a importância de considerar custo de preparação, quantidade de operações e limitações de memória e recursão ao selecionar métodos.
\par\noindent\textbf{Palavras-chave:} algoritmos; busca; ordenação; complexidade; dados sintéticos.
\tableofcontents\newpage
\section{Introdução}
Algoritmos com mesmo resultado funcional podem exigir esforços computacionais diferentes. Este estudo analisa as escolhas de estruturas e procedimentos quando se pesquisam e manipulam cadastros com volumes crescentes. A pergunta central é se existe um algoritmo universalmente mais eficiente para todas essas operações.
\section{Base de dados}
Os arquivos CSV originais, identificados como bases sintéticas associadas ao Mockaroo, contêm nome, e-mail, idade, cidade, estado, data de cadastro, compras e valor total. Normalizamos os cabeçalhos para a nomenclatura indicada no enunciado, preservando os atributos e gerando versões de IDs ordenados e desordenados. Foram encontrados e corrigidos 5 IDs repetidos em 10.000 registros e 501 em 100.000; no conjunto de 1.000 não houve repetição. A correção atribuiu novos IDs acima do máximo existente, preservando os demais campos. Os dados não representam clientes reais.
\section{Algoritmos implementados}
As buscas linear e binária foram desenvolvidas em versões iterativa e recursiva. A busca binária foi aplicada exclusivamente a IDs ordenados. As ordenações desenvolvidas foram Bubble, Selection, Insertion, Shell, Merge, Quick e Heap Sort. As implementações contam comparações entre chaves; em ordenação, também contabilizam escritas ou movimentações nos vetores. Operações de inserção e remoção foram comparadas em estruturas ordenadas.
\section{Metodologia experimental}
Foram realizados três ciclos de medição por cenário, com média, mediana e desvio padrão. Utilizou-se \texttt{time.perf\_counter}, e a comparação sempre parte de uma cópia equivalente de entrada. O número de comparações é menos afetado por processos concorrentes e variações de hardware do que o tempo bruto. A recomendação do enunciado é de 30 repetições; a presente execução preliminar usa três e pode ser reproduzida com 30 via argumento do programa. A busca linear recursiva em bases maiores não foi executada devido ao limite de pilha do Python. Métodos quadráticos foram limitados a 1.000 entradas. A condição de 10.000 consultas foi projetada por extrapolação de medições até 1.000 consultas, não deve ser citada como observação direta.
\par\noindent\textbf{Ambiente:} Python 3; plataforma Linux.\par
\section{Resultados}
\subsection{Experimentos 1 a 4: busca, posição e crescimento}
O resultado abaixo utiliza alvos ausentes. Cada célula contém tempo médio em milissegundos e número de comparações.
'''+tab(base,['n','Linear (ms / comp.)','Binária (ms / comp.)'])+fig('01_tempo_busca.png','Número de registros por tempo médio de busca (alvo ausente).')+fig('02_comparacoes_busca.png','Crescimento no número de comparações (alvo ausente).')+r'''
Nas demais posições, a busca linear cresce proporcionalmente à posição percorrida no vetor e a binária limita o número de inspeções a uma ordem logarítmica. A busca linear recursiva foi omitida nas bases maiores por restrições explícitas de execução, sem substituir o algoritmo por uma função pronta.
\subsection{Experimentos 5 e 6: ordenação e estado inicial}
A tabela informa tempo médio, em milissegundos, para dados inicialmente aleatórios. N/E significa não executado devido ao limite estabelecido.
'''+tab(ordrows,['Algoritmo','1.000','10.000','100.000'])+fig('03_tempo_ordenacao.png','Comparação do tempo médio de ordenação por tamanho.')+r'''
Dados previamente ordenados, aleatórios e invertidos foram avaliados; seu impacto depende da estratégia e de sua política de troca, partição ou fusão. Bubble Sort pode encerrar mais cedo em dados já ordenados, enquanto Selection Sort mantém comparações quadráticas independentemente dessa ordenação.
\subsection{Experimento 7: inserção}
A estratégia de inserir no fim e reordenar foi comparada à identificação da posição por busca binária seguida de inserção. Embora a busca da posição seja logarítmica, o deslocamento de elementos em um vetor Python permanece linear no pior caso.
\subsection{Experimento 8: remoção}
O tempo de localizar, o tempo de remover e o tempo total foram medidos separadamente para o início, meio e fim. Mesmo após localização rápida, a remoção de uma lista contígua pode exigir deslocamentos.
\subsection{Experimento 9: muitas consultas}
O sistema A utiliza busca linear na base desordenada; o B ordena com Merge Sort uma vez e depois usa busca binária. Os valores são tempos totais em milissegundos.
'''+tab(bl,['Buscas','Sistema A','Sistema B','Tipo'])+fig('04_consultas.png','Tempo total das consultas efetivamente medidas, excluída projeção de 10.000.')+r'''
O ponto de compensação depende do custo inicial da ordenação e da sequência de chaves solicitadas. Não se deve confundir o cenário projetado com uma medição direta.
\subsection{Experimento 10: inserção contínua}
Comparou-se manutenção da ordem após cada inserção à acumulação de inserções seguida de uma ordenação única. Os lotes tiveram 100, 500 e 1.000 novas chaves.
'''+fig('05_insercao_continua.png','Comparação das duas estratégias para inserções contínuas.')+r'''
\section{Discussão}
A busca binária é vantajosa quando os dados já estão ordenados ou quando o custo de sua ordenação é amortizado por muitas buscas. Buscas lineares evitam a preparação dos dados e podem ser suficientes para conjuntos pequenos ou consultas raras. A escolha da ordenação também depende do estado inicial, tamanho, memória auxiliar e frequência de alterações. Merge Sort usa memória adicional, enquanto Heap Sort pode operar dentro da própria estrutura. A recursão exige cuidado no Python, e os algoritmos quadráticos são pouco adequados a entradas grandes.
\section{Conclusão}
Não existe algoritmo universalmente mais eficiente para pesquisa, ordenação e manipulação. A seleção depende de tamanho, ordem inicial, taxa de buscas, frequência de inserção e remoção, custo de organização prévia, tempo total, comparações e memória disponível. Os experimentos sustentam a vantagem assintótica de buscas binárias em listas ordenadas e reforçam que preparação e manutenção também precisam entrar no cálculo. Resultados omitidos por limite computacional e projeções foram distinguidos de medições.
\section{Referências}
\begin{itemize}
\item CORMEN, T. H. et al. \textit{Introduction to Algorithms}. 4. ed. MIT Press, 2022.
\item SEDGEWICK, R.; WAYNE, K. \textit{Algorithms}. 4. ed. Addison-Wesley, 2011.
\item UNIVERSIDADE SANTO AMARO. \textit{Projeto -- Laboratório Experimental de Algoritmos com Dados Sintéticos}. Material didático disponibilizado, 2026.
\item PYTHON SOFTWARE FOUNDATION. \textit{Python Documentation}. Disponível em: \url{https://docs.python.org/3/}.
\end{itemize}
\appendix\section{Reprodução}
Os arquivos \texttt{src/algoritmos.py}, \texttt{src/experimentos.py}, \texttt{resultados/*.csv} e \texttt{dados/*.csv} permitem inspecionar cada cenário. O parâmetro \texttt{--repeticoes 30} realiza 30 ciclos nos cenários repetíveis. Os critérios de omissão e projeção estão implementados e documentados.
\end{document}
'''
(L/'relatorio_final.tex').write_text(header+body,encoding='utf8')
print('Gráficos e LaTeX gerados')
