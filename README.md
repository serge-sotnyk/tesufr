# tesufr
Multilingual Text Summarizing Framework

## Build package

python setup.py sdist

## Evaluate metrics

Currently, framework has two cores (FallbackCore and SummaCore) and two corpus 
providers (BbcNewsProvider and Krapivin2009Provider). Quality metrics for these
cores and corpora:

```
python.exe tesufr/evaluate_with_corpora.py
Check metrics for BBC News / FallbackCore
100%|██████████| 445/445 [00:10<00:00, 43.59it/s]
{'rouge_1': 0.5489569227407518, 'rouge_2': 0.44733345610434844, 'rouge_3': 0.4047945705861156, 'rouge_4': 0.3695602606075601, 'bleu': 41.611864189349895}
Check metrics for BBC News / SummaCore
100%|██████████| 445/445 [00:31<00:00, 14.65it/s]
{'rouge_1': 0.7736740467482042, 'rouge_2': 0.7057150991231917, 'rouge_3': 0.6553423520070746, 'rouge_4': 0.6053681996983519, 'bleu': 68.8648511166897}
Check metrics for Krapivin2009 / FallbackCore
100%|██████████| 461/461 [00:44<00:00, 11.13it/s]
{'precision': 0.4030932949690004, 'recall': 0.14229306838749253, 'f1': 0.20524058808381612, 'rouge_1': 0.024238965325505984, 'rouge_2': 0.008135379808691693, 'rouge_3': 0.003927411070078904, 'rouge_4': 0.0025979649815830105, 'bleu': 0.5387344660957267}
Check metrics for Krapivin2009 / SummaCore
100%|██████████| 461/461 [19:07<00:00,  2.26s/it]
{'precision': 0.202779777328585, 'recall': 0.17495413450880182, 'f1': 0.1809694582787395, 'rouge_1': 0.026164841589721592, 'rouge_2': 0.006921741294599503, 'rouge_3': 0.001973890294264275, 'rouge_4': 0.0007699996243221003, 'bleu': 0.37001081799842556}
```

Krapivin2009 corpus contains much longer texts, so the lower values for metrics
are expected.