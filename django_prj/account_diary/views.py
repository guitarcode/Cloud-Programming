import calendar
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import AccountDiaryForm
from .models import AccountDiary
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
            form.instance.author = current_user
            return super().form_valid(form)
        else:
            return redirect('/account-diary/')


def get_account_diary_data(request):
    now = datetime.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    # 해당 년도와 달에 해당하는 AccountDiary 데이터 가져오기
    account_diaries = AccountDiary.objects.filter(date__year=year, date__month=month, user=request.user)
    incomes = account_diaries.filter(type='IN').all()
    expenditures = account_diaries.filter(type='EX').all()

    # 해당 달의 마지막 날짜 구하기
    last_day = calendar.monthrange(year, month)[1]

    # 날짜별 수입과 지출 데이터 가져오기
    data = {}
    for day in range(1, last_day + 1):
        account_diaries_day = account_diaries.filter(date__day=day)
        income_cnt = account_diaries_day.filter(type='IN').count()
        income = account_diaries_day.filter(type='IN').aggregate(total=Sum('amount'))['total'] or 0
        expenditure_cnt = account_diaries_day.filter(type='EX').count()
        expenditure = account_diaries_day.filter(type='EX').aggregate(total=Sum('amount'))['total'] or 0
        data[day] = {'income_cnt': income_cnt,
                     'income': income,
                     'expenditure_cnt': expenditure_cnt,
                     'expenditure': expenditure}

    # 수입과 지출의 합 계산
    total_income = account_diaries.filter(type='IN').aggregate(total=Sum('amount'))['total'] or 0
    total_expenditure = account_diaries.filter(type='EX').aggregate(total=Sum('amount'))['total'] or 0

    # 월별 수입과 지출 계산
    monthly_income = \
        AccountDiary.objects.filter(date__year=year, date__month=month, type='IN').aggregate(total=Sum('amount'))[
            'total'] or 0
    monthly_expenditure = \
        AccountDiary.objects.filter(date__year=year, date__month=month, type='EX').aggregate(total=Sum('amount'))[
            'total'] or 0

    data_json = json.dumps(data)
    response_data = {
        'data_json': data_json,
        'total_income': total_income,
        'total_expenditure': total_expenditure,
        'monthly_income': monthly_income,
        'monthly_expenditure': monthly_expenditure,
        'incomes': incomes,
        'expenditures': expenditures,
    }

    return render(request, 'account_diary/my_account_diary.html', response_data)

# Create your views here.
