from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('reg', views.reg),
    path('log_in', views.log_in),
    path('dashboard', views.dashboard),
    path('add_quote', views.add_quote),
    path('quote/<int:quote_id>/like', views.like),
    path('quote/<int:quote_id>/unlike', views.unlike),
    path('myaccount/<int:user_id>', views.edit_self),
    path('users/self/update', views.update_user),
    path('user/<int:user_id>', views.view_other_user),
    path('quotes/<int:quote_id>/delete', views.delete),
    path('log_out', views.log_out)
]
