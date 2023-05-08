EXTRACT_MAIN_SECTIONS = r"\d+\.\s\w+(?:[\w~˜çáàâãéèêíìîóòôõúùû]*)\s*\n"
EXTRACT_ABSTRACT = r"(?<=\n\nAbstract\. ).*?(?=\n\n)"
EXTRACT_SECTION_INTEVAL = r"(?<={start_section}).*?(?={end_section})"

TEMP_FILE_PATH = './temp/article.pdf'

SBC_SEARCH_STRING = '''
    https://sol.sbc.org.br/busca/index.php/integrada/results?
    isAdvanced=1
    &archiveIds%5B%5D=1
    &query={search_term_inside}
    &field-3={search_title}
    &field-15={search_summary}
    &field-4={search_authors}
    &field-14={search_keywords}
    &field-16={search_event_journal}
    &field-7-fromMonth={search_from_month}
    &field-7-fromDay={search_from_day}
    &field-7-fromYear={search_from_yaer}
    &field-7-toMonth={search_to_month}
    &field-7-toDay={search_to_day}
    &field-7-toYear={search_to_year}
'''