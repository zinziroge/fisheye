import inspect
import os
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from glfw import *

from glfw_wrapper import *
from gg import *

# ウィンドウ関連の処理
#
#
class Window:
"""
  #if defined(USE_OCULUS_RIFT)
    #
    # Oculus Rift
    #

    # Oculus Rift のセッション
    ovrSession session

    # Oculus Rift の状態
    ovrHmdDesc hmdDesc

    # Oculus Rift のスクリーンのサイズ
    GLfloat screen[ovrEye_Count][4]

    # Oculus Rift 表示用の FBO
    GLuint oculusFbo[ovrEye_Count]

    # ミラー表示用の FBO
    GLuint mirrorFbo

    #if OVR_PRODUCT_VERSION > 0
      # Oculus Rift に送る描画データ
      ovrLayerEyeFov layerData

      # Oculus Rift にレンダリングするフレームの番号
      long long frameIndex

      # Oculus Rift 表示用の FBO のデプステクスチャ
      GLuint oculusDepth[ovrEye_Count]

      # ミラー表示用の FBO のサイズ
      int mirrorWidth, mirrorHeight

      # ミラー表示用の FBO のカラーテクスチャ
      ovrMirrorTexture mirrorTexture
    #else
      # Oculus Rift に送る描画データ
      ovrLayer_Union layerData

      # Oculus Rift のレンダリング情報
      ovrEyeRenderDesc eyeRenderDesc[ovrEye_Count]

      # Oculus Rift の視点情報
      ovrPosef eyePose[ovrEye_Count]

      # ミラー表示用の FBO のカラーテクスチャ
      ovrGLTexture *mirrorTexture
    #  endif
  #endif
"""

  #  # コピーコンストラクタを封じる
  #  Window(const Window &w)
  #
  #  # 代入を封じる
  #  Window &operator=(const Window &w)

  #
  # コンストラクタ
  #
  def __init__(self, title = "GLFW Window", width = 640, height = 480, fullscreen = 0, share = None):
    # ウィンドウの識別子
    #GLFWwindow *window
    self.window = None

    # ビューポートの幅と高さ
    self.width = 1920
    self.height = 960

    # ビューポートのアスペクト比
    self.aspect = 1.0

    # シフトキー
    self.shift_key = False

    # コントロールキー
    self.control_key = False

    # 矢印キー
    self.arrow = [0, 0]

    # シフトキーを押しながら矢印キー
    self.shift_arrow = [0, 0]

    # コントロールキーを押しながら矢印キー
    self.control_arrow = [0, 0]

    # マウスの現在位置
    self.mouse_x = 0
    self.mouse_y = 0

    # マウスホイールの回転量
    self.wheel_rotation = 0

    # シフトを押しながらマウスホイールの回転量
    self.shift_wheel_rotation = 0

    # コントロールを押しながらマウスホイールの回転量
    self.control_wheel_rotation = 0

    # 左ドラッグによるトラックボール
    self.trackball_left = GgTrackball()

    # 右ドラッグによるトラックボール
    self.trackball_right = GgTrackball()

    self.initialized = False

    # 初期化済なら true
    #static bool initialized(false)
    #self.initialized = False

    # GLFW が初期化されていなければ
    if (not self.initialized):
      # GLFW を初期化する
      if (glfwInit() == GL_FALSE):
        return

      # @todo:
      #  プログラム終了時の処理を登録
      #atexit(glfwTerminate)

      # @todo: implement oculus rift

      # OpenGL Version 3.2 Core Profile を選択する
      glfwWindowHint(CONTEXT_VERSION_MAJOR, 4)
      glfwWindowHint(CONTEXT_VERSION_MINOR, 1)
      glfwWindowHint(OPENGL_FORWARD_COMPAT, GL_TRUE)
      glfwWindowHint(OPENGL_PROFILE, OPENGL_CORE_PROFILE)

      # 矢印キーとマウス操作の初期値を設定する
      self.arrow = [0, 0]
      self.shift_arrow = [0, 0]
      self.control_arrow = [0, 0]
      self.wheel_rotation = 0.0
      self.shift_wheel_rotation = 0.0
      self.control_wheel_rotation = 0.0

      # 初期化済みの印をつける
      self.initialized = True

      # ディスプレイの情報
      #GLFWmonitor *monitor(nullptr)
      monitor = None

      # フルスクリーン表示
      if (fullscreen > 0):
        # 接続されているモニタの数を数える
        #int mcount
        #GLFWmonitor **const monitors = glfwGetMonitors(&mcount)
        mcount, monitors = glfwGetMonitors()

        # セカンダリモニタがあればそれを使う
        if (fullscreen > mcount):
          fullscreen = mcount
        monitor = monitors[fullscreen - 1]

        # モニタのモードを調べる
        #const GLFWvidmode *mode(glfwGetVideoMode(monitor))
        mode = glfwGetVideoMode(monitor)

        # ウィンドウのサイズをディスプレイのサイズにする
        width = mode.width
        height = mode.height

      # GLFW のウィンドウを作成する
      self.window = glfwCreateWindow(width, height, title, monitor, share)

      # ウィンドウが作成できなければ戻る
      if (not self.window):
        return

      # 現在のウィンドウを処理対象にする
      glfwMakeContextCurrent(self.window)

      # @todo:
      # ゲームグラフィックス特論の都合による初期化を行う
      #ggInit()

      # このインスタンスの this ポインタを記録しておく
      #glfwSetWindowUserPointer(self.window, this)
      glfwSetWindowUserPointer(self.window, self)

      # キーボードを操作した時の処理を登録する
      glfwSetKeyCallback(self.window, self.keyboard)

      # マウスボタンを操作したときの処理を登録する
      glfwSetMouseButtonCallback(self.window, self.mouse)

      # マウスホイール操作時に呼び出す処理を登録する
    glfwSetScrollCallback(self.window, self.wheel)

    # ウィンドウのサイズ変更時に呼び出す処理を登録する
    glfwSetFramebufferSizeCallback(self.window, self.resize)

    # @todo: implement oculus rift

    # スワップ間隔を待つ
    glfwSwapInterval(1)

    # ビューポートと投影変換行列を初期化する
    self.resize(self.window, width, height)

  #
  # デストラクタ
  #
  def destructor(self):
    # ウィンドウが作成されていなければ戻る
    if (not self.window):
      return

    # @todo: implement oculus rift

    # ウィンドウを破棄する
    glfwDestroyWindow(self.window)

    # @todo: implement oculus rift

    return True


  #
  # ウィンドウの識別子の取得
  #
  #GLFWwindow *get() const
  def get(self):
    return self.window

  #
  # ウィンドウを閉じるべきかを判定する
  #
  def shouldClose(self):
    # ウィンドウを閉じるか ESC キーがタイプされていれば真を返す
    return glfwWindowShouldClose(self.window) or glfwGetKey(self.window, KEY_ESCAPE)

  #
  # ビューポートをもとに戻す
  #
  def restoreViewport(self):
    glViewport(0, 0, self.width, self.height)

  # https://stackoverflow.com/questions/6810999/how-to-determine-file-function-and-line-number
  def getFrame(self):
    callerframerecord = inspect.stack()[1]  # 0 represents this line
    # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    #print
    #info.filename  # __FILE__     -> Test.py
    #print
    #info.function  # __FUNCTION__ -> Main
    #print
    #info.lineno  # __LINE__     -> 13
    return info

  #
  # カラーバッファを入れ替えてイベントを取り出す
  #
  def swapBuffers(self):
    # エラーチェック
    #ggError(__FILE__, __LINE__)
    info= self.getFrame()
    ggError(info.filename, info.lineno)

    # @todo: implement oculus rift

    # カラーバッファを入れ替える
    glfwSwapBuffers(self.window)

    # シフトキーとコントロールキーの状態をリセットする
    self.shift_key = False
    self.control_key = False

    # イベントを取り出す
    glfwPollEvents()

    # マウスの位置を調べる
    #glfwGetCursorPos(self.window, &mouse_x, &mouse_y)
    mouse_x, mouse_y = glfwGetCursorPos(self.window)
    x = mouse_x
    y = mouse_y

    # 左ボタンドラッグ
    if (glfwGetMouseButton(self.window, MOUSE_BUTTON_1)):
      self.trackball_left.motion(x, y)

    # 右ボタンドラッグ
    if (glfwGetMouseButton(self.window, MOUSE_BUTTON_2)):
      self.trackball_right.motion(x, y)

  #
  # ウィンドウのサイズ変更時の処理
  #
  #def resize(self, GLFWwindow *window, int width, int height):
  def resize(self, _window, _width, _height):
    # このインスタンスの this ポインタを得る
    instance = glfwGetWindowUserPointer(_window)

    if (instance):
      # ウィンドウのサイズを保存する
      instance.width = _width
      instance.height = _height

      # トラックボール処理の範囲を設定する
      instance.trackball_left.region(_width, _height)
      instance.trackball_right.region(_width, _height)

      #if !defined(USE_OCULUS_RIFT)
      # ウィンドウのアスペクト比を保存する
      instance.aspect = self.width / float(self.height)

      # ウィンドウ全体に描画する
      instance.restoreViewport()
      #endif

  #
  # キーボードをタイプした時の処理
  #
  #def keyboard(self, GLFWwindow *window, int key, int scancode, int action, int mods):
  def keyboard(self, window, key, scancode, action, mods):
    # このインスタンスの this ポインタを得る
    instance = glfwGetWindowUserPointer(window)

    if (instance):
      if (action == PRESS):
        if key == KEY_R:
          # マウスホイールの回転量をリセットする
          instance.wheel_rotation = 0.0
          instance.shift_wheel_rotation = 0.0
          instance.control_wheel_rotation = 0.0

          # 矢印キーの設定値をリセットする
          instance.arrow[0] = 0
          instance.arrow[1] = 0
          instance.shift_arrow[0] = 0
          instance.shift_arrow[1] = 0
          instance.control_arrow[0] = 0
          instance.control_arrow[1] = 0

        elif key == KEY_O:
          # トラックボールをリセットする
          instance.trackball_left.reset()
          instance.trackball_right.reset()
          return

        elif key == KEY_SPACE:
          return

        elif key in {KEY_BACKSPACE, KEY_DELETE}:
          return

        elif key in {KEY_LEFT_SHIFT, KEY_RIGHT_SHIFT}:
          instance.shift_key = True
          return

        elif key in {KEY_LEFT_CONTROL, KEY_RIGHT_CONTROL}:
          instance.control_key = True
          return

        elif key == KEY_UP:
          if (instance.shift_key):
            instance.shift_arrow[1] += 1
          elif (instance.control_key):
            instance.control_arrow[1] += 1
          else:
            instance.arrow[1] += 1
          return

        elif key == KEY_DOWN:
          if (instance.shift_key):
            instance.shift_arrow[1] -= 1
          elif (instance.control_key):
            instance.control_arrow[1] -= 1
          else:
            instance.arrow[1] -= 1
          return

        elif key == KEY_RIGHT:
          if (instance.shift_key):
            instance.shift_arrow[0] += 1
          elif (instance.control_key):
            instance.control_arrow[0] += 1
          else:
            instance.arrow[0] += 1
          return

        elif key == KEY_LEFT:
          if (instance.shift_key):
            instance.shift_arrow[0] -= 1
          elif (instance.control_key):
            instance.control_arrow[0] -= 1
          else:
            instance.arrow[0] -= 1
          return

        else:
          return

  #
  # マウスボタンを操作したときの処理
  #
  #def mouse(self, GLFWwindow *window, int button, int action, int mods):
  def mouse(self, window, button, action, mods):
    # このインスタンスの this ポインタを得る
    instance = glfwGetWindowUserPointer(window)

    if (instance):
      # マウスの現在位置を得る
      x = instance.mouse_x
      y = instance.mouse_y

      if button == MOUSE_BUTTON_1:
        if (action):
          # 左ドラッグ開始
          instance.trackball_left.start(x, y)
        else:
          # 左ドラッグ終了
          instance.trackball_left.stop(x, y)
        return

      elif button == MOUSE_BUTTON_2:
        if (action):
          # 右ドラッグ開始
          instance.trackball_right.start(x, y)
        else:
          # 右ドラッグ終了
          instance.trackball_right.stop(x, y)
        return

      elif button == MOUSE_BUTTON_3:
        return

      else:
        return

  #
  # マウスホイールを操作した時の処理
  #
  #def wheel(GLFWwindow *window, double x, double y):
  def wheel(self, window, x, y):
    # このインスタンスの this ポインタを得る
    instance = glfwGetWindowUserPointer(window)

    if (instance):
      if (instance.shift_key):
        instance.shift_wheel_rotation += y
      elif (instance.control_key):
        instance.control_wheel_rotation += y
      else:
        instance.wheel_rotation += y
        if (instance.wheel_rotation < -100.0):
          instance.wheel_rotation = -100.0
        elif (instance.wheel_rotation > 49.0):
          instance.wheel_rotation = 49.0

  #
  # ウィンドウの幅を得る
  #
  def getWidth(self):
    return self.width

  #
  # ウィンドウの高さを得る
  #
  def getHeight(self):
    return self.height

  #
  # ウィンドウのサイズを得る
  #
  def getSize(self, size):
    return [self.getWidth(), self.getHeight()]

  #
  # ウィンドウのアスペクト比を得る
  #
  def getAspect(self):
    return self.aspect

  #
  # 矢印キーの現在の X 値を得る
  #
  def getArrowX(self):
    return self.arrow[0]

  #
  # 矢印キーの現在の Y 値を得る
  #
  def getArrowY(self):
    return self.arrow[1]

  #
  # 矢印キーの現在の値を得る
  #
  #def getArrow(self, GLfloat *arrow):
  def getArrow(self):
    return [self.getArrowX() ,self.getArrowY()]

  #
  # シフトキーを押しながら矢印キーの現在の X 値を得る
  #
  def getShiftArrowX(self):
    return self.shift_arrow[0]

  #
  # シフトキーを押しながら矢印キーの現在の Y 値を得る
  #
  def getShiftArrowY(self):
    return self.shift_arrow[1]

  #
  # シフトキーを押しながら矢印キーの現在の値を得る
  #
  #def getShiftArrow(self, GLfloat *shift_arrow):
  def getShiftArrow(self):
    return [self.getShiftArrowX(), self.getShiftArrowY()]

  #
  # コントロールキーを押しながら矢印キーの現在の X 値を得る
  #
  def getControlArrowX(self):
    return self.control_arrow[0]

  #
  # コントロールキーを押しながら矢印キーの現在の Y 値を得る
  #
  def getControlArrowY(self):
    return self.control_arrow[1]

  #
  # コントロールキーを押しながら矢印キーの現在の値を得る
  #
  #def getControlArrow(self, GLfloat *control_arrow):
  def getControlArrow(self):
    return [self.getControlArrowX(), self.getControlArrowY()]

  #
  # マウスの X 座標を得る
  #
  def getMouseX(self):
    return self.mouse_x

  #
  # マウスの Y 座標を得る
  #
  def getMouseY(self):
    return self.mouse_y

    #
    # マウスの現在位置を得る
    #
  #  def getMouse(self, GLfloat *position):
  def getMouse(self):
    return [self.getMouseX(), self.getMouseY()]

  #
  # マウスホイールの現在の回転角を得る
  #
  def getWheel(self):
    return self.wheel_rotation

  #
  # シフトを押しながらマウスホイールの現在の回転角を得る
  #
  def getShiftWheel(self):
    return self.shift_wheel_rotation

  #
  # コントロールを押しながらマウスホイールの現在の回転角を得る
  #
  def getControlWheel(self):
    return self.control_wheel_rotation

  #
  # 左ボタンによるトラックボールの回転変換行列を得る
  #
  def getLeftTrackball(self):
    return self.trackball_left.getMatrix()

  #
  # 右ボタンによるトラックボールの回転変換行列を得る
  #
  def getRightTrackball(self):
    return self.trackball_right.getMatrix()
