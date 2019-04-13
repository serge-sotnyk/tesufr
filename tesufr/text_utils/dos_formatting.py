from typing import List

_paragraph_terminators = {'\r', '\n', '\u2029'}


def is_text_dos_formatted(text: str) -> bool:
    lines_counter: int = 0
    suspect_lines_counter: int = 0
    for line in text.splitlines():
        line = line.strip()
        line_len = len(line)
        if line_len > 0:
            lines_counter += 1
            if 58 < line_len < 100:
                suspect_lines_counter += 1
    result = 2 * suspect_lines_counter > lines_counter
    return result


def remove_dos_formatting(text: str) -> str:
    res: List[str] = []
    prev_len: int = 0
    prev_end_with_hyphens: bool = False
    for line in text.splitlines():
        line = line.strip()
        line_len = len(line)
        if line_len > 0:
            if 58 < prev_len < 100:
                if prev_end_with_hyphens:
                    res[-1] = res[-1][:-1] + line
                else:
                    res[-1] = res[-1] + ' ' + line
            else:
                res.append(line)
        else:
            res.append(line)
        prev_len = line_len
        prev_end_with_hyphens = line.endswith('-')
    return '\n'.join(res)
