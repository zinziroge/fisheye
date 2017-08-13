// �E�B���h�E�֘A�̏���
#include "Window.h"

// ���ʓW�J�̐ݒ�ꗗ
#include "ExpansionShader.h"

// OpenCV �ɂ��r�f�I�L���v�`��
#include "CamCv.h"

//
// �ݒ�
//

// �w�i�摜�̎擾�Ɏg�p����f�o�C�X
//#define CAPTURE_INPUT 0               // 0 �Ԃ̃L���v�`���f�o�C�X�������
//#define CAPTURE_INPUT "sp360.mp4"     // Kodak SP360 4K �� Fish Eye �摜
#define CAPTURE_INPUT "theta.mp4"     // THETA S �� Equirectangular �摜

// �w�i�摜��W�J�����@ (ExpansionShader.h �Q��)
//constexpr int shader_selection(6);    // Kodak SP360 4K
//constexpr int shader_selection(7);    // THETA S �� Dual Fisheye �摜
constexpr int shader_selection(2);    // THETA S �� Equirectangular �摜

// �w�i�摜�̓W�J�Ɏg�p����o�[�e�b�N�X�V�F�[�_�̃\�[�X�t�@�C����
const char *const capture_vsrc(shader_type[shader_selection].vsrc);

// �w�i�摜�̓W�J�Ɏg�p����t���O�����g�V�F�[�_�̃\�[�X�t�@�C����
const char *const capture_fsrc(shader_type[shader_selection].fsrc);

// �w�i�摜�̎擾�Ɏg�p����J�����̉𑜓x (0 �Ȃ�J��������擾)
const int capture_width(shader_type[shader_selection].width);
const int capture_height(shader_type[shader_selection].height);

// �w�i�摜�̎擾�Ɏg�p����J�����̃t���[�����[�g (0 �Ȃ�J��������擾)
constexpr int capture_fps(0);

// �w�i�摜�̊֐S�̈�
const float *const capture_circle(shader_type[shader_selection].circle);

// �w�i�摜�̕`��ɗp���郁�b�V���̊i�q�_��
constexpr int screen_samples(1271);

// �w�i�F�͕\������Ȃ����������� 0 �ɂ��Ă����K�v������
constexpr GLfloat background[] = { 0.0f, 0.0f, 0.0f, 0.0f };

//
// ���C��
//

int main()
{
  // �J�����̎g�p���J�n����
  CamCv camera;
  if (!camera.open(CAPTURE_INPUT, capture_width, capture_height, capture_fps))
  {
    std::cerr << "Can't open capture device.\n";
    return EXIT_FAILURE;
  }
  camera.start();

  // �E�B���h�E���쐬����
  Window window;

  // �E�B���h�E���J�������ǂ����m���߂�
  if (!window.get())
  {
    // �E�B���h�E���J���Ȃ�����
    std::cerr << "Can't open GLFW window.\n";
    return EXIT_FAILURE;
  }

  // �w�i�`��p�̃V�F�[�_�v���O������ǂݍ���
  const GLuint expansion(ggLoadShader(capture_vsrc, capture_fsrc));
  if (!expansion)
  {
    // �V�F�[�_���ǂݍ��߂Ȃ�����
    std::cerr << "Can't create program object.\n";
    return EXIT_FAILURE;
  }

  // uniform �ϐ��̏ꏊ���w�肷��
  const GLuint gapLoc(glGetUniformLocation(expansion, "gap"));
  const GLuint screenLoc(glGetUniformLocation(expansion, "screen"));
  const GLuint focalLoc(glGetUniformLocation(expansion, "focal"));
  const GLuint rotationLoc(glGetUniformLocation(expansion, "rotation"));
  const GLuint circleLoc(glGetUniformLocation(expansion, "circle"));
  const GLuint imageLoc(glGetUniformLocation(expansion, "image"));

  // �w�i�p�̃e�N�X�`�����쐬����
  //   �|���S���Ńr���[�|�[�g�S�̂𖄂߂�̂Ŕw�i�͕\������Ȃ��B
  //   GL_CLAMP_TO_BORDER �ɂ��Ă����΃e�N�X�`���̊O�� GL_TEXTURE_BORDER_COLOR �ɂȂ�̂ŁA���ꂪ�w�i�F�ɂȂ�B
  const GLuint image([]() { GLuint image; glGenTextures(1, &image); return image; } ());
  glBindTexture(GL_TEXTURE_2D, image);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, camera.getWidth(), camera.getHeight(), 0, GL_BGR, GL_UNSIGNED_BYTE, NULL);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
  glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, background);

  // �w�i�`��̂��߂̃��b�V�����쐬����
  //   ���_���W�l�� vertex shader �Ő�������̂� VBO �͕K�v�Ȃ�
  const GLuint mesh([]() { GLuint mesh; glGenVertexArrays(1, &mesh); return mesh; } ());

  // �B�ʏ�����ݒ肷��
  glDisable(GL_DEPTH_TEST);
  glDisable(GL_CULL_FACE);

  // �E�B���h�E���J���Ă���ԌJ��Ԃ�
  while (!window.shouldClose())
  {
    // �w�i�摜�̓W�J�ɗp����V�F�[�_�v���O�����̎g�p���J�n����
    glUseProgram(expansion);

    // �X�N���[���̋�`�̊i�q�_��
    //   �W�{�_�̐� (���_��) n = x * y �Ƃ���Ƃ��A����ɃA�X�y�N�g�� a = x / y ��������΁A
    //   a * n = x * x �ƂȂ邩�� x = sqrt(a * n), y = n / x; �ŋ��߂���B
    //   ���̕��@�͒��_�����������Ă��Ȃ��̂Ŏ��s���ɕW�{�_�̐���A�X�y�N�g��̕ύX���e�ՁB
    const GLsizei slices(static_cast<GLsizei>(sqrt(window.getAspect() * screen_samples)));
    const GLsizei stacks(screen_samples / slices - 1); // �`�悷��C���X�^���X�̐��Ȃ̂Ő�� 1 �������Ă����B

    // �X�N���[���̊i�q�Ԋu
    //   �N���b�s���O��ԑS�̂𖄂߂�l�p�`�� [-1, 1] �͈̔͂��Ȃ킿�c�� 2 �̑傫��������A
    //   ������c���� (�i�q�� - 1) �Ŋ����Ċi�q�̊Ԋu�����߂�B
    glUniform2f(gapLoc, 2.0f / (slices - 1), 2.0f / stacks);

    // �X�N���[���̃T�C�Y�ƒ��S�ʒu
    //   screen[0] = (right - left) / 2
    //   screen[1] = (top - bottom) / 2
    //   screen[2] = (right + left) / 2
    //   screen[3] = (top + bottom) / 2
    const GLfloat screen[] = { window.getAspect(), 1.0f, 0.0f, 0.0f };
    glUniform4fv(screenLoc, 1, screen);

    // �X�N���[���܂ł̏œ_����
    //   window.getWheel() �� [-100, 49] �͈̔͂�Ԃ��B
    //   ���������ďœ_���� focal �� [1 / 3, 1] �͈̔͂ɂȂ�B
    //   ����͏œ_�����������Ȃ�ɂ��������ĕω����傫���Ȃ�B
    glUniform1f(focalLoc, -50.0f / (window.getWheel() - 50.0f));

    // �w�i�ɑ΂��鎋���̉�]�s��
    glUniformMatrix4fv(rotationLoc, 1, GL_TRUE, window.getLeftTrackball().get());

    // �e�N�X�`���̔��a�ƒ��S�ʒu
    //   circle[0] = �C���[�W�T�[�N���� x �����̔��a
    //   circle[1] = �C���[�W�T�[�N���� y �����̔��a
    //   circle[2] = �C���[�W�T�[�N���̒��S�� x ���W
    //   circle[3] = �C���[�W�T�[�N���̒��S�� y ���W
    const GLfloat circle[] =
    {
      capture_circle[0] + window.getShiftWheel() * 0.001f,
      capture_circle[1] + window.getShiftWheel() * 0.001f,
      capture_circle[2] + (window.getShiftArrowX() - window.getControlArrowX()) * 0.001f,
      capture_circle[3] + (window.getShiftArrowY() + window.getControlArrowY()) * 0.001f
    };
    glUniform4fv(circleLoc, 1, circle);

    // �L���v�`�������摜��w�i�p�̃e�N�X�`���ɓ]������
    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, image);
    camera.transmit();

    // �e�N�X�`�����j�b�g���w�肷��
    glUniform1i(imageLoc, 0);

    // ���b�V����`�悷��
    glBindVertexArray(mesh);
    glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, slices * 2, stacks);

    // �J���[�o�b�t�@�����ւ��ăC�x���g�����o��
    window.swapBuffers();
  }
}
