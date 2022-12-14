import cgi
from http import cookies
import os

form = cgi.FieldStorage()

text1 = form.getfirst("text-1", "не задано")
text2 = form.getfirst("text-2", "не задано")
if form.getvalue("realmadrid") :
    realmadrid = form.getvalue("realmadrid")
else : realmadrid = ""
if form.getvalue("barcelona") :
    barcelona = form.getvalue("barcelona")
else : barcelona = ""
if form.getvalue("liverpool") :
    liverpool = form.getvalue("liverpool")
else : liverpool = ""
if form.getvalue("psg") :
    psg = form.getvalue("psg")
else : psg = ""
if form.getvalue("fav_player"):
    fav_player = form.getvalue("fav_player")
else : fav_player = "немає"

cs = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
counter = cs.get("counter")

if counter is None:
    print("Set-cookie: counter=0")
else:
    counterVal = int(counter.value)
    counterVal += 1
    print("Set-cookie: counter={}".format(counterVal))



print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="cp1251">
            <title>Обробка даних форм</title>
        </head>
        <body>""")

print("<h1>Обробка даних форм!</h1>")
print("<p>Перший текст: {}</p>".format(text1))
print("<p>Другий текст: {}</p>".format(text2))
print("<p>Улюблені клуби: {} {} {} {}</p>".format(realmadrid,barcelona,liverpool,psg))
print("<p>Улюблений футболіст: {}</p>".format(fav_player))
print("<p>Cookie: Кількість заповнених форм: {} </p> ".format(counterVal))
print("""</body>
        </html>""")