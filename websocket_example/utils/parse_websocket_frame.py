import codecs,binascii
def test9():
    all1=b"\x81\x8b%HK\xefI',\x86Kr)\x86Q+#"
    all2=b'\x81\x8b\x03\xf0\xa4[o\x9f\xc32m\xca\xc62w\x93\xcc'
    all=b'\x81\x8bk\xe3\xf74\x07\x8c\x90]\x05\xd9\x95]\x1f\x80\x9f'
    head=b'\x81\x8bk\xe3\xf74'
    load = b'\x07\x8c\x90]\x05\xd9\x95]\x1f\x80\x9f'
    loadx = 'login:bitch'
    print('all:','--','len:',len(all))
    print('head:', '--', 'len:', len(head))
    print('load:', '--', 'len:', len(load))
    print(head.hex())
    print(all.hex())
    print(all.hex()[4:12]) #8
    print(all.hex()[12:]) #22
    # print(bytes.fromhex(all1.hex()[12:]))
    # print(binascii.unhexlify(all.hex()[12:]).decode('utf-8'))


def xor(i,j):
    return i^j
#mask_key=all.hex[5:]
def mask_str(mask_key,string):
    pass
def parse_websocket_req_str(req):
    result = demask_str(req.hex()[4:13],req.hex()[12:])
    return result
def demask_str(mask_key,string):
    string_list=[]
    print('原来的string:',string)
    print('原来的string的数字:',[int(string[i*2:i*2+2],16) for i in range(len(string)>>1)])
    mask_key_list=[int(mask_key[i*2:i*2+2],16) for i in range(4)]  #int(16进制字符串，16),[107, 190, 227, 63]
    print('mask_key:',mask_key_list)
    for i in range((len(string)>>1)): #len-string:22 ,11个字符(每个8bit),[1]代表1个4bit
        string_list.append(mask_key_list[i%4]^int((string[i*2:i*2+2]),16))
    hex_str = ''.join([hex(string_list[i])[2:] for i in range(len(string_list))])
    print('解码的string:',hex_str)
    print('解码的string的数字:', string_list)
    result = bytes.fromhex(hex_str)
    return result
if __name__ == '__main__':
    #818b 25484bef 49272c864b722986512b23
    #all = b"\x81\x8b%HK\xefI',\x86Kr)\x86Q+#"
    all=b'\x81\x8a\x86\xf1\x9a\x84\xea\x9e\xfd\xed\xe8\xcb\xef\xf7\xe3\x83'
    print(all.hex(),'--','len:',len(all.hex())) #len:34  单位4bit 共17*8 bit,一个英文字母编码 8bit
    demask_str(all.hex()[4:13],all.hex()[12:])  #hex()
    print(all.hex()[4:13],',',all.hex()[12:])
    print(parse_websocket_req_str(all))
    # print(120^190)
    # print(198^190)
    #be 1011 1110 107

