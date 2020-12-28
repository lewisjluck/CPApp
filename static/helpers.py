class Client :
    #Initialise a client with appropriate details
    def __init__(self, first_name, last_name, dva_num, address, suburb, state, postcode, number):
        self.first_name = first_name
        self.last_name = last_name
        self.dva_num = dva_num
        self.address = address
        self.suburb = suburb
        self.state = state
        self.postcode = postcode
        self.number = number

class Product:
    #Initialise a product with appropriate details
    def __init__(self, reference, lot, quantity, description):
        self.reference = reference
        self.lot = lot
        self.quantity = quantity
        self.description = description

class Form:
    #Initialise a form with a Client, a list of Products, and options
    def __init__(self, client, products, options, new):
        self.client = client
        self.products = products
        self.options = options
        self.new = new

    def find_distance(self):
        #Import API libaries
        import googlemaps

        #CPAP Select Work Address
        ORIGIN = "737 Logan Road Greenslopes QLD"

        #Google Maps API Key
        GOOGLE_MAPS_API_KEY = "AIzaSyCSk58iSStU1iZCRWAlvXmmhArg0HOAYdA"

        #Find distance between origin and form address using Google Maps API
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        distances = gmaps.distance_matrix(ORIGIN, self.client.address + self.client.suburb + self.client.state)

        #Try to use distance to output appropriate reference
        try:
            dist = distances["rows"][0]["elements"][0]["distance"]["value"] * 2
            if dist < 50000:
                distance = 50
            elif dist >= 50000 and dist < 100000:
                distance = 100
            elif dist >= 100000 and dist < 200000:
                distance = 200
            elif dist >=200000:
                distance = 201

            return str(distance) + "DIST"

        #If address is not found, will return reference of "ERROR" and print an error message
        except:
            print("Location not found, as per matrix: \n", distances)
            return "ERROR"

    def make_pdf(self):
        #Import dependencies
        from PyPDF2 import PdfFileReader, PdfFileWriter
        from PyPDF2.generic import NameObject, BooleanObject, IndirectObject
        from datetime import date

        #Product codes for frequent service products
        SERVICE_PRODUCTS = {
            "report":["REPORT-PAP", "SERVICE CLINICAL", "1", "PAP COMPLIANCE DOWNLOAD REPORT"],
            "visit":["VISIT-PAP", "SERVICE CLINICAL", "1", "PAP CONSULTATION"],
            "delivery":[self.find_distance(), "SERVICE TRAVEL", "1", "DELIVERY"],
            "setup":["SETUP-PAP", "SERVICE CLINICAL", "1", "PAP SETUP AND COMPLIANCE"]
        }

        #Read pdf templates using PyPDF2
        form = PdfFileReader("static/pdf_templates/form.pdf")

        #Get main form field names from pdf reader
        fields = form.getFields(tree=None, retval=None, fileobj=None)
        field_names = list(fields.keys())
        print(field_names)

        #Format address appropriately across the three fields
        addresses = [self.client.address, "", ""]
        for (i, address) in enumerate(addresses):
            if len(address) > 25:
                for j in range(len(address.split())):
                    new = " ".join(address.split()[:-(j+1)])
                    if len(new) < 25 and not new == address:
                        addresses[i] = new
                        addresses[i+1] = " ".join(address.split()[-j-1:])
                        break

        #Assign main details to values
        field_values = [
        self.client.dva_num,
        self.client.first_name[0],
        self.client.last_name,
        self.client.suburb,
        self.client.state,
        self.client.postcode,
        ""
        ]
        field_values[3:3] = addresses

        #Fill in products
        for product in self.products:
            field_values += [product.reference, product.lot, product.quantity, product.description]

        #Fill in service products using option settings
        for option, setting in self.options.items():
            if setting:
                field_values += SERVICE_PRODUCTS[option]

        #Pad out unused fields, zip into dict for writing
        field_values += [""] * (len(field_names) - len(field_values))
        field_dict = dict(zip(field_names, map(lambda x:x.upper(), field_values)))

        #Get pdf templates using PyPDF2
        end_form = PdfFileReader("static/pdf_templates/end_page.pdf")

        #Get end form fields from reader
        end_fields = end_form.getFields(tree=None, retval=None, fileobj=None)
        end_field_names = list(end_fields.keys())

        #Populate end field values with name and date, position depending on options
        end_field_values = [""] * 4
        index = 2 if self.new else 0
        current_date = date.today()
        end_field_values[index:index+1] = [self.client.first_name + " " + self.client.last_name, current_date.strftime("%d/%m/%Y")]

        #Zip end field values and names into dict
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
