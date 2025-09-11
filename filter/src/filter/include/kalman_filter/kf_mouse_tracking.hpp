#ifndef KALMAN_FILTER_HPP
#define KALMAN_FILTER_HPP

#include <opencv2/opencv.hpp>
#include <iostream>

class KalmanFilter {
private:
    cv::KalmanFilter kf_;
    cv::Mat measurement_;
    bool initialized_;
    cv::Point2f last_position_;
    
public:
    KalmanFilter();
    ~KalmanFilter();
    
    // 칼만 필터 초기화
    void initialize(const cv::Point2f& initial_position);
    
    // 새로운 측정값으로 예측 및 업데이트
    cv::Point2f update(const cv::Point2f& measurement);
    
    // 예측만 수행 (측정값 없이)
    cv::Point2f predict();
    
    // 초기화 상태 확인
    bool isInitialized() const { return initialized_; }
    
    // 마지막 위치 반환
    cv::Point2f getLastPosition() const { return last_position_; }
};

#endif // KALMAN_FILTER_HPP
