from django.urls import path
from .views import   combined_charts

urlpatterns = [
    #path('', ChartData, name='graficos'),
    #path('', chart_data1, name='chart_data1'),
    path("",combined_charts, name="graficos")
]
