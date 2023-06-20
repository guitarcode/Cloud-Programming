# Create your views here.
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View

from .models import Store, City, Country, Industry


class StoreCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Store
    fields = ['id', 'name', 'city', 'country', 'industry']

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(StoreCreate, self).form_valid(form)
        else:
            return redirect('/store')


class StoreListView(View):

    def get(self, request):
        # 필터링할 city, country, industry 값들
        city_id = request.GET.get('city_id')
        country_id = request.GET.get('country_id')
        industry_id = request.GET.get('industry_id')

        # 모든 Store 객체 가져오기
        stores = Store.objects.all()
        cities = City.objects.all()
        countries = Country.objects.all()
        industries = Industry.objects.all()

        # city, country, industry 필터링
        if city_id:
            stores = stores.filter(city_id=city_id)
        if country_id:
            stores = stores.filter(country_id=country_id)
        if industry_id:
            stores = stores.filter(industry_id=industry_id)

        # 페이징 처리
        paginator = Paginator(stores, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'stores': page_obj,
            'cities': cities,
            'countries': countries,
            'industries': industries
        }

        return render(request, 'store/store_list.html', context)


def store_detail(request, store_id):
    store = Store.objects.get(id=store_id)
    context = {'store': store}
    return render(request, 'store/store_detail.html', context)