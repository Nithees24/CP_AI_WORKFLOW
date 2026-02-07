import fitz

def extract_lines_from_pdf(pdf_path:str):
    """
    Extract lines from a PDF file, preservation of order of lines in maintained
    Returns a list of dictionaries  with text and page numbers

    :param pdf_path:D:\CP_AI_WORKFLOW\data\input.pdf
    :return:dict
    """

    document = fitz.open(pdf_path)

    extracted_lines = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")
        lines =  text.split("\n")

        for line in lines:
            clean_line = line.strip() #used to strip blank spaces and tab spaces
            if clean_line:
                extracted_lines.append({"text":clean_line, "page_number": page_number})

    return extracted_lines


"""
TEST BLOCK 


lines = extract_lines_from_pdf("D:\CP_AI_WORKFLOW\data\input.pdf")
for l in lines[:12]:
    print(l["page_number"])
    print(l["text"])
"""