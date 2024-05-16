from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from dash_app import create_dash_application
from dash_app2 import create_dash_application2
from dash_app3 import create_dash_application3
from dash_app4 import create_dash_application4
from dash_app5 import create_dash_application5
from dash_app6 import create_dash_application6
from dash_app7 import create_dash_application7
app = FastAPI()

dash_app = create_dash_application()
dash_app2 = create_dash_application2()
dash_app3 = create_dash_application3()
dash_app4 = create_dash_application4()
dash_app5 = create_dash_application5()
dash_app6 = create_dash_application6()
dash_app7 = create_dash_application7()

app.mount("/dash", WSGIMiddleware(dash_app.server))
app.mount("/dash2", WSGIMiddleware(dash_app2.server))
app.mount("/dash3", WSGIMiddleware(dash_app3.server))
app.mount("/dash4", WSGIMiddleware(dash_app4.server))
app.mount("/dash5", WSGIMiddleware(dash_app5.server))
app.mount("/dash6", WSGIMiddleware(dash_app6.server))
app.mount("/dash7", WSGIMiddleware(dash_app7.server))
