from convert_file_to_png import file_to_hex_multiprocessing
from multiprocessing import freeze_support
from time import time

#### Configuration ####

save_dir = 'C:\\Gather\\'
undecodedByte = 'FF'

start_msg = '''
            악성코드 분류 딥러닝 모델에 적용할 데이터 수집 프로그램
1. C:\\Gather라는 폴더에 데이터가 수집됩니다.
2. 해당 프로그램은 .exe파일에 대한 이미지 파일을 만드는 것이 목적입니다.
3. 단순히 .exe파일을 실행하지 않고, 읽어서 작업하기 때문에 걱정하지 않아도 됩니다.
4. 프로그램에 문제가 있거나, 소스코드가 궁금하면 010-2002-6205로 연락바랍니다.
5. 5MB 미만의 exe 파일만 수집합니다.
                                                    made by Choi Hyun Woong

먼저 탐색할 드라이브를 입력하세요.(C, D, E)
'''

end_msg = '''
모든 데이터 수집이 끝났습니다.
C:\\Gather\Images와 list 폴더를 압축하여서 chlrjsdnd2@naver.com으로 보내주시기 바랍니다.
감사합니다.

'''


# MAIN
if __name__ == '__main__':

    freeze_support()

    print(start_msg)

    drive = input('Ex. C, D or E = ')
    print(drive + ' 드라이브 탐색을 시작합니다.')

    try:
        start_time = time()

        file_to_hex_multiprocessing(drive + ':\\', "exe", 4)

        end_time = time()

        print("WorkingTime : {0:0.6f} sec\n".format(end_time - start_time))
        print(end_msg)

        input("Press Enter key to exit...")

    except PermissionError as e:
        print(e)