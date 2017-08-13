#pragma once

//
// ���ʓW�J�Ɏg���V�F�[�_
//

// �V�F�[�_�̃Z�b�g�ƃp�����[�^
struct ExpansionShader
{
  // �o�[�e�b�N�X�V�F�[�_�̃\�[�X�v���O�����̃t�@�C����
  const char *vsrc;

  // �t���O�����g�V�F�[�_�̃\�[�X�v���O�����̃t�@�C����
  const char *fsrc;

  // �J�����̉𑜓x
  const int width, height;

  // �C���[�W�T�[�N���̔��a�ƒ��S�ʒu
  const float circle[4];
};

// �V�F�[�_�̎��
constexpr ExpansionShader shader_type[] =
{
  // 0: �ʏ�̃J����
  { "fixed.vert",     "normal.frag",    640,  480, 1.0f, 1.0f, 0.0f, 0.0f },

  // 1: �ʏ�̃J�����Ŏ��_����]
  { "rectangle.vert", "normal.frag",    640,  480, 1.0f, 1.0f, 0.0f, 0.0f },

  // 2: �����~���}�@�̉摜 (�c���������ɂ� GL_CLAMP_TO_BORDER �� GL_REPEAT �ɂ��Ă�������)
  { "panorama.vert",  "panorama.frag", 1280,  720, 1.0f, 1.0f, 0.0f, 0.0f },

  // 3: 180������J���� : 3.1415927 / 2 (�� 180��/ 2)
  { "fisheye.vert",   "normal.frag",   1280,  720, 1.570796327f, 1.570796327f, 0.0f, 0.0f },

  // 4: 180������J���� (FUJINON FE185C046HA-1 + SENTECH STC-MCE132U3V) : 3.5779249 / 2 (�� 205��/ 2)
  { "fisheye.vert",   "normal.frag",   1280, 1024, 1.797689129f, 1.797689129f, 0.0f, 0.0f },

  // 5: 206������J���� (Kodak PIXPRO SP360 4K, ��U��␳����) : 3.5953783 / 2 (�� 206��/ 2)
  { "fisheye.vert",   "normal.frag",   1440, 1440, 1.797689129f, 1.797689129f, 0.0f, 0.0f },

  // 6: 235������J���� (Kodak PIXPRO SP360 4K, ��U��␳�Ȃ�) : 4.1015237 / 2 (�� 235��/ 2)
  { "fisheye.vert",   "normal.frag",   1440, 1440, 2.050761871f, 2.050761871f, 0.0f, 0.0f },

  // 7: RICHO THETA �� USB ���C�u�X�g���[�~���O�f�� : (�蓮�����Ō��߂��l)
  { "theta.vert",     "theta.frag",    1280,  720, 1.003f, 1.003f, 0.0f, -0.002f },

  // 8: RICHO THETA �� HDMI ���C�u�X�g���[�~���O�f�� : (�蓮�����Ō��߂��l)
  { "theta.vert",     "theta.frag",    1920,  1080, 1.003f, 1.003f, 0.0f, -0.002f }
};
