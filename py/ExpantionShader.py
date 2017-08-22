class ExpantionShader:
    def __init__(self, vsrc, fsrc, width, height, circle):
        # バーテックスシェーダのソースプログラムのファイル名
        self.vsrc  = vsrc
        
        # フラグメントシェーダのソースプログラムのファイル名
        self.fsrc = fsrc
        
        # カメラの解像度
        self.width = width
        self.height = height
        
        # イメージサークルの半径と中心位置
        self.circle = circle

shader_type = [
    # 0: 通常のカメラ
    ExpantionShader( "fixed.vert",     "normal.frag",    640,  480, [1.0, 1.0, 0.0, 0.0] ),

    # 1: 通常のカメラで視点を回転
    ExpantionShader( "rectangle.vert", "normal.frag",    640,  480, [1.0, 1.0, 0.0, 0.0] ),

    # 2: 正距円筒図法の画像 (縦線を消すには GL_CLAMP_TO_BORDER を GL_REPEAT にしてください)
    ExpantionShader( "panorama.vert",  "panorama.frag", 1280,  720, [1.0, 1.0, 0.0, 0.0] ),
    
    # 3: 180°魚眼カメラ : 3.1415927 / 2 (≒ 180°/ 2)
    ExpantionShader( "fisheye.vert",   "normal.frag",   1280,  720, [1.570796327, 1.570796327, 0.0, 0.0]),
    
    # 4: 180°魚眼カメラ (FUJINON FE185C046HA-1 + SENTECH STC-MCE132U3V) : 3.5779249 / 2 (≒ 205°/ 2)
    ExpantionShader( "fisheye.vert",   "normal.frag",   1280, 1024, [1.797689129, 1.797689129, 0.0, 0.0]),
    
    # 5: 206°魚眼カメラ (Kodak PIXPRO SP360 4K, 手振れ補正あり) : 3.5953783 / 2 (≒ 206°/ 2)
    ExpantionShader( "fisheye.vert",   "normal.frag",   1440, 1440, [1.797689129, 1.797689129, 0.0, 0.0 ]),
    
    # 6: 235°魚眼カメラ (Kodak PIXPRO SP360 4K, 手振れ補正なし) : 4.1015237 / 2 (≒ 235°/ 2)
    ExpantionShader( "fisheye.vert",   "normal.frag",   1440, 1440, [2.050761871, 2.050761871, 0.0, 0.0 ]),
    
    # 7: RICHO THETA の USB ライブストリーミング映像 : (手動調整で決めた値)
    ExpantionShader( "theta.vert",     "theta.frag",    1280,  720, [1.003, 1.003, 0.0, -0.002 ]),
    
    # 8: RICHO THETA の HDMI ライブストリーミング映像 : (手動調整で決めた値)
    ExpantionShader( "theta.vert",     "theta.frag",    1920,  1080, [1.003, 1.003, 0.0, -0.002 ])
    ]
