from tesufr import Processor
from tesufr.cores import SummaCore, FallbackCore
from tesufr.cores.em_core import EmCoresWrapper
from tesufr.corpora.providers import BbcNewsProvider, Krapivin2009Provider, LimitedProvider
from tesufr.keysum_evaluator import evaluate_processor_on_corpus


def evaluate_all_corpora():
    processor_baseline = Processor([FallbackCore()])
    processor_summa = Processor([SummaCore()])
    processor_em = Processor([EmCoresWrapper()])

    corpus = BbcNewsProvider()
    metrics = evaluate_processor_on_corpus(processor_em, corpus, "BBC News / EmCore")
    print(metrics)
    metrics = evaluate_processor_on_corpus(processor_baseline, corpus, "BBC News / FallbackCore")
    print(metrics)
    metrics = evaluate_processor_on_corpus(processor_summa, corpus, "BBC News / SummaCore")
    print(metrics)

    corpus = LimitedProvider(Krapivin2009Provider(), 30)
    #corpus = Krapivin2009Provider()
    metrics = evaluate_processor_on_corpus(processor_em, corpus, "Krapivin2009 / EmCore")
    print(metrics)
    metrics = evaluate_processor_on_corpus(processor_baseline, corpus, "Krapivin2009 / FallbackCore")
    print(metrics)
    metrics = evaluate_processor_on_corpus(processor_summa, corpus, "Krapivin2009 / SummaCore")
    print(metrics)


if __name__ == "__main__":

    evaluate_all_corpora()
