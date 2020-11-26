from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import re
from operator import itemgetter

def get_html_from_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec="utf-8", laparams=laparams)

    fp = open(path, 'rb')

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    html = retstr.getvalue().decode()
    fp.close()
    device.close()
    retstr.close()
    return html

if __name__ == "__main__":
    pdf_html = get_html_from_pdf('/Users/semudu/Downloads/a.pdf')

    start_line_rgx = (r'<br><\/span><\/div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:20px; top:(\d+)px; width:88px; height:10px;"><span style="font-family: Helvetica-Bold; font-size:10px">HİSSE SENETLERİ')
    end_line_rgx = (r'<br><\/span><\/div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:160px; top:(\d+)px; width:43px; height:10px;"><span style="font-family: ArialMT; font-size:10px">TOPLAM:')
    stock_line_rgx = (r'<br><\/span><\/div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:(\d+)px; top:(\d+)px; width:\d+px; height:\d+px;"><span style="font-family: ArialMT; font-size:\d+px">([\d\w\.\s\-\,]+)')

    start_line = int(re.search(start_line_rgx, pdf_html, re.MULTILINE).group(1))
    end_line = int(re.search(end_line_rgx, pdf_html, re.MULTILINE).group(1))

    lines = re.finditer(stock_line_rgx, pdf_html, re.MULTILINE)

    x = []

    for matchNum, match in enumerate(lines, start=1):
        if(int(match.group(2))>start_line and int(match.group(2))<end_line):
            x.append({"value":match.group(3),"top":int(match.group(2)),"left":int(match.group(1))})

    result = []
    y = {}

    for i in x:
        if i["top"] not in y:
            y[i["top"]] = []
        y[i["top"]].append(i)

    # for j in y:
    #     y[j] = sorted(y[j], key=lambda k: k["left"])
    #     print(y[j])        
    
    for j in y:
        y[j] = sorted(y[j], key=lambda k: k["left"])
        result.append({
            "name": y[j][0]["value"].replace("\n",""),
            "a": float(y[j][1]["value"].replace(".","").replace(",",".")),
            "b": float(y[j][2]["value"].replace(".","").replace(",",".")),
            "c": float(y[j][3]["value"].replace(".","").replace(",","."))
        })
    
    for j in result:
        print(j)

