from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.i18n import javascript_catalog

from . import views
from .util.graphDesigner import render_graph_controls, get_graph_data
from .util import formulas

js_info_dict = {
    'packages': ('derisk_app',),
}

urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
    url(r'^$', views.index, name='index'),
    url(r'^overview', views.overview, name='overview'),
    url(r'^privacyterms', views.privacyterms, name='privacyterms'),
    url(r'^becomedataprovider', views.becomedataprovider, name='becomedataprovider'),
    url(r'^termsuse', views.termsuse, name='termsuse'),
    url(r'^projects/$', views.ProjectList, name='project-list'),
    url('^projects/upload-from-excel/$', views.upload_from_excel, name='upload-from-excel'),
    url('^projects/upload-for-verification/$', views.upload_for_verification, name='upload-for-verifcation'),
    url('^projects/(?P<pk>[\w-]+)$', views.ProjectUpdate.as_view(), name='project-edit'),
    url('^projects/delete/(?P<pk>[\w-]+)$', views.ProjectDelete, name='project-delete'),
    url('^projects/create/$', views.ProjectCreate, name='project-create'),
    url('^profile/edit/(?P<pk>\w+)$', views.UserProfileView.as_view(),name='profile-edit'),
    url('^projects/setaccesslevel/$', views.ProjectSetAccessLevel, name='profile-accessle'),
    url('^projects/unlock-all/$', views.ProjectUnlockAll, name='project-unlock-all'),
    url('^projects/lock-all/$', views.ProjectLockAll, name='project-lock-all'),
    url('^projects/delete-portfolio/$', views.ProjectDeletePortfolio, name='project-delete-portfolio'),
    url('^test/$', views.test, name='test'),
    url('^viewcharts/industry/$', views.FactSheetIndustry, name='factsheet-industry'),
    url('^viewcharts/buildings/$', views.FactSheetBuildings, name='factsheet-buildings'),
    url('^factsheet/quick/$', views.FactSheetQuick, name='factsheet-quick'),
    url('^benchmark/$', views.Benchmark, name='benchmark'),
    url('^api/overview/$', views.ApiOverview, name='apioverview'),
    url('^api/projects/list$', views.ApiProjectsList, name='apiprojectslit'),
    url('^api/benchmark/$', views.ApiBenchmark, name='apibenchmark'),
    url('^api/benchmark/loadprojects$', views.ApiBenchmarkLoadProjects, name='apibenchmarkloadprojects'),
    url('^api/benchmark/numberofprojects/$', views.ApiBenchmarkNumberOfProjects, name='apibenchmarknumberofprojects'),
    url('^api/factsheet/numberofprojects/$', views.ApiFactsheetNumberOfProjects, name='apifactsheetnumberofprojects'),
    url('^api/factsheet/industry/saving/$', views.ApiFactsheetIndustrySaving, name='apifactsheetindustry'),
    url('^api/factsheet/industry/candlestickdistributionmeasures/$', views.ApiFactsheetIndustryCandleStickDistributionMeasures, name='apifactsheetindustrycandlestickdistributionmeasures'),
    url('^api/factsheet/industry/candlestickdistributionsize/$', views.ApiFactsheetIndustryCandleStickDistributionSize, name='apifactsheetindustrycandlestickdistributionsize'),
    url('^api/factsheet/industry/candlestickdistributioneurmwh/$',views.ApiFactsheetIndustryCandleStickDistributionEURmwh, name='apifactsheetindustryddistributioneurmwh'),
    url('^api/factsheet/buildings/saving/$', views.ApiFactsheetBuildingsSaving, name='apifactsheetbuildingsaving'),
    url('^api/factsheet/buildings/candlestickmeasure/$', views.ApiFactsheetBuildingsMeasure, name='apifactsheetbuildingmeasure'),
    url('^api/factsheet/buildings/candlestickmeasure2/$', views.ApiFactsheetBuildingsMeasure2, name='apifactsheetbuildingmeasure2'),
    url('^api/factsheet/buildings/candlestickbuilding/$', views.ApiFactsheetBuildingsBuilding, name='apifactsheetbuildingbuilding'),
    url('^api/factsheet/buildings/candlestickdistributioneurmwh/$', views.ApiFactsheetBuildingsCandleStickDistributionEURmwh, name='apifactsheetbuildingddistributioneurmwh'),
    url('^api/factsheet/buildings/candlestickdistributioneurmwh2/$', views.ApiFactsheetBuildingsCandleStickDistributionEURmwh2, name='apifactsheetbuildingddistributioneurmwh2'),
    url('^api/factsheet/buildings/candlestickdistributioneurm2/$', views.ApiFactsheetBuildingsCandleStickDistributionEURm2, name='apifactsheetbuildingddistributioneurm2'),
    url('^api/factsheet/buildings/candlestickdistributioneurmwhbuilding/$', views.ApiFactsheetBuildingsCandleStickDistributionEURmwhBuilding, name='apifactsheetbuildingddistributioneurmwhBuilding'),
    url('^api/factsheet/buildings/candlestickdistributioneurm2building/$', views.ApiFactsheetBuildingsCandleStickDistributionEURm2Building, name='apifactsheetbuildingddistributioneurm2Building'),

    # Language
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # analytical toolbox
    # main views
    url('^toolbox/$', views.toolbox, name='toolbox'),
    url('^toolbox/my-charts/$', views.toolbox_all, name='toolbox-all'),
    url('^toolbox/(?P<pk>\d+)/$', views.toolbox, name='toolbox-open'),

    # partial views
    url('^toolbox/util/graphControl/$', render_graph_controls, name='render_graph_controls'),
    url('^toolbox/util/graphData/$', get_graph_data, name='get_graph_data'),

    # charts
    url('^chart/list/$', views.list_charts, name='list-charts'),
    url('^chart/open/(?P<pk>\w+)/$', views.open_chart, name='save-chart'),
    url('^chart/save/$', views.save_chart, name='save-chart'),
    url('^chart/(?P<pk>\w+)/delete/$', views.delete_chart, name='save-chart'),
    url('^chart/filter-info/$', views.filter_info, name='filter-info'),

    # formulas
    url('^formulas/save/$', formulas.save_formulas, name='save-formula'),
    url('^formulas/delete/$', formulas.delete_formula, name='delete-formula'),
    url('^formulas/$', formulas.index, name='formula-editor'),
]

admin.site.site_header = 'DEEP Platform administration'
