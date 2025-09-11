#include "kalman_filter/kf_mouse_tracking.hpp"

KalmanFilter::KalmanFilter() : initialized_(false) {
    // 상태 벡터: [x, y, vx, vy] (위치와 속도)
    kf_.init(4, 2, 0);

    // 전이 행렬 (상태 전이 모델)
    kf_.transitionMatrix = (cv::Mat_<float>(4, 4) << 
        1, 0, 1, 0,  // x = x + vx
        0, 1, 0, 1,  // y = y + vy
        0, 0, 1, 0,  // vx = vx
        0, 0, 0, 1); // vy = vy

    // 측정 행렬 (측정 모델)
    kf_.measurementMatrix = (cv::Mat_<float>(2, 4) << 
        1, 0, 0, 0,  // 측정값은 위치만
        0, 1, 0, 0);

    // 프로세스 노이즈 공분산
    kf_.processNoiseCov = (cv::Mat_<float>(4, 4) << 
        0.1, 0, 0, 0,
        0, 0.1, 0, 0,
        0, 0, 0.1, 0,
        0, 0, 0, 0.1);

    // 측정 노이즈 공분산
    kf_.measurementNoiseCov = (cv::Mat_<float>(2, 2) << 
        1, 0,
        0, 1);

    // 오차 공분산
    kf_.errorCovPost = (cv::Mat_<float>(4, 4) << 
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1);

    measurement_ = cv::Mat::zeros(2, 1, CV_32F);
}

KalmanFilter::~KalmanFilter() {
}

void KalmanFilter::initialize(const cv::Point2f& initial_position) {
    // 초기 상태 설정
    kf_.statePre.at<float>(0) = initial_position.x;
    kf_.statePre.at<float>(1) = initial_position.y;
    kf_.statePre.at<float>(2) = 0; // 초기 속도 x
    kf_.statePre.at<float>(3) = 0; // 초기 속도 y

    // 초기 측정값 설정
    measurement_.at<float>(0) = initial_position.x;
    measurement_.at<float>(1) = initial_position.y;

    // 칼만 필터 초기화
    kf_.correct(measurement_);

    last_position_ = initial_position;
    initialized_ = true;

    std::cout << "칼만 필터 초기화 완료: (" << initial_position.x << ", " << initial_position.y << ")" << std::endl;
}

cv::Point2f KalmanFilter::update(const cv::Point2f& measurement) {
    if (!initialized_) {
        std::cerr << "칼만 필터가 초기화되지 않았습니다!" << std::endl;
        return cv::Point2f(0, 0);
    }

    // 예측 단계
    cv::Mat prediction = kf_.predict();

    // 측정값 설정
    measurement_.at<float>(0) = measurement.x;
    measurement_.at<float>(1) = measurement.y;

    // 업데이트 단계
    cv::Mat corrected = kf_.correct(measurement_);

    // 결과 저장
    last_position_ = cv::Point2f(corrected.at<float>(0), corrected.at<float>(1));

    return last_position_;
}

cv::Point2f KalmanFilter::predict() {
    if (!initialized_) {
        std::cerr << "칼만 필터가 초기화되지 않았습니다!" << std::endl;
        return cv::Point2f(0, 0);
    }

    // 예측만 수행
    cv::Mat prediction = kf_.predict();

    return cv::Point2f(prediction.at<float>(0), prediction.at<float>(1));
}
