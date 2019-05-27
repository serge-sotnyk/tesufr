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
Check metrics for WikiHow / EmCore
100%|██████████| 2334/2334 [27:30<00:00,  1.32it/s]
{'rouge_1': 0.21221243842664408, 'rouge_2': 0.041996718039235534, 'rouge_3': 0.007889859419232238, 'rouge_4': 0.00150271803824145, 'bleu': 2.104255901427864}
Check metrics for WikiHow / FallbackCore
100%|██████████| 2334/2334 [02:06<00:00, 20.24it/s]
{'rouge_1': 0.1755649497246625, 'rouge_2': 0.02847542058470131, 'rouge_3': 0.005052340426484645, 'rouge_4': 0.0009938591938436366, 'bleu': 1.6123428232388846}
Check metrics for WikiHow / SummaCore
100%|██████████| 2334/2334 [13:58<00:00,  2.80it/s]
{'rouge_1': 0.2037257297679502, 'rouge_2': 0.041451172583973885, 'rouge_3': 0.007915307924970524, 'rouge_4': 0.001506414755712027, 'bleu': 2.021723020276366}
Check metrics for BBC News / EmCore
100%|██████████| 445/445 [01:13<00:00,  6.15it/s]
{'rouge_1': 0.7239626948735038, 'rouge_2': 0.6595887663951285, 'rouge_3': 0.6146782628817632, 'rouge_4': 0.570495358990877, 'bleu': 57.207885964100385}
Check metrics for BBC News / FallbackCore
100%|██████████| 445/445 [00:09<00:00, 45.98it/s]
{'rouge_1': 0.5489569227407518, 'rouge_2': 0.44733345610434844, 'rouge_3': 0.4047945705861156, 'rouge_4': 0.3695602606075601, 'bleu': 41.611864189349895}
Check metrics for BBC News / SummaCore
100%|██████████| 445/445 [00:33<00:00, 14.09it/s]
{'rouge_1': 0.7736740467482042, 'rouge_2': 0.7057150991231917, 'rouge_3': 0.6553423520070746, 'rouge_4': 0.6053681996983519, 'bleu': 68.8648511166897}
Check metrics for Krapivin2009 / EmCore
100%|██████████| 461/461 [27:19<00:00,  3.84s/it]
{'precision': 0.18000818793414078, 'recall': 0.1895432603789429, 'f1': 0.18275273220561422, 'rouge_1': 0.23216789604430094, 'rouge_2': 0.0671106638215793, 'rouge_3': 0.022922174857761858, 'rouge_4': 0.009808677744847692, 'bleu': 3.950225497248875}
Check metrics for Krapivin2009 / FallbackCore
100%|██████████| 461/461 [00:57<00:00,  6.58it/s]
{'precision': 0.3379095625240477, 'recall': 0.215303208679965, 'f1': 0.26007970955477006, 'rouge_1': 0.2032406108204436, 'rouge_2': 0.0640569919020275, 'rouge_3': 0.026070043742752593, 'rouge_4': 0.013915184246029402, 'bleu': 3.8588710947452083}
Check metrics for Krapivin2009 / SummaCore
100%|██████████| 461/461 [14:18<00:00,  2.04s/it]
{'precision': 0.1607479214868431, 'recall': 0.25338215049913665, 'f1': 0.1934375739042254, 'rouge_1': 0.23211195935064075, 'rouge_2': 0.06762135922056278, 'rouge_3': 0.023458390801289284, 'rouge_4': 0.010188675735886383, 'bleu': 3.966227280134763}
```

Krapivin2009 corpus contains much longer texts, so the lower values for metrics
are expected.