from pathlib import Path
from os.path import basename
import os
from multiprocessing import Process
from threading import Thread
import numpy as np
import array
from math import ceil
from PIL import Image

# 저장 위치
save_dir = 'C:\\Gather'


# hex를 이미지화 시켜주는 메소드
def bytes2png(f, width):

    undecodedByte = 'FF'

    file = f

    """
        Construct image name and return if file already exists
    """
    image_name = f.split('.')[0]
    image_buf = image_name.split('\\')
    image_name = image_buf[0] + '\\' + image_buf[1] + '\\' + 'Images' + '\\' + image_buf[2] + '.png'

    if os.path.isfile(image_name):
        print('Image already exists: {}'.format(image_name))
        return

    # 이미지 저장 경로 설정
    # Images 폴더가 없으면 새로 생성
    if not os.path.exists(save_dir + '\\Images'):
        os.mkdir(save_dir + '\\Images')

    b_data = array.array('i')
    for line in open(file, 'r'):
        for byte in line.rstrip().split():
            # 각 라인마다 앞의 8개의 코드는 주소를 뜻하므로, 제외함.
            # 실제 데이터에서 가져올 때에는 주소 개념이 없음.

            # byte가 ??인 파트는 따로 처리하는 작업
            # 이 부분이 정확도에 크게 기여하는 곳이므로, 처리할 필요가 있음.
            if byte == '??':
                byte = undecodedByte

            # 간혹 byte 코드에 \\이라고 적힌 부분이 있어서 건너뛰어야 함.
            if byte.__contains__('\\'):
                continue

            b_data.append(int(byte, base=16))
            # 16진수 형태로 배열에 부착함

    height = ceil(len(b_data) / width)
    if len(b_data) < (width * height):
        b_data += array.array('i', (0,) * (width * height - len(b_data)))
    image_buffer = np.fromiter(b_data, dtype=np.uint8).reshape((height, width))
    img = Image.fromarray(image_buffer, 'L')
    img.save(image_name)

    # list 폴더가 없다면 새로 생성
    if not os.path.exists(save_dir + '\\list'):
        os.mkdir(save_dir + '\\list')
    txtfile = save_dir + '\\list\\' + 'saveInstance.txt'

    with open(txtfile, mode='a+') as f:
        f.write(file.split('\\')[-1] + '\n')


# 리스트를 n개로 나누기
def chunkify(lst, n):
   return [lst[i::n] for i in range(n)]


# 파일을 읽어 데이터를 리스트로 반환
def read_file(file_path):
    try:
        data_list = []
        with open(file_path, mode="rb") as f:
            while True:
                buf = f.read(16)
                if not buf:
                    break
                else:
                    data_list.append(buf)

        return data_list

    except Exception as ex:
        print("[ERROR] : {0}".format(ex))
        raise Exception(ex) from ex


# data를 hex로 기록한 .txt파일 생성
def create_txt_file(file_name, data):
    file_path = save_dir + '\\' + file_name
    try:
        with open(file_path, mode="wb") as f:
            for i in data:
                f.write(b' '.join(['{:02x}'.format(int(x)).upper().encode() for x in list(i)]))
                f.write(b'\r\n')

            print("[생성 완료] {}".format(file_name))

    except Exception as e:
        print(e)

    return file_path


# hex file 만들기
def make_hex_file(file_path):
    try:
        data_list = read_file(file_path)
        # file_path에서 파일이름만 추출하여 매개변수로 넘겨줌
        create_txt_file(basename(file_path)[:-4] + ".txt", data_list)
    except Exception:
        pass


# 한 번에 여러 개의 hex file 만들기
def make_hex_files(list_of_file_path):
    for file_path in list_of_file_path:
        try:
            data_list = read_file(file_path)
            create_txt_file(basename(file_path)[:-4] + ".txt", data_list)
        except Exception:
            pass


# 여러개의 hex file들을 이미지로 변환
def make_img_files(list_of_file_path):
    for file_path in list_of_file_path:
        try:
            bytes2png(file_path, 256)
        except Exception as e:
            raise e


# 하위 경로에서 file_ext 확장자를 가진 모든 파일 변환
# 기본 버전
def file_to_hex(file_path, file_ext):
    for p in Path(file_path).glob("**\\*."+file_ext):
        make_hex_file(p)


# 멀티프로세싱 적용
# num_of_proc : 사용할 프로세스 개수
def file_to_hex_multiprocessing(file_path, file_ext, num_of_proc):

    """
    :param file_path: 파일이 있는 디렉토리 (주로 C:, D: 등 드라이브 디렉토리를 사용)
    :param file_ext: hex파일로 변환할 파일의 확장자명 (점 제외하고 입력)
    :param num_of_proc: (멀티프로세싱에 사용할 프로세스 개수)

    """

    '''
    hex파일로 변환
    '''
    lst = []

    dir_list = []
    black_list = ["C:\\Windows", ]  # Windows 폴더는 변환 대상에서 제외

    # C:\\ 에 위치한 폴더들(black_list 제외)을 리스트에 추가
    for p in Path(file_path).glob("*"):
        if not(str(p) in black_list):
            dir_list.append(p)
            print(p)

    # dir_list에 있는 폴더에 있는 파일들 모두 검색 (recursively)
    for d in dir_list:
        try:
            for path in Path(d).glob("**\\*."+file_ext):
                try:
                    # 100KB < 파일크기 < 5MB 인 파일만 변환
                    if (100*1024) < os.path.getsize(str(path)) < (5*1024*1024):
                        print(path)
                        lst.append(path)

                except OSError as e:
                    print(e)

        except FileNotFoundError as e:
            print(e)
    # 멀티프로세싱을 위한 task 나누기
    task_list = chunkify(lst, num_of_proc)

    processes = []  # 프로세스 객체를 담을 리스트

    print("Converting exe_file to hex_file...")

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # exe파일들을 hex로 변환한 파일 생성
    for task in task_list:
        process = Process(target=make_hex_files, args=(task, ))
        processes.append(process)
        process.start() # 프로세스 시작

    for proc in processes:
        proc.join()

    print("exe파일의 hex값 추출 완료")

    '''
    이미지로 변환
    '''
    # 재사용을 위한 리스트 비우기
    processes.clear()
    lst.clear()
    task_list.clear()

    for p in Path(save_dir).glob("*.txt"):
        lst.append(str(p))
    # 멀티프로세싱을 위한 task 나누기
    task_list = chunkify(lst, num_of_proc)

    print("이미지로 변환 시작")
    print("변환 중...")

    # hex파일들을 이미지로 변환한 파일 생성
    for task in task_list:
        process = Process(target=make_img_files, args=(task,))
        processes.append(process)
        process.start()  # 프로세스 시작

    for proc in processes:
        proc.join()

    print("이미지 변환 완료")


# 멀티스레딩 적용, 하지만 GIL 때문에 기본 버전과 성능이 같다.
# num_of_proc : 사용할 스레드 개수
def file_to_hex_multithreading(file_path, file_ext, num_of_thread):

    lst = []
    # file_path 포함한, 하위 경로에 있는 파일들 모두 검색
    for p in Path(file_path).glob("**\\*."+file_ext):
        lst.append(p)
    # 멀티프로세싱을 위한 task 나누기
    task_list = chunkify(lst, num_of_thread)

    threads = []  # 스레드 객체를 담을 리스트
    for task in task_list:
        thread = Thread(target=make_hex_files, args=(task, ))
        threads.append(thread)
        thread.start() # 프로세스 시작

    for th in threads:
        th.join()
