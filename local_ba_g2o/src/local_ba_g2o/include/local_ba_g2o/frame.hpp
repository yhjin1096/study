#ifndef FRAME_HPP
#define FRAME_HPP

#include <local_ba_g2o/type.h>
#include <opencv2/opencv.hpp>
#include <unordered_map>
class Frame
{
    public:
        Frame(const Vec2_t& xy, unsigned int id, int num_landmarks)
        {
            // yaw를 -90도로 설정하고 z를 1.6m로 고정
            pose_w2c_ = Mat44_t::Identity();
            pose_w2c_.block<3,3>(0,0) = Eigen::AngleAxisd(-M_PI/2.0, Eigen::Vector3d::UnitZ()).toRotationMatrix();
            pose_w2c_(0,3) = xy(0);
            pose_w2c_(1,3) = xy(1);
            pose_w2c_(2,3) = 1.6;

            pose_c2w_ = pose_w2c_.inverse();

            id_ = id;
            intrinsic_ << 600, 0, 320,
                         0, 600, 240,
                         0, 0, 1;

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
        int id_ = 0;

        Mat33_t intrinsic_;
        
        std::unordered_map<unsigned int, Vec2_t> observations_;
        std::unordered_map<unsigned int, Vec2_t> gt_observations_;
};

#endif
