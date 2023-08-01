from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('rider/', include('client.rider.urls')),
    path('dispatch/', include('client.dispatch.urls')),
    path('sales/', include('staff.sales.urls')),
    path('driver/', include('staff.driver.urls')),
    path('finance/', include('staff.finance.urls')),

    # third party apps urls
    path('ckeditor/', include('ckeditor_uploader.urls')),

    #   password reset urls
    path('reset-password/', PasswordResetView.as_view(
        template_name="accounts/forgot-password.html",
        html_email_template_name="accounts/emails/password-reset.html",
        subject_template_name="accounts/emails/password_reset_subject.txt",
    ), name="password_reset"),
    path('reset-password-done/', PasswordResetDoneView.as_view(
        template_name="accounts/password-reset-done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="accounts/reset-password.html"),
         name="password_reset_confirm"),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(
        template_name="accounts/password-reset-complete.html"),
         name="password_reset_complete"),

    path('', include('accounts.urls')),
    path('', include('client.customer.urls')),
    path('', include('supply.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
