from corpora.providers import BbcNewsProvider
from keysum_evaluator import evaluate_processor_on_corpus
from tesurf import Processor


def evaluate_all_corpora():
    processor = Processor()
    corpus = BbcNewsProvider()
    metrics = evaluate_processor_on_corpus(processor, corpus)
    print(metrics)


if __name__ == "__main__":
    evaluate_all_corpora()
