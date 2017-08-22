import sys
from math import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

def ggCreateShader(vsrc=None, fsrc=None, gsrc=None, nvarying=0, varyings=0, vtext="", ftext="", gtext=""):
    # シェーダプログラムの作成
    program = glCreateProgram()

    if (program > 0):
        if (vsrc):
            # バーテックスシェーダのシェーダオブジェクトを作成する
            vertShader = glCreateShader(GL_VERTEX_SHADER)
            #glShaderSource(vertShader, 1, vsrc, None)
            glShaderSource(vertShader, vsrc)
            glCompileShader(vertShader)

            # バーテックスシェーダのシェーダオブジェクトをプログラムオブジェクトに組み込む
            if (printShaderInfoLog(vertShader, vtext)):
                glAttachShader(program, vertShader)
            glDeleteShader(vertShader)

        if (fsrc):
            # フラグメントシェーダのシェーダオブジェクトを作成する
            fragShader = glCreateShader(GL_FRAGMENT_SHADER)
            #glShaderSource(fragShader, 1, fsrc, None)
            glShaderSource(fragShader, fsrc)
            glCompileShader(fragShader)

            # フラグメントシェーダのシェーダオブジェクトをプログラムオブジェクトに組み込む
            if (printShaderInfoLog(fragShader, ftext)):
                glAttachShader(program, fragShader)
            glDeleteShader(fragShader)

        if (gsrc):
            # ジオメトリシェーダのシェーダオブジェクトを作成する
            geomShader = glCreateShader(GL_GEOMETRY_SHADER)
            #glShaderSource(geomShader, 1, gsrc, None)
            glShaderSource(geomShader, gsrc)
            glCompileShader(geomShader)

            # ジオメトリシェーダのシェーダオブジェクトをプログラムオブジェクトに組み込む
            if (printShaderInfoLog(geomShader, gtext)):
                glAttachShader(program, geomShader)
            glDeleteShader(geomShader)

    # feedback に使う varying 変数を指定する
    if (nvarying > 0):
        glTransformFeedbackVaryings(program, nvarying, varyings, GL_SEPARATE_ATTRIBS)

    # シェーダプログラムをリンクする
    glLinkProgram(program)

    # プログラムオブジェクトが作成できなければ 0 を返す
    if (printProgramInfoLog(program) == GL_FALSE):
        glDeleteProgram(program)
        return False

    # プログラムオブジェクトを返す
    return program

def readShaderSource(name):
    # ファイル名が nullptr ならそのまま戻る
    if (name == None):
        return True, ""

    # ソースファイルを開く
    try:
        with open(name, "rb") as f:
            src = f.readlines()
        #src =  map(lambda x : x, src)
        src =  [x + b"\0" for x in src]

    except:
        # ファイルが開けなければエラーで戻る
        print("Error: Can't open source file: " + name + "\n", file=sys.stderr)
        return False, ""

    return True, src

def ggLoadShader( vert=None, frag=None, geom=None, nvarying=0, varyings=[]):
    v_state, vsrc = readShaderSource(vert)
    f_state, fsrc = readShaderSource(frag)
    g_state, gsrc = readShaderSource(geom)
    # シェーダのソースファイルを読み込む
    if (v_state and f_state and g_state):
        # プログラムオブジェクトを作成する
        return ggCreateShader(vsrc, fsrc, gsrc, nvarying, varyings, vert, frag, geom)

    # プログラムオブジェクト作成失敗
    return False

def printShaderInfoLog(shader, str):
    # コンパイル結果を取得する
    status = None
    status = glGetShaderiv(shader, GL_COMPILE_STATUS, status)
    if (status == GL_FALSE):
        print("Compile Error in ", file=sys.stderr)

    # シェーダのコンパイル時のログの長さを取得する
    bufSize = 0
    glGetShaderiv(shader, GL_INFO_LOG_LENGTH, bufSize)

    if (bufSize > 1):
        # シェーダのコンパイル時のログの内容を取得する
        infoLog = glGetShaderInfoLog(shader)
        print(infoLog, file=sys.stderr)

    # コンパイル結果を返す
    return status


# OpenGL のエラーをチェックする
#
#   OpenGL の API を呼び出し直後に実行すればエラーのあるときにメッセージを表示する
#
#   msg エラー発生時に標準エラー出力に出力する文字列. nullptr なら何も出力しない
#
def ggError(name, line):
    error = glGetError()

    if (error != GL_NO_ERROR):
        if (name):
            print(name, file=sys.stderr)
            if (line > 0):
                print(" (" + line + ")\n", file=sys.stderr)
            print(": \n", file=sys.stderr)

        if (error == GL_INVALID_ENUM):
            print(": ", file=sys.stderr)
            print("An unacceptable value is specified for an enumerated argument\n", file=sys.stderr)
            return
        elif( error == GL_INVALID_VALUE):
            print("A numeric argument is out of range\n", file=sys.stderr)
            return
        elif( error == GL_INVALID_OPERATION):
            print("The specified operation is not allowed in the current state\n", file=sys.stderr)
            return
        elif( error == GL_OUT_OF_MEMORY):
            print("There is not enough memory left to execute the command\n", file=sys.stderr)
            return
        elif( error == GL_INVALID_FRAMEBUFFER_OPERATION):
            print("The specified operation is not allowed current frame buffer\n", file=sys.stderr)
            return
        else:
            print("An OpenGL error has occured: \n", file=sys.stderr)
            return


#! \brief (x, y, z) を軸として角度 a 回転する四元数を返す.
#!   \param x 軸ベクトルの x 成分.
#!   \param y 軸ベクトルの y 成分.
#!   \param z 軸ベクトルの z 成分.
#!   \param a 回転角.
#!   \return 回転を表す四元数.
def ggRotateQuaternion(x, y, z, a):
    q = GgQuaternion()
    return q.loadRotate(x, y, z, a)

class GgQuaternion:
    def __init__(self):
        # 四元数の要素
        # \brief 4 要素の単精度実数の配列
        #GgVector quaternion
        #self.quaternion = np.empty((1,4), dtype=np.float32)
        self.quaternion = np.zeros((4), dtype=np.float32)

    #def __mul__(self, other):
    #    r[0] = p[1] * q[2] - p[2] * q[1] + p[0] * q[3] + p[3] * q[0];
    #    r[1] = p[2] * q[0] - p[0] * q[2] + p[1] * q[3] + p[3] * q[1];
    #    r[2] = p[0] * q[1] - p[1] * q[0] + p[2] * q[3] + p[3] * q[2];
    #    r[3] = p[3] * q[3] - p[0] * q[0] - p[1] * q[1] - p[2] * q[2];

    #
    # 四元数：(x, y, z) を軸とし角度 a 回転する四元数を求める
    #
    def loadRotate(self, x, y, z, a):
        l = x * x + y * y + z * z

        if (l is not 0.0):
            #GLfloat s(sin(a *= 0.5f) / sqrt(l))
            if a * 0.5:
                s = sin(a * 0.5) / sqrt(l)
            else:
                s = sin(a * 0.5) / sqrt(l)

            self.quaternion[0] = x * s
            self.quaternion[1] = y * s
            self.quaternion[2] = z * s
        else:
            self.quaternion[0] = 0.0
            self.quaternion[1] = 0.0
            self.quaternion[2] = 0.0

        self.quaternion[3] = cos(a)

        #return *this
        return self

    def loadIdentity(self):
        #return load(0.0, 0.0, 0.0, 1.0)
        self.quaternion = [0.0, 0.0, 0.0, 1.0]
        return self.quaternion

    #! \brief 四元数が表す回転の変換行列を a に求める. #!   \param a 回転の変換行列を格納する GLfloat 型の 16 要素の配列.
    #def getMatrix(self. GLfloat *a) const
    #def getMatrix(self, a):
    def getMatrix(self):
        #return self.toMatrix(a, self.quaternion)
        return self.toMatrix(self.quaternion)

    # 四元数：GGQUATERNION 型の四元数 Q が表す変換行列を M に求める
    #def  toMatrix(self, m, q):
    def  toMatrix(self, q):
        xx = q[0] * q[0] * 2.0
        yy = q[1] * q[1] * 2.0
        zz = q[2] * q[2] * 2.0
        xy = q[0] * q[1] * 2.0
        yz = q[1] * q[2] * 2.0
        zx = q[2] * q[0] * 2.0
        xw = q[0] * q[3] * 2.0
        yw = q[1] * q[3] * 2.0
        zw = q[2] * q[3] * 2.0

        m = np.empty((16,1))
        m[ 0] = 1.0 - yy - zz
        m[ 1] = xy + zw
        m[ 2] = zx - yw
        m[ 4] = xy - zw
        m[ 5] = 1.0 - zz - xx
        m[ 6] = yz + xw
        m[ 8] = zx + yw
        m[ 9] = yz - xw
        m[10] = 1.0 - xx - yy
        m[ 3] = m[ 7] = m[11] = m[12] = m[13] = m[14] = 0.0
        m[15] = 1.0

        return m

class GgTrackball:
    def __init__(self):
        self.cx  = 0
        self.cy  = 0                        # ドラッグ開始位置
        self.drag = False                             # ドラッグ中か否か
        self.sx = 0
        self.sy = 0                         # マウスの絶対位置→ウィンドウ内での相対位置の換算係数
        self.cq = GgQuaternion()
        self.tq = GgQuaternion()
        self.cq.quaternion = [0,0,0,0]              # ドラッグ中の回転 (四元数)
        self.tq.quaternion = [0,0,0,0]
        self.rt = None                           # 回転の変換行列

        self.reset()

    #! \brief トラックボール処理するマウスの移動範囲を指定する.
    #!   \brief ウィンドウのリサイズ時に呼び出す.
    #!   \param w 領域の幅.
    #!   \param h 領域の高さ.
    def region(self, w, h):
        # マウスポインタ位置のウィンドウ内の相対的位置への換算用
        self.sx = 1.0 / w
        self.sy = 1.0 / h

    #! \brief トラックボール処理を開始する.
    #!   \brief マウスのドラッグ開始時 (マウスボタンを押したとき) に呼び出す.
    #!   \param x 現在のマウスの x 座標.
    #!   \param y 現在のマウスの y 座標.
    def start(self, x, y):
        # ドラッグ開始
        self.drag = True

        # ドラッグ開始点を記録する
        self.cx = x
        self.cy = y

    #! \brief 回転の変換行列を計算する.
    #!   \brief マウスのドラッグ中に呼び出す.
    #!   \param x 現在のマウスの x 座標.
    #!   \param y 現在のマウスの y 座標.
    def motion(self, x, y):
        if (self.drag):
            # マウスポインタの位置のドラッグ開始位置からの変位
            dx = ((x - self.cx) * self.sx)
            dy = ((y - self.cy) * self.sy)

            # マウスポインタの位置のドラッグ開始位置からの距離
            a = (sqrt(dx * dx + dy * dy))

            if (a is not 0.0):
                # 現在の回転の四元数に作った四元数を掛けて合成する
                self.tq = ggRotateQuaternion(dy, dx, 0.0, a * 6.283185) * self.cq

            # 合成した四元数から回転の変換行列を求める
            self.tq.getMatrix(self.rt)

    #! \brief トラックボールの回転角を修正する.
    #!   \param q 修正分の回転角の四元数.
    def rotate(self, q):
        if (not self.drag):
            # 保存されている四元数に修正分の四元数を掛けて合成する
            self.tq.quaternion = q * self.cq

            # 合成した四元数から回転の変換行列を求める
            self.tq.getMatrix(self.rt)

            # 誤差を吸収するために正規化して保存する
            self.cq = self.tq.normalize()

    #! \brief トラックボール処理を停止する.
    #!   \brief マウスのドラッグ終了時 (マウスボタンを離したとき) に呼び出す.
    #!   \param x 現在のマウスの x 座標.
    #!   \param y 現在のマウスの y 座標.
    def stop(self, x, y):
        # ドラッグ終了点における回転を求める
        self.motion(x, y)

        # 誤差を吸収するために正規化して保存する
        self.cq = self.tq.normalize()

        # ドラッグ終了
        self.drag = False

    #! \brief トラックボールをリセットする
    def reset(self):
        # ドラッグ中ではない
        self.drag = False

        # 単位クォーターニオンで初期化する
        self.tq.quaternion = self.cq.loadIdentity()

        # 回転行列を初期化する
        #print(type(self.cq))
        #print(type(self.tq))
        #self.tq.getMatrix()
        self.tq = self.tq.getMatrix()

    #! \brief 現在の回転の変換行列を取り出す.
    #!   \return 回転の変換を表す GLfloat 型の 16 要素の配列.
    def get(self):
        return self.rt

    #! \brief 現在の回転の変換行列を取り出す.
    #!   \return 回転の変換を表す GgMatrix 型の変換行列.
    def getMatrix(self):
        return self.rt

    #! \brief 現在の回転の四元数を取り出す.
    #!   \return 回転の変換を表す Quaternion 型の四元数.
    def getQuaternion(self):
        return self.tq

#
# プログラムオブジェクトのリンク結果を表示する
#
def printProgramInfoLog(program):
    # リンク結果を取得する
    status = glGetProgramiv(program, GL_LINK_STATUS)
    if (status == GL_FALSE):
        print("Link Error.\n", file=sys.stderr)

    # シェーダのリンク時のログの長さを取得する
    bufSize = glGetProgramiv(program, GL_INFO_LOG_LENGTH)

    # シェーダのリンク時のログの内容を取得する
    if (bufSize > 1):
        infoLog = glGetProgramInfoLog(program, bufSize)
        print(infoLog + "\n", file=sys.stderr)

    # リンク結果を返す
    return status
