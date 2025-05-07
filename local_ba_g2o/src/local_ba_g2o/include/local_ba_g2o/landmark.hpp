#ifndef LANDMARK_HPP
#define LANDMARK_HPP

#include <local_ba_g2o/type.h>

class Landmark
{
    public:
        Landmark(const Vec3_t& pos, unsigned int id)
        {
            pos_ = pos;
            id_ = id;
        }
        ~Landmark()
        {

        }
        Vec3_t pos_;
        unsigned int id_;
};

#endif