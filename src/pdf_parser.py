import os
from pathlib import Path
import itertools
import logging
import argparse
import pdftotext
import pandas as PDF


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(path_folder: str, path_output: str) -> None:

    list_files = os.listdir(PATH_FOLDER)

    # Load PDFs
    paragraphs = []
    docs = []
    pages = []

    regex_split = ".\n"

    for i, pdf_file in enumerate(list_files):
        with open(Path(PATH_FOLDER, pdf_file), "rb") as f:
            pdf = pdftotext.PDF(f)
            for i_page, page in enumerate(pdf):
            paras = page.split(regex_split)
            paragraphs.extend(paras)
            docs.extend([pdf_file] * len(paras))
            pages.extend([i_page+1] * len(paras))

    df = pd.DataFrame({
        "source": docs,
        "source_page": pages,
        "source_content": paragraphs
    })
    df.to_csv(path_output)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Script to parse PDFs")
    parser.add_argument("--path-folder", type=str, help="Path where PDFs are")
    parser.add_argument("--path-output", type=str, help="Path where to save the output csv")

    args = parser.parse_args()

    main(args.path_folder, args.path_output)

