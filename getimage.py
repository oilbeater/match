# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import json
import ConfigParser
import requests
from facepp import API
from facepp import File
import base64
from tornado.escape import json_encode
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        f = open("index.html").read()
        self.write(f)
        print self.__dict__

    def post(self):
        # http://apicn.faceplusplus.com/detection/detect?url=http%3A%2F%2F7jpqp7.com1.z0.glb.clouddn.com%2F16.pic.jpg&api_secret=OAPK3f05zT8jUt_B3DR2pUmT0kdR0uD1&api_key=4cab5d38969f3fc390f08cdf6d1b81d5
        api_key='4cab5d38969f3fc390f08cdf6d1b81d5'
        api_secret='OAPK3f05zT8jUt_B3DR2pUmT0kdR0uD1'
        api = API(api_key, api_secret)
        s = self.request.arguments['img'][0][23:]
        f = open("1.jpg", "w")
        f.write(base64.b64decode(s))
        f.close()
        x = api.detection.detect(img=File('1.jpg'))
        print x
        message ={}
        message['img_id'] = x['face'][0]['face_id']
        message['text'] = u"帅爆了".encode('utf-8')
        # image_url = "http://7jpqp7.com1.z0.glb.clouddn.com/16.pic.jpg"
        # payload = {'api_key': api_key, 'api_secret': api_secret}
        # api_url = 'http://apicn.faceplusplus.com/detection/detect'
        # s = requests.get(api_url, params=payload, data=self.request.content())
        # print s.url
        # print s.json()
        self.write(json_encode(message))

class CompareHandler(tornado.web.RequestHandler):
    def get(self):
        print self.request.uri


application = tornado.web.Application([(r"/", MainHandler),
                                       (r"/compare", CompareHandler),
                                       (r"/(fileinput\.css)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__))))])

if __name__ == "__main__":

    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
