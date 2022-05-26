# MemeGenerator
Final Project for Udacity's "Intermediate Python" Nanodegree. 

## Overview
The meme generator will generate random memes according to an input of quotes and pictures.

## Setting up and running the programm

## Roles and Responsibilities

### QuoteEngine Package
The Quote Engine module is responsible for ingesting many types of files that contain quotes. For our purposes, a quote contains a body and an author:

> "This is a quote" - Author

Quotes are represented by QuoteModel objects, which encapsulate body and author of a quote. QuoteModel objects are generated by parsing input files. Supported file types are pdf, txt, docx and csv. The different file types have their own ingestor and parse methods. The ingestors realize the abstract IngestorInterface and are encapsulated by the Ingestor class. This class checks input files with the class method "can_ingest" and the corresponding file extension and decideds if they can be parsed. If so the correct Ingestor implementation is selected.

#### CsvIngestor
The csv file is read using pandas and saved in a dataframe. The quotes are read from the dataframe and saved to a list of QuoteModel objects.

#### DocxIngestor
The docx file is read using py-docx package. The quotes are saved to a list of QuoteModel objects.

#### PdfIngestor
The PDFIngestor class utilizes the subprocess module to call the pdftotext CLI utility—creating a pipeline that converts PDFs to text and then ingests the text.

#### TxtIngestor
The TxtIngestor uses the built-in capabilities of python without using another package. The quotes are read and saved to a list of QuoteModel objects.

#### Ingestor
Ingestor class encapsulates the helper classes for the different file type (pdf, txt, csv, docx) and picks the Ingestor according to the file type. Realizes IngestorInterface

### MemeEnginge
The Meme Engine Module is responsible for manipulating and drawing text onto images. The
