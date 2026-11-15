# Laboratório Experimental de Algoritmos — UNISA (2026)

Projeto da disciplina Técnicas de Programação, com experimentos sobre busca, ordenação, inserção e remoção de dados sintéticos.

## Organização do pacote completo
- `src/algoritmos.py`: quatro buscas e sete algoritmos de ordenação.
- `src/preparar_dados.py`: adaptação e validação das bases.
- `src/experimentos.py`: dez experimentos.
- `src/testes.py`: verificações funcionais.
- `src/gerar_relatorio.py`: gráficos e relatório.
- `dados/`: bases em CSV.
- `resultados/`: métricas em CSV.
- `graficos/`: figuras.
- `relatorio/`: PDF e fontes LaTeX.

## Execução
Requer Python 3.10+ e matplotlib. Na raiz do projeto:

```bash
python src/testes.py
python src/preparar_dados.py
python src/experimentos.py --repeticoes 3
python src/gerar_relatorio.py
```

Para o plano completo de 30 repetições, use `--repeticoes 30`. Alguns casos grandes têm alto custo computacional.

## Limitações importantes
Os dados originais tinham IDs repetidos: 5 na base de 10.000 e 501 na de 100.000. Os scripts reatribuem os repetidos preservando os demais campos.

As medições do pacote foram realizadas com 3 repetições nos testes repetíveis, não 30. Bubble, Selection e Insertion foram limitados a 1.000 registros; busca linear recursiva, limitada pela pilha, a 1.000. O resultado para 10.000 consultas no experimento 9 é uma **projeção declarada**, não uma medição.

O repositório pode conter apenas parte dos arquivos enquanto o carregamento estiver em andamento. Para submissão acadêmica, o relatório em PDF e os CSVs completos devem acompanhar o código.

## Identificação acadêmica
Preencher nomes, RA, curso e turma na capa do relatório antes da entrega.
