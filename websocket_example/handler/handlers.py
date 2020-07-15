from utils.genkey import generate_websocket_key
from utils.document_write import read_html
from utils.des_util import denc,ddec
from dto.websocket_frame import resp_frame

#/register?id=123
def register_conn_handler(conn,conn_context,http_request):
    print('..........register_conn_handler')
    params=http_request.get_params()
    id=params['id']
    conn_context[id]=conn
    try:
        #conn.send(('your id--'+str(id)+'--registered').encode('utf-8'))
        msg='your id--' + str(id) + '--registered'+'\n'
        head1='HTTP/1.1 200 OK\r\nServer:Apache Tomcat/5.0.12\r\nDate:Mon,6Oct2003 13:23:42 GMT\r\nContent-Length:'+str(len(msg))+'\r\n\r\n'
        conn.send((head1+msg).encode('utf-8'))
    except Exception as e:
        print('**********Exception in register_conn_handler************')
        print(e)
        print('************************************')

# /sendmsg?source=256target=123&msg=我是123
#conn_context['target']=conn
def send_msg_handler(conn,conn_context,http_request):
    print('..........conn_context in send_msg_handler',conn_context)
    params=http_request.get_params()
    print('..........parms in send_msg_handler',params)
    source=params['source']
    target=params['target']
    msg   =params['msg']
    try:
        #conn_context[target].send(('msg from--'+source+'--'+msg).encode('utf-8'))
        msg = 'msg from--'+source+'--'+msg+'\n'
        head1 = 'HTTP/1.1 200 OK\r\nServer:Apache Tomcat/5.0.12\r\nDate:Mon,6Oct2003 13:23:42 GMT\r\nContent-Length:' + str(len(msg)) + '\r\n\r\n'

        conn_context[target].send(denc(msg))
        #conn_context[target].send(msg.encode('utf-8'))
        conn.send((head1 + msg).encode('utf-8'))
        conn.close()
    except Exception as e:
        conn.close()
        print('*******Exception in send_msg_handler***************')
        print(e)
        print('************************************')
    finally:
        conn.close()

#/w/register?id=123
def websocket_register_handler(conn,conn_context,http_request):
    print('..........websocket_register_handler')
    params = http_request.get_params()
    id = params['id']
    conn_context[id] = conn
    key=http_request.get_header('Sec-WebSocket-Key')
    print('.........key in websocket_register_handler',key)
    print('.........keys in websocket_register_handler',http_request.get_headers())
    accept_key = generate_websocket_key(key.strip())
    head1='HTTP/1.1 101 Switching Protocols\r\nUpgrade: WebSocket\r\nConnection: Upgrade\r\n'
    str1='Sec-WebSocket-Accept: '+accept_key.decode('utf-8')+'\r\n\r\n'
    print('.....................send data to broswer in register_con_handler:', resp_frame('hello').get_frame())
    conn.send((head1+str1).encode('utf-8'))
    conn.send(resp_frame('hello').get_frame())

# /w/sendmsg?source=256target=123&msg=im256
#conn_context['target']=conn
def websocket_send_msg_handler(conn,conn_context,http_request):
    print('..........conn_context in websocket_send_msg_handler',conn_context)
    params=http_request.get_params()
    print('..........parms in send_msg_handler',params)
    source=params['source']
    target=params['target']
    msg   =params['msg']
    try:
        conn_context[target].send(resp_frame(msg).get_frame())

        head1 = 'HTTP/1.1 200 OK\r\nServer:Apache Tomcat/5.0.12\r\nDate:Mon,6Oct2003 13:23:42 GMT\r\nContent-Length:' +str(len(msg)) + '\r\n\r\n'
        conn.send((head1 + msg).encode('utf-8'))
        conn.close()
    except Exception as e:
        conn.close()
        print(e)
    finally:
        conn.close()




