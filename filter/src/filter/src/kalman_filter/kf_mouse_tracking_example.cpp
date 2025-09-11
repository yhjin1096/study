#include <iostream>
#include <opencv2/opencv.hpp>
#include "kalman_filter/kf_mouse_tracking.hpp"

// 전역 변수
KalmanFilter kalman_filter;
cv::Mat black_image;
std::vector<cv::Point2f> measurements;
std::vector<cv::Point2f> predictions;

// 마우스 콜백 함수
void mouseCallback(int event, int x, int y, int flags, void* userdata) {
    cv::Mat* img = static_cast<cv::Mat*>(userdata);
    cv::Mat display_img = img->clone();
    cv::circle(display_img, cv::Point(x, y), 5, cv::Scalar(0, 0, 255), -1);
    switch (event) {
        case cv::EVENT_MOUSEMOVE:
            std::cout << "마우스 이동: (" << x << ", " << y << ")" << std::endl;

            if (kalman_filter.isInitialized()) {
                cv::Point2f prediction = kalman_filter.predict();
                cv::circle(display_img, cv::Point(prediction.x, prediction.y), 8, cv::Scalar(255, 255, 0), 2); // 노란색 원

                // 측정값으로 업데이트
                cv::Point2f filtered = kalman_filter.update(cv::Point2f(x, y));
                cv::circle(display_img, cv::Point(filtered.x, filtered.y), 6, cv::Scalar(0, 255, 0), -1); // 초록색 원

                // 궤적 그리기
                measurements.push_back(cv::Point2f(x, y));
                predictions.push_back(filtered);

                // 최근 50개 점만 표시
                if (measurements.size() > 50) {
                    measurements.erase(measurements.begin());
                    predictions.erase(predictions.begin());
                }

                // 측정값 궤적 (빨간색)
                for (size_t i = 1; i < measurements.size(); i++) {
                    cv::line(display_img, measurements[i-1], measurements[i], cv::Scalar(0, 0, 255), 1);
                }

                // 필터링된 궤적 (초록색)
                for (size_t i = 1; i < predictions.size(); i++) {
                    cv::line(display_img, predictions[i-1], predictions[i], cv::Scalar(0, 255, 0), 2);
                }
            }
            break;

        case cv::EVENT_LBUTTONDOWN:
            std::cout << "왼쪽 클릭 - 칼만 필터 초기화: (" << x << ", " << y << ")" << std::endl;
            kalman_filter.initialize(cv::Point2f(x, y));

            measurements.clear();
            predictions.clear();
            measurements.push_back(cv::Point2f(x, y));
            predictions.push_back(cv::Point2f(x, y));

            cv::circle(display_img, cv::Point(x, y), 15, cv::Scalar(0, 255, 0), 3); // 초기화 표시
            break;
    }
    cv::imshow("Kalman Filter Mouse Tracking", display_img);
}

int main(int argc, char** argv) {
    black_image = cv::Mat::zeros(600, 800, CV_8UC3);
    cv::namedWindow("Kalman Filter Mouse Tracking", cv::WINDOW_AUTOSIZE);
    cv::setMouseCallback("Kalman Filter Mouse Tracking", mouseCallback, &black_image);
    cv::imshow("Kalman Filter Mouse Tracking", black_image);
    while (true) {
        int key = cv::waitKey(1) & 0xFF;
        if (key == 27) { // ESC 키
            break;
        }
    }
    cv::destroyAllWindows();
    return 0;
}
