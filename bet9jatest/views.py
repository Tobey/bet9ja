from django.views.generic.base import View
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from rest_framework.views import APIView
from django.http import JsonResponse



home_page = 'https://web.bet9ja2.com/Sport/Default.aspx'

class Bet9jaScraper:
    def get_stuff(self, request, *args, **kwargs):
        context = dict()
        booking = request.GET.get('booking', None)
        stuff = None

        if booking:
            # New http session
            headers = {
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Content-Length": "7436",
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://web.bet9ja2.com",
                "Referer": "https://web.bet9ja2.com/Sport/Default.aspx",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                "X-Microsoftajax": "Delta=true",
                "X-Requested-With": "XMLHttpRequest",
            }
            form_data = {
                "h$w$PC$cCoupon$txtPrenotatore": booking,
                "h$w$SM": "h$w$PC$cCoupon$atlasCoupon|h$w$PC$cCoupon$lnkLoadPrenotazione",
                "__PREVIOUSPAGE": "uocENRZD2yWUBVGQhGhaqlYkdNLVux1d56NH-LFCjXEeO052nCfeqasG0poKngNd4H7IVy3GTvC3Po2g70ZZEcCm2ys1",
                "h$w$cLogin$ctrlLogin$Username": "",
                "h$w$cLogin$ctrlLogin$Password": "",
                "h$w$PC$oddsSearch$txtSearch": "Search",
                "h$w$PC$cCoupon$hidRiserva": "0",
                "h$w$PC$cCoupon$hidAttesa": "0",
                "h$w$PC$cCoupon$hidCouponAsincrono": "0",
                "h$w$PC$cCoupon$hidTipoCoupon": "4",
                "h$w$PC$cCoupon$hidStatoCoupon": "10",
                "h$w$PC$cCoupon$hidBonusNumScommesse": "1",
                "h$w$PC$cCoupon$hidQuotaTotaleDIMax": "",
                "h$w$PC$cCoupon$hidQuotaTotaleDIMin": "",
                "h$w$PC$cCoupon$hidQuotaTotale": "14.85",
                "h$w$PC$cCoupon$hidIDQuote": "5834283143&61436333|5833378986&61436542",
                "h$w$PC$cCoupon$hidModificatoQuote": "1",
                "h$w$PC$cCoupon$hidBonusQuotaMinimaAttivo": "0",
                "h$w$PC$cCoupon$hidBonusRaggruppamentoMinimo": "5",
                "h$w$PC$cCoupon$hidNumItemCoupon": "2",
                "h$w$PC$cCoupon$hidIDCoupon": "",
                "h$w$PC$cCoupon$hidIDBookmakerCoupon": "",
                "h$w$PC$cCoupon$hidIDUtentePiazzamento": "",
                "h$w$PC$cCoupon$hidPrintAsincronoDisabled": "0",
                "h$w$PC$cCoupon$txtImportoValuta": "",
                "h$w$PC$cCoupon$txtImporto": "",
                "h$w$PC$cCoupon$txtIDQuota": "",
                "h$w$PC$cCoupon$txtQB": "",
                "h$w$PC$cCoupon$txtAddImporto": "",
                "h$w$PC$cCoupon$txtIDCouponPrecompilato": "",
                "h$w$PC$cCoupon$txtImportoCouponPrecompilato": "",
                "h$w$PC$cCoupon$txtIDCouponReload": "",
                "h$w$PC$ctl09$txtCodiceCoupon": "",
                "h$w$PC$ctl13$txtVincita": "",
                "h$w$PC$ctl13$txtGiocata": "",
                "__EVENTTARGET": "h$w$PC$cCoupon$lnkLoadPrenotazione",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": "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",
                "__VIEWSTATEGENERATOR": "15C4A0A3",
                "__VIEWSTATEENCRYPTED": "",
                "__ASYNCPOST": "true",
            }

            response = requests.post(home_page, data=form_data, headers=headers)

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
    
    
