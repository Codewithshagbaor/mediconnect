from django.urls import path
from . import views
from .views import UploadFileView

urlpatterns = [
  path('', views.homepage, name="home"),
  path('entry/<str:auto_id>/', views.view_submission, name="view_submission"),
  path('entry/', views.entry_submission, name="entry_submission"),
  path('upload/', UploadFileView.as_view(), name='upload_file'),
  path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
  path('dashboard/entry/<str:auto_id>/', views.admin_view_submission, name="admin_view_submission"),
  path('grade_submission/', views.grade_submission, name='grade_submission'),
  path('enter-access-code/', views.enter_access_code, name='enter_access_code'),
  path('protected/', views.protected_view, name='protected_view'),
  path('add_judge/', views.add_judge, name='add_judge'),
  path('Submission/', views.user_list, name='user_list'),
  path('check_submission/', views.check_submission, name='check_submission'),




]