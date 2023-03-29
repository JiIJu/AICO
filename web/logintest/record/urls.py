from django.urls import path
from . import views

app_name = 'record'

urlpatterns = [
    path('', views.main, name='main'),
    path('regist/<int:pk>', views.regist, name='regist'),
    path('chart/',views.chart,name='chart'),
    path('live/<int:pk>',views.live,name='live'),
    path('totalrecord/',views.totalrecord, name='totalrecord'),
    path('create/',views.create,name='create'),
    path('deepcreate/',views.deepcreate,name='deepcreate'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('stream2/',views.stream2,name='stream2'),
    path('page404/',views.page404,name='page404'),
    path('finish/<int:pk>/',views.finish,name='finish'),
    path('jsonrecord/',views.jsonrecord,name='jsonrecord'),
    path('video/<int:pk>/',views.video,name='video'),
    path('videoclose/<int:pk>/',views.videoclose,name='videoclose'),
    path('exside/<int:pk>/',views.exside,name='exside'),
    path('exfront/<int:pk>/',views.exfront,name='exfront'),
]