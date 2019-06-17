from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'test_templates', views.TestTemplatesView)
router.register(r'test_schedule', views.TestScheduleView)
router.register(r'answers', views.AnswersView)


urlpatterns = [
    path('login/', views.login),
    path('tutorsapp/api/', include(router.urls)),
    path('tutorsapp/', views.main),
    path('test', views.test_page)
]


urlpatterns += staticfiles_urlpatterns()
