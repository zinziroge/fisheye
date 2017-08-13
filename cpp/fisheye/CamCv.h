#pragma once

//
// OpenCV ���g�����L���v�`��
//

// �J�����֘A�̏���
#include "Camera.h"

// OpenCV
#include <opencv2/highgui/highgui.hpp>

// OpenCV ���g���ăL���v�`������N���X
class CamCv
  : public Camera
{
  // OpenCV �̃L���v�`���f�o�C�X
  cv::VideoCapture camera;

  // OpenCV �̃L���v�`���f�o�C�X����擾�����t���[��
  cv::Mat frame;

  // ���݂̃t���[���̎���
  double frameTime;

  // �I�o�Ɨ���
  int exposure, gain;

  // �L���v�`���f�o�C�X������������
  bool init(int initial_width, int initial_height, int initial_fps)
  {
    // �J�����̉𑜓x��ݒ肷��
    if (initial_width > 0) camera.set(CV_CAP_PROP_FRAME_WIDTH, initial_width);
    if (initial_height > 0) camera.set(CV_CAP_PROP_FRAME_HEIGHT, initial_height);
    if (initial_fps > 0) camera.set(CV_CAP_PROP_FPS, initial_fps);

    // �J��������ŏ��̃t���[�����L���v�`������
    if (camera.grab())
    {
      // �ŏ��̃t���[�����擾������������ɂ���
      glfwSetTime(0.0);

      // �ŏ��̃t���[���̎����� 0 �ɂ���
      frameTime = 0.0;

      // �L���v�`�������t���[���̃T�C�Y���擾����
      width = static_cast<GLsizei>(camera.get(CV_CAP_PROP_FRAME_WIDTH));
      height = static_cast<GLsizei>(camera.get(CV_CAP_PROP_FRAME_HEIGHT));

      // macOS ���Ɛݒ�ł��Ă� 0 ���Ԃ��Ă���
      if (width == 0) width = initial_width;
      if (height == 0) height = initial_height;

      // �J�����̗����ƘI�o���擾����
      gain = static_cast<GLsizei>(camera.get(CV_CAP_PROP_GAIN));
      exposure = static_cast<GLsizei>(camera.get(CV_CAP_PROP_EXPOSURE) * 10.0);

      // �L���v�`�������t���[���̃t�H�[�}�b�g��ݒ肷��
      format = GL_BGR;

      // �t���[�������o���ăL���v�`���p�̃��������m�ۂ���
      camera.retrieve(frame, 3);

      // �t���[�����L���v�`�����ꂽ���Ƃ��L�^����
      buffer = frame.data;

      // �J�������g����
      return true;
    }

    // �J�������g���Ȃ�
    return false;
  }

  // �t���[�����L���v�`������
  virtual void capture()
  {
    // ���炩���߃L���v�`���f�o�C�X�����b�N����
    mtx.lock();

    // �X���b�h�����s�̊�
    while (run)
    {
      // �o�b�t�@����̂Ƃ��o�ߎ��Ԃ����݂̃t���[���̎����ɒB���Ă���
      if (!buffer && glfwGetTime() >= frameTime)
      {
        // ���̃t���[�������݂����
        if (camera.grab())
        {
          // �L���v�`�������t���[���̎������L�^����
          frameTime = camera.get(CV_CAP_PROP_POS_MSEC) * 0.001;

          // ���������t���[����؂�o����
          camera.retrieve(frame, 3);

          // �t���[�����X�V��
          buffer = frame.data;

          // ���̃t���[���ɐi��
          continue;
        }

        // �t���[�����擾�ł��Ȃ������烀�[�r�[�t�@�C���������߂�
        if (camera.set(CV_CAP_PROP_POS_FRAMES, 0.0))
        {
          // �o�ߎ��Ԃ����Z�b�g����
          glfwSetTime(0.0);

          // �t���[���̎��������Z�b�g��
          frameTime = 0.0;

          // ���̃t���[���ɐi��
          continue;
        }
      }

      // �t���[�����؂�o���Ȃ���΃��b�N����������
      mtx.unlock();

      // ���̃X���b�h�����\�[�X�ɃA�N�Z�X���邽�߂ɏ����҂��Ă���
      std::this_thread::sleep_for(std::chrono::milliseconds(10L));

      // �܂��L���v�`���f�o�C�X�����b�N����
      mtx.lock();
    }

    // �I���Ƃ��̓��b�N����������
    mtx.unlock();
  }

public:

  // �R���X�g���N�^
  CamCv() {}

  // �f�X�g���N�^
  virtual ~CamCv()
  {
    // �X���b�h���~����
    stop();
  }

  // �J����������͂���
  bool open(int device, int width = 0, int height = 0, int fps = 0)
  {
    // �J�������J��
    camera.open(device);

    // �J�������g����΃J����������������
    if (camera.isOpened() && init(width, height, fps)) return true;

    // �J�������g���Ȃ�
    return false;
  }

  // �t�@�C���^�l�b�g���[�N������͂���
  bool open(const std::string &file, int width = 0, int height = 0, int fps = 0)
  {
    // �t�@�C���^�l�b�g���[�N���J��
    camera.open(file);

    // �t�@�C���^�l�b�g���[�N���g����Ώ���������
    if (camera.isOpened() && init(width, height, fps)) return true;

    // �t�@�C���^�l�b�g���[�N���g���Ȃ�
    return false;
  }

  // �I�o���グ��
  virtual void increaseExposure()
  {
    if (camera.isOpened()) camera.set(CV_CAP_PROP_EXPOSURE, ++exposure * 0.1);
  }

  // �I�o��������
  virtual void decreaseExposure()
  {
    if (camera.isOpened()) camera.set(CV_CAP_PROP_EXPOSURE, --exposure * 0.1);
  }

  // �������グ��
  virtual void increaseGain()
  {
    if (camera.isOpened()) camera.set(CV_CAP_PROP_GAIN, ++gain);
  }

  // ������������
  virtual void decreaseGain()
  {
    if (camera.isOpened()) camera.set(CV_CAP_PROP_GAIN, --gain);
  }
};
