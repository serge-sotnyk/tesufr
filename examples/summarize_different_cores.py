from tesufr import Processor, TextProcessParams, SummarySize
from tesufr.cores import SummaCore, FallbackCore
from tesufr.cores.em_core import EmCoresWrapper
from tesufr.corpora.providers import BbcNewsProvider, Krapivin2009Provider, LimitedProvider
from tesufr.keysum_evaluator import evaluate_processor_on_corpus
from tesufr.corpora import SetType, CorpusDocument, CorpusPurpose


def process_and_report(text, process_params, processor, title: str = ''):
    print(f"========= {title} =========")
    doc = processor.process_text(text, process_params)
    print("Keywords: "+' | '.join([str(kw) for kw in doc.keywords]))
    print(f"Summary ({len(doc.summary)}):")
    for s in doc.summary:
        print("* "+s.lemma)
    print()


def print_reference(sample: CorpusDocument):
    print("========= Sample document: =========")
    print("Keywords: "+' | '.join([str(kw) for kw in sample.ref_keywords]))
    print(f"Summary ({len(sample.ref_summary)}):")
    for s in sample.ref_summary:
        print("* "+s)
    print()


def main():
    processor_summa = Processor([SummaCore()])
    processor_em = Processor([EmCoresWrapper()])
    corpus = Krapivin2009Provider()
    sample = corpus.document_by_id(corpus.ids_train[74])

    process_params = TextProcessParams(SummarySize.new_absolute(len(sample.ref_summary)), len(sample.ref_keywords))
    print(process_params)
    print_reference(sample)

    process_and_report(sample.text, process_params, processor_summa, 'SummaCore')
    process_and_report(sample.text, process_params, processor_em, 'EmCoresWrapper')


if __name__=='__main__':
    main()
