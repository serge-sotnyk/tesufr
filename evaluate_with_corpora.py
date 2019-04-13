from tesurf.corpora.providers import BbcNewsProvider, Krapivin2009Provider
from tesurf.keysum_evaluator import evaluate_processor_on_corpus
from tesurf import Processor


def evaluate_all_corpora():
    processor = Processor()
    corpus = BbcNewsProvider()
    metrics = evaluate_processor_on_corpus(processor, corpus, "BBC News")
    print(metrics)

    corpus = Krapivin2009Provider()
    metrics = evaluate_processor_on_corpus(processor, corpus, "Krapivin2009")
    print(metrics)


if __name__ == "__main__":
    evaluate_all_corpora()
