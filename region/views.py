from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from region.models import Region

@require_http_methods(["POST"])
def get_province(request):
  country_name = request.POST["county"]
  provinces = list(Region.objects.filter(country=country_name).values_list('province').distinct())
  return JsonResponse(
      {"provinces": provinces}
  )

@require_http_methods(["POST"])
def get_city(request):
  country_name = request.POST["county"]
  province_name = request.POST["province"]
  cities = list(Region.objects.filter(country=country_name,province=province_name).values_list('city').distinct())
  return JsonResponse(
      {"cities": cities}
  )

@require_http_methods(["POST"])
def get_district(request):
  country_name = request.POST["county"]
  province_name = request.POST["province"]
  city_name = request.POST["city"]
  districts = list(Region.objects.filter(country=country_name,province=province_name,city=city_name).values_list('district').distinct())
  return JsonResponse(
      {"districts": districts}
  )
