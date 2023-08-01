from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class PDFGeneratorMixin:
    def generate_pdf_response(self, objects, context, template_path, filename):
        # Prepare the context with the provided objects
        context['objects'] = objects

        # Load the template for the PDF using Django's template loader
        template = get_template(template_path)

        # Render the template with the context data to generate HTML content
        html = template.render(context)

        # Create a file-like buffer to receive PDF data
        buffer = BytesIO()

        # Generate the PDF from the HTML content
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), buffer)

        if not pdf.err:
            # Get the value of the BytesIO buffer and close it
            pdf_value = buffer.getvalue()
            buffer.close()

            # Create an HttpResponse with the PDF content
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'filename="{filename}.pdf"'
            response.write(pdf_value)
            return response

        return HttpResponse('Error generating PDF!')
