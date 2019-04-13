from tesufr.models import *


def test_fragment():
    src = "a text "
    substr: str = 'text'    
    container = TextContainer(src)
    fragment = Fragment.fragment_with_len(container, src.find(substr), len(substr))
    assert fragment.text == substr
    assert len(fragment) == len(substr)
