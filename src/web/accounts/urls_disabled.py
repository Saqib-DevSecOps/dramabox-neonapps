from django.urls import path

from src.web.accounts.views import InActiveView

disabled_all_auth_url_patterns = [
    path('accounts/signup/', InActiveView.as_view(), name='account_signup'),
    # path('accounts/reauthenticate/', InActiveView.as_view(), name='account_signup'),
    # path('accounts/3rdparty/', InActiveView.as_view(), name='account_signup'),
    # path('accounts/login/', InActiveView.as_view(), name='account_login'),
    # path('accounts/logout/', InActiveView.as_view(), name='account_logout'),
    # path('accounts/password/change/', InActiveView.as_view(), name='account_change_password'),
    # path('accounts/password/set/', InActiveView.as_view(), name='account_set_password'),
    # path('accounts/inactive/', InActiveView.as_view(), name='account_inactive'),
    # path('accounts/email/', InActiveView.as_view(), name='account_email'),
    # path('accounts/confirm-email/', InActiveView.as_view(), name='account_email_verification_sent'),
    # path('accounts/confirm-email/<key>/', InActiveView.as_view(), name='account_confirm_email'),
    # path('accounts/password/reset/', InActiveView.as_view(), name='account_reset_password'),
    # path('accounts/password/reset/done/', InActiveView.as_view(), name='account_reset_password_done'),
    # path('accounts/password/reset/key/<uidb36>-<key>/', InActiveView.as_view(), name='account_reset_password_from_key'),
    # path('accounts/password/reset/key/done/', InActiveView.as_view(), name='account_reset_password_from_key_done'),
]