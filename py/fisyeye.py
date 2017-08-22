import sys from math import *
import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glfw

# OpenCV によるビデオキャプチャ
##include "CamCv.h"
from CamCV import CamCV

## ウィンドウ関連の処理
##include "Window.h"
from Window import Window

## 平面展開の設定一覧
##include "ExpansionShader.h"
from ExpantionShader import ExpantionShader, shader_type

from gg import *
from glfw_wrapper import *

class Fisheye:
    #
    # 設定
    #

    # 背景画像の取得に使用するデバイス
    #CAPTURE_INPUT = 0               # 0 番のキャプチャデバイスから入力
    #CAPTURE_INPUT = "sp360.mp4"     # Kodak SP360 4K の Fish Eye 画像
    CAPTURE_INPUT  = "theta.mp4"     # THETA S の Equirectangular 画像

    def __init__(self):
        # 背景画像を展開する手法 (ExpansionShader.h 参照)
        #constexpr int shader_selection(6)    # Kodak SP360 4K
        #constexpr int shader_selection(7)    # THETA S の Dual Fisheye 画像
        shader_selection = 2    # THETA S の Equirectangular 画像

        # 背景画像の展開に使用するバーテックスシェーダのソースファイル名
        #const char *const capture_vsrc(shader_type[shader_selection].vsrc)
        self.capture_vsrc = shader_type[shader_selection].vsrc

        # 背景画像の展開に使用するフラグメントシェーダのソースファイル名
        #const char *const capture_fsrc(shader_type[shader_selection].fsrc)
        self.capture_fsrc = shader_type[shader_selection].fsrc

        # 背景画像の取得に使用するカメラの解像度 (0 ならカメラから取得)
        #const int capture_width(shader_type[shader_selection].width)
        #const int capture_height(shader_type[shader_selection].height)
        self.capture_width = shader_type[shader_selection].width
        self.capture_height = shader_type[shader_selection].height

        # 背景画像の取得に使用するカメラのフレームレート (0 ならカメラから取得)
        #constexpr int capture_fps(0)
        self.capture_fps = 0

        # 背景画像の関心領域
        #const float *const capture_circle(shader_type[shader_selection].circle)
        self.capture_circle  = shader_type[shader_selection].circle

        # 背景画像の描画に用いるメッシュの格子点数
        #screen_samples(1271)
        self.screen_samples = 1271

        # 背景色は表示されないが合成時に 0 にしておく必要がある
        #constexpr GLfloat background[] = { 0.0f, 0.0f, 0.0f, 0.0f }
        self.background = [ 0.0, 0.0, 0.0, 0.0 ]

        # @todo: added by zinziroge. check this code.
        glfw.init()

    def main(self):
        # カメラの使用を開始する
        camera = CamCV()
        if (not camera.open(self.CAPTURE_INPUT, self.capture_width, self.capture_height, self.capture_fps)):
            print("Can't open capture device.\n", file=sys.stderr)
            #return EXIT_FAILURE
            return False
        camera.start()

        # ウィンドウを作成する
        window = Window()

        # ウィンドウが開けたかどうか確かめる
        if (not window.get()):
            # ウィンドウが開けなかった
            print("Can't open GLFW window.\n", file=sys.stderr)
            return False

        # 背景描画用のシェーダプログラムを読み込む
        expansion = ggLoadShader(self.capture_vsrc, self.capture_fsrc)
        if (not expansion):
            # シェーダが読み込めなかった
            print("Can't create program object.\n", file=sys.stderr)
            return False

        # uniform 変数の場所を指定する
        gapLoc = glGetUniformLocation(expansion, "gap")
        screenLoc = glGetUniformLocation(expansion, "screen")
        focalLoc = glGetUniformLocation(expansion, "focal")
        rotationLoc = glGetUniformLocation(expansion, "rotation")
        circleLoc = glGetUniformLocation(expansion, "circle")
        imageLoc = glGetUniformLocation(expansion, "image")

        # 背景用のテクスチャを作成する
        #   ポリゴンでビューポート全体を埋めるので背景は表示されない。
        #   GL_CLAMP_TO_BORDER にしておけばテクスチャの外が GL_TEXTURE_BORDER_COLOR になるので、これが背景色になる。
        #const GLuint image([]() { GLuint image glGenTextures(1, &image) return image } ())
        image = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, image)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, camera.getWidth(), camera.getHeight(), 0, GL_BGR, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, self.background)

        # 背景描画のためのメッシュを作成する
        #   頂点座標値を vertex shader で生成するので VBO は必要ない
        #const GLuint mesh([]() { GLuint mesh glGenVertexArrays(1, &mesh) return mesh } ())
        #mesh = [glGenVertexArrays(1)]
        mesh = glGenVertexArrays(1)

        # 隠面消去を設定する
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        # ウィンドウが開いている間繰り返す
        while (not window.shouldClose()):
            # 背景画像の展開に用いるシェーダプログラムの使用を開始する
            glUseProgram(expansion)

            # スクリーンの矩形の格子点数
            #   標本点の数 (頂点数) n = x * y とするとき、これにアスペクト比 a = x / y をかければ、
            #   a * n = x * x となるから x = sqrt(a * n), y = n / x で求められる。
            #   この方法は頂点属性を持っていないので実行中に標本点の数やアスペクト比の変更が容易。
            #const GLsizei slices(static_cast<GLsizei>(sqrt(window.getAspect() * screen_samples)))
            #const GLsizei stacks(screen_samples / slices - 1) # 描画するインスタンスの数なので先に 1 を引いておく。
            slices = int(sqrt(window.getAspect() * self.screen_samples))
            stacks = int(self.screen_samples / slices - 1) # 描画するインスタンスの数なので先に 1 を引いておく。

            # スクリーンの格子間隔
            #   クリッピング空間全体を埋める四角形は [-1, 1] の範囲すなわち縦横 2 の大きさだから、
            #   それを縦横の (格子数 - 1) で割って格子の間隔を求める。
            glUniform2f(gapLoc, 2.0 / (slices - 1), 2.0 / stacks)

            # スクリーンのサイズと中心位置
            #   screen[0] = (right - left) / 2
            #   screen[1] = (top - bottom) / 2
            #   screen[2] = (right + left) / 2
            #   screen[3] = (top + bottom) / 2
            #const GLfloat screen[] = { window.getAspect(), 1.0, 0.0, 0.0 }
            screen = [ window.getAspect(), 1.0, 0.0, 0.0 ]
            glUniform4fv(screenLoc, 1, screen)

            # スクリーンまでの焦点距離
            #   window.getWheel() は [-100, 49] の範囲を返す。
            #   したがって焦点距離 focal は [1 / 3, 1] の範囲になる。
            #   これは焦点距離が長くなるにしたがって変化が大きくなる。
            glUniform1f(focalLoc, -50.0 / (window.getWheel() - 50.0))

            # 背景に対する視線の回転行列
            # @todo
            #glUniformMatrix4fv(rotationLoc, 1, GL_TRUE, window.getLeftTrackball().get())

            # テクスチャの半径と中心位置
            #   circle[0] = イメージサークルの x 方向の半径
            #   circle[1] = イメージサークルの y 方向の半径
            #   circle[2] = イメージサークルの中心の x 座標
            #   circle[3] = イメージサークルの中心の y 座標
            circle = [
                self.capture_circle[0] + window.getShiftWheel() * 0.001,
                self.capture_circle[1] + window.getShiftWheel() * 0.001,
                self.capture_circle[2] + (window.getShiftArrowX() - window.getControlArrowX()) * 0.001,
                self.capture_circle[3] + (window.getShiftArrowY() + window.getControlArrowY()) * 0.001
            ]
            glUniform4fv(circleLoc, 1, circle)

            # キャプチャした画像を背景用のテクスチャに転送する
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, image)
            camera.transmit()

            # テクスチャユニットを指定する
            glUniform1i(imageLoc, 0)

            # メッシュを描画する
            glBindVertexArray(mesh)
            glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, slices * 2, stacks)

            # カラーバッファを入れ替えてイベントを取り出す
            window.swapBuffers()


if __name__ == "__main__":
    fe = Fisheye()
    fe.main()
