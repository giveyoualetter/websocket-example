import re
class HttpRequest:
    line=''
    headers={} #
    body=''
    def __init__(self):
        pass
    def get_route(self):
        line=self.get_line()
        print('................line in httpmsg',line)
        url=re.search('(/.*?)\s',line)
        if url!=None:
            url=url.groups()[0]
            if url.find('?')<0:
                return url
            else:
                return url.split('?')[0]
    def get_params(self):
        dict={}
        line=self.get_line()
        if line.find('?')<0:
            return None
        else:
            line=re.search('/(.*?)\s',line).groups()[0]
            params_str=line.split('?')[1]
            params_list=params_str.split('&')
            for param_str in params_list:
                if param_str!='':
                    param_list=param_str.split('=')
                    dict[param_list[0]]=param_list[1]
        return dict
    def get_line(self):
        return self.line
    def get_header(self,header_name):
        if header_name in self.headers.keys():
            return self.headers[header_name]
        else:
            return None
    def get_headers(self):
        return self.headers
    def get_body(self):
        return self.body
    def set_line(self,line):
        self.line=line
    def set_header(self, header_key,header_value):
        self.headers[header_key]=header_value
    def set_body(self,body):
        self.body=body
    def to_string(self):
        header_string='\\r\\n'.join([str(i)+':'+str(self.headers[i]) for i in list(self.headers)])
        if self.body=='':
            return '\\r\\n'.join([self.line,header_string])
        else:
            return '\\r\\n'.join([self.line,header_string,self.body])+'\\n'
class HttpResponse:
    line = ''
    headers = {}  #
    body = ''
    def __init__(self):
        pass
    def get_line(self):
        return self.line
    def get_header(self, header_name):
        if header_name in self.headers.keys():
            return self.headers[header_name]
        else:
            return None
    def get_headers(self):
        return self.headers
    def get_body(self):
        return self.body
    def set_line(self,line):
        self.line=line
    def set_header(self, header_key,header_value):
        self.headers[header_key]=header_value
    def set_body(self,body):
        self.body=body
    def to_string(self):
        header_string = '\\r\\n'.join([str(i) + ':' + str(self.headers[i]) for i in list(self.headers)])
        if self.body == '':
            return '\\r\\n'.join([self.line, header_string])
        else:
            return '\\r\\n'.join([self.line, header_string, self.body]) + '\\n'