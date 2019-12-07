from django.views.generic.base import View
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from rest_framework.views import APIView
from django.http import JsonResponse



home_page = 'https://web.bet9ja2.com/Sport/Odds'
form_data = {
             'h$w$PC$cCoupon$hidAttesa': '0',
             'h$w$PC$cCoupon$hidBonusNumScommesse': '1',
             'h$w$PC$cCoupon$hidBonusQuotaMinimaAttivo': '0',
             'h$w$PC$cCoupon$hidBonusRaggruppamentoMinimo': '5',
             'h$w$PC$cCoupon$hidCouponAsincrono': '0',
             'h$w$PC$cCoupon$hidIDQuote': '5791287496&61575098',
             'h$w$PC$cCoupon$hidModificatoQuote': '1',
             'h$w$PC$cCoupon$hidNumItemCoupon': '1',
             'h$w$PC$cCoupon$hidPrintAsincronoDisabled': '0',
             'h$w$PC$cCoupon$hidQuotaTotale': '1.25',
             'h$w$PC$oddsSearch$txtSearch': 'Search',
             'h$w$SM': 'h$w$PC$cCoupon$atlasCoupon|h$w$PC$cCoupon$btnAddCoupon'}

class Bet9jaScraper:
    def get_stuff(self, request, *args, **kwargs):
        context = dict()
        booking = request.GET.get('booking', None)
        stuff = None

        if booking:
            # New http session
            session = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'Cookie': 'ASP.NET_SessionId=dxefh1vqng0axa2adjei2x2t; _fbp=fb.1.1575407400286.2144714362; _ga=GA1.2.1951396111.1575407400; _gid=GA1.2.790801012.1575680974; _hjid=72d179a7-1dc7-4ad4-860d-dd55bb26582e; landingRedirection=true; ISBets_CurrentCulture=2; ISBets_CurrentGMT=35; ISBets_CurrentOddsFormat=1; mb9j_nodesession=2080442122.20480.0000',
            }
            session.headers.update(headers)
            session.get(home_page)
            new_form = form_data.copy()
            new_form['h$w$PC$cCoupon$txtPrenotatore'] = booking
            response = session.post(home_page, data=new_form)

            s = BeautifulSoup(response.text)
            thing = s.select('.CItem.te1')
            for item in thing:
                if stuff is None:
                    stuff = []
                competition = item.select_one('.CEvento').text.strip()
                teams = item.select_one('.CSubEv').text.strip()
                thing = item.select_one('.CSegno').text.strip()
                odds = item.select_one('.valQuota_1').text.strip()

                print(f'{competition}  | {teams} | {thing}  | {odds} ')
                stuff.append([competition, teams, thing, odds])

        context['stuff'] = stuff
        context['booking'] = booking
        return context


class HomeView(Bet9jaScraper, View):    
    
    def get(self, request, *args, **kwargs):  
        context = self.get_stuff(request, *args, **kwargs)
        return render(request, 'index.html', context=context)

class ApiView(Bet9jaScraper, APIView):
    
   def get(self, request, *args, **kwargs):  
       context = self.get_stuff(request, *args, **kwargs)
       return JsonResponse(context)
    
    
