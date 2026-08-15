#include <iostream>

#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>
#include <Eigen/Geometry>

#include <local_ba_g2o/local_ba_g2o/random.hpp>
#include <local_ba_g2o/local_ba_g2o/frame.hpp>

#include <local_ba_g2o/optimize/optimizer.hpp>

#include <local_ba_g2o/data_io/dataio.hpp>

pcl::PointCloud<pcl::PointXYZRGB>::Ptr convertLandmarksToPointCloud(const std::vector<Landmark>& landmarks, cv::Scalar color) {
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    cloud->points.resize(landmarks.size());

    double min_z = std::numeric_limits<double>::max();
    double max_z = std::numeric_limits<double>::lowest();
    for(const auto& landmark : landmarks) {
        min_z = std::min(min_z, landmark.pos_(2));
        max_z = std::max(max_z, landmark.pos_(2));
    }

    for(size_t i = 0; i < landmarks.size(); ++i) {
        cloud->points[i].x = landmarks[i].pos_(0);
        cloud->points[i].y = landmarks[i].pos_(1);
        cloud->points[i].z = landmarks[i].pos_(2);

        cloud->points[i].r = static_cast<uint8_t>(color(2));
        cloud->points[i].g = static_cast<uint8_t>(color(1));
        cloud->points[i].b = static_cast<uint8_t>(color(0));
    }
    cloud->width = landmarks.size();
    cloud->height = 1;
    cloud->is_dense = false;

    return cloud;
}

pcl::PointCloud<pcl::PointXYZRGB>::Ptr convertLandmarksToPointCloud(const Optimizer& optimizer,
                                                                const std::vector<Landmark>& landmarks,
                                                                int num_frames) {
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    cloud->points.resize(landmarks.size());
    
    for(size_t i = 0; i < landmarks.size(); ++i) {
        auto vertex_it = optimizer.optimizer_.vertices().find(landmarks[i].id_ + num_frames);
        if(vertex_it != optimizer.optimizer_.vertices().end()) {
            g2o::VertexPointXYZ* vtx = dynamic_cast<g2o::VertexPointXYZ*>(vertex_it->second);

            if(vtx) {
                cloud->points[i].x = vtx->estimate()(0);
                cloud->points[i].y = vtx->estimate()(1);
                cloud->points[i].z = vtx->estimate()(2);
                cloud->points[i].r = static_cast<uint8_t>(255);
                cloud->points[i].g = static_cast<uint8_t>(255);
                cloud->points[i].b = static_cast<uint8_t>(0);
            }
        }
    }
    cloud->width = landmarks.size();
    cloud->height = 1;
    cloud->is_dense = false;

    return cloud;
}

void publishLandmarks(const pcl::PointCloud<pcl::PointXYZRGB>::Ptr& cloud, 
                     ros::Publisher& pub) {
    sensor_msgs::PointCloud2 cloud_msg;
    pcl::toROSMsg(*cloud, cloud_msg);
    cloud_msg.header.frame_id = "map";
    cloud_msg.header.stamp = ros::Time::now();
    pub.publish(cloud_msg);
}

void publishFramePose(const Frame& frame, tf2_ros::TransformBroadcaster& broadcaster) {
    geometry_msgs::TransformStamped transform;
    transform.header.stamp = ros::Time::now();
    transform.header.frame_id = "map";
    transform.child_frame_id = "frame_" + std::to_string(frame.id_);

    // pose에서 translation 추출
    transform.transform.translation.x = frame.pose_w2c_(0,3);
    transform.transform.translation.y = frame.pose_w2c_(1,3);
    transform.transform.translation.z = frame.pose_w2c_(2,3);

    // pose에서 rotation 추출 (rotation matrix를 quaternion으로 변환)
    Eigen::Matrix3d rot = frame.pose_w2c_.block<3,3>(0,0);
    Eigen::Quaterniond q(rot);
    transform.transform.rotation.x = q.x();
    transform.transform.rotation.y = q.y();
    transform.transform.rotation.z = q.z();
    transform.transform.rotation.w = q.w();

    broadcaster.sendTransform(transform);
}

void publishFramePoses(const Optimizer& optimizer, tf2_ros::TransformBroadcaster& broadcaster, int num_frames)
{
    for(int i = 0; i < num_frames; ++i) {
        auto vertex_it = optimizer.optimizer_.vertices().find(i);
        if(vertex_it != optimizer.optimizer_.vertices().end()) {
            g2o::VertexSE3Expmap* vtx = dynamic_cast<g2o::VertexSE3Expmap*>(vertex_it->second);
            if(vtx) {
                geometry_msgs::TransformStamped transform;
                transform.header.stamp = ros::Time::now();
                transform.header.frame_id = "map";
                transform.child_frame_id = "optimal_frame_" + std::to_string(i);

                // pose에서 translation 추출
                g2o::SE3Quat pose_inv = vtx->estimate().inverse();
                transform.transform.translation.x = pose_inv.translation()(0);
                transform.transform.translation.y = pose_inv.translation()(1);
                transform.transform.translation.z = pose_inv.translation()(2);

                // pose에서 rotation 추출 (rotation matrix를 quaternion으로 변환)
                Eigen::Quaterniond q = pose_inv.rotation();
                transform.transform.rotation.x = q.x();
                transform.transform.rotation.y = q.y();
                transform.transform.rotation.z = q.z();
                transform.transform.rotation.w = q.w();

                broadcaster.sendTransform(transform);
            }
        }
    }
}

void setObservations(std::vector<Frame>& frames, const std::vector<Landmark>& gt_landmarks, const std::vector<Landmark>& noise_landmarks)
{
    for(auto& frame : frames)
    {
        int width = static_cast<int>(frame.intrinsic_(0,2) * 2);
        int height = static_cast<int>(frame.intrinsic_(1,2) * 2);
        frame.gt_image_ = cv::Mat::zeros(height, width, CV_8UC3);
        frame.observed_image_ = cv::Mat::zeros(height, width, CV_8UC3);

        for(const auto& landmark : gt_landmarks)
        {
            Eigen::Vector4d gt_point_world(landmark.pos_(0), landmark.pos_(1), landmark.pos_(2), 1.0);
            Eigen::Vector4d gt_point_frame = frame.pose_w2c_.inverse() * gt_point_world;

            if(gt_point_frame(2) <= 0) continue;

            int gt_x = static_cast<int>(gt_point_frame(0) * frame.intrinsic_(0,0) / gt_point_frame(2) + frame.intrinsic_(0,2));
            int gt_y = static_cast<int>(gt_point_frame(1) * frame.intrinsic_(1,1) / gt_point_frame(2) + frame.intrinsic_(1,2));

            if(gt_x < 0 || gt_x >= width || gt_y < 0 || gt_y >= height) continue;

            frame.addGTObservation(landmark.id_, Vec2_t(gt_x, gt_y));

            // int noise_x = gt_x + static_cast<int>(Random::UniformRand(-2.0, 2.0));
            // int noise_y = gt_y + static_cast<int>(Random::UniformRand(-2.0, 2.0));
            int noise_x = gt_x + static_cast<int>(Random::GaussRand(0.0, 1.0));
            int noise_y = gt_y + static_cast<int>(Random::GaussRand(0.0, 1.0));

            if(noise_x < 0 || noise_x >= width || noise_y < 0 || noise_y >= height) continue;

            frame.addObservation(landmark.id_, Vec2_t(noise_x, noise_y));
        }
    }
}

void observedImage(const Optimizer& optimizer, std::vector<Frame>& frames, const std::vector<Landmark>& landmarks)
{
    cv::Mat concat_image;
    bool is_first = true;

    for(auto& frame : frames)
    {
        cv::Mat whole_image = cv::Mat::zeros(frame.intrinsic_(1,2) * 2, frame.intrinsic_(0,2) * 2, CV_8UC3);
        frame.gt_image_ = cv::Mat::zeros(frame.intrinsic_(1,2) * 2, frame.intrinsic_(0,2) * 2, CV_8UC3);
        frame.observed_image_ = cv::Mat::zeros(frame.intrinsic_(1,2) * 2, frame.intrinsic_(0,2) * 2, CV_8UC3);
        cv::Mat line_image = cv::Mat(frame.gt_image_.rows, 1, CV_8UC3, cv::Scalar(255, 255, 255));

        for(const auto& observation : frame.observations_)
        {
            int x = observation.second(0);
            int y = observation.second(1);
            if(x >= 0 && x < frame.observed_image_.cols && y >= 0 && y < frame.observed_image_.rows)
                cv::circle(whole_image, cv::Point(x, y), 4, cv::Scalar(0, 0, 255), -1);
        }

        for(const auto& observation : frame.gt_observations_)
        {
            int x = observation.second(0);
            int y = observation.second(1);
            if(x >= 0 && x < frame.gt_image_.cols && y >= 0 && y < frame.gt_image_.rows)
                cv::circle(whole_image, cv::Point(x, y), 4, cv::Scalar(0, 255, 0), -1);
        }

        // cv::add(frame.gt_image_, frame.observed_image_, whole_image);

        for(const auto& landmark : landmarks)
        {
            auto vertex_it = optimizer.optimizer_.vertices().find(landmark.id_ + frames.size());
            if(vertex_it != optimizer.optimizer_.vertices().end())
            {
                g2o::VertexPointXYZ* vtx = dynamic_cast<g2o::VertexPointXYZ*>(vertex_it->second);
                if(vtx)
                {
                    // 3D -> 2D 투영
                    Eigen::Vector4d point_world(vtx->estimate()(0), vtx->estimate()(1), vtx->estimate()(2), 1.0);
                    Eigen::Vector4d point_frame = frame.pose_w2c_.inverse() * point_world;

                    if(point_frame(2) > 0)  // 카메라 앞에 있는 경우만
                    {
                        int x = static_cast<int>(point_frame(0) * frame.intrinsic_(0,0) / point_frame(2) + frame.intrinsic_(0,2));
                        int y = static_cast<int>(point_frame(1) * frame.intrinsic_(1,1) / point_frame(2) + frame.intrinsic_(1,2));

                        if(x >= 0 && x < whole_image.cols && y >= 0 && y < whole_image.rows)
                            cv::circle(whole_image, cv::Point(x, y), 2, cv::Scalar(0, 255, 255), -1);
                    }
                }
            }
        }

        if(is_first)
        {
            concat_image = whole_image.clone();
            is_first = false;
        }
        else
        {
            cv::hconcat(concat_image, line_image, concat_image);
            cv::hconcat(concat_image, whole_image, concat_image);
        }
    }

    // 이미지 크기 조정 및 표시
    // cv::resize(concat_image, concat_image, cv::Size(), 0.7, 0.7);
    cv::imshow("observed image", concat_image);
    cv::waitKey(1);
}


Eigen::Vector3d convertRotationMatrixToRPY(const Eigen::Matrix3d& rot)
{
    double roll = atan2(rot(2,1), rot(2,2));
    double pitch = atan2(-rot(2,0), sqrt(rot(2,1)*rot(2,1) + rot(2,2)*rot(2,2)));
    double yaw = atan2(rot(1,0), rot(0,0));
    return Eigen::Vector3d(roll, pitch, yaw);
}

void printResult(const Optimizer& optimizer, const std::vector<Landmark>& gt_landmarks, const std::vector<Landmark>& noise_landmarks, const std::vector<Frame>& frames)
{
    for(const auto& frame : frames)
    {
        auto vertex_it = optimizer.optimizer_.vertices().find(frame.id_);
        if(vertex_it != optimizer.optimizer_.vertices().end())
        {
            g2o::VertexSE3Expmap* vtx = dynamic_cast<g2o::VertexSE3Expmap*>(vertex_it->second);
            if(vtx)
            {
                Vec3_t gt_rpy = convertRotationMatrixToRPY(frame.pose_w2c_.block<3,3>(0,0));
                Vec3_t optimized_rpy = convertRotationMatrixToRPY(vtx->estimate().inverse().rotation().toRotationMatrix());
                Vec3_t gt_translation = frame.pose_w2c_.block<3,1>(0,3);
                Vec3_t optimized_translation = vtx->estimate().inverse().translation();

                std::cout << " Frame id                       : " << frame.id_  << std::endl;
                std::cout << " GT Rotation(r, p, y)           : " << gt_rpy(0) << ", " << gt_rpy(1) << ", " << gt_rpy(2) << std::endl;
                std::cout << " Optimized Rotation(r, p, y)    : " << optimized_rpy(0) << ", " << optimized_rpy(1) << ", " << optimized_rpy(2) << std::endl;
                std::cout << " GT Translation(x, y, z)        : " << gt_translation(0) << ", " << gt_translation(1) << ", " << gt_translation(2) << std::endl;
                std::cout << " Optimized Translation(x, y, z) : " << optimized_translation(0) << ", " << optimized_translation(1) << ", " << optimized_translation(2) << std::endl;
            }
        }
    }
    // // 자유도, 95% 신뢰구간 threshold
    // // (1, 3.841), (2, 5.991), (3, 7.815), (4, 9.488), (5, 11.070)
    // double chi2 = optimizer.optimizer_.activeChi2();
    // std::cout << " Total chi2 error               : " << chi2 << std::endl;
    // for(const auto& edge : optimizer.optimizer_.activeEdges())
    // {
    //     std::cout << " Edge id                       : " << edge->id() << std::endl;
    //     std::cout << " Edge chi2 error               : " << edge->chi2() << std::endl;
    // }
    std::cout << std::endl;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "local_ba_g2o");
    ros::NodeHandle nh;

    int num_landmarks = nh.param<int>("num_landmarks", 100);
    int num_frames = nh.param<int>("num_frames", 5);
    int num_iter = nh.param<int>("num_iter", 30);
    bool use_data = nh.param<bool>("use_data", false);
    bool save_data = nh.param<bool>("save_data", false);
    std::string data_path = nh.param<std::string>("data_path", "");

    ros::Publisher gt_landmarks_pub = nh.advertise<sensor_msgs::PointCloud2>("/gt_landmarks", 1);
    ros::Publisher noise_landmarks_pub = nh.advertise<sensor_msgs::PointCloud2>("/observed_landmarks", 1);
    ros::Publisher optimal_landmarks_pub = nh.advertise<sensor_msgs::PointCloud2>("/optimized_landmarks", 1);

    tf2_ros::TransformBroadcaster tf_broadcaster;

    //optimizer
    Optimizer optimizer;

    std::vector<Frame> frames;
    std::vector<Landmark> gt_landmarks;
    std::vector<Landmark> noise_landmarks;
    if(use_data)
        DataIO::load(frames, gt_landmarks, noise_landmarks, data_path);

    ros::Rate loop_rate(10);
    while(ros::ok())
    {
        int count = 0;
        optimizer.reset();

        if(!use_data)
        {
            frames.clear();
            gt_landmarks.clear();
            noise_landmarks.clear();

            //landmarks
            gt_landmarks = Random::getRandomLandmarks(num_landmarks);
            noise_landmarks = gt_landmarks;
            for(auto& landmark : noise_landmarks)
                landmark.pos_ += Vec3_t(Random::UniformRand(-0.1, 0.1), Random::UniformRand(-0.1, 0.1), Random::UniformRand(-0.1, 0.1));
                // landmark.pos_ += Vec3_t(Random::GaussRand(0.0, 1.0), Random::GaussRand(0.0, 1.0), Random::GaussRand(0.0, 1.0));

            //frames
            for(int i = 0; i < num_frames; ++i)
                frames.push_back(Frame(Vec2_t(0.5 * i, 0.0), i, num_landmarks));

            setObservations(frames, gt_landmarks, noise_landmarks);
        }

        if(save_data)
        {
            DataIO::save(frames, gt_landmarks, noise_landmarks, data_path);
            break;
        }

        if(!optimizer.setup(frames, noise_landmarks))
            break;

        //structure only ba
        // optimizer.doStructureOnlyBA(10);

        while(count < num_iter)
        {
            //publish landmarks
            publishLandmarks(convertLandmarksToPointCloud(gt_landmarks, cv::Scalar(0, 255, 0)), gt_landmarks_pub);
            publishLandmarks(convertLandmarksToPointCloud(noise_landmarks, cv::Scalar(0, 0, 255)), noise_landmarks_pub);
            publishLandmarks(convertLandmarksToPointCloud(optimizer, noise_landmarks, num_frames), optimal_landmarks_pub);

            //publish frame poses
            publishFramePoses(optimizer, tf_broadcaster, num_frames);

            //imshow
            observedImage(optimizer, frames, gt_landmarks);

            //optimize
            optimizer.optimize(1);

            count++;
            loop_rate.sleep();
            ros::spinOnce();
        }
        std::cout << "chi2: " << optimizer.optimizer_.activeChi2() << std::endl;
        std::cout << "num of edges: " << optimizer.optimizer_.edges().size() << std::endl;
        // printResult(optimizer, gt_landmarks, noise_landmarks, frames);
    }

    return 0;
}
