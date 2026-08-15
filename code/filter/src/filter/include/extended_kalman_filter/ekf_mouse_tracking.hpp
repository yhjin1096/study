#ifndef EKF_MOUSE_TRACKING_HPP
#define EKF_MOUSE_TRACKING_HPP

#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>

class EKFMouseTracking {
private:
    // EKF 상태 벡터: [x, y, vx, vy, ax, ay] (위치, 속도, 가속도)
    cv::Mat state_;           // 6x1 상태 벡터
    cv::Mat covariance_;      // 6x6 공분산 행렬
    cv::Mat process_noise_;   // 6x6 프로세스 노이즈
    cv::Mat measurement_noise_; // 2x2 측정 노이즈
    
    bool initialized_;
    double dt_;               // 시간 간격
    cv::Point2f last_position_;
    
    // 비선형 함수들
    cv::Mat stateTransition(const cv::Mat& state, double dt);
    cv::Mat measurementFunction(const cv::Mat& state);
    cv::Mat computeJacobianF(const cv::Mat& state, double dt);
    cv::Mat computeJacobianH(const cv::Mat& state);
    
public:
    EKFMouseTracking();
    ~EKFMouseTracking();
    
    // EKF 초기화
    void initialize(const cv::Point2f& initial_position);
    
    // EKF 예측 단계
    cv::Point2f predict();
    
    // EKF 업데이트 단계
    cv::Point2f update(const cv::Point2f& measurement);
    
    // 초기화 상태 확인
    bool isInitialized() const { return initialized_; }
    
    // 마지막 위치 반환
    cv::Point2f getLastPosition() const { return last_position_; }
    
    // 상태 벡터 반환 (디버깅용)
    cv::Mat getState() const { return state_.clone(); }
    
    // 공분산 행렬 반환 (디버깅용)
    cv::Mat getCovariance() const { return covariance_.clone(); }
};

#endif // EKF_MOUSE_TRACKING_HPP
