#include "pgo_toy_example/pgo_additional_edge.hpp"

#include <ros/ros.h>

#include <geometry_msgs/Point.h>
#include <visualization_msgs/Marker.h>
#include <visualization_msgs/MarkerArray.h>

#include <Eigen/Dense>

#include <g2o/core/sparse_optimizer.h>
#include <g2o/core/optimizable_graph.h>
#include <g2o/core/block_solver.h>
#include <g2o/core/solver.h>
#include <g2o/core/robust_kernel_impl.h>
#include <g2o/core/optimization_algorithm_levenberg.h>
#include <g2o/solvers/dense/linear_solver_dense.h>
#include <g2o/types/slam3d/types_slam3d.h>

#include <iostream>
#include <vector>

int Sampling::Uniform(int from, int to)
{
    return static_cast<int>(UniformRand(from, to));
}

double Sampling::Uniform()
{
    return UniformRand(0., 1.);
}

double Sampling::Gaussian(double sigma)
{
    return GaussRand(0., sigma);
}

PGOAdditionalEdge::PGOAdditionalEdge(bool verbose)
    : vertex_id_(0), verbose_(verbose)
{
    num_poses_ = 15;
    std::unique_ptr<g2o::BlockSolver_6_3::LinearSolverType> linear_solver;
    linear_solver = std::make_unique<g2o::LinearSolverDense<g2o::BlockSolver_6_3::PoseMatrixType>>();

    g2o::OptimizationAlgorithmLevenberg* solver = 
        new g2o::OptimizationAlgorithmLevenberg(std::make_unique<g2o::BlockSolver_6_3>(std::move(linear_solver)));

    solver->setUserLambdaInit(1);

    optimizer_ = new g2o::SparseOptimizer();
    optimizer_->setAlgorithm(solver);
}

void PGOAdditionalEdge::SetOriginalPoses()
{
    for(int i = 0; i < num_poses_; i++)
    {
        Eigen::Matrix<double, 3, 1> trans;
        if(i == 0)
            trans = Eigen::Matrix<double, 3, 1>(0, 0, 1.5);
        else if(i >= 1 && i <= 7)
        {
            trans = Eigen::Matrix<double, 3, 1>(i + Sampling::Gaussian(.2),
                                                Sampling::Gaussian(.2),
                                                1.5);
        }
        else if(i == 8)
        {
            trans = Eigen::Matrix<double, 3, 1>(8 + Sampling::Gaussian(.2),
                                                7 - i + Sampling::Gaussian(.2),
                                                1.5);
        }
        else if(i >= 9)
        {
            trans = Eigen::Matrix<double, 3, 1>(17 - i + Sampling::Gaussian(.2),
                                                -1 + Sampling::Gaussian(.2),
                                                1.5);
        }

        Eigen::Quaterniond q;
        q.setIdentity();

        g2o::SE3Quat pose;
        pose.setRotation(q);
        pose.setTranslation(trans);

        original_poses_.push_back(pose);

        Eigen::Matrix<double, 3, 1> trans_tmp;
        trans_tmp = Eigen::Matrix<double, 3, 1>(trans(0) + Sampling::Gaussian(.05),
                                                trans(1) + Sampling::Gaussian(.05),
                                                1.5);

        pose.setTranslation(trans_tmp);
        additional_poses_.push_back(pose);
    }
}

void PGOAdditionalEdge::MakeCurrentPoseAndAddVertex()
{
    for(int i = 0; i < original_poses_.size(); i++)
    {
        g2o::VertexSE3Expmap* vtx = new g2o::VertexSE3Expmap();
        vtx->setId(vertex_id_++);

        if(i == 0)
            vtx->setFixed(true);
        
        Eigen::Matrix<double, 3, 1> trans(Sampling::Gaussian(.2),
                                          Sampling::Gaussian(.2),
                                          Sampling::Gaussian(.05));
        Eigen::Quaterniond q;
        q.UnitRandom();

        g2o::SE3Quat origin = original_poses_.at(i);
        g2o::SE3Quat noise;
        noise.setTranslation(origin.translation() + trans);
        
        vtx->setEstimate(noise);
        optimizer_->addVertex(vtx);
    }
}

void PGOAdditionalEdge::AddEdge()
{
    for(int i = 1; i < original_poses_.size(); i++)
    {
        g2o::EdgeSE3Expmap* e = new g2o::EdgeSE3Expmap();
        g2o::SE3Quat relative_pose = original_poses_.at(i-1).inverse() * original_poses_.at(i);
// std::cout << original_poses_.at(i-1).translation().transpose() << std::endl;
// std::cout << original_poses_.at(i).translation().transpose() << std::endl;
// std::cout << relative_pose.translation().transpose() << std::endl;
        e->setMeasurement(relative_pose);
        
        #if 0
            MatXX information = Eigen::MatrixXd::Identity(6, 6);
        #else   
            MatXX A = Eigen::MatrixXd::Random(6, 6).cwiseAbs();
            MatXX information = A.transpose() * A;
        #endif

        e->setInformation(information);
        e->setVertex(0, optimizer_->vertex(i-1));
        e->setVertex(1, optimizer_->vertex(i));

        optimizer_->addEdge(e);


        /*------------------------------------------------------------------*/
        // g2o::SE3Quat additional_relative_pose = additional_poses_.at(i-1).inverse() * additional_poses_.at(i);
        // e->setMeasurement(additional_relative_pose);
        // e->setInformation(information);
        // e->setVertex(0, optimizer_->vertex(i-1));
        // e->setVertex(1, optimizer_->vertex(i));

        // optimizer_->addEdge(e);
    }

    // g2o::EdgeSE3Expmap* e511(new g2o::EdgeSE3Expmap());
    // g2o::SE3Quat relative_pose = original_poses_.at(5).inverse() * original_poses_.at(11);
    // e511->setMeasurement(relative_pose);
    // MatXX A = Eigen::MatrixXd::Random(6,6).cwiseAbs();
    // MatXX information = A.transpose() * A;
    // e511->setInformation(information);
    // e511->vertices()[0] = optimizer_->vertex(5);
    // e511->vertices()[1] = optimizer_->vertex(11);
    // optimizer_->addEdge(e511);

    // relative_pose = additional_poses_.at(5).inverse() * additional_poses_.at(11);
    // e511->setMeasurement(relative_pose);
    // optimizer_->addEdge(e511);

    // g2o::EdgeSE3Expmap* e314(new g2o::EdgeSE3Expmap());
    // relative_pose = original_poses_.at(3).inverse() * original_poses_.at(14);
    // e314->setMeasurement(relative_pose);
    // A = Eigen::MatrixXd::Random(6,6).cwiseAbs();
    // information = A.transpose() * A;
    // e314->setInformation(information);
    // e314->vertices()[0] = optimizer_->vertex(3);
    // e314->vertices()[1] = optimizer_->vertex(14);
    // optimizer_->addEdge(e314);

    // relative_pose = additional_poses_.at(3).inverse() * additional_poses_.at(14);
    // e511->setMeasurement(relative_pose);
    // optimizer_->addEdge(e314);
}

void PGOAdditionalEdge::Reset()
{
    optimizer_->clear();
    original_poses_.clear();
    additional_poses_.clear();
    vertex_id_ = 0;

    SetOriginalPoses();

    MakeCurrentPoseAndAddVertex();

    AddEdge();

    optimizer_->initializeOptimization();
    optimizer_->setVerbose(verbose_);
}