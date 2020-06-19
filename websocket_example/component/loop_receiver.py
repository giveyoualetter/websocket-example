import socketserver,threading,time,socket,struct
from component.dispatcher import Dispatcher
from utils.parsehttp import ParseHttp
from utils.parse_websocket_frame import demask_str,parse_websocket_req_str
from concurrent.futures import ThreadPoolExecutor
#{ id : conn}
conn_context={}
#{ id : current_time}
conn_context_afi_time = {}
def close_silent_socket(conn_context_afi_time,conn_context):
    while True:
        #print('..........gc started!')
        try:
            time.sleep(2)
            for i in list(conn_context_afi_time.keys()):
                    if time.time() - conn_context_afi_time[i] > 20:
                        if i in conn_context.keys():
                            #print(conn_context[i].getsockopt(socket.SOL_SOCKET, socket.SO_LINGER))
                            conn_context[i].shutdown(socket.SHUT_RDWR)
                            conn_context[i].close()
                            del conn_context[i]
                            del conn_context_afi_time[i]
        except Exception as e:
            print('...........Exception in close_silent_socket:',e)
#{conn:[b'',time]}
conn_context_reg_time = {}
def close_unregister_socket(conn_context_reg_time):
    while True:
        try:
            time.sleep(2)
            for i in list(conn_context_reg_time.keys()):
                if i.fileno()<0:
                    del conn_context_reg_time[i]
                else:
                    if conn_context_reg_time[i][0]==b'':
                        if time.time()-conn_context_reg_time[i][1]>10:
                            i.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
                            i.shutdown(socket.SHUT_RDWR)
                            i.close()
                            del conn_context_reg_time[i]
                    else:
                        del conn_context_reg_time[i]
        except Exception as e:
            print('...........Exception in close_unregister_socket:',e)

executor = ThreadPoolExecutor(max_workers=10)
task=executor.submit(close_silent_socket,conn_context_afi_time,conn_context)
executor.submit(close_unregister_socket,conn_context_reg_time)
#print('..........after',task.done())
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # try:
            conn_context_reg_time[self.request]=[b'',time.time()]
            while True:
                print('**********************************')
                if self.request.fileno()>0:
                    print(self.request.getpeername(), ':', self.request.fileno())
                    self.data=b''

                    empty_count=0
                    start_time=0

                    while self.data==b'':
                        self.data = self.request.recv(6000)
                        if self.data==b'':
                            empty_count+=1
                            if empty_count==1:
                                start_time=time.time()
                            if empty_count==10:
                                if time.time()-start_time<10:
                                    for i in list(conn_context.keys()):
                                        if conn_context[i]==self.request:
                                            del conn_context[i]
                                            del conn_context_afi_time[i]
                                    self.request.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 1, 0))
                                    self.request.shutdown(socket.SHUT_RDWR)
                                    self.request.close()
                                else:
                                    empty_count=0

                        if self.data!=b'':
                            break
                else:
                    break
                print('............self.data in MyTcpHandler',self.data)
                if self.data[0]==129: #0x81
                    print('..................websocket data in MyTcpHandler:',parse_websocket_req_str(self.data))
                    continue
                if self.data==b'live':
                    for i in list(conn_context.keys()):
                        if conn_context[i]==self.request:
                            if i in conn_context.keys():
                                conn_context_afi_time[i] = time.time()
                            break
                    continue
                http_request=ParseHttp.parse_http_request(self.data.decode('utf-8'))

                if http_request.get_route()=='/register':
                    params = http_request.get_params()
                    id = params['id']
                    conn_context_afi_time[id] = time.time()
                    KEY = 'mHAxsLYz'
                    self.request.send(KEY.encode("utf-8"))
                    conn_context_reg_time[self.request][0]=id.encode('utf-8')
                    conn_context_reg_time[self.request][1]=time.time()

                route_flag=Dispatcher.invoke_method(self.request,conn_context,http_request)
         # except Exception as e:
        #     print(self.client_address,"连接断开")
        # finally:
        #     self.request.close()
    def setup(self):
        print("before handle,连接建立：",self.client_address)
    def finish(self):
        print("finish run  after handle",self.client_address)