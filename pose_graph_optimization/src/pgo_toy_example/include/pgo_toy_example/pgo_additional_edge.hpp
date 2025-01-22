#include "pgo_toy_example/alias_types.h"

#include <Eigen/Dense>

#include <g2o/core/sparse_optimizer.h>
#include <g2o/core/optimizable_graph.h>
#include <g2o/core/block_solver.h>
#include <g2o/core/solver.h>
#include <g2o/core/robust_kernel_impl.h>
#include <g2o/core/optimization_algorithm_levenberg.h>
#include <g2o/core/optimization_algorithm_gauss_newton.h>
#include <g2o/solvers/dense/linear_solver_dense.h>
#include <g2o/types/sba/types_six_dof_expmap.h>
#include <g2o/types/slam3d/se3quat.h>
#include <g2o/types/slam3d/types_slam3d.h>

#include <iostream>
#include <vector>


/// \brief Get data from the random uniform distribution.
/// \param[in] lowerBndr Lower bound.
/// \param[in] lowerBndr Upper bound.
static double UniformRand(double lowerBndr, double upperBndr){
  return lowerBndr + ((double) std::rand() / (RAND_MAX + 1.0)) * (upperBndr - lowerBndr);
}

/// \brief Get data from the random gaussian distribution.
/// \param[in] mean Mean of gaussian distribution.
/// \param[in] sigma Sigma of gaussian distribution.
static double GaussRand(double mean, double sigma){
  double x, y, r2;
  do {
    x = -1.0 + 2.0 * UniformRand(0.0, 1.0);
    y = -1.0 + 2.0 * UniformRand(0.0, 1.0);
    r2 = x * x + y * y;
  } while (r2 > 1.0 || r2 == 0.0);
  return mean + sigma * y * std::sqrt(-2.0 * log(r2) / r2);
}

class Sampling
{
  public:
    static int Uniform(int from, int to);
    static double Uniform();
    static double Gaussian(double sigma);
  private:
};

class PGOAdditionalEdge
{
    public:
        PGOAdditionalEdge(bool verbose=true);
        
        void SetOriginalPoses();

        void Reset();

        void MakeCurrentPoseAndAddVertex();

        void AddEdge();

        g2o::SparseOptimizer* GetOptimizer() { return optimizer_; }

        std::vector<g2o::SE3Quat, Eigen::aligned_allocator<g2o::SE3Quat>> GetOriginalPoses() { return original_poses_; }
        std::vector<g2o::SE3Quat, Eigen::aligned_allocator<g2o::SE3Quat>> GetAdditionalPoses() { return additional_poses_; }

        int GetOriginalPosesSize() { return original_poses_.size(); }
        
    private:
        g2o::SparseOptimizer* optimizer_;
        std::vector<g2o::SE3Quat, Eigen::aligned_allocator<g2o::SE3Quat>> original_poses_;
        std::vector<g2o::SE3Quat, Eigen::aligned_allocator<g2o::SE3Quat>> additional_poses_;
        int vertex_id_;
        bool verbose_;
        int num_poses_;
};