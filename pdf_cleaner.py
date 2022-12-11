import fitz
print(fitz.__doc__)




def cleaner(filename):


    counter += 1
    doc = fitz.open(filename)
    if doc == None:
        return "nodata"

    number_of_pages = doc.page_count

    for page_no in range(0, number_of_pages):
        page = doc.load_page(page_no)

        page_widget = page.first_widget
        if page_widget == None:
            continue
        page_widget.reset()
        page_widget.update()

        while(True):
            current_widget = page_widget.next
            if current_widget == None:
                break
            else:
                current_widget.reset()
                current_widget.update()
    cleaned_filename = "pdfs/" +"2"+".pdf"
    doc.save(cleaned_filename)
    return cleaned_filename