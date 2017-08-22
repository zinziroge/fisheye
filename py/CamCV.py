from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#import glfw
import cv2

from glfw_wrapper import *
from Camera import Camera

# OpenCV を使ってキャプチャするクラス
class CamCV(Camera):
    def __init__(self):
        super().__init__()

        # OpenCV のキャプチャデバイス
        self.camera = cv2.VideoCapture()
        # OpenCV のキャプチャデバイスから取得したフレーム
        self.frame = None
        # 現在のフレームの時刻
        self.frameTime = 0
        # 露出と利得
        self.exposure = 0
        self.gain = 0

    def init_setting(self, initial_width, initial_height, initial_fps):
        # カメラの解像度を設定する
        if (initial_width > 0):
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, initial_width)
        if (initial_height > 0):
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, initial_height)
        if (initial_fps > 0):
            self.camera.set(cv2.CAP_PROP_FPS, initial_fps)

        # カメラから最初のフレームをキャプチャする
        if (self.camera.grab()):
            # 最初のフレームを取得した時刻を基準にする
            glfwSetTime(0.0)

            # 最初のフレームの時刻は 0 にする
            self.frameTime = 0.0

            # キャプチャしたフレームのサイズを取得する
            self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

            # macOS だと設定できても 0 が返ってくる
            if (self.width == 0):
                self.width = initial_width
            if (self.height == 0):
                self.height = initial_height

            # カメラの利得と露出を取得する
            self.gain = self.camera.get(cv2.CAP_PROP_GAIN)
            self.exposure = self.camera.get(cv2.CAP_PROP_EXPOSURE) * 10.0

            # キャプチャされるフレームのフォーマットを設定する
            self.format = GL_BGR

            # フレームを取り出してキャプチャ用のメモリを確保する
            #self.frame = self.camera.retrieve(self.frame, 3)
            is_success, self.frame = self.camera.retrieve(self.frame, 3)
            #(frame_len, is_success, self.frame) = self.camera.retrieve(self.frame, 3)
            print(self.frame.shape)

            # フレームがキャプチャされたことを記録する
            self.buffer = self.frame #.data

            # カメラが使える
            return True

        # カメラが使えない
        return False

    # @todo: implement thread process
    def capture(self):
        # フレームをキャプチャする
        super(CamCV, self).capture()
        # あらかじめキャプチャデバイスをロックして
        #mtx.lock()

        # スレッドが実行可の間
        #while (self.run):
            # バッファが空のとき経過時間が現在のフレームの時刻に達していて
            #if (not self.buffer and glfwGetTime() >= self.frameTime):
            #if (self.buffer is not None and glfwGetTime() >= self.frameTime):
            #    # 次のフレームが存在すれば
            #    if (self.camera.grab()):
            #        # キャプチャしたフレームの時刻を記録して
            #        self.frameTime = self.camera.get(cv2.CAP_PROP_POS_MSEC) * 0.001

            #        # 到着したフレームを切り出して
            #        # cv2.camera.retrieve(self.frame, 3)
            #        is_success, self.frame = self.camera.retrieve(3)

            #        # フレームを更新し
            #        self.buffer = self.frame #.data

            #        # 次のフレームに進む
            #        continue

            #    # フレームが取得できなかったらムービーファイルを巻き戻し
            #    if (self.camera.set(cv2.CAP_PROP_POS_FRAMES, 0.0)):
            #        # 経過時間をリセットして
            #        glfwSetTime(0.0)

            #        # フレームの時刻をリセットし
            #        self.frameTime = 0.0

            #        # 次のフレームに進む
            #        continue

        is_success, self.frame = self.camera.retrieve(3)
        self.buffer = self.frame #.data

        #    # フレームが切り出せなければロックを解除して
        #    mtx.unlock()

        #    # 他のスレッドがリソースにアクセスするために少し待ってから
        #    std::this_thread::sleep_for(std::chrono::milliseconds(10L))

        #    # またキャプチャデバイスをロックする
        #    mtx.lock()

        # 終わるときはロックを解除する
        #mtx.unlock()

    # デストラクタ
    def finish(self):
        # スレッドを停止する
        self.stop()

    def open(self, device_or_file, _width = 0, _height = 0, _fps = 0):
        if ( isinstance(device_or_file, int)):
            return self.__open_camera(device_or_file, _width, _height, _fps)
        else:
            return self.__open_file_network(device_or_file, _width, _height, _fps)

    # カメラから入力する
    def __open_camera(self, device, _width, _height, _fps):
        # カメラを開く
        self.camera.open(device)

        # カメラが使えればカメラを初期化する
        if (self.camera.isOpened() and self.init_setting(_width, _height, _fps)):
            return True

        # カメラが使えない
        print("Can't open camera.\n", file=sys.stderr)
        return False

    # ファイル／ネットワークから入力する
    def __open_file_network(self, file, _width, _height, _fps):
        # ファイル／ネットワークを開く
        self.camera.open(file)

        # ファイル／ネットワークが使えれば初期化する
        if (self.camera.isOpened() and self.init_setting(_width, _height, _fps)):
            return True

        # ファイル／ネットワークが使えない
        print("Can't open file or network.\n", file=sys.stderr)
        return False

    # 露出を上げる
    def increaseExposure(self):
        if (self.camera.isOpened()):
            self.camera.set(cv2.CAP_PROP_EXPOSURE, ++self.exposure * 0.1)

    # 露出を下げる
    def decreaseExposure(self):
        if (self.camera.isOpened()):
            self.exposure -= 1
            self.camera.set(cv2.CAP_PROP_EXPOSURE, self.exposure * 0.1)

    # 利得を上げる
    def increaseGain(self):
        self.gain += 1
        if (self.camera.isOpened()):
            self.camera.set(cv2.CAP_PROP_GAIN, self.gain)

    # 利得を下げる
    def decreaseGain(self):
        if (self.camera.isOpened()):
            self.gain -= 1
            self.camera.set(cv2.CAP_PROP_GAIN, self.gain)
