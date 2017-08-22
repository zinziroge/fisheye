#
# カメラ関連の処理
#

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# 補助プログラム
import gg

##include "gg.h"
##using namespace gg

## キャプチャを非同期で行う
##include <thread>
##include <mutex>

#
# カメラ関連の処理を担当するクラス
#
class Camera(object):
    #  # コピーコンストラクタを封じる
    #  Camera(const Camera &c)
    #
    #  # 代入を封じる
    #  Camera &operator=(const Camera &w)

    def __init__(self):
        # キャプチャした画像
        #GLubyte self.buffer
        self.buffer = None

        # キャプチャした画像の幅と高さ
        self.width = 0
        self.height = 0

        # キャプチャされる画像のフォーマット
        #GLenum format
        self.format = 0

        # スレッド
        #std::thread thr
        #self.thr

        # ミューテックス
        #std::mutex mtx
        #self.mtx

        # 実行状態
        self.run = False

        # 画像がまだ取得されていないことを記録しておく
        #buffer = nullptr
        self.buffer = None

        # スレッドが停止状態であることを記録しておく
        self.run = False

    # フレームをキャプチャする
    def capture(self):
        pass

    # スレッドを起動する
    def start(self):
        # スレッドが起動状態であることを記録しておく
        self.run = True

        # @todo: implement thread process
        # スレッドを起動する
        #thr = std::thread([this](){ this->capture() })
        self.capture()

    # スレッドを停止する
    def stop(self):
        # @todo: implement thread process
        ## キャプチャスレッドが実行中なら
        #if (self.run):
        #  # キャプチャデバイスをロックする
        #  mtx.lock()

        #  # キャプチャスレッドのループを止めて
        #  run = false

        #  # ロックを解除し
        #  mtx.unlock()

        #  # 合流する
        #  thr.join()
        pass

    # 画像の幅を得る
    def getWidth(self):
        return self.width

    # 画像の高さを得る
    def getHeight(self):
        return self.height

    # Ovrvision Pro の露出を上げる
    def increaseExposure(self):
        pass

    # Ovrvision Pro の露出を下げる
    def decreaseExposure(self):
        pass

    # Ovrvision Pro の利得を上げる
    def increaseGain(self):
        pass

    # Ovrvision Pro の利得を下げる
    def decreaseGain(self):
        pass

    # カメラをロックして画像をテクスチャに転送する
    def transmit(self):
        # カメラのロックを試みる
        #if (mtx.try_lock()):
        # 新しいデータが到着していたら
        if (self.buffer is not None):
            # データをテクスチャに転送する
            glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.width, self.height, self.format, GL_UNSIGNED_BYTE, self.buffer)

            # データの転送完了を記録する
            self.buffer = None

            #    # 左カメラのロックを解除する
            #    mtx.unlock()
