import re
import wget

from selenium import webdriver
from selenium.webdriver.common.by import By
from pdfminer.high_level import extract_text

from transformers import PegasusForConditionalGeneration, PegasusTokenizer, pipeline

from backend.constants import (
    EXTRACT_MAIN_SECTIONS,
    TEMP_FILE_PATH,
    SBC_SEARCH_STRING,
    EXTRACT_ABSTRACT,
    EXTRACT_SECTION_INTEVAL
)


class ArticleSummarizer:

    def summarize_file(self, file_path, output_path) -> None:
        pdf_text = extract_text(file_path)

        sections = re.findall(pattern=EXTRACT_MAIN_SECTIONS, string=pdf_text)

        abstract = re.findall(pattern=EXTRACT_ABSTRACT, string=pdf_text, flags=re.DOTALL)[0].replace('\n', '')

        conclusion_section = re.findall(
            pattern=EXTRACT_SECTION_INTEVAL.format(start_section=sections[-2], end_section=sections[-1]),
            string=pdf_text,
            flags=re.DOTALL
        )[0].replace('\n', '')

        final_text = abstract+' '+conclusion_section

        model_name = 'google/pegasus-xsum'
        pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)

        """
            using pre_trained model to summarize, takes longer but more precise

            pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)
            tokens = pegasus_tokenizer(final_text, truncation=True, padding='longest', return_tensors='pt')
            encoded_symmary = pegasus_model.generate(**tokens)
            decoded_summary = pegasus_tokenizer.decode(encoded_symmary[0], skip_special_tokens=True)
        """

        """ using pipeline to summarize """
        summarizer = pipeline('summarization', model=model_name, tokenizer=pegasus_tokenizer, framework='pt')
        decoded_summary = summarizer(final_text, max_length=150, min_length=50)[0]['summary_text']

        with open(f'{output_path}/summary.txt', 'w') as output_file:
            output_file.write(decoded_summary)

    def summarize_search(
        self,
        search_title: str=' ',
        search_term_inside: str=' ',
        search_summary: str=' ',
        search_authors: str=' ',
        search_keywords: str=' ',
        search_event_journal: str=' ',
        search_from_month: str=' ',
        search_from_day: str=' ',
        search_from_yaer: str=' ',
        search_to_month: str=' ',
        search_to_day: str=' ',
        search_to_year: str=' '
    ) -> None:

        driver=webdriver.Firefox()

        driver.get(SBC_SEARCH_STRING.format(
            search_term_inside=search_term_inside, search_title=search_title, search_summary=search_summary,
            search_authors=search_authors, search_keywords=search_keywords, search_event_journal=search_event_journal,
            search_from_month=search_from_month, search_from_day=search_from_day, search_from_yaer=search_from_yaer,
            search_to_month=search_to_month, search_to_day=search_to_day, search_to_year=search_to_year
        ))

        article = driver.find_element(By.CLASS_NAME, 'record_title')
        article_link = article.get_attribute('href')

        driver.get(article_link)

        web_view = driver.find_element(By.CLASS_NAME, 'obj_galley_link')
        web_view_link = web_view.get_attribute('href').replace('view', 'download')

        wget.download(web_view_link, TEMP_FILE_PATH)

        driver.close()

        self.summarize_file(file_path=TEMP_FILE_PATH)
