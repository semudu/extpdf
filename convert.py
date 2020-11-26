from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import re

def convert_pdf(path, format='text', codec='utf-8', password=''):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    laparams = LAParams()
    if format == 'text':
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    elif format == 'html':
        device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    elif format == 'xml':
        device = XMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    else:
        raise ValueError('provide format, either text, html or xml!')
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue().decode()
    fp.close()
    device.close()
    retstr.close()
    return text



if __name__ == "__main__":
    pdf_html = convert_pdf('/Users/semudu/Downloads/a.pdf',format = 'html')

    start_line_rgx = (r'<br><\/span><\/div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:20px; top:(\d+)px; width:88px; height:10px;"><span style="font-family: Helvetica-Bold; font-size:10px">HİSSE SENETLERİ')
    end_line_rgx = (r'<br><\/span><\/div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:160px; top:(\d+)px; width:43px; height:10px;"><span style="font-family: ArialMT; font-size:10px">TOPLAM:')
    stock_line_rgx = (r'<br><\/span><\/div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:(\d+)px; top:(\d+)px; width:\d+px; height:\d+px;"><span style="font-family: ArialMT; font-size:10px">([A-Z\s]+|(-?\d{1,3}(.?\d{3})*(\,\d{2}?)))')

    start_line = int(re.search(start_line_rgx, pdf_html, re.MULTILINE).group(1))
    end_line = int(re.search(end_line_rgx, pdf_html, re.MULTILINE).group(1))

    print(start_line)
    print(end_line)

    lines = re.finditer(stock_line_rgx, pdf_html, re.MULTILINE)

    for matchNum, match in enumerate(lines, start=1):
        if(int(match.group(2))>start_line and int(match.group(2))<end_line):
            print(match.group(3))
            
