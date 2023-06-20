import calendar
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView

from .forms import AccountDiaryForm

from .models import AccountDiary
from store.models import Store, City, Country, Industry
import json


class DiaryCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AccountDiary
    form_class = AccountDiaryForm
    success_url = '/account-diary/'

    def test_func(self):
        return self.request.user.is_authenticated

    def get_initial(self):
        initial = super().get_initial()
        year = self.request.GET.get('year', datetime.now().year)
        month = self.request.GET.get('month', datetime.now().month)
        day = self.request.GET.get('date', datetime.now().day)
        initial['date'] = datetime(int(year), int(month), int(day))
        return initial

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated:
            form.instance.user = current_user
            return super().form_valid(form)
        else:
            return redirect('/account-diary/')


def account_diary_detail(request, pk):
    account_diary = get_object_or_404(AccountDiary, pk=pk)

    context = {
        'account_diary': account_diary,
    }

    return render(request, 'account_diary/account_diary_detail.html', context)


@login_required
def get_account_diary_day_data(request):
    now = datetime.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    # 해당 년도와 달에 해당하는 AccountDiary 데이터 가져오기
    account_diaries = AccountDiary.objects.filter(date__year=year, date__month=month, user=request.user)

    # 해당 달의 마지막 날짜 구하기
    last_day = calendar.monthrange(year, month)[1]

    # 날짜별 수입과 지출 데이터 가져오기
    data = {}
    for day in range(1, last_day + 1):
        account_diaries_day = account_diaries.filter(date__day=day)

        income = account_diaries_day.filter(type='IN').aggregate(total=Sum('amount'))['total'] or 0
        expenditure = account_diaries_day.filter(type='EX').aggregate(total=Sum('amount'))['total'] or 0

        data[day] = {
            'income': income,
            'expenditure': expenditure,
        }

    data_json = json.dumps(data, default=str)
    response_data = {
        'data_json': data_json,
        'year': year,
        "month": month
    }

    return render(request, 'account_diary/my_account_diary_calendar.html', response_data)


@login_required
def daily_list(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('date')

    if day:
        start_date = datetime(year=int(year), month=int(month), day=int(day))
        end_date = start_date.replace(hour=23, minute=59, second=59)
        view_type = 'day'

    else:
        start_date = datetime(year=int(year), month=int(month), day=1)
        last_day = calendar.monthrange(int(year), int(month))[1]
        end_date = start_date.replace(day=last_day)
        view_type = 'month'

    datas = AccountDiary.objects.filter(user=request.user, date__range=(start_date, end_date)).order_by('date')
    expenditures = AccountDiary.objects.filter(user=request.user, type='EX', date__range=(start_date, end_date))
    incomes = AccountDiary.objects.filter(user=request.user, type='IN', date__range=(start_date, end_date))

    total_expenditure = expenditures.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    difference = total_income - total_expenditure

    context = {
        'datas': datas,
        'total_expenditure': total_expenditure,
        'total_income': total_income,
        'difference': difference,
        'view_type': view_type
    }
    return render(request, 'account_diary/account_diary_list.html', context)


@login_required
def diary_others_list(request):
    # 필터링에 사용할 필드들을 미리 가져옵니다.
    cities = City.objects.all()
    countries = Country.objects.all()
    industries = Industry.objects.all()

    # 필터링 조건을 받아옵니다.
    city_id = request.GET.get('city')
    country_id = request.GET.get('country')
    industry_id = request.GET.get('industry')

    # 필터링 조건에 해당하는 지출 내역을 가져옵니다.
    expenses = AccountDiary.objects.filter(type='EX', is_public=True)

    if city_id:
        expenses = expenses.filter(store__city_id=city_id)
    if country_id:
        expenses = expenses.filter(store__country_id=country_id)
    if industry_id:
        expenses = expenses.filter(store__industry_id=industry_id)

    context = {
        'expenses': expenses,
        'cities': cities,
        'countries': countries,
        'industries': industries,
        'selected_city_id': city_id,
        'selected_country_id': country_id,
        'selected_industry_id': industry_id,
    }

    return render(request, 'account_diary/others_diary_list.html', context)


@login_required
def account_diary_update(request, pk):
    account_diary = get_object_or_404(AccountDiary, pk=pk)

    # 작성자 검증
    if account_diary.user != request.user:
        return redirect('account_diary_list')

    if request.method == 'POST':
        form = AccountDiaryForm(request.POST, instance=account_diary)
        if form.is_valid():
            form.save()
            return redirect('account_diary_detail', pk=pk)
    else:
        form = AccountDiaryForm(instance=account_diary)
    return render(request, 'account_diary/accountdiary_form.html', {'form': form, 'account_diary': account_diary})


@login_required
def account_diary_delete(request, pk):
    account_diary = get_object_or_404(AccountDiary, pk=pk)

    # 작성자 검증
    if account_diary.user != request.user:
        return redirect('account_diary_list')

    account_diary.delete()

    return redirect('/account-diary/')
# Create your views here.
