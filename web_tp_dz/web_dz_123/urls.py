from django.urls import path
from web_dz_123 import views
from web_tp_dz import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:pk>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name = 'logout'),
    path('signup/', views.signup, name='signup'),
    path('tag/<str:name>/', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
    path('settings/', views.settings, name='settings'),
    path('member/<str:member_name>/', views.member, name='member'),
    path('like-question/', views.like_question, name = 'like-question'),
    path('like-answer/', views.like_answer, name = 'like-answer'),
    path('mark-answer/', views.mark_answer, name = 'mark-answer')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)