#!/usr/bin/python3
# coding=utf-8
"""OpenAI 兼容 VLM 客户端 (支持 GPT-4o / Qwen-VL / Ollama 等)"""

import json
import base64
import urllib.request
import urllib.error


class VLMClient(object):
    def __init__(self, api_base, api_key='', model='gpt-4o-mini', timeout=60):
        self.api_base = api_base.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def _post_chat(self, messages):
        url = self.api_base + '/chat/completions'
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': 0.1,
            'max_tokens': 256,
        }
        data = json.dumps(payload).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = 'Bearer ' + self.api_key
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf-8', errors='replace')
            raise RuntimeError('VLM HTTP %s: %s' % (e.code, detail))
        return body['choices'][0]['message']['content']

    @staticmethod
    def _encode_image_bgr(image_bgr):
        import cv2
        ok, buf = cv2.imencode('.jpg', image_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if not ok:
            raise RuntimeError('图像编码失败')
        return base64.b64encode(buf).decode('ascii')

    def select_object_index(self, query, objects_desc, image_bgr=None):
        """根据自然语言从物体列表中选择索引，失败返回 None"""
        system_prompt = (
            '你是机械臂抓取助手。根据物体列表和用户指令，选出应抓取的物体编号。'
            '坐标系为机器人 base_link：X 前方，Y 左侧为正。'
            '只回复一个 JSON：{"index": <int>, "reason": "<简短说明>"}。'
            '若无法确定，回复 {"index": -1, "reason": "..."}。'
        )
        user_text = '用户指令：%s\n\n物体列表：\n%s' % (query, objects_desc)

        if image_bgr is not None:
            image_b64 = self._encode_image_bgr(image_bgr)
            user_content = [
                {'type': 'text', 'text': user_text + '\n\n可参考附带的桌面相机图像。'},
                {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + image_b64}},
            ]
        else:
            user_content = user_text

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_content},
        ]
        raw = self._post_chat(messages).strip()
        return self._parse_index(raw)

    @staticmethod
    def _parse_index(text):
        start = text.find('{')
        end = text.rfind('}')
        if start < 0 or end <= start:
            raise RuntimeError('VLM 返回非 JSON: %s' % text[:200])
        data = json.loads(text[start:end + 1])
        idx = int(data.get('index', -1))
        reason = data.get('reason', '')
        if idx < 0:
            return None, reason
        return idx, reason
