from wsgiref.simple_server import make_server
from html import escape
from urllib.parse import parse_qs
import datetime as dt

html = b"""
<html>
    <body>
        <form method="get" action="">
            <p>
                x: <input type="number" name="x" value="%(x)s">
            </p>

            <p>
                y: <input type="number" name="y" value="%(y)s">
            </p>
            <p>
                <input type="submit" value="Submit">
            </p>
        </form>

        <p>
            Sum: %(sum)s<br>
        </p>
        <p>
            Date: %(date)s<br>
        </p>
    </body>
</html>
"""




def application(environment, start_response):

    d = parse_qs(environment['QUERY_STRING'])
    x = d.get('x', [''])[0]
    y = d.get('y', [''])[0]

    x = escape(x)
    y = escape(y)
    if x.isnumeric() and y.isnumeric() :
        x = int(x)
        y = int(y)
        sum = x + y
    else :
        sum = ''
    
    date = dt.datetime.now()

    response_body = html %{
        b'x' : str.encode(str(x)),
        b'y' : str.encode(str(y)),
        b'sum' : str.encode(str(sum)),
        b'date' : str.encode(str(date))
    }
    status='200 OK'

    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status,response_headers)
    return [response_body]


with make_server('', 8000, application) as server:
    print('Serving on port 8000...')
    server.serve_forever()
