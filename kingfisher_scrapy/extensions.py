from urllib3.filepost import encode_multipart_formdata
from scrapy.http import Request

# https://github.com/scrapy/scrapy/pull/1954#issuecomment-316438959

class MultipartFormRequest(Request):
    def __init__(self, *args, **kwargs):
        formdata = kwargs.pop('formdata', None)
        if formdata and kwargs.get('method') is None:
            kwargs['method'] = 'POST'

        super(MultipartFormRequest, self).__init__(*args, **kwargs)

        if formdata:
            body, content_type = encode_multipart_formdata(formdata)
            self.headers[b'Content-Type'] = content_type.encode('utf-8')

            print(body)