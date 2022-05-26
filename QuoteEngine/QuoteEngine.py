from abc import ABC, abstractmethod
import docx
import csv
import subprocess
import tempfile
import os


class QuoteModel:
    """Quotemodell class encapsulates body and author of Quotes"""
    body = ''
    author = ''

    def __init__(self, body, author):
        self.body = body
        self.author = author

    def __str__(self):
        print(f"{self.body} - {self.author}")


class IngestorInterface(ABC):
    """Abstract base class for the Ingestor"""
    # abstract attribute for file extension
    @property
    @abstractmethod
    def file_extension(self):
        pass

    @classmethod
    def can_ingest(cls, path) -> bool:
        """
        Class method to check if the file can be ingested
        Input: path (String)
        Output: Boolean
        """
        file_ext = path.split('.')
        return file_ext[-1] == cls.file_extension

    @abstractmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Abstract method to parse the file
        """
        pass


class CsvIngestor(IngestorInterface):
    """Ingestor for csv input. Implements IngestorInterface"""
    file_extension = 'csv'

    # override abstract method
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Parses the input in form of a csv file to a
        list of QuoteModel objects
        input: path to csv (String)
        output: List of QuoteModel objects
        """
        quote_list = []
        with open(path, mode='r') as file:
            csv_file = csv.reader(file)
            for line in csv_file:
                quote_list.append(QuoteModel(line[0], line[1]))

        return quote_list


class DocxIngestor(IngestorInterface):
    """Ingestor for docx input. Implements IngestorInterface"""

    file_extension = 'docx'

    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Parses the input in form of a docx file to a
        list of QuoteModel objects
        input: path to docx (String)
        output: List of QuoteModel objects
        """
        quote_list = []
        doc = docx.Document(path)

        for para in doc.paragraphs:
            content = para.text.split('-')
            quote_list.append(QuoteModel(content[0], content[1]))

        return quote_list


class PdfIngestor(IngestorInterface):
    """Ingestor for pdf input. Implements IngestorInterface"""
    file_extension = ' pdf'

    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Method converts the pdf to text via subprocess and cli
        utility. The text is then ingested.
        Input: path to pdf file (string)
        Output: List of QuoteModel objects
        """
        quote_list = []
        # create temporary file for txt input
        # TODO check if this works on windods -> see tempfile doc
        # if not create txt file and delete manually after transfer
        temp = tempfile.NamedTemporaryFile(delete=True)
        temp_path = os.path.dirname(temp.name)

        # create cmd input for cli
        cmd = r"""{} "{}" "{}" -enc UTF-8""".format('pdftotext', path, temp_path)

        # call subprocess
        subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)

        # process txt
        with open(temp, 'r') as file:
            for line in file.readlines():
                content = line.split('-')
                quote_list.append(QuoteModel(content[0], content[1]))
        return quote_list


class TxtIngestor(IngestorInterface):
    """Ingestor for txt input. Implements IngestorInterface"""
    file_extension = 'txt'

    def parse(cls, path: str) -> list[QuoteModel]:
        """
        Parses the input in form of a txt file to a
        list of QuoteModel objects
        input: path to txt (String)
        output: List of QuoteModel objects
        """
        quote_list = []
        with open(path, 'r') as file:
            for line in file.readlines():
                content = line.split('-')
                quote_list.append(QuoteModel(content[0], content[1]))

        return quote_list


class Ingestor(IngestorInterface):
    """
    Ingestor class encapsulates the helper classes for the different file type
    (pdf, txt, csv, docx) and picks the Ingestor according to the file type. Realizes
    IngestorInterface
    """
    ingestors = [DocxIngestor, PdfIngestor, TxtIngestor, CsvIngestor]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Select appropriate helper for given file based on file type"""
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)