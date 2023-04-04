from stock.forms import RiderProductLoanModelForm
from stock.models import Order
from django.http import HttpResponse
from django.template.loader import render_to_string
# from weasyprint import HTML


class CartMixin:
    form_class = RiderProductLoanModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'], created = Order.objects.get_or_create(user=self.request.user, complete=False)
        context['product_loan_form'] = self.form_class()
        return context


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View


class GeneratePdfMixin(View):
    pdf_name = 'document'

    def get_pdf_data(self):
        raise NotImplementedError

    def get_pdf_name(self):
        return f"{self.pdf_name}.pdf"

    def get(self, request, *args, **kwargs):
        pdf_data = self.get_pdf_data().get('pdf')
        pdf_name = self.get_pdf_name()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'

        pdf_file = BytesIO(pdf_data)
        response.write(pdf_file.getvalue())
        pdf_file.close()

        return response
