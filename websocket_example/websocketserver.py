import socket,socketserver
from component.dispatcher import Dispatcher
from component.context import MyTCPHandler
from handler.handlers import send_msg_handler,register_conn_handler,websocket_register_handler,\
                              websocket_send_msg_handler,index_page,jquery_min_js

class BootStrap:
    def __init__(self):
        Dispatcher.register('/sendmsg',send_msg_handler)
        Dispatcher.register('/register',register_conn_handler)
        Dispatcher.register('/w/register',websocket_register_handler)
        Dispatcher.register('/w/sendmsg', websocket_send_msg_handler)
        Dispatcher.register('/index',index_page)
        Dispatcher.register('/jquery-min.js',jquery_min_js)
    def start(self):
        HOST, PORT = "127.0.0.1", 8000
        server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()
if __name__=='__main__':
    BootStrap().start()
