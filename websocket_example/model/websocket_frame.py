
class req_frame:
    pass

class resp_frame:
    '''
    用于描述消息是否结束，如果为1则该消息为消息尾部,如果为零则还有后续数据包
    '''
    FIN             =0b1000 #<1>0000000
    RESERVED        =0b0000 #0<000>0000
    '''
    0x0表示附加数据帧
    0x1表示文本数据帧
    0x2表示二进制数据帧
    0x3 - 7暂时无定义，为以后的非控制帧保留
    0x8表示连接关闭
    0x9表示ping
    0xA表示pong
    0xB - F暂时无定义，为以后的控制帧保留
    '''
    OP_CODE_BIN     =0x2#0b0001 #00000<0001>
    OP_CODE_TEXT    =0x1#0b0010 #00000<0010>
    OP_CODE         =OP_CODE_TEXT
    MASK            =0b0000 #<0>0000000   #此处忽略
    '''
    PayloadData的长度：7位，7+16位，7+64位
    如果其值在0-125，则是payload的真实长度。
    如果值是126，则后面2个字节形成的16位无符号整型数的值是payload的真实长度。
    如果值是127，则后面8个字节形成的64位无符号整型数的值是payload的真实长度
    '''
    PAYLOAD_LENGTH_7_1  ='0x0'#0b0000 #0<0000000>
    PAYLOAD_LENGTH_7_2  ='0x0'#0b0000
    PAYLOAD_LENGTH_16_1  ='0x0'#0b0000
    PAYLOAD_LENGTH_16_2  ='0x0'#0b0000
    PAYLOAD_LENGTH_16_3  ='0x0'#0b0000
    PAYLOAD_LENGTH_16_4  ='0x0'#0b0000
    PAYLOAD_LENGTH_16_list=[PAYLOAD_LENGTH_16_1,PAYLOAD_LENGTH_16_2,PAYLOAD_LENGTH_16_3,PAYLOAD_LENGTH_16_4]
    pay_load=''
    def __init__(self,pay_load):
        self.pay_load=pay_load
        length = len(pay_load)
        if length<125:
            '''
            0111 1101 125
            0000 1111 15
            0100 0001 65   
            0111 1110 126
            0111 1111 127   
            '''
            if length<16:
                self.PAYLOAD_LENGTH_7_2=hex(length)
            else:
                b=bin(length)  #b:str 0b100 0001  注意不是 0b0100 0001
                self.PAYLOAD_LENGTH_7_1= hex(int(b[2:5],2))
                self.PAYLOAD_LENGTH_7_2= hex(int(b[-4:],2))
        elif length<sum([0b1<<i for i in range(16)]):
            self.PAYLOAD_LENGTH_7_1='0xe'
            self.PAYLOAD_LENGTH_7_2='0xf'
            b=bin(length)  # 0b1001
            n=len(b[2:])
            b2=b[2:]       # 1 1001 1110 0001
            t=int(n/4)     # 3   3个4bit
            r=t%4   #余数   剩余0/1个数
            index=3
            for i in range(t):
                self.PAYLOAD_LENGTH_16_list[index]=hex(int(b2[r+4*i:r+4*i+4],2))
                index-=1
            #index= 3->2->1->0
            if r!=0:
                self.PAYLOAD_LENGTH_16_list[index]=hex(int(b2[:r],2))
        else:
            pass
    def set_opcode(self,k):
        if k=='bin':
            self.OP_CODE=self.OP_CODE_BIN
    def get_frame(self):
        head = None
        if len(self.pay_load)<125:
            FR      =hex(int(self.FIN+self.RESERVED))[2:] #0b -> int ->hex
            OC      =hex(self.OP_CODE)[2:]                #hex->hex
            PL_7_1  =hex(int(self.PAYLOAD_LENGTH_7_1,16))[2:] #hex_str ->int ->hex
            PL_7_2  =hex(int(self.PAYLOAD_LENGTH_7_2,16))[2:]
            print(FR,'--',OC,'--',PL_7_1,'--',PL_7_2,'--',)
            head=FR+OC+PL_7_1+PL_7_2
        elif len(self.pay_load)<sum([0b1<<i for i in range(16)]):
            FR      = hex(int(self.FIN + self.RESERVED))[2:]  # 0b -> int ->hex
            OC      = hex(self.OP_CODE)[2:]  # hex->hex
            PL_7    = hex(int(self.PAYLOAD_LENGTH_7_1,16))[2:]+hex(int(self.PAYLOAD_LENGTH_7_2,16))[2:]
            print(PL_7)
            PL_16   = hex(int(self.PAYLOAD_LENGTH_16_list[0],16))[2:]+hex(int(self.PAYLOAD_LENGTH_16_list[1],16))[2:]+\
                      hex(int(self.PAYLOAD_LENGTH_16_list[2], 16))[2:]+hex(int(self.PAYLOAD_LENGTH_16_list[3],16))[2:]
            head=FR+OC+PL_7+PL_16
        print(len(self.pay_load))
        return bytes.fromhex(head)+self.pay_load.encode('utf-8')
if __name__=='__main__':
    print(resp_frame('').get_frame())


