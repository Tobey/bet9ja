from django.views.generic.base import View
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from rest_framework.views import APIView
from django.http import JsonResponse



home_page = 'https://web.bet9ja2.com/Sport/Odds'
form_data = '''
h%24w%24SM=h%24w%24PC%24cCoupon%24atlasCoupon%7Ch%24w%24PC%24cCoupon%24btnAddCoupon&__PREVIOUSPAGE=uocENRZD2yWUBVGQhGhaqlYkdNLVux1d56NH-LFCjXEeO052nCfeqasG0poKngNd4H7IVy3GTvC3Po2g70ZZEcCm2ys1&h%24w%24cLogin%24ctrlLogin%24Username=&h%24w%24cLogin%24ctrlLogin%24Password=&h%24w%24PC%24oddsSearch%24txtSearch=Search&h%24w%24PC%24cCoupon%24txtPrenotatore=&h%24w%24PC%24cCoupon%24hidRiserva=0&h%24w%24PC%24cCoupon%24hidAttesa=0&h%24w%24PC%24cCoupon%24hidCouponAsincrono=0&h%24w%24PC%24cCoupon%24hidTipoCoupon=1&h%24w%24PC%24cCoupon%24hidStatoCoupon=10&h%24w%24PC%24cCoupon%24hidBonusNumScommesse=1&h%24w%24PC%24cCoupon%24hidQuotaTotaleDIMax=&h%24w%24PC%24cCoupon%24hidQuotaTotaleDIMin=1.82&h%24w%24PC%24cCoupon%24hidQuotaTotale=1.25&h%24w%24PC%24cCoupon%24hidIDQuote=5791287496%2661575098&h%24w%24PC%24cCoupon%24hidModificatoQuote=1&h%24w%24PC%24cCoupon%24hidBonusQuotaMinimaAttivo=0&h%24w%24PC%24cCoupon%24hidBonusRaggruppamentoMinimo=5&h%24w%24PC%24cCoupon%24hidNumItemCoupon=1&h%24w%24PC%24cCoupon%24hidIDCoupon=&h%24w%24PC%24cCoupon%24hidIDBookmakerCoupon=&h%24w%24PC%24cCoupon%24hidIDUtentePiazzamento=&h%24w%24PC%24cCoupon%24hidPrintAsincronoDisabled=0&h%24w%24PC%24cCoupon%24txtImportoValuta=&h%24w%24PC%24cCoupon%24txtImporto=&h%24w%24PC%24cCoupon%24txtIDQuota=5792330158&h%24w%24PC%24cCoupon%24txtQB=&h%24w%24PC%24cCoupon%24txtAddImporto=&h%24w%24PC%24cCoupon%24txtIDCouponPrecompilato=&h%24w%24PC%24cCoupon%24txtImportoCouponPrecompilato=&h%24w%24PC%24cCoupon%24txtIDCouponReload=&h%24w%24PC%24ctl09%24txtCodiceCoupon=&h%24w%24PC%24ctl13%24txtVincita=&h%24w%24PC%24ctl13%24txtGiocata=&__EVENTTARGET=h%24w%24PC%24cCoupon%24btnAddCoupon&__EVENTARGUMENT=&__VIEWSTATE=nvDaXQ%2FVoioN1h7%2FUbrJIT%2B1rshm3sEhuLLigU1N0XhcXwo7u8i4jfqywXxb4htED1uCm8Pg4UJPcD2j4iO8EzBNkY05WiBtwbP6oj%2B3tsxSk2kfOAqxY5So5lyzGXQvAXmsKlqpOthmwAtwhjZvSRoxItIL36%2BTDILlwjaytTPFr6tShlQ%2BLRZhvKNm%2BEkJHfDqIAF%2FUpB4Op9r16eoRGjgxBQNYzu%2Fi5SNhPLPfYAMaEtfXfviL9r79WeQ5qo5uIph4kAwrmQNyx61GJaD%2FQbwHz41erE1mF6pj8AuSW6xK%2F%2F9iSnmQmAKbGZ6hy%2BG85DzjID1DCsbsio2qwKxQxnP7v%2FqwagUrQ%2Bre3d9XBaFEfx08pOpywiela7L%2FrbTT7XGXAzD9vmCG4epsiWZntqLS%2BQLl84JrJ%2FpJXHhztTICUVKtwNHWF7qcPFeNkvSSTi8o%2B%2Bgrvce1b9RwN6EIwnPKX1OjzOoDXgerqwRfER6C5Jp2Z2M3qriFJQ3Leiau6lHvw20Xv4ShYkqeGeQMEFzFNdde3DwH28EYeSbbcD5hy6qG6v23VJWUvbSD73XrOFLkptM6z%2F4%2BSQC2GRj1Rv4LxUNFezcLfDJFgCyfqNPT7AlkXm%2F6qnYiouzLuuuPdBT6Aw25UktltJDWnCO7eUjV38A4H0bESwSSE56bf%2FIjz31FK3yMkJcRnkWtwPFHEzL32phwn%2Blho8%2BsW68DXg5A9nN1DTZLKvZKrJ7TyEAuEXSVgnvTI26uWfSNBzDNCh2qrQlNyX6RX3MI6xpeJmil%2BJycHKqZ5uCwClN1Pg5dHPtQcFvY1yZBBQHEYXokfOs2Vs%2Fq7haEHkeltZspyoox4mj65UqIWaPIFAHRMa0CrYLTSX3AY%2B%2Fdal3HcHXfQiAHn1NtkbV5mZzx3eZlpMjxub%2Fz5tSW%2BfVzaLqumYPjZ84ugvdM22uF5OoTlAi0S8JSX3IMnrQSvh9bEiOkO1hv3ZgaoUOKj%2BosfAf1tbB9e0xLlKIirsLgAWwiNLLKPfR9l8PwG5olpqzFE0Xld2yh3IDHmCcOgrAqXecXVAq%2Foi2ZZMYjQirs6QQv1GSN0XRsWEl4lk72Ve0LhROsUgAf%2Fp48jAKK88T%2B1Ds45pKsXzvAMb1Za7C8NZwKRpFRW6mUdFxCYl2PPNl%2Fg2mpeY2mDcbZZB6auY342u1iz%2BqDANn%2FwEO4y4ZYp05QonzedkLcVHW7soCEyzuN1snO8%2BuhhhRCXeN6UP7P2v%2FIssDbILqfHsGApSIqPkfu%2BzHHK%2FurdkFpICDYFuHwi%2FJutVCTVE0RrgKJSDH02wyhoTOUWMHnyIfO3zKZBJ0J%2FG0Q8OmHeANkLiE1Qu9H3OjeSkKy34G1UzeilRBQ7PKrXGf2o98G%2FL%2BYf562FB3UhXhXs4x7%2F0TseSpNhPqZ37KnuCav0l3x8q1TCowqzennBx1QF7xQ16DNf3o%2B2jnofVoDI6Sbzri84Lm9ndOcgh0vrIAtk9V%2Ba0BUO4fpG%2Fe20NAqNYGNW9cWK%2BrT06ki%2FEXbhQyvcZ05smRCNFzemufwfVF%2Fnv9jmqZ2lsSkJg47HLAwW7kUR9rBZkzIEiNHUVOIAFAZrjwp2GEhXxXgQSugsvfoPUdYgUsV%2BRSziIZOeZZsFIHYzqHZVac0MdVfbL%2BeuphmpTmKv6qye%2FHoJQNGtnj6Yn4HBRJCbhWIarIgOZrLg9KoCoHdRwh9PuSENtNwTCMi9ZWaf5Ui8KYegQ5hZPQ905wzRYHuYrXL0STUVq0ZMfpZY%2B3%2FyZVHPBaVZTelFkgFsA0M7dXoBRG8ubkUqexj7kqacGskgkElKjYyHxkgcV%2BYSSCYQ75h6lMeEcPT5Di3VMhvTQCRUNBUViu0o9Y3aWSwE6Ao7uO75uNWS2Z%2BeQlGIVHuCQ0gPPtcdJgQe7PsTGF1Lh4krs3TX8ToopPXYooaebVZfxJaC%2FOMLOFKCMBCaPVR4eZgvz0ReyPWtVgPNV8L0Q9Id%2FYJGZQWDNtz57fV2AX5nibW1ntqsCXLDO%2B7h59VUdB3ytHJS6mAu6vQXl8L%2BoNg93pUUj28CF6avTWCQINTXiIGE1abqdyAG62dBo0iFTcRysPfiyegM%2BLy1PD8Z08Oo9t%2FivbPI9KuX9Yc1OUf%2FjzwpM%2BxoFZ%2BqwCtlX4%2BXfNuNT2qCM4FJ36ZL%2FJqNQ6jK2zFISsnU4w0MuWNeVJHtNFMfnL7YJcgs2WMb20Md7ZqsHNt4iGEfC%2BRneg%2BDgkKpvylkAUDh04V6iBvzqBHvnwnmw929m2zKztZZmgknVV87KIV5CWCuagp215pwKvDENcgyuByyS4LpCI9851kB9rcUw9AY7bL3d4DY93A97ToMkmhwSRCRF4bQbx6jnfUXOBLXwQ5vQGyjsZSh3mZN83g5wBAp5Yc6HLlgBkMS3oll9zpB%2FVKyjpGX8H%2FQgAv1L3KClaVOF61x1gXL4HPoxTDS4%2BDCNqi1O2S%2FBdJCRs39hXXlrs7toKy%2FVOUkAMCg20vjXKUVZSI9XK6R4wBeWbtH8Es6TXPpvlF3SgQQ8qVosloatY0LlBwSjTqxkcTVnv4s%2F30AfCo3QlCBtiMziXMYZqmXzoy%2FDTVZKPtLtvBnZaHa1Awb2fd%2FsMmMple%2B98R%2B5Xf3VpPkVtP1L3YZUZYGCd2l47zA5UJbDT0U4y8W6apy5Ka8ArykhHeuK1vJh1LJaikp%2FLAV9W6bbuDpJ9r9F%2FOY2DbencwmxyUnvneE18cXOzZs7EDcaJ%2B%2FRXEFpEnxQCiWUEKdE8D5Dp5i0qJtkaN%2BmF5KGHAYCpxv%2FynOWdjdTUZNEk8Ia9OdwJP8T5OuutYSV6923eE5%2FE7dzKNWc2Sh9QZFBzLKRJsEPw3h%2BcBdhCnsXeTtJiWTaqtufAH6u6zSgd8KX76fOPBx8zPSJENXoIoa9VQTque2CKDjuJ5SHMueEfFJ00%2FP5tJKNQDErJjWJqmo33AnT6HmIV0xguASTxlh%2Fn5hmoNOvacw1y5AYSJallony5uY79ze%2Freli0Jeo1eayUNMFQzdMs%2Fi%2BdAqHbB7ktnLBfvRVeKCdTqp7TCD%2BuJQHRSFOboWO5DsjosME%2FF77k%2BpIkOW9yjjDo2RmzGEQSfRpiU2WR3STxfFlzpuMH5zAgmbbUhA5EhBwR%2BkKNpZ5Hg061OZFNXpCv6IVP%2B2NMZjhK0j4COxJauDkoxnr6QRZKEEOCIIbSqF14hfHhUsAe7dpIB2Lh6xNtaN5c56hrp4cOZWM3bBXuIySsEYuUu2Dxx8%2F8eRZveziu%2BMFRxgYBiynxsfFMKqRrsgU%2BBHdfVNC1QRfPKX0a5ukhE%2B4ws6oKAU5SgFCdaNn6I3wRI1nXLW%2B9PEk7rw715kNbz1zX%2BE74D1mLnTkNkxLGUfuynwzR3gth%2BjWusOkwfzCfQJQIUrKh6ctcraRzvx%2BSo5d4XNyuXOC78atnEYCmN7KlDyLsj%2BIIpxu6lEL8fDlxvnGUMXrR0GRmhyLBTKR7cFunVxZ0Y8OmHEqd5aXa1Aneror7VyRIWYjautInriR7BRaLRJ5svInqeTkRh4WHzmQj0Gue56HHDVSj4EYYDicKueJkakVtqJuwO8UOyzRGifur9jPPdxtfLnuTrdTqdTi1bV2SjSRbD%2FcZlIOskggqblmfXHYwaD1ykJUN4RUMuHZxxjRoZRka0dowdKRhib8%2BW0raNFtn14PRtz%2BiQR8MjZCGt%2Bge5Rvh2UgYlX7UtAacUTf1sQ5%2BlOFE7avltgn%2BvdlccLwDjU%2FGIRQBNgecRIXI9JOVWcMr3AFc1H6MsNGPyzZOR5q2Op9YbS0JJI%2BctC4RCQHhydQBKSSZmQ7hWjlEHJA5rzSfKj1Bw5FyM4rZlDYZLe5ij34RLuk3GJRp%2BNlJyjeu%2FLQV5YBNwYpY9CWIEq4zCVDgOZnaF1ZJFhFscgZdesXP9YgscosQka0Vngd22syHcdXy2FQP%2FqVOePj4Nrx8xXkchKEYP6%2BBdKrnB8Inw%2BNQt5fAhR72qISc9X2N5fWNfcuvsNePQduMaO5hAIK%2BrVgAHw6uAtoUqxU11KyanMgUcAxKg20k2OqhGFigFu9sOQjzkLtjHieNDyFDGFvctdfJmQZZZIimtiUEl7X2cnLzxtifLoGusBs3n9D4lGiCI9jdV9W880xYn08VX%2FEEp%2FF%2FPtmZpD9kJhFtYwhqqaQiJ8%2F%2FyhSiPxIp88Wg2AD9eKPAd404A%2BGYgB7odcZjsIMeGMFd%2BRKzqPT4PLeEji6FLcU9mayI6CdOAFmzcXEUl9VvpGKdwV7RDw69z%2BRSgTVIpL8o29w3cf5XmZEYGrDXB3PyGc2skfneGULOqhZK4z7fgqmpaZrwE2x2RXk%2F3nZ0KwEtpHPZry3qiEttukuZI9j3Yd7tGMrMHdgJTPt85uXzuteuNBPXSoPwV99xz9Q7iOOm1dBI9tgBT1qm1dbtC2UEX2j4lBXyqtYctX2pOgDD6semCL4B45SHXrPS5t1kTFT4JEmplgfR162%2B6Ue4EVf05P9NEba6D%2FlyegIBM2Yqp0m9x9ze6BCJzl2Z7U7mSfAS%2FhbwykICkzwcTlSLLTfhjAQRpJA3gUDiZHZA2iaHspi8QT0P1ZmCjkgYd7FFlpcdC0lamCAI0eLPyXyOdJWj05k%2FXC65pDWtDAt%2Bbu8N7sEoRJonBh7dVm%2BROos7Lwb0S2tKQm0rDgJgZahCur5necWwmmJiedAc2FsDO9GoXfAQu7NTXZHcqFbaa8MwSbtdEw4y8rTDKQmKwtJk5fKELHMKHiotTO37ah5QvkMYps7k6oHqclFZJJ9XqEy63DhkZ81QLvVuJl7Rt%2F4427wje%2Fxh37C3esZckTwoNNq6EkyaHGIKCcFrcVQ79rYs%2B1mGdPhkRXsEZY1vz89Cx%2B%2FvFIw61eJ8%2FenDGZJWPVEv1iZe9vn6MYLwZTlEsW9RSpQ3i7ryOzIx4gfl45t7eVMZWVs3EAA4miJRBrpNpjtpqjmYr1Rsm3btkLC0yNR1TqSgxDP01DvFvIay1YFTP%2BXfv8MUi1JNW26DA3Os%2B1U5i0bPtcKfFc4XNTrW1l5aMKbjQJfetaq37pgk2BKHcLibhE8oI2ze09u%2FaalvMAqkiXU0YXT6nKRevGnVJcWViMrU%2BwaoudxLBTy3wrfjZ5ThAbFgc4Vq3XXYHx%2Bml3KGxC6Y335pSNwzC0S%2FyZ7JLT9rE0HlhWrt%2BCo9ywakW3VGq6R6G8O8jOxWNGCba4FPjG6QW5VHH4LazTIzVwOoMLU5T1mIs9wEPOEUmHdX0mZC%2FQpWHpR8cMOakIkmrrfojmBIPxY%2B80WKbX9OUILtcbnUgRQHZuk%3D&__VIEWSTATEGENERATOR=15C4A0A3&__VIEWSTATEENCRYPTED=&__ASYNCPOST=true&
'''.strip()
form_data = {k: v[0] for k, v in parse_qs(form_data).items()}

class Base:
    def base_get(self, request, *args, **kwargs):
        context = dict()
        booking = request.GET.get('booking', None)
        stuff = None

        if booking:
            # New http session
            session = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            }
            session.headers.update(headers)
            r = session.get(home_page)
            
            # headers['Cookie'] = r.headers['Set-Cookie']
            headers['Cookie'] = 'SBets_CurrentCulture=2; ISBets_CurrentOddsFormat=1; ISBets_CurrentGMT=35; mb9j_nodesession=2030110474.20480.0000; ASP.NET_SessionId=d2klaohkm0imwxu5jni12g4a; _ga=GA1.2.1951396111.1575407400; _gid=GA1.2.483641337.1575407400; _fbp=fb.1.1575407400286.2144714362; _hjid=72d179a7-1dc7-4ad4-860d-dd55bb26582e'
            
            new_form = form_data.copy()
            new_form['h$w$PC$cCoupon$txtPrenotatore'] = booking
            response = session.post(home_page, data=new_form, headers=headers)

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


class HomeView(Base, View):    
    
    def get(self, request, *args, **kwargs):  
        context = self.base_get(request, *args, **kwargs)
        return render(request, 'index.html', context=context)

class ApiView(Base, APIView):
    
   def get(self, request, *args, **kwargs):  
       context = self.base_get(request, *args, **kwargs)
       return JsonResponse(context)
    
    
