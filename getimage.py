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
import math

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
        message = {}
        print x
        if len(x['face']) != 0:
            print x
            message['img_id'] = x['face'][0]['face_id']
            message['text'] = self.guess(x)

        else:
            message['img_id'] = ""
            message['text'] = u"你不是人".encode('utf-8')
            print "Not a picture"
        self.write(json_encode(message))

    def guess(self, face):
        age = face['face'][0]['attribute']['age']['value']
        gender = face['face'][0]['attribute']['gender']['value']
        smiling = face['face'][0]['attribute']['smiling']['value']
        result = []
        if gender == 'Male':
            result.append(str(age))
            result.append(u"帅哥")
            if int(age) > 31:
                result.append(u"老男人")
            else:
                result.append(u"小鲜肉")
            if smiling > 50:
                result.append(u"心花怒放")
            elif smiling < 5:
                result.append(u"内心紧张")
            else:
                result.append(u"蓄势待发")
        else:
            result.append(age)
            result.append(u"美女")
            if int(age) > 31:
                result.append(u"小女生")
            else:
                result.append(u"小女生")
            if smiling > 50:
                result.append(u"得意的笑")
            elif smiling < 5:
                result.append(u"楚楚可人")
            else:
                result.append(u"开心")

        return result

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
        print face1['face_info'][0]['attribute']['gender']['value']
        print face1['face_info'][0]['attribute']['age']['value']
        print face1['face_info'][0]['attribute']['smiling']['value']
        print face2['face_info'][0]['attribute']['gender']['value']
        print face2['face_info'][0]['attribute']['age']['value']
        print face2['face_info'][0]['attribute']['smiling']['value']
        # temp = {u'face_info': [{u'url': None, u'attribute':
        #     {u'gender': {u'confidence': 99.9995, u'value': u'Male'}, u'age': {u'range': 5, u'value': 30},
        #      u'race': {u'confidence': 99.995, u'value': u'Asian'}, u'smiling': {u'value': 0.717482}}, u'faceset': [], u'person': [], u'tag': u'', u'img_id': u'33403fb43468d49468e8d206a67b85ba', u'position': {u'eye_left': {u'y': 53.277778, u'x': 37.85}, u'center': {u'y': 62.585034, u'x': 50.0}, u'width': 55.865922, u'mouth_left': {u'y': 76.586168, u'x': 39.467877}, u'height': 45.351474, u'mouth_right': {u'y': 76.668707, u'x': 59.82067}, u'nose': {u'y': 63.254195, u'x': 49.865084}, u'eye_right': {u'y': 53.65941, u'x': 62.284916}}, u'face_id': u'b48cb740bac8abd625cf8e4d03eb0402'}
        if float(similiar['similarity']) > 90:
            message = {'text': u"你就和自己过一辈子吧！".encode('utf-8')}
        else:
            if face1['face_info'][0]['attribute']['gender']['value'] == face2['face_info'][0]['attribute']['gender']['value'] == 'Male':
                message = {'text': u"好基友一辈子！".encode('utf-8')}
            if face1['face_info'][0]['attribute']['gender']['value'] == face2['face_info'][0]['attribute']['gender']['value'] == 'Female':
                message = {'text': u"幸福姐妹二人组！".encode('utf-8')}
            if face1['face_info'][0]['attribute']['gender']['value'] != face2['face_info'][0]['attribute']['gender']['value']:
                if -8 < face1['face_info'][0]['attribute']['age']['value'] - face2['face_info'][0]['attribute']['age']['value'] < 8:
                    print face1['face_info'][0]['attribute']['age']['value'] - face2['face_info'][0]['attribute']['age']['value']
                    message = {'text': u"金童玉女，幸福一生！".encode('utf-8')}
                else:
                    message = {'text': u"老牛吃嫩草！".encode('utf-8')}
        return json_encode(message)

application = tornado.web.Application([(r"/", MainHandler),
                                       (r"/compare", CompareHandler),
                                       (r"/(fileinput\.css)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__))))])

if __name__ == "__main__":

    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
