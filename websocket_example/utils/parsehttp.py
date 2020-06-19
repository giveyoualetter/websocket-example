import re
from dto.httpmsg import HttpRequest
class ParseHttp:
    def __init__(self):
        pass
    def parse_http_request(http_req_str):
        try:
            http_request=HttpRequest()
            #获得line
            req_list=http_req_str.split('\r\n')
            http_request.set_line(req_list[0])
            #获得headers
            for i in req_list[1:]:
                if i != '':
                    result = re.match('(.*?):(.*)', i)
                    if result != None:
                        http_request.set_header(result.group(1),result.group(2))
            #获得body
            req_list=http_req_str.split('\r\n\r\n')
            if len(req_list)>1:
                if req_list[1]!='':
                    http_request.set_body(req_list[1])
        except Exception as e:
            print('**********Exception in parse_http_request************')
            print(e)
            print('************************************')
        return http_request


