from django.views.generic import ListView
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from .forms import *
from django.shortcuts import get_object_or_404, render
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import SupplyTender
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.urls import reverse_lazy




def supplier(request):
    user = request.user
    all_tenders_count = SupplyTender.objects.filter( user=user).count()
    pending_tenders_count = SupplyTender.objects.filter(tender_status='Pending', user=user).count()
    complete_tenders_count = SupplyTender.objects.filter(tender_status='Complete', user=user).count()
    context = {
        'all_tenders_count': all_tenders_count,
        'pending_tenders_count': pending_tenders_count,
        'complete_tenders_count': complete_tenders_count,
    }
    return render(request, 'supplier/index.html', context=context)




class SupplyTenderCreateView(CreateView):
    model = SupplyTender
    form_class = SupplyTenderForm
    template_name = 'supplier/create_tender.html'
    success_url = reverse_lazy('supplier:pending-tenders')

    def form_valid(self, form):
        return super().form_valid(form)


class PendingSupplyTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/pending_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        return SupplyTender.objects.filter(tender_status='Pending')


from .models import SupplyTender

class PendingTenderListView(LoginRequiredMixin, ListView):
    model = SupplyTender
    template_name = 'supplier/supplier_pending_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Pending' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Pending')

    def post(self, request, *args, **kwargs):
        tender_id = request.POST.get('tender_id')
        price = request.POST.get('price')

        if tender_id and price:
            # Update the SupplyTender object with the provided price and change the tender_status to 'Supplied'
            tender = SupplyTender.objects.get(id=tender_id)
            tender.price = price



            tender.tender_status = 'Accepted'
            tender.user = request.user  # set the supplied_by attribute to the current user
            tender.save()
            messages.success(request, '{} Thanks for acccepting our tender request.Please  Wait for confirmation.'.format(request.user.get_full_name()))
    
        return redirect('supplier:supplier_pending_tenders')

# class PendingApprovalTenderListView(ListView):
#     model = SupplyTender
#     template_name = 'supplier/pending_approval_tenders.html'
#     context_object_name = 'tenders'

#     def get_queryset(self):
#         return SupplyTender.objects.filter(tender_status='Accepted')

#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         tender_id = request.POST.get('tender_id')
#         status = request.POST.get('status')
#         tender = SupplyTender.objects.get(id=tender_id)

#         with transaction.atomic():
#             product = tender.product
#             product.quantity += tender.quantity
#             product.save()

#             tender.tender_status = status
#             tender.save()

#         messages.success(request, 'Tender status has been successfully Approved.')
#         return redirect('supplier:pending_approval_tenders')

# pending approval tenders
class PendingApprovalTenderListView(LoginRequiredMixin, ListView):
    model = SupplyTender
    template_name = 'supplier/pending_approval_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Accepted' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Accepted')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tender_id = request.POST.get('tender_id')
        status = request.POST.get('status')
        tender = SupplyTender.objects.get(id=tender_id)
        tender.tender_status = status
        tender.save()

      
        messages.success(request, 'Tender status has been successfully updated.')
        return redirect('supplier:pending_approval_tenders')




class ApprovedSupplierTenderListView(LoginRequiredMixin, ListView):
    model = SupplyTender
    template_name = 'supplier/approved-supplier-tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Accepted' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Approved', user_id=self.request.user.id )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tender_id = request.POST.get('tender_id')
        status = request.POST.get('status')
        tender = SupplyTender.objects.get(id=tender_id)
        tender.tender_status = status
        tender.save()
        messages.success(request, '{} Thanks for supplying our tender request.Please  Wait for payment confirmation.'.format(request.user.get_full_name()))

      
        messages.success(request, '.')
        return redirect('supplier:approved-supplier-tenders')



class SupplierConfirmRecievedPayments(LoginRequiredMixin, ListView):
    model = SupplyTender
    template_name = 'supplier/supplier-confirm-tender-payments.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Accepted' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Paid', user_id=self.request.user.id)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tender_id = request.POST.get('tender_id')
        status = request.POST.get('status')
        tender = SupplyTender.objects.get(id=tender_id)
        tender.tender_status = status
        tender.save()
        messages.success(request, '{} Thanks for confirmining tender payment received.'.format(request.user.get_full_name()))

      
        messages.success(request, '.')
        return redirect('supplier:approved-supplier-tenders')




class SuppliedTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/supplied_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Pending' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Supplied', user_id=self.request.user.id)

class confirmedSupplierTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/confirmed_supplied_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Pending' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Confirmed', user_id=self.request.user.id)



class RejectedSupplierTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/rejected_supply_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Pending' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Rejected', user_id=self.request.user.id)


class CompleteTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/complete_supply_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Pending' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Complete', user_id=self.request.user.id)



from django.db import transaction

class ConfirmTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/confirm_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        return SupplyTender.objects.filter(tender_status='Supplied')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tender_id = request.POST.get('tender_id')
        status = request.POST.get('status')
        tender = SupplyTender.objects.get(id=tender_id)

        with transaction.atomic():
            product = tender.product
            product.quantity += tender.quantity
            product.save()

            tender.tender_status = status
            tender.save()

        messages.success(request, 'Tender status has been successfully updated.')
        return redirect('supplier:confirm-tenders')



class InventoryConfirmTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/inventory_confirmed_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        return SupplyTender.objects.filter(tender_status='Confirmed')



class FinanceSupplierTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/finance_supplied_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        return SupplyTender.objects.filter(tender_status='Confirmed')

    def post(self, request, *args, **kwargs):
        tender_id = request.POST.get('tender_id')
        status = 'Paid'
        try:
            tender = SupplyTender.objects.get(id=tender_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Tender payment failed. Invalid tender ID.')
            return redirect('supplier:pay-tenders')
        tender.tender_status = status
        tender.save()
        messages.success(request, 'Tender payment has been successfully made.')
        return redirect('supplier:pay-tenders')



class PaidTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/paid_supply_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Pending' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Paid')


class ConfirmedPaidTenderListView(ListView):
    model = SupplyTender
    template_name = 'supplier/confirmed_paid_supply_tenders.html'
    context_object_name = 'tenders'

    def get_queryset(self):
        # Filter the supply tenders by tender_status = 'Pending' and user_id = the logged-in user's id
        return SupplyTender.objects.filter(tender_status='Complete')