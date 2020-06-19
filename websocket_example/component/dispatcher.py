import time
class Dispatcher:
    route_method={}
    def register(route,method):
        Dispatcher.route_method[route]=method
    def invoke_method(con,conn_context,http_request):
        route=http_request.get_route()
        print('..........route in Dispatcher',route)
        if route==None:
            return None
        if route not in Dispatcher.route_method.keys():
            return None
        Dispatcher.route_method[route](con,conn_context,http_request)
        return None