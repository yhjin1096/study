#include <iostream>
#include <opencv2/opencv.hpp>
#include "extended_kalman_filter/ekf_mouse_tracking.hpp"

EKFMouseTracking ekf_tracker;
cv::Mat black_image;
std::vector<cv::Point2f> measurements;
std::vector<cv::Point2f> predictions;
std::vector<cv::Point2f> ekf_predictions;

void mouseCallback(int event, int x, int y, int flags, void* userdata) {
    cv::Mat* img = static_cast<cv::Mat*>(userdata);
    cv::Mat display_img = img->clone();
    cv::circle(display_img, cv::Point(x, y), 5, cv::Scalar(0, 0, 255), -1);

    switch (event) {
        case cv::EVENT_MOUSEMOVE:
            std::cout << "마우스 이동: (" << x << ", " << y << ")" << std::endl;

            if (ekf_tracker.isInitialized()) {
                cv::Point2f ekf_prediction = ekf_tracker.predict();
                cv::Point2f ekf_filtered = ekf_tracker.update(cv::Point2f(x, y));

                cv::circle(display_img, cv::Point(ekf_prediction.x, ekf_prediction.y), 8, cv::Scalar(255, 255, 0), 2); // 노란색 원 (예측)
                cv::circle(display_img, cv::Point(ekf_filtered.x, ekf_filtered.y), 6, cv::Scalar(0, 255, 0), -1); // 초록색 원 (필터링)

                measurements.push_back(cv::Point2f(x, y));
                ekf_predictions.push_back(ekf_filtered);

                if (measurements.size() > 100) {
                    measurements.erase(measurements.begin());
                    ekf_predictions.erase(ekf_predictions.begin());
                }

                for (size_t i = 1; i < measurements.size(); i++) {
                    cv::line(display_img, measurements[i-1], measurements[i], cv::Scalar(0, 0, 255), 1);
                }

                for (size_t i = 1; i < ekf_predictions.size(); i++) {
                    cv::line(display_img, ekf_predictions[i-1], ekf_predictions[i], cv::Scalar(0, 255, 0), 2);
                }

                cv::Mat state = ekf_tracker.getState();
                std::cout << "EKF 상태: pos(" << state.at<float>(0) << ", " << state.at<float>(1) 
                         << ") vel(" << state.at<float>(2) << ", " << state.at<float>(3) 
                         << ") acc(" << state.at<float>(4) << ", " << state.at<float>(5) << ")" << std::endl;
            }
            break;

        case cv::EVENT_LBUTTONDOWN:
            std::cout << "왼쪽 클릭 - EKF 초기화: (" << x << ", " << y << ")" << std::endl;
            ekf_tracker.initialize(cv::Point2f(x, y));

            measurements.clear();
            ekf_predictions.clear();
            measurements.push_back(cv::Point2f(x, y));
            ekf_predictions.push_back(cv::Point2f(x, y));

            cv::circle(display_img, cv::Point(x, y), 15, cv::Scalar(0, 255, 0), 3); // 초기화 표시
            break;

        case cv::EVENT_RBUTTONDOWN:
            std::cout << "오른쪽 클릭 - EKF 리셋" << std::endl;
            measurements.clear();
            ekf_predictions.clear();
            cv::circle(display_img, cv::Point(x, y), 15, cv::Scalar(255, 0, 0), 3); // 리셋 표시
            break;

        case cv::EVENT_MBUTTONDOWN:
            if (ekf_tracker.isInitialized()) {
                cv::Mat state = ekf_tracker.getState();
                cv::Mat covariance = ekf_tracker.getCovariance();
                std::cout << "=== EKF 상태 정보 ===" << std::endl;
                std::cout << "위치: (" << state.at<float>(0) << ", " << state.at<float>(1) << ")" << std::endl;
                std::cout << "속도: (" << state.at<float>(2) << ", " << state.at<float>(3) << ")" << std::endl;
                std::cout << "가속도: (" << state.at<float>(4) << ", " << state.at<float>(5) << ")" << std::endl;
                std::cout << "위치 불확실성: (" << sqrt(covariance.at<float>(0,0)) << ", " << sqrt(covariance.at<float>(1,1)) << ")" << std::endl;
            }
            break;
    }

    cv::imshow("Extended Kalman Filter Mouse Tracking", display_img);
}

int main(int argc, char** argv) {
    black_image = cv::Mat::zeros(600, 800, CV_8UC3);
    cv::namedWindow("Extended Kalman Filter Mouse Tracking", cv::WINDOW_AUTOSIZE);
    cv::setMouseCallback("Extended Kalman Filter Mouse Tracking", mouseCallback, &black_image);
    cv::imshow("Extended Kalman Filter Mouse Tracking", black_image);

    while (true) {
        int key = cv::waitKey(1) & 0xFF;
        if (key == 27) { // ESC 키
            break;
        }
    }

    cv::destroyAllWindows();

    return 0;
}
