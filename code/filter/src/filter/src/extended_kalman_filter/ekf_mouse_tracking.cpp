#include "extended_kalman_filter/ekf_mouse_tracking.hpp"

EKFMouseTracking::EKFMouseTracking() : initialized_(false), dt_(0.0166) { // 약 60 FPS
    // 상태 벡터 초기화 [x, y, vx, vy, ax, ay]
    state_ = cv::Mat::zeros(6, 1, CV_32F);

    // 공분산 행렬 초기화 (6x6)
    covariance_ = cv::Mat::eye(6, 6, CV_32F) * 10.0f;

    // 프로세스 노이즈 (6x6)
    process_noise_ = cv::Mat::eye(6, 6, CV_32F);
    process_noise_.at<float>(0, 0) = 0.1f; // 위치 x 노이즈
    process_noise_.at<float>(1, 1) = 0.1f; // 위치 y 노이즈
    process_noise_.at<float>(2, 2) = 0.5f; // 속도 x 노이즈
    process_noise_.at<float>(3, 3) = 0.5f; // 속도 y 노이즈
    process_noise_.at<float>(4, 4) = 1.0f; // 가속도 x 노이즈
    process_noise_.at<float>(5, 5) = 1.0f; // 가속도 y 노이즈

    // 측정 노이즈 (2x2)
    measurement_noise_ = cv::Mat::eye(2, 2, CV_32F) * 2.0f;
}

EKFMouseTracking::~EKFMouseTracking() {
}

void EKFMouseTracking::initialize(const cv::Point2f& initial_position) {
    // 초기 상태 설정
    state_.at<float>(0) = initial_position.x; // x
    state_.at<float>(1) = initial_position.y; // y
    state_.at<float>(2) = 0.0f; // vx
    state_.at<float>(3) = 0.0f; // vy
    state_.at<float>(4) = 0.0f; // ax
    state_.at<float>(5) = 0.0f; // ay

    // 초기 공분산 설정
    covariance_ = cv::Mat::eye(6, 6, CV_32F) * 1.0f;

    last_position_ = initial_position;
    initialized_ = true;

    std::cout << "EKF 초기화 완료: (" << initial_position.x << ", " << initial_position.y << ")" << std::endl;
}

cv::Mat EKFMouseTracking::stateTransition(const cv::Mat& state, double dt) {
    cv::Mat new_state = state.clone();

    float x = state.at<float>(0);
    float y = state.at<float>(1);
    float vx = state.at<float>(2);
    float vy = state.at<float>(3);
    float ax = state.at<float>(4);
    float ay = state.at<float>(5);

    // 비선형 상태 전이 (등가속도 운동)
    new_state.at<float>(0) = x + vx * dt + 0.5f * ax * dt * dt; // x = x + vx*dt + 0.5*ax*dt^2
    new_state.at<float>(1) = y + vy * dt + 0.5f * ay * dt * dt; // y = y + vy*dt + 0.5*ay*dt^2
    new_state.at<float>(2) = vx + ax * dt; // vx = vx + ax*dt
    new_state.at<float>(3) = vy + ay * dt; // vy = vy + ay*dt
    new_state.at<float>(4) = ax; // ax = ax (가속도는 일정)
    new_state.at<float>(5) = ay; // ay = ay

    return new_state;
}

cv::Mat EKFMouseTracking::measurementFunction(const cv::Mat& state) {
    cv::Mat measurement = cv::Mat::zeros(2, 1, CV_32F);
    
    float x = state.at<float>(0);
    float y = state.at<float>(1);
    
    // 기본 측정값
    measurement.at<float>(0) = x;
    measurement.at<float>(1) = y;
    
    // 실제로는 여기에 측정 노이즈가 추가됨
    // measurement += noise;
    
    return measurement;
}

cv::Mat EKFMouseTracking::computeJacobianF(const cv::Mat& state, double dt) {
    cv::Mat jacobian = cv::Mat::eye(6, 6, CV_32F);

    // 상태 전이 함수의 야코비안 계산
    jacobian.at<float>(0, 2) = dt; // dx/dvx = dt
    jacobian.at<float>(0, 4) = 0.5f * dt * dt; // dx/dax = 0.5*dt^2
    jacobian.at<float>(1, 3) = dt; // dy/dvy = dt
    jacobian.at<float>(1, 5) = 0.5f * dt * dt; // dy/day = 0.5*dt^2
    jacobian.at<float>(2, 4) = dt; // dvx/dax = dt
    jacobian.at<float>(3, 5) = dt; // dvy/day = dt

    return jacobian;
}

cv::Mat EKFMouseTracking::computeJacobianH(const cv::Mat& state) {
    cv::Mat jacobian = cv::Mat::zeros(2, 6, CV_32F);

    // 측정 함수의 야코비안 계산 (위치만 측정)
    jacobian.at<float>(0, 0) = 1.0f; // dx/dx = 1
    jacobian.at<float>(1, 1) = 1.0f; // dy/dy = 1

    return jacobian;
}

cv::Point2f EKFMouseTracking::predict() {
    if (!initialized_) {
        std::cerr << "EKF가 초기화되지 않았습니다!" << std::endl;
        return cv::Point2f(0, 0);
    }

    // 1. 상태 예측 (비선형 함수 사용)
    cv::Mat predicted_state = stateTransition(state_, dt_);

    // 2. 야코비안 계산
    cv::Mat jacobian_F = computeJacobianF(state_, dt_);

    // 3. 공분산 예측
    cv::Mat predicted_covariance = jacobian_F * covariance_ * jacobian_F.t() + process_noise_;

    // 4. 상태와 공분산 업데이트
    state_ = predicted_state;
    covariance_ = predicted_covariance;

    return cv::Point2f(state_.at<float>(0), state_.at<float>(1));
}

cv::Point2f EKFMouseTracking::update(const cv::Point2f& measurement) {
    if (!initialized_) {
        std::cerr << "EKF가 초기화되지 않았습니다!" << std::endl;
        return cv::Point2f(0, 0);
    }

    // 1. 측정값 벡터 생성
    cv::Mat measurement_vec = cv::Mat::zeros(2, 1, CV_32F);
    measurement_vec.at<float>(0) = measurement.x;
    measurement_vec.at<float>(1) = measurement.y;

    // 2. 예측된 측정값 계산
    cv::Mat predicted_measurement = measurementFunction(state_);

    // 3. 야코비안 계산
    cv::Mat jacobian_H = computeJacobianH(state_);

    // 4. 칼만 게인 계산
    cv::Mat S = jacobian_H * covariance_ * jacobian_H.t() + measurement_noise_;
    cv::Mat K = covariance_ * jacobian_H.t() * S.inv();

    // 5. 상태 업데이트
    cv::Mat innovation = measurement_vec - predicted_measurement;
    state_ = state_ + K * innovation;

    // 6. 공분산 업데이트
    cv::Mat I = cv::Mat::eye(6, 6, CV_32F);
    covariance_ = (I - K * jacobian_H) * covariance_;

    last_position_ = cv::Point2f(state_.at<float>(0), state_.at<float>(1));

    return last_position_;
}
