import base64
import os

from pydub import AudioSegment

from generalRequest import Gen_req_url
import json
import requests


APPId = "a69d6c98"


def gen_create_group():
    body = {
        "header": {
            "app_id": APPId,
            "status": 3
        },
        "parameter": {
            "s782b4996": {
                "func": "createGroup",
                "groupId": "home",
                "createFeatureRes": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
    }
    return body


def gen_create_feature(group_id, feature_id, voice_file_path):
    with open(voice_file_path, "rb") as f:
        audioBytes = f.read()
    body = {
        "header": {
            "app_id": APPId,
            "status": 3
        },
        "parameter": {
            "s782b4996": {
                "func": "createFeature",
                "groupId": group_id,
                "featureId": feature_id,
                "createFeatureRes": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "resource": {
                "encoding": "lame",
                "sample_rate": 16000,
                "channels": 1,
                "bit_depth": 16,
                "status": 3,
                "audio": str(base64.b64encode(audioBytes), 'UTF-8')
            }
        }
    }
    return body


def gen_search_feature(group_id, voice_file_path):
    with open(voice_file_path, "rb") as f:
        audioBytes = f.read()
    body = {
        "header": {
            "app_id": APPId,
            "status": 3
        },
        "parameter": {
            "s782b4996": {
                "func": "searchFea",
                "groupId": group_id,
                "topK": 2,
                "searchFeaRes": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "resource": {
                "encoding": "lame",
                "sample_rate": 16000,
                "channels": 1,
                "bit_depth": 16,
                "status": 3,
                "audio": str(base64.b64encode(audioBytes), 'UTF-8')
            }
        }
    }
    return body


def req_url(file_path=None):
    """
    开始请求
    :param file_path: body里的文件路径
    :return:
    """

    APISecret = "MzNhZWY0YTM0MzBkOWU4MDY5ZTVkMzNl"
    APIKey = "542ef30748a29afb6837bab801610898"
    gen_req_url = Gen_req_url()
    if file_path.endswith(".wav"):
        file_path = convert_wav_to_mp3(file_path)
    body = gen_search_feature("home", file_path)
    request_url = gen_req_url.assemble_ws_auth_url(requset_url='https://api.xf-yun.com/v1/private/s782b4996', method="POST", api_key=APIKey, api_secret=APISecret)

    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'appid': '$APPID'}
    response = requests.post(request_url, data=json.dumps(body), headers=headers)
    tempResult = json.loads(response.content.decode('utf-8'))
    print(tempResult)
    result = decode_base64_to_dict(tempResult['payload']['searchFeaRes']['text'])
    print('current speaker: ', result['scoreList'][0]['featureId'])


def convert_wav_to_mp3(input_wav_path, output_mp3_path=None, bitrate="16k"):
    """
    将 WAV 文件转换为 MP3 文件

    参数:
        input_wav_path (str): 输入的 WAV 文件路径
        output_mp3_path (str): 输出的 MP3 文件路径（可选，默认与输入同目录）
        bitrate (str): 输出的比特率，默认为 "192k"
    """
    # 如果没有指定输出路径，则使用输入文件相同目录，仅修改扩展名
    if output_mp3_path is None:
        output_mp3_path = input_wav_path.rsplit('.', 1)[0] + '.mp3'

    # 加载 WAV 文件
    audio = AudioSegment.from_wav(input_wav_path)

    # 导出为 MP3
    audio.export(output_mp3_path, format="mp3", bitrate=bitrate)

    print(f"转换成功: {input_wav_path} -> {output_mp3_path}")
    return output_mp3_path


def decode_base64_to_dict(base64_str):
    """
    将base64字符串解码为字典
    """
    # 将base64字符串转换为字节
    base64_bytes = base64_str.encode('utf-8')
    # 进行base64解码
    bytes_data = base64.b64decode(base64_bytes)
    # 将字节转换为字符串
    json_str = bytes_data.decode('utf-8')
    # 将JSON字符串转换为字典
    return json.loads(json_str)


if __name__ == '__main__':
    file_path = 'read_book.wav'
    # apiname取值:
    # 1.创建声纹特征库 createGroup
    # 2.添加音频特征 createFeature
    # 3.查询特征列表 queryFeatureList
    # 4.特征比对1:1 searchScoreFea
    # 5.特征比对1:N searchFea
    # 6.更新音频特征 updateFeature
    # 7.删除指定特征 deleteFeature
    # 8.删除声纹特征库 deleteGroup
    req_url(file_path=file_path)
