import os    
import winerror
from win32com.client.dynamic import Dispatch, ERRORS_BAD_CONTEXT

ERRORS_BAD_CONTEXT.append(winerror.E_NOTIMPL)
PDSaveLinearized = True
PDSaveFull = True


def pdf_to_html(filename):
    src = os.path.abspath(filename)

    try:
        AvDoc = Dispatch("AcroExch.AVDoc")

        if AvDoc.Open(src, ""):            
            pdDoc = AvDoc.GetPDDoc()
            jsObject = pdDoc.GetJSObject()
            jsObject.SaveAs("C:/Users/Administrator/Desktop/proj_para_split/htmls/" +filename+ ".html", "com.adobe.acrobat.html")

    except Exception as e:
        print(str(e))
        return "nodata"

    finally:        
        AvDoc.Close(True)

        jsObject = None
        pdDoc = None
        AvDoc = None

    return "htmls/" +filename+ ".html"