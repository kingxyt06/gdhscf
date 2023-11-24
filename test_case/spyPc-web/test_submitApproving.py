import base64
import json
import os

import pytest


class TestsubmitApproving:
    def test_submitApproving(self, get_agw_token, req_SP):
        # {"assetIds": ["1724346144393887745"]}
        pass

    def saveAsset(self):
        pass

    # @pytest.fixture()
    def test_uploadMediaFile(self, get_sp_token_qy, req_SP):
        modelCode = "MC002"
        catgId = "MC002A"
        busiKey = "1724341809857527809"
        # url = f"media-web/media/opera/do/uploadMediaFiles?modelCode={modelCode}&catgId={catgId}&busiKey={busiKey}"
        url = "media-web/media/opera/do/uploadMediaFiles"
        cookies = get_sp_token_qy
        r = req_SP

        # fileObject = {
        #     # 'modelCode': (None, 'MC002', None),
        #     # 'catgId': (None, 'MC002A', None),
        #     # 'busiKey': (None, '1724341809857527809', None),
        #     'file': (
        #     '1000.jpg', open('1000.jpg', 'rb'), 'image/jpeg')
        # }

        params = {
            'modelCode': 'MC002',
            'catgId': 'MC002B',
            'busiKey': '1722867004222136321',
        }
        with open("1000.jpg", "rb") as img:
            img_file = img.read()
        img_file = base64.b64encode(img_file).decode("utf8")
        img_file = json.dumps({'image': img_file})
        # data = f'------WebKitFormBoundarypk9XbpXgpivNMHVg\r\nContent-Disposition: form-data; name="files"; filename={img_file}\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundarypk9XbpXgpivNMHVg--\r\n'.encode()
        files = {
            'file': ('1000.jpg', open('1000.jpg', 'rb'),
                     'image/jpeg',
                     {'Expires': '0'})
        }

        headers = {'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarypk9XbpXgpivNMHVg'}
        res = r.visit(method="POST", url=url, cookies=cookies, headers=headers, params=params, data=files)
        print(res.request.body)
        res = json.loads(res.text)
        print(res)
