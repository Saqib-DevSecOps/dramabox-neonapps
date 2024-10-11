from django.urls import path

from .urls_disabled import disabled_all_auth_url_patterns
from .views import (
    CrossAuthView, DeactivateUserView, DeleteUserView
)

app_name = 'accounts'
urlpatterns = [

    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth'),
    path('deactivate-account/', DeactivateUserView.as_view(), name='deactivate-account'),
    path('delete-account/', DeleteUserView.as_view(), name='delete-account'),
]

urlpatterns += disabled_all_auth_url_patterns