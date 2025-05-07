#ifndef RANDOM_HPP
#define RANDOM_HPP

#include <local_ba_g2o/type.h>
#include <local_ba_g2o/landmark.hpp>

#include <vector>

class Random
{
    public:
        /// \brief Get data from the random uniform distribution.
        /// \param[in] lowerBndr Lower bound.
        /// \param[in] lowerBndr Upper bound.
        static double UniformRand(double lowerBndr, double upperBndr)
        {
            return lowerBndr + ((double) std::rand() / (RAND_MAX + 1.0)) * (upperBndr - lowerBndr);
        }

        /// \brief Get data from the random gaussian distribution.
        /// \param[in] mean Mean of gaussian distribution.
        /// \param[in] sigma Sigma of gaussian distribution.
        static double GaussRand(double mean, double sigma)
        {
            double x, y, r2;
            do {
                x = -1.0 + 2.0 * UniformRand(0.0, 1.0);
                y = -1.0 + 2.0 * UniformRand(0.0, 1.0);
                r2 = x * x + y * y;
            } while (r2 > 1.0 || r2 == 0.0);
            return mean + sigma * y * std::sqrt(-2.0 * log(r2) / r2);
        }

        static std::vector<Landmark> getRandomLandmarks(int num_landmarks)
        {
            std::vector<Landmark> landmarks;
            for(int i = 0; i < num_landmarks; i++)
            {
                landmarks.push_back(Landmark(Vec3_t(UniformRand(-10.0, 10.0), UniformRand(-10.0, 10.0), 20.0 + GaussRand(0.0, 1.0)), i));
            }
            return landmarks;
        }
};

#endif
