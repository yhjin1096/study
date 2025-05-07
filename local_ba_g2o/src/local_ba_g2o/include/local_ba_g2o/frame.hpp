#ifndef FRAME_HPP
#define FRAME_HPP

#include <local_ba_g2o/type.h>
#include <opencv2/opencv.hpp>
class Frame
{
    public:
        Frame(const Vec2_t& xy, unsigned int id)
        {
            // yaw를 -90도로 설정하고 z를 1.6m로 고정
            pose_ = Mat44_t::Identity();
            pose_.block<3,3>(0,0) = Eigen::AngleAxisd(-M_PI/2.0, Eigen::Vector3d::UnitZ()).toRotationMatrix();
            pose_(0,3) = xy(0);
            pose_(1,3) = xy(1);
            pose_(2,3) = 1.6;

            id_ = id;
            intrinsic_ << 1000, 0, 320,
                         0, 1000, 240,
                         0, 0, 1;
        }
        ~Frame()
        {

        }

        cv::Mat gt_image_, image_;
        Mat44_t pose_;
        unsigned int id_ = 0;

        Mat33_t intrinsic_;
};

#endif
