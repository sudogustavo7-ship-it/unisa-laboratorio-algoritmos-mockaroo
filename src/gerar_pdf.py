"""Gera relatório PDF reproduzível a partir dos CSVs e gráficos do repositório."""
from pathlib import Path
from xml.sax.saxutils import escape
import csv
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/'relatorio'/'relatorio_final.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
ss=getSampleStyleSheet()
ss.add(ParagraphStyle(name='TituloAcad',parent=ss['Title'],fontSize=20,leading=26,textColor=colors.HexColor('#163C69'),spaceAfter=15))
ss.add(ParagraphStyle(name='SecaoAcad',parent=ss['Heading2'],fontSize=13,leading=17,textColor=colors.HexColor('#163C69'),spaceBefore=12,spaceAfter=8))
ss.add(ParagraphStyle(name='CorpoAcad',parent=ss['BodyText'],fontSize=10.2,leading=15,spaceAfter=9))
ss.add(ParagraphStyle(name='LegendaAcad',parent=ss['BodyText'],fontSize=9,leading=12,alignment=TA_CENTER,spaceAfter=13))
story=[]
def p(t):story.append(Paragraph(t,ss['CorpoAcad']))
def h(t):story.append(Paragraph(t,ss['SecaoAcad']))
def tbl(rows,widths=None):
    t=Table([[str(v) for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='CENTER')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#163C69')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),('LEADING',(0,0),(-1,-1),10),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#EFF4F8')]),('GRID',(0,0),(-1,-1),.25,colors.lightgrey),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(t);story.append(Spacer(1,12))
def figure(filename,label):
    path=BASE/'graficos'/filename
    if path.exists():
        from PIL import Image as PI
        w,hh=PI.open(path).size
        avail=16*cm; im=Image(str(path),width=avail,height=avail*hh/w);story.append(im)
        story.append(Paragraph(label,ss['LegendaAcad']))
def read(name):
    with (BASE/'resultados'/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
search=read('buscas.csv');sorts=read('ordenacoes.csv');many=read('muitas_consultas.csv')
def row(data,**criteria):
    return next((x for x in data if all(x.get(k)==str(v) for k,v in criteria.items())),None)
story.append(Spacer(1,3.3*cm))
story.append(Paragraph('UNIVERSIDADE SANTO AMARO - UNISA',ss['TituloAcad']))
p('<b>Disciplina:</b> Técnicas de Programação | <b>Ano:</b> 2026')
story.append(Spacer(1,2*cm))
story.append(Paragraph('Laboratório Experimental de Algoritmos com Dados Sintéticos',ss['TituloAcad']))
story.append(Spacer(1,2*cm))
p('<b>Aluno:</b> Gustavo Alves Borges')
p('<b>RA:</b> 5682207')
p('<b>Curso:</b> Análise e Desenvolvimento de Sistemas (ADS)')
p('<b>Semestre:</b> 4º')
p('<b>Repositório do projeto:</b> https://github.com/sudogustavo7-ship-it/unisa-laboratorio-algoritmos-mockaroo')
story.append(Spacer(1,2*cm));p('São Paulo - 2026')
story.append(PageBreak())
h('Resumo')
p('Este estudo analisa experimentalmente algoritmos de busca, ordenação e manipulação de dados por meio de bases sintéticas com 1.000, 10.000 e 100.000 registros. Foram implementadas quatro buscas e sete ordenações em Python, além de testes de inserção, remoção e consultas em lote. Os tempos e comparações foram registrados em CSV e apresentados em gráficos. Os limites de repetição e tamanho de entrada são explicitados na metodologia.')
h('1. Introdução')
p('O desempenho de um algoritmo depende da quantidade de registros, da ordenação inicial da estrutura, do tipo e frequência de operações e dos custos de preparação. A questão central do projeto é se existe um algoritmo universalmente mais eficiente para pesquisar, ordenar e manipular dados.')
h('2. Base de dados')
p('Os arquivos de dados sintéticos de clientes contêm ID, nome, idade, cidade, estado, data de cadastro, número de compras e valor total. Foram mantidas versões ordenadas e desordenadas para cada tamanho de base. Para assegurar IDs únicos, foram corrigidas 5 repetições na base com 10.000 entradas e 501 na base com 100.000 entradas. O procedimento de normalização é reproduzível no script preparar_dados.py.')
h('3. Algoritmos implementados')
p('<b>Busca:</b> linear iterativa e recursiva, binária iterativa e recursiva. <b>Ordenação:</b> Bubble Sort, Selection Sort, Insertion Sort, Shell Sort, Merge Sort, Quick Sort e Heap Sort. As contagens de comparações e movimentações foram incorporadas às implementações, sem substituir os métodos obrigatórios por funções prontas de ordenação ou busca.')
h('4. Metodologia')
p('Os cenários computacionalmente viáveis foram medidos em 30 repetições, calculando média, mediana e desvio padrão com time.perf_counter. As condições de 1.000 e 10.000 consultas lineares exigiram respectivamente 3 e 1 repetições por alto custo computacional. Os métodos quadráticos ficaram limitados a 1.000 elementos e a busca linear recursiva não foi executada nas bases maiores devido ao limite de pilha. Nenhuma projeção é apresentada como medição.')
h('5. Resultados: buscas (experimentos 1 a 4)')
rows=[['Registros','Linear (ms)','Linear (comp.)','Binária (ms)','Binária (comp.)']]
for n in [1000,10000,100000]:
    a=row(search,n=n,cenario='ausente',algoritmo='linear')
    b=row(search,n=n,cenario='ausente',algoritmo='binaria')
    if a and b:rows.append([n,f"{float(a['media_ms']):.3f}",a['comparacoes'],f"{float(b['media_ms']):.3f}",b['comparacoes']])
tbl(rows,[2.2*cm,3*cm,3*cm,3*cm,3*cm])
figure('01_tempo_busca.png','Figura 1 - Tamanho da base e tempo de busca.')
figure('02_comparacoes_busca.png','Figura 2 - Tamanho da base e comparações.')
p('Em um alvo ausente, a busca linear pode percorrer todos os registros, enquanto a binária exige poucos passos em uma sequência ordenada. As posições de início, 25%, 50%, 75% e final, além da ausência, estão detalhadas em resultados/buscas.csv.')
h('6. Resultados: ordenação (experimentos 5 e 6)')
rows=[['Algoritmo','1.000 (ms)','10.000 (ms)','100.000 (ms)']]
for algo in ['bubble','selection','insertion','shell','merge','quick','heap']:
    vals=[]
    for n in [1000,10000,100000]:
        q=row(sorts,n=n,cenario='aleatorio',algoritmo=algo)
        vals.append(f"{float(q['media_ms']):.3f}" if q and q.get('status')=='medido' else 'N/E')
    rows.append([algo,*vals])
tbl(rows,[4*cm,3.5*cm,3.5*cm,3.5*cm])
figure('03_tempo_ordenacao.png','Figura 3 - Tempos de ordenação, com escala logarítmica.')
p('A influência do estado inicial é diferente entre os métodos: Bubble Sort pode encerrar cedo sobre dados já ordenados, enquanto Selection Sort segue comparando pares independentemente da ordem de entrada. Os CSVs incluem entradas aleatórias, ordenadas e inversas.')
h('7. Inserção e remoção (experimentos 7 e 8)')
p('Na inserção, foram comparadas a estratégia de acrescentar uma chave ao fim e reordenar a estrutura e a de encontrar por busca binária a posição apropriada e inserir mantendo a ordem. Na remoção, registraram-se separadamente os tempos de localização, retirada e operação total nas regiões inicial, central e final. A busca binária pode ser logarítmica, mas a lista contígua ainda incorre em deslocamento de elementos.')
h('8. Muitas consultas (experimento 9)')
p('Foram comparados o sistema A, com dados desordenados e buscas lineares, e o sistema B, que ordena uma vez com Merge Sort e executa buscas binárias.')
rows=[['Consultas','Sistema A (ms)','Sistema B (ms)','Tipo']]
for n in [1,10,100,1000,10000]:
    a=row(many,quantidade_buscas=n,sistema='A_linear')
    b=row(many,quantidade_buscas=n,sistema='B_merge_binaria')
    if a and b:rows.append([n,f"{float(a['tempo_total_ms']):.2f}",f"{float(b['tempo_total_ms']):.2f}",'1 repetição' if n==10000 else ('3 repetições' if n==1000 else '30 repetições')])
tbl(rows,[2.3*cm,4*cm,4*cm,3.8*cm])
figure('04_consultas.png','Figura 4 - Custo total conforme a quantidade de consultas medidas.')
p('A ordenação inicial torna o sistema B mais caro para poucas consultas, mas esse custo pode ser amortizado à medida que o número de buscas aumenta. O cenário de 10.000 consultas contém medição direta com uma repetição; por isso deve ser interpretado com cautela.')
h('9. Inserção contínua (experimento 10)')
p('Foram comparadas sequências de 100, 500 e 1.000 inserções com manutenção imediata da ordem e inserção em lote seguida de reordenação.')
figure('05_insercao_continua.png','Figura 5 - Estratégias de inserção contínua.')
h('10. Discussão e conclusão')
p('Não existe algoritmo universalmente mais eficiente. Quando os dados já estão ordenados ou há muitas consultas, a busca binária tende a oferecer vantagem em comparações. Para bases pequenas e consultas esporádicas, a busca linear dispensa preparação prévia. Ordenações quadráticas crescem rapidamente com o tamanho; alternativas eficientes são mais adequadas a bases grandes, mas seus requisitos de memória e custos de manutenção também importam. Frequência de inserções e remoções pode alterar a escolha ideal. A interpretação dos resultados respeita as limitações declaradas de repetição, tamanho e profundidade de recursão.')
h('Referências')
p('CORMEN, T. H. et al. Introduction to Algorithms. 4. ed. MIT Press, 2022.')
p('SEDGEWICK, R.; WAYNE, K. Algorithms. 4. ed. Addison-Wesley, 2011.')
p('UNIVERSIDADE SANTO AMARO. Projeto - Laboratório Experimental de Algoritmos com Dados Sintéticos. 2026.')
p('PYTHON SOFTWARE FOUNDATION. Python Documentation. https://docs.python.org/3/.')
h('Apêndice: reprodução')
p('Execute python src/testes.py, python src/preparar_dados.py, python src/experimentos.py --repeticoes 30. As métricas coletadas são preservadas em resultados/*.csv; o script aplica limites expressos para os cenários de custo elevado. O projeto deve ser interpretado com as limitações claramente registradas neste relatório. Código e dados: https://github.com/sudogustavo7-ship-it/unisa-laboratorio-algoritmos-mockaroo')
def footer(canvas,doc):
    canvas.saveState();canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#536275'))
    canvas.drawString(2.4*cm,1.3*cm,'UNISA | Técnicas de Programação')
    canvas.drawRightString(19.1*cm,1.3*cm,str(doc.page));canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=2.4*cm,leftMargin=2.4*cm,topMargin=2.1*cm,bottomMargin=2.2*cm,title='Laboratório Experimental de Algoritmos - Gustavo Alves Borges')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('PDF gerado:',OUT)
