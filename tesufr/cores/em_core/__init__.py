"""
Core, based on embeddings (BPemb), spacy models
- Keywords extraction: implementation of https://arxiv.org/pdf/1801.04470.pdf
"""

from .em_core import EmCore, construct_em_core
from .em_cores_wrapper import EmCoresWrapper
