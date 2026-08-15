#ifndef OPTIMIZER_HPP
#define OPTIMIZER_HPP

#include <local_ba_g2o/local_ba_g2o/type.h>
#include <local_ba_g2o/local_ba_g2o/frame.hpp>
#include <local_ba_g2o/local_ba_g2o/landmark.hpp>

#include "g2o/core/optimization_algorithm_factory.h"
#include "g2o/core/robust_kernel_impl.h"
#include "g2o/core/sparse_optimizer.h"
#include "g2o/solvers/structure_only/structure_only_solver.h"
#include "g2o/stuff/sampler.h"
#include "g2o/types/sba/types_six_dof_expmap.h"

#if defined G2O_HAVE_CHOLMOD
G2O_USE_OPTIMIZATION_LIBRARY(cholmod);
#else
G2O_USE_OPTIMIZATION_LIBRARY(eigen);
#endif

class Optimizer
{
    public:
        Optimizer(){};

        g2o::SparseOptimizer optimizer_;
        std::vector<g2o::SE3Quat, Eigen::aligned_allocator<g2o::SE3Quat>> camera_poses_;
        std::vector<g2o::Vector3, Eigen::aligned_allocator<g2o::Vector3>> landmark_poses_;

        void reset()
        {
            camera_poses_.clear();
            landmark_poses_.clear();
            optimizer_.clearParameters();
            optimizer_.clear();
        }

        bool setup(std::vector<Frame>& frames, std::vector<Landmark>& landmarks)
        {
            /*--------------------------------------------------------------*/
            // optimizer 설정
            std::string solverName;
            #ifdef G2O_HAVE_CHOLMOD
                        solverName = "lm_fix6_3_cholmod";
            #else
                        solverName = "lm_fix6_3";
            #endif

            g2o::OptimizationAlgorithmProperty solverProperty;
            g2o::OptimizationAlgorithm* solver = 
                g2o::OptimizationAlgorithmFactory::instance()->construct(solverName, solverProperty);

            if (!solver) {
                std::cerr << "Failed to create solver: " << solverName << std::endl;
                return false;
            }

            optimizer_.setAlgorithm(solver);

            /*--------------------------------------------------------------*/
            // 카메라 파라미터 추가
            double focal_length = frames[0].intrinsic_(0,0);
            Vec2_t principal_point(frames[0].intrinsic_(0,2), frames[0].intrinsic_(1,2));
            g2o::CameraParameters* camera_parameters_ = new g2o::CameraParameters(focal_length, principal_point, 0);
            camera_parameters_->setId(0);

            if (!optimizer_.addParameter(camera_parameters_)) {
                // assert(false);
                std::cerr << "Failed to add camera parameters" << std::endl;
                delete camera_parameters_;
                camera_parameters_ = nullptr;
                return false;
            }

            /*--------------------------------------------------------------*/
            // pose 설정
            for(auto& frame : frames)
            {
                g2o::SE3Quat camera_pose(frame.pose_c2w_.block<3,3>(0,0), frame.pose_c2w_.block<3,1>(0,3));
                camera_poses_.push_back(camera_pose);
            }

            /*--------------------------------------------------------------*/
            // landmark 설정
            for(auto& landmark : landmarks)
            {
                g2o::Vector3 landmark_pose(landmark.pos_(0), landmark.pos_(1), landmark.pos_(2));
                landmark_poses_.push_back(landmark_pose);
            }

            /*--------------------------------------------------------------*/
            // pose vertex 추가
            int vertex_id = 0;
            for(auto& pose : camera_poses_)
            {
                if(vertex_id == 0)
                    addPoseVertex(pose, vertex_id++, true);
                else
                    addPoseVertex(pose, vertex_id++, false);
            }
            
            /*--------------------------------------------------------------*/
            // landmark vertex 추가
            for (auto& landmark : landmarks)
            {
                // landmark 관찰한 frame 2개 이상인지 확인
                std::vector<int> frame_ids;
                for(auto& frame : frames)
                    if(frame.observations_.find(landmark.id_) != frame.observations_.end())
                        frame_ids.push_back(frame.id_);

                if(frame_ids.size() < 2)
                    continue;

                addLandmarkVertex(landmark_poses_[landmark.id_], landmark.id_ + vertex_id);

                // edge 추가
                for(auto& frame_id : frame_ids)
                {
                    g2o::EdgeProjectXYZ2UV* e = new g2o::EdgeProjectXYZ2UV();
                    e->setVertex(0, dynamic_cast<g2o::OptimizableGraph::Vertex*>(
                        optimizer_.vertices().find(landmark.id_ + vertex_id)->second));
                    e->setVertex(1, dynamic_cast<g2o::OptimizableGraph::Vertex*>(
                        optimizer_.vertices().find(frame_id)->second));
                    e->setMeasurement(frames[frame_id].gt_observations_[landmark.id_]);
                    e->information() = Mat22_t::Identity();

                    g2o::RobustKernelHuber* rk = new g2o::RobustKernelHuber;
                    e->setRobustKernel(rk);

                    e->setParameterId(0, 0);
                    optimizer_.addEdge(e);
                }
            }

            return true;
        }

        void addPoseVertex(g2o::SE3Quat pose, int id, bool is_fixed)
        {\
            g2o::VertexSE3Expmap* v = new g2o::VertexSE3Expmap();
            v->setId(id);
            v->setFixed(is_fixed);
            v->setEstimate(pose);
            optimizer_.addVertex(v);
        }

        void addLandmarkVertex(g2o::Vector3 pos, int id)
        {
            g2o::VertexPointXYZ* v = new g2o::VertexPointXYZ();
            v->setId(id);
            v->setEstimate(pos);
            v->setMarginalized(true);
            optimizer_.addVertex(v);
        }

        void addEdge()
        {

        }

        void doStructureOnlyBA(int num_iter)
        {
            g2o::StructureOnlySolver<3> structure_only_ba;
            std::cout << "Performing structure-only BA:" << std::endl;
            g2o::OptimizableGraph::VertexContainer points;
            for (g2o::OptimizableGraph::VertexIDMap::const_iterator it =
                    optimizer_.vertices().begin();
                it != optimizer_.vertices().end(); ++it) {
                g2o::OptimizableGraph::Vertex* v =
                    static_cast<g2o::OptimizableGraph::Vertex*>(it->second);
                if (v->dimension() == 3) points.push_back(v);
            }
            structure_only_ba.calc(points, num_iter);
        }

        void optimize(int num_iter)
        {
            optimizer_.setVerbose(true);
            optimizer_.initializeOptimization();

            optimizer_.optimize(num_iter);
        }
};

#endif