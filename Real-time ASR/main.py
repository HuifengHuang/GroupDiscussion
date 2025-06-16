import shutil
import os
import real_time_recording
import time
from speech_recognition import speech_recognition
from speaker_recognition import req_url
from statement_manager import statement_manager


def recognition(file_path, times):
    text = speech_recognition(file_path)
    if text == '':
        print('there is no voice')
        return
    speaker, score = req_url('search feature', group_id='home', file_path=file_path)
    print('====*Recognition*====', times, ':', speaker, ':', text)
    statement_manager.add_statements(times + '&' + speaker + '&' + text)


def clear_folder(folder_path):
    """
    清空文件夹
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


if __name__ == '__main__':
    clear_folder('./Recording')
    clear_folder('./segment_recording')
    recorder = real_time_recording.AudioRecorder()
    try:
        recorder.start_recording()
        # 主线程可以继续做其他事情
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        recorder.stop_recording()
