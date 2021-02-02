# CPApp
An all-in-one tool for optimising office paperwork management and other processes, specifically designed for sleep apnoea health practices. 

## Help guide for CPApp Version 1.0
CPApp has one main function: producing DVA receipt of purchase forms for sleep apnoea equipment across a variety of brands including Resmed and Philips Respironics. Below is a guide to navigating the web app.

### Contracts
This tab is the main page for producing DVA contracts. This is a brief outline of the contract process:
1. Enter your client name into the appropriate box and it will auto-fill the contract with this client's details. This is courtesy of the Coreplus API as found at [Coreplus Developers](https://developers.coreplus.com.au/).

2. Enter your product by searching through either reference number or key words in its form description. Upon click of the suggestion, reference and description will be auto-filled, and if any lots are available, it will prompt you for selection.
> Upon printing a contract, any new lots for products will be added. The next time any of these products are entered, the lot and date that it was added will be displayed. This is designed to help with unpackaged parts where lots are not readily available.

3. Customise additional options. This includes if a report, consultation and/or delivery is required, along with other codes. 

> New pages can be added such as a phone consult page or the delivery checklist page, also prefilled. Phone consults can be customised to include visits and reports or just visits. 

> Presets (all selecting phone consult and delivery checklist) are also available for standard delivery (report, visit, dist), rental machines (report, setup, dist), new clients (setup, dist, new client) or custom configurations. 

> Distance codes are automatically calculated using [Google Maps](https://pypi.org/project/googlemaps/).

4. Finally, press print and your generated pdf document will be served in a new tab!
### Products
This page can access the database of products that autocomplete in the contracts form. Enter your reference number of the product, and it will either add a new product if the ref is new, or update the exisiting product of that ref with whatever lot and description is provided. 

### Deliveries
This tab provides a text file of all clients printed since last cleared. To clear, press the red "Clear details" button, and to download, press the "Download details" button.

## Planned updates
1. Connect to AirView Exchange when it is available in Australia to dynamically produce Sleep Reports for clients. Overseas information for this product is available from [this document](https://document.resmed.com/documents/epn/10110364r1%20AirView%20Integration%20Solutions%20Brochure%20EMEA%20ENG%20LOW%20page2.pdf). 
2. Implement smart routing with the deliveries to optimise fuel, traffic and distance parameters. 
3. Depending on expansion opportunities, add sign in functionality for different offices/users, generating different apis and databases.

### Dependencies Acknowledgement
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) 
* [PyPdf2](https://pypi.org/project/PyPDF2/) and [pypdftk](https://pypi.org/project/pypdftk/)
* [Coreplus API](https://developers.coreplus.com.au/)
* Google Maps' [Python Framework](https://pypi.org/project/googlemaps/), using [Distance Matrix](https://developers.google.com/maps/documentation/distance-matrix/overview)
* Standard [Python](https://www.python.org/), [JSON](https://www.json.org/json-en.html), [Javascript Web Tokens](https://jwt.io/) and [HTTP Requests](https://requests.readthedocs.io/en/master/) libraries


