import hashlib,base64
def generate_websocket_key(sec_websocket_key):
    str=(sec_websocket_key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode('utf-8')
    return base64.b64encode(hashlib.sha1(str).digest())