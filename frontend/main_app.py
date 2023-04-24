import customtkinter
from customtkinter import filedialog

from backend.file_scrapper import ArticleSummarizer

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

# TODO add progress bar to summazing process
class App(customtkinter.CTk):
    file_path = None
    output_path = None
    article_summarizer = ArticleSummarizer()

    def __init__(self):
        super().__init__()

        self.title('AutoResumo')
        self.minsize(400, 300)

        self.title_lebel = customtkinter.CTkLabel(master=self, text="AutoResumo", font=('roboto', 25))
        self.title_lebel.pack(padx=20, pady=5)

        self.sub_title_label = customtkinter.CTkLabel(master=self, text="sistema web para automação de resumos com processamento de linguagem natural", font=('roboto', 11))
        self.sub_title_label.pack(padx=20, pady=3)

        self.select_article_button = customtkinter.CTkButton(
            master=self,
            command=self.select_file_path,
            text='escolha artigo',
            font=('roboto', 13.5)
        )
        self.select_article_button.pack(padx=20, pady=15)

        self.chosen_input_label = customtkinter.CTkLabel(master=self, text="Escolha artigo a ser resumido", font=('roboto', 13.5))
        self.chosen_input_label.pack(padx=20, pady=5)

        self.select_output_button = customtkinter.CTkButton(
            master=self,
            command=self.select_output_path,
            text='escolha local de saide de pdf',
            font=('roboto', 13.5)
        )
        self.select_output_button.pack(padx=20, pady=15)

        self.chosen_output_label = customtkinter.CTkLabel(master=self, text="escolha local se salvamento do resumo", font=('roboto', 13.5))
        self.chosen_output_label.pack(padx=20, pady=5)

        self.button = customtkinter.CTkButton(master=self, command=self.sum_article, text="Resumir", font=('roboto', 15))
        self.button.pack(padx=20, pady=20)

    def select_file_path(self) -> None:
        """selects file path to be summarized"""
        file_path = filedialog.askopenfilename(
            initialdir="~/",
            title="Select a article",
            filetypes=(("Articles", "*.pdf*"), ("all files", "*.*"))
        )
        self.file_path = file_path
        self.chosen_input_label.configure(text=file_path)

    def select_output_path(self) -> None:
        """selects directory path to dump file summarize output file"""
        file_path = filedialog.askdirectory(
            initialdir="~/",
            title="Select a article",
            mustexist=True
        )
        self.output_path = file_path
        self.chosen_output_label.configure(text=file_path)

    def sum_article(self):
        """calls summarizer"""
        self.article_summarizer.summarize_file(file_path=self.file_path, output_path=self.output_path)
