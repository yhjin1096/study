#ifndef FRAME_HPP
#define FRAME_HPP

#include <local_ba_g2o_with_wheel/local_ba_g2o/type.h>
#include <opencv2/opencv.hpp>
#include <unordered_map>
class Frame
{
    public:
        Frame(const Vec3_t& xy, unsigned int id, int num_landmarks)
        {
            // yaw를 -90도로 설정하고 z를 1.6m로 고정
            pose_w2c_ = Mat44_t::Identity();
            pose_w2c_.block<3,3>(0,0) = Eigen::AngleAxisd(-M_PI/2.0, Eigen::Vector3d::UnitZ()).toRotationMatrix();
            pose_w2c_(0,3) = xy(0);
            pose_w2c_(1,3) = xy(1);
            pose_w2c_(2,3) = xy(2);

            // 노이즈가 추가된 pose 생성
            pose_w2c_noise_ = pose_w2c_;
            double noise_angle = Random::UniformRand(-3.0 * M_PI/180.0, 3.0 * M_PI/180.0);
            pose_w2c_noise_.block<3,3>(0,0) = pose_w2c_.block<3,3>(0,0) * Eigen::AngleAxisd(noise_angle, Eigen::Vector3d::UnitZ()).toRotationMatrix();
            pose_w2c_noise_(0,3) += Random::UniformRand(-0.5, 0.5);
            pose_w2c_noise_(1,3) += Random::UniformRand(-0.5, 0.5);
            pose_w2c_noise_(2,3) += Random::UniformRand(-0.5, 0.5);

            // pose_w2c_noise_(0,3) = pose_w2c_(0,3)/2.0;
            // pose_w2c_noise_(1,3) = pose_w2c_(1,3)/2.0;
            // pose_w2c_noise_(2,3) = pose_w2c_(2,3);

            pose_c2w_ = pose_w2c_.inverse();
            pose_c2w_noise_ = pose_w2c_noise_.inverse();
            id_ = id;
            intrinsic_ << 600, 0, 320,
                         0, 600, 240,
                         0, 0, 1;

            observations_.reserve(num_landmarks);
        }
        Frame(const Mat44_t& pose_w2c, unsigned int id, int num_landmarks)
        {
            pose_w2c_ = pose_w2c;
            pose_c2w_ = pose_w2c_.inverse();

            pose_w2c_noise_ = pose_w2c_;
            pose_c2w_noise_ = pose_c2w_;

            intrinsic_ << 600, 0, 320,
                         0, 600, 240,
                         0, 0, 1;
            id_ = id;
            observations_.reserve(num_landmarks);
        }
        ~Frame()
        {

        }

        void addObservation(unsigned int landmark_id, const Vec2_t& observation)
        {
            observations_[landmark_id] = observation;
        }

        void addGTObservation(unsigned int landmark_id, const Vec2_t& observation)
        {
            gt_observations_[landmark_id] = observation;
        }

        cv::Mat gt_image_, observed_image_;
        Mat44_t pose_w2c_, pose_c2w_;
        Mat44_t pose_w2c_noise_, pose_c2w_noise_;
        int id_ = 0;

        Mat33_t intrinsic_;

        std::unordered_map<unsigned int, Vec2_t> observations_;
        std::unordered_map<unsigned int, Vec2_t> gt_observations_;
};

#endif
