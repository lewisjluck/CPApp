class Form :
    def __init__(self, client, products, new=False):
        self.client = client
        self.products = products
        self.new = new
    def make_pdf(self):
        from PyPDF2 import PdfFileReader, PdfFileWriter
        from PyPDF2.generic import NameObject, BooleanObject, IndirectObject
        from datetime import date

        form = PdfFileReader("static/pdf_templates/form.pdf")
        end_form = PdfFileReader("static/pdf_templates/end_page.pdf")
        fields = form.getFields(tree=None, retval=None, fileobj=None)
        field_names = list(fields.keys())[0:9]
        addresses = [self.client.address, "", ""]
        for (i, address) in enumerate(addresses):
            if len(address) > 25:
                for j in range(len(address.split())):
                    new = " ".join(address.split()[:-(j+1)])
                    if len(new) < 25 and not new == address:
                        addresses[i] = new
                        addresses[i+1] = " ".join(address.split()[-j-1:])
                        break
        field_values = [
        self.client.dva_num,
        self.client.first_name[0],
        self.client.last_name,
        self.client.suburb,
        self.client.state,
        self.client.postcode
        ]
        field_values[3:3] = addresses
        field_dict = dict(zip(field_names, map(lambda x:x.upper(), field_values)))
        end_fields = end_form.getFields(tree=None, retval=None, fileobj=None)
        end_field_names = list(end_fields.keys())
        end_field_values = [""] * 4
        index = 2 if self.new else 0
        current_date = date.today()
        end_field_values[index:index+1] = [self.client.first_name + " " + self.client.last_name, current_date.strftime("%d/%m/%Y")]
        end_field_dict = dict(zip(end_field_names, end_field_values))
        print("Main form fields: ", field_dict)
        print("End page fields: ", end_field_dict)
        writer = PdfFileWriter()
        writer.addPage(form.getPage(0))
        writer.updatePageFormFieldValues(writer.getPage(0), field_dict)
        writer.addPage(end_form.getPage(0))
        writer.updatePageFormFieldValues(writer.getPage(1), end_field_dict)
        if "/AcroForm" not in writer._root_object:
            writer._root_object.update({NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})
        writer._root_object["/AcroForm"][NameObject("/NeedAppearances")] = BooleanObject(True)
        with open("print.pdf", "wb") as output:
            writer.write(output)
            output.close()
