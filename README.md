# Laboratório Experimental de Algoritmos — UNISA (2026)

**Aluno:** Gustavo Alves Borges  
**RA:** 5682207  
**Curso:** Análise e Desenvolvimento de Sistemas (ADS), 4º semestre  
**Disciplina:** Técnicas de Programação  
**Instituição:** Universidade Santo Amaro (UNISA)

## Entregáveis

- [Relatório em PDF](relatorio/relatorio_final.pdf) — relatório com identificação acadêmica, gráficos e link para este repositório;
- [Código Python](src/) — quatro buscas, sete algoritmos de ordenação e dez experimentos;
- [Bases sintéticas](dados/) — 1.000, 10.000 e 100.000 registros, ordenados e desordenados;
- [Resultados das medições](resultados/) — CSVs de busca, ordenação, inserção, remoção e consultas;
- [Cinco gráficos](graficos/) — visualizações dos dados coletados.

## Reprodução

Python 3.11+:

```bash
python -m pip install -r requirements.txt
python src/testes.py
python src/preparar_dados.py
python src/experimentos.py --repeticoes 30
python src/gerar_relatorio.py
python -m pip install reportlab pillow
python src/gerar_pdf.py
```

O script `gerar_relatorio.py` gera os cinco gráficos e, quando o template LaTeX está disponível, também produz uma fonte LaTeX. O PDF identificado também pode ser produzido com o script `gerar_pdf.py`. A geração automatizada é configurada em [GitHub Actions](.github/workflows/gerar-pdf.yml).

## Método e limitações

As bases são sintéticas, com normalização das chaves únicas. O script original encontrou 5 IDs duplicados na base de 10 mil e 501 na de 100 mil e os reatribuiu.

Nos cenários computacionalmente viáveis, o experimento usa **30 repetições**, calculando média, mediana e desvio padrão. Os resultados de 1.000 e 10.000 buscas em lote realizam respectivamente **3 e 1 repetições**, devido ao custo computacional elevado da busca linear pura em 100 mil registros. Esses casos são medições diretas, **não projeções**. Algoritmos quadráticos foram limitados à base de 1.000 entradas, e a busca linear recursiva não foi executada nas bases grandes por restrição de profundidade recursiva.

Todas as restrições permanecem transparentes nos CSVs e no relatório; não se deve interpretar os casos limitados como 30 repetições.

## Repositório público

https://github.com/sudogustavo7-ship-it/unisa-laboratorio-algoritmos-mockaroo
