from tesufr.text_utils.dos_formatting import is_text_dos_formatted, remove_dos_formatting

dos_formatted_text = """
Introduction
The problem of shape similarity has been extensively investigated in both machine vision
and biological vision. Although for human perception, different features such as shape,
color, reflectance, functional information play an important role while comparing objects,
in machine vision usually only geometric properties of shapes are used to introduce shape
similarity. In the literature, one finds two concepts for expressing the similarity of shapes:
distance functions measuring dissimilarity and similarity measures expressing how similar
two shapes are. In this paper we shall work with similarity measures.
In practice, similarity approaches have to be invariant under certain classes of transfor-
mations, e.g. similitudes (i.e., translations, rotations, change of scale). Affine transformations
are also of great practical value as these can approximate shape distortions arising
when an object is observed by a camera under arbitrary orientations with respect to the
image plane [1]. A well-known method to develop a similarity approach which is invariant
under a given class of transformations is to perform a shape normalization first [2], [3], [4].
In Subsection IV-C of this paper we discuss one particular method based on the ellipse of
inertia.
"""

not_dos_formatted_text = """
I have thousands of text files with data like the above and words have been wrapped using hyphens and newlines.

What I am trying to do is remove the hyphen and place the newline at the end of the word. I do not want to remove all hyphenated words if possible only those that are at the end of the line.
"""


def test_is_text_dos_formatted():
    result = is_text_dos_formatted(dos_formatted_text)
    assert result is True

    result = is_text_dos_formatted(not_dos_formatted_text)
    assert result is False


def test_remove_dos_formatting():
    actual = remove_dos_formatting(dos_formatted_text)
    assert len(actual.splitlines()) == 3
    assert actual.find('transformations,') > 0

    actual = remove_dos_formatting(not_dos_formatted_text)
    assert len(actual.splitlines()) == 4
