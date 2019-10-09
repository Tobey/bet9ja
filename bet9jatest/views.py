from django.views.generic.base import View
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs


session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}
session.headers.update(headers)
home_page = 'https://web.bet9ja.com/Sport/Default.aspx'
form_data = '__EVENTTARGET=h%24w%24PC%24cCoupon%24lnkLoadPrenotazione&__EVENTARGUMENT=&__VIEWSTATE=9DEXK2qKtZnm4A6gnuQTrpgIJK4vjwRQsoUsPeW9WAnQl11AqqiJ9fSnAGzFJOmuSWvGx51uf9Q%2B8KUWvEbKX4uq9y7Wlnoz4GQwbVMbQHCv%2Fe1wHl2k72Tvru%2BUNKDkR6V3jFo%2Frtgm%2B2uss4XZE9GAJJG9R2BJlKwkXnGUoRWMNt%2F1m1v17wpR1ZbBS9NxpZTkg6c8wHHViMoLEG9tXb3kMvvauPmfZZxTckJ2UHVNF0l5gHyTph66%2FICZTDMQditvmThaavUDGtUctSYj5Ws3cLXy%2FkRDIL6RSHJWF0lzFzK%2FfD0ENoDd7B9krjiHbXQhhXLw20%2BlkiYIFAHRhKII5eGnuDLllMOpUifAulx8XOeobVggP%2B%2BgN0Es1bFriljHg4dC1sOqGOF1H6vkWRWEnDQlauRioKGuslJWVe85aVcsT3c2nnaFHGGUauLJfiTpLm1%2Bustrgs4dbeqD58PB9bUHX%2B9gPUa%2BCHA0PnpbnpLW1HDnrKB0%2Fpm6VuO725fS6OjVKzi4mqDP2Lc0aAYN0N%2FnROCSCMajMpi6Lvdy8cZKQjvYYY%2BFavH9pnbye6TqkGGxirzJIMDrCf7Hw3YiJlmEtVBr3wmKh9T%2F6hNou0Esa8ndy55j5wOGOpHwKNHTydvlFVcsE5Uzp8oRNK5UL27IF7wRzJYNfSjTLI1G3hzMAiP3RYvgA%2Bvfs1fIA5CjCbaPbEZ%2FLuyPqrLbM2evCkdMIerSfRHFGhVl77foUAnbqZ3j7KjuIjjnbDcLvlkG49%2F4gISSwCb4iWYbEEfJqC2v8lafzCe7t1p94R7saF%2F%2BqDZol%2F1oFD3%2FxpJQTnE4iAMNu%2FXiBkKK8PlkdM9k9GqBM6GB%2FMuDJo08WtwyzcyvPL2oOj3UnJoIVWL9DNsM8EsN88q4KoBZK1DmTY8E665DDpQ6%2FHt9YPJiCcrJYaKDDq%2FobLkpQ3iWCxcRo5kUnbMQCyrBykFpeazMqiPwf2bdgffkbSSDK6bnp%2F86qYWmqEusm%2FM5VnnAQoe9WOQbWZKQgvVAPVQWLoi3aTI%2BYiCqzdgHQ5YpuZJD3TbWkOasabaUa3BKRw5FzWxPQCw9asLt7Pre%2Fv8YRoScPhZvKqxungeMK5mx02LMmooIs0T%2FNErD2ZUobjBhPpy3msN3lusb2LGLgFAOFp%2FmjJvvx4DZ1skmB5BEW7OLbQS0bvqw9TX5iB8TxL7MAcXn1b3DIJtnHYiXDgyQcpOr3EAMg418V92o7p9o0WeRYjeUGExdu37dLqdACrxsYrdINJNkkwAX7cNpRUt4sMOhR5NJS1zfsEXBHK0AHRoKAV%2FazJVSW54%2BT%2F0SAqOJRRrME29%2FnrFxQRTaLR1eztOzjxVbUr16mhG7QOQkfmHp%2BLgA%2BO0WPVSmqRGX8%2B5e%2BbPjk6WRkXDfsSWyWjEwo%2FSc68dA%2FxpeYPAPBJNxaBimwYsrJTaYns85KPPoEOOOIzAR8yUAbCqRJySsF7g506cs3x2scVk%2BdjnISpHhoM7MH%2Fg8gnNm%2Fz26cwoxy3np%2FQ0r3CDXXvT6Ioq9iVhd%2FSB4HHd7iHshut6WaEVla6WmFgJii7TU1Q%2Fh%2Fqc042otS4lz%2BOVSoJpuMphLjdiFb0HU9OPE3M%2FX00cR2MJu8tthEa3btdNJKTReXbZFn0ZO4fk20Q3I%2B5qfCJiKJMF4kQbbihtf3vS4sShDAdRhUdjHiOH%2Bak2KA7LzmSFScoeprUDvffyMQYS%2BM1TgZPwyZYgkiE6GEJRGf0EtUhEj6vspjOlYc7PVDvABPTvq9A1XzPHE%2FbrOA7wo2RBbTiPqWRUYqCrHAjah03VmBfOBfXaFcL8qDMph0%2BlJ20aWtEDc0wIa38bbnVcIdNLqtYhS%2FN6HaJIaplKgbX5VETlUx6V5oIr5lCoHjeJvtT7QvwxQNPphfMqrMpdgy8TNtSNX5UnHoJyM5cD3cdRYxiyBiai8i7xiqQNDmdW7vWQw2LrdZcR4VGbPTKUvcIteN3nm74B0KqIXzycsmddF%2F3sg4dsb8oi1xhhkutMSOGSPKyZPp55ggjeArlFcR84u7GD%2Fx9dh%2Ftl1DW%2FMZhFZWnG60s%2BTHZp1yR%2Fu0%2BSOE9RIG45J%2BYizxz2LkJPqIYSBUrr8Z9YMONSDJBfNBE%2BgIK9kFPjaMTf82pra4fKMm65Olq%2Fh0Aoz6Ho8Z7Q0UM9M41lLQhfEa07UiD4aAFsVlRQLfU6a6C50M6EoHtfp88b4k68h9BVsKFaQ%2BudjRetyvw0wkCfC56pA1n%2BFK%2BlBuquajGw5ADFmvuRQwl3mMa8lFrX5tbe1ADSXCh4gRCs8CkBEI3nmb%2BZlSFbxdgMiOU3TmC1f%2Bl5xBqKeiUpw43Tn0kBV%2BeOKT8WqKki25lmeLNC%2FAQmOkXCVdUMZQQwlLG3vWOudv6ffOqICgZDTdBes5kj1%2FZaJxBny0%2Fc7%2FApmb0fCdieRK2zCxb2K2XmofIt3RCtBvt2EiytkhXB4HgK71tfZaiaWi%2F6EWny9OxlyoSozo7iH5BKbBxsa2ouQIjbDAQCAwuX8Tg%2BoFqwKDfqzV%2Fi6kybFjaEK%2Bat%2BV%2FTBETXyCL%2BiPxOWyAtiG%2BH5H2EXQELZL3bhvjX3pSYW1sIJl1karQ%2F%2BjpipADLKJQBLOdu7RSRm1IumxqOKuk6yIMM33zwDMudHR5i8LFEC8EBffI8Az3TbxlmTKuNZOH9wAHbsrNhiKqc5BA7ZngvYxbhXWcfyG7xbQBtDtXaNzykk0%2BrLOUFFsZa4M1R3KMp3gVQSST4RrW8aULEyTaZ47ZEGzXcP7pywz%2Bx9h2hquQQs%2FpEbt2K8H8kVgdQRz%2BvMOJTJRjS81SUrlJuhEfS1Op496QoI%2F9CckCMef8EV75%2BK1RhPh9vjIOHUIfTMiRIdpUaonXzV4dtTQgAVKYG2%2FkzOV4qpKraMa4OxctVbS3Vgp3Pjlud%2BVhNP0wAWYYmLNiN3lY4lB09pvqMNmS5Rxfd8fmVEI8inhuw1yCJD2pWNqoLeI88cuML%2FDI801eACmEcZVA2NubB55MxYDmCmYuo%2FIhFGOqLNzaA1vsHLQ9uBB41eLDrqtAnj8%2F5CZi6FNcthvKYn%2FuFDApQwxFceqm1fd54lIhfpRvPEzeYa01Nwrt2kcMcR5Sh99GJ6rsFZjE1l8tRTfRAfAGyCTuIC7VOpZc86VbX0E5I3lZGro0%2By5kuGda0ai%2BUoW4KWnAxhqBVhiMOpK87dBt8vyBgvzsasY3cZdo8J1OX9ySxyZkrQ%2FZsS142%2FZda4YxznM4BblpmLYieNiJ6yRAINEnf0aCzDwG7fbmD555vxzrcx31xz4n0GyFykiWeDODTZhs5cMWh0BAbHZVjHbQE%3D&__VIEWSTATEGENERATOR=15C4A0A3&__VIEWSTATEENCRYPTED=&__PREVIOUSPAGE=uocENRZD2yWUBVGQhGhaqlYkdNLVux1d56NH-LFCjXEeO052nCfeqasG0poKngNd4H7IVy3GTvC3Po2g70ZZEcCm2ys1&h%24w%24cLogin%24ctrlLogin%24Username=&h%24w%24cLogin%24ctrlLogin%24Password=&h%24w%24PC%24oddsSearch%24txtSearch=&h%24w%24PC%24cCoupon%24txtPrenotatore=Z3XYCZLW&h%24w%24PC%24cCoupon%24hidRiserva=0&h%24w%24PC%24cCoupon%24hidAttesa=0&h%24w%24PC%24cCoupon%24hidCouponAsincrono=0&h%24w%24PC%24cCoupon%24hidTipoCoupon=&h%24w%24PC%24cCoupon%24hidStatoCoupon=0&h%24w%24PC%24cCoupon%24hidBonusNumScommesse=&h%24w%24PC%24cCoupon%24hidQuotaTotaleDIMax=&h%24w%24PC%24cCoupon%24hidQuotaTotaleDIMin=&h%24w%24PC%24cCoupon%24hidQuotaTotale=&h%24w%24PC%24cCoupon%24hidIDQuote=&h%24w%24PC%24cCoupon%24hidModificatoQuote=1&h%24w%24PC%24cCoupon%24hidBonusQuotaMinimaAttivo=0&h%24w%24PC%24cCoupon%24hidBonusRaggruppamentoMinimo=0&h%24w%24PC%24cCoupon%24hidNumItemCoupon=0&h%24w%24PC%24cCoupon%24hidIDCoupon=&h%24w%24PC%24cCoupon%24hidIDBookmakerCoupon=&h%24w%24PC%24cCoupon%24hidIDUtentePiazzamento=&h%24w%24PC%24cCoupon%24hidPrintAsincronoDisabled=0&h%24w%24PC%24cCoupon%24txtIDQuota=&h%24w%24PC%24cCoupon%24txtQB=&h%24w%24PC%24cCoupon%24txtAddImporto=&h%24w%24PC%24cCoupon%24txtIDCouponPrecompilato=&h%24w%24PC%24cCoupon%24txtImportoCouponPrecompilato=&h%24w%24PC%24cCoupon%24txtIDCouponReload=&h%24w%24PC%24ctl09%24txtCodiceCoupon=&h%24w%24PC%24ctl13%24txtVincita=&h%24w%24PC%24ctl13%24txtGiocata='
form_data = {k: v[0] for k, v in parse_qs(form_data).items()}


class HomeView(View):
    def get(self, request, *args, **kwargs):
        contex = dict()
        booking = request.GET.get('booking', None)
        stuff = None

        if booking:
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

        contex['stuff'] = stuff
        contex['booking'] = booking

        return render(request, 'index.html', context=contex)

