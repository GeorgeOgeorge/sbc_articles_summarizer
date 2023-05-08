import wget

from selenium import webdriver
from selenium.webdriver.common.by import By
from pdfminer.high_level import extract_text
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
from langdetect import detect as detect_lang

from backend.constants import TEMP_FILE_PATH, SBC_SEARCH_STRING
from backend.utils import extract_text_rgx


class ArticleSummarizer:

    def summarize_file(self, file_path: str, output_path: str) -> None:
        """summraizes articles and creates a text file as output
            Accepted langueges: pt, en

        Args:
            file_path (str): article path
            output_path (str): directory path for output text file
        """
        summarize_text = {
            'pt': self.summarize_pt,
            'en': self.summarize_en
        }

        pdf_text = extract_text(file_path)
        text_lang = detect_lang(final_text)

        breakpoint()
        final_text = extract_text_rgx(pdf_text)

        min_tokens = int(len(final_text.split(" ")) * 0.6)
        max_tokens = int(len(final_text.split(" ")) * 0.7)

        decoded_summary = summarize_text[text_lang](final_text, max_tokens, min_tokens)

        with open(f'{output_path}/summary.txt', 'w') as output_file:
            output_file.write("\n-----------------texto orignial-----------------\n")
            output_file.write(final_text)
            output_file.write("\n-----------------texto resumido-----------------\n")
            output_file.write(decoded_summary)

    def summarize_en(self, final_text: str, max_tokens: int, min_tokens: int) -> str:
        """ summarizes text on english

        Args:
            final_text (str): text to be summarized
            max_tokens (int): max number of tokens(words) to be summarized
            min_tokens (int): min number of tokens(words) to be summarized

        Returns:
            str: summaried
        """
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        decoded_summary = summarizer(final_text, max_length=max_tokens, min_length=min_tokens, do_sample=False)

        return decoded_summary[0]['summary_text']

    def summarize_pt(self, final_text: str, min_tokens: int, max_tokens: int) -> str:
        """ summarizes text on portuguese

        Args:
            final_text (str): text to be summarized
            min_tokens (int): max number of tokens(words) to be summarized
            max_tokens (int): min number of tokens(words) to be summarized

        Returns:
            str: summaried
        """
        token_name = 'unicamp-dl/ptt5-base-portuguese-vocab'
        model_name = 'phpaiola/ptt5-base-summ-xlsum'

        tokenizer = T5Tokenizer.from_pretrained(token_name)
        model_pt = T5ForConditionalGeneration.from_pretrained(model_name)

        inputs = tokenizer.encode(final_text, max_length=max_tokens, truncation=True, return_tensors='pt')
        summary_ids = model_pt.generate(
            inputs,
            max_length=max_tokens,
            min_length=min_tokens,
            num_beams=5,
            no_repeat_ngram_size=3,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0])

        return summary

    def article_search(
        self,
        search_title: str = ' ',
        search_term_inside: str = ' ',
        search_summary: str = ' ',
        search_authors: str = ' ',
        search_keywords: str = ' ',
        search_event_journal: str = ' ',
        search_from_month: str = ' ',
        search_from_day: str = ' ',
        search_from_yaer: str = ' ',
        search_to_month: str = ' ',
        search_to_day: str = ' ',
        search_to_year: str = ' '
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
