import re

from backend.constants import EXTRACT_MAIN_SECTIONS, EXTRACT_ABSTRACT, EXTRACT_SECTION_INTEVAL

def extract_text_rgx(pdf_text: str) -> str:
    """extracts summary and conclusion from text

    Args:
        pdf_text (str): full article text

    Returns:
        str: concated abstract and conclusion strings
    """
    sections = re.findall(pattern=EXTRACT_MAIN_SECTIONS, string=pdf_text)

    abstract = re.findall(pattern=EXTRACT_ABSTRACT, string=pdf_text, flags=re.DOTALL)[0].replace('\n', '')
    conclusion_section = re.findall(
        pattern=EXTRACT_SECTION_INTEVAL.format(start_section=sections[-2], end_section=sections[-1]),
        string=pdf_text,
        flags=re.DOTALL
    )[0].replace('\n', '')

    final_text = abstract+' '+conclusion_section

    return final_text
