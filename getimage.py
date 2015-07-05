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
from urlparse import parse_qs, urlparse

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print self.request
        f = open("index.html").read()
        self.write(f)

    def post(self):
        print self.request
        # http://apicn.faceplusplus.com/detection/detect?url=http%3A%2F%2F7jpqp7.com1.z0.glb.clouddn.com%2F16.pic.jpg&api_secret=OAPK3f05zT8jUt_B3DR2pUmT0kdR0uD1&api_key=4cab5d38969f3fc390f08cdf6d1b81d5
        api_key = '4cab5d38969f3fc390f08cdf6d1b81d5'
        api_secret = 'OAPK3f05zT8jUt_B3DR2pUmT0kdR0uD1'
        api = API(api_key, api_secret)
        s = self.request.arguments['img'][0][23:]
        f = open("1.jpg", "w")
        f.write(base64.b64decode(s))
        f.close()
        x = api.detection.detect(img=File('1.jpg'))
        message ={}
        if len(x['face']) != 0:
            message['img_id'] = x['face'][0]['face_id']
            message['text'] = u"帅爆了".encode('utf-8')
            print x
        else:
            message['img_id'] = ""
            message['text'] = u"你在逗我".encode('utf-8')
            print "Not a picture"
        self.write(json_encode(message))

class CompareHandler(tornado.web.RequestHandler):
    def get(self):
        params = parse_qs(urlparse(self.request.uri).query, keep_blank_values=True)
        print params
        if len(params['idA']) > 0 and len(params['idB']) > 0 and params['idA'][0] != '' and params['idB'][0] != '':
            id1 = params['idA'][0]
            id2 = params['idB'][0]
            api_key = '4cab5d38969f3fc390f08cdf6d1b81d5'
            api_secret = 'OAPK3f05zT8jUt_B3DR2pUmT0kdR0uD1'
            api = API(api_key, api_secret)
            face1 = api.info.get_face(face_id=id1)
            face2 = api.info.get_face(face_id=id2)
            similiar = api.recognition.compare(face_id1=id1, face_id2=id2)
            print similiar, face1, face2
            self.write(self.judge(face1, face2, similiar))
        else:
            message = {'text': u"你的性取向很奇怪".encode('utf-8')}
            self.write(json_encode(message))

    def judge(self, face1, face2, similiar):
        return "Be together"

application = tornado.web.Application([(r"/", MainHandler),
                                       (r"/compare", CompareHandler),
                                       (r"/(fileinput\.css)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__))))])

if __name__ == "__main__":

    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
