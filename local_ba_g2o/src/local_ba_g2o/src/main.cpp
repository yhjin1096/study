#include <iostream>

#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>
#include <Eigen/Geometry>

#include <local_ba_g2o/random.hpp>
#include <local_ba_g2o/frame.hpp>

#include <tinycolormap.hpp>

pcl::PointCloud<pcl::PointXYZRGB>::Ptr convertLandmarksToPointCloud(const std::vector<Landmark>& landmarks) {
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

        double normalized_z = (landmarks[i].pos_(2) - min_z) / (max_z - min_z);

        auto color = tinycolormap::GetColor(normalized_z, tinycolormap::ColormapType::Heat);

        cloud->points[i].r = static_cast<uint8_t>(color.r() * 255);
        cloud->points[i].g = static_cast<uint8_t>(color.g() * 255);
        cloud->points[i].b = static_cast<uint8_t>(color.b() * 255);
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
    transform.transform.translation.x = frame.pose_(0,3);
    transform.transform.translation.y = frame.pose_(1,3);
    transform.transform.translation.z = frame.pose_(2,3);

    // pose에서 rotation 추출 (rotation matrix를 quaternion으로 변환)
    Eigen::Matrix3d rot = frame.pose_.block<3,3>(0,0);
    Eigen::Quaterniond q(rot);
    transform.transform.rotation.x = q.x();
    transform.transform.rotation.y = q.y();
    transform.transform.rotation.z = q.z();
    transform.transform.rotation.w = q.w();

    broadcaster.sendTransform(transform);
}

void setImages(std::vector<Frame>& frames, pcl::PointCloud<pcl::PointXYZRGB>::Ptr& cloud)
{
    for(auto& frame : frames)
    {
        int width = static_cast<int>(frame.intrinsic_(0,2) * 2);
        int height = static_cast<int>(frame.intrinsic_(1,2) * 2);
        frame.image_ = cv::Mat::zeros(height, width, CV_8UC3);
        int count = 0;

        for(const auto& point : cloud->points)
        {
            Eigen::Vector4d point_world(point.x, point.y, point.z, 1.0);
            Eigen::Vector4d point_frame = frame.pose_.inverse() * point_world;

            if(point_frame(2) <= 0) continue;

            int x = static_cast<int>(point_frame(0) * frame.intrinsic_(0,0) / point_frame(2) + frame.intrinsic_(0,2));
            int y = static_cast<int>(point_frame(1) * frame.intrinsic_(1,1) / point_frame(2) + frame.intrinsic_(1,2));

            if(x < 0 || x >= width || y < 0 || y >= height) continue;

            frame.image_.at<cv::Vec3b>(y, x) = cv::Vec3b(point.b, point.g, point.r);
            count++;
        }
        std::cout << "Frame " << frame.id_ << " points: " << count << std::endl;
    }

    // 모든 프레임 이미지를 가로로 연결
    cv::Mat concat_image = frames[0].image_.clone();
    cv::Mat line_image = cv::Mat(concat_image.rows, 3, CV_8UC3, cv::Scalar(255, 255, 255));
    for(size_t i = 1; i < frames.size(); ++i)
    {
        cv::hconcat(concat_image, line_image, concat_image);
        cv::hconcat(concat_image, frames[i].image_, concat_image);
    }
    cv::imshow("All Frames", concat_image);
    cv::waitKey(1);
}
int main(int argc, char **argv)
{
    ros::init(argc, argv, "local_ba_g2o");
    ros::NodeHandle nh;

    int num_landmarks = nh.param<int>("num_landmarks", 100);
    int num_frames = nh.param<int>("num_frames", 5);

    //landmarks
    std::vector<Landmark> landmarks = Random::getRandomLandmarks(num_landmarks);
    ros::Publisher landmarks_pub = nh.advertise<sensor_msgs::PointCloud2>("/landmarks", 1);
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud = convertLandmarksToPointCloud(landmarks);

    //frames
    std::vector<Frame> frames;
    for(int i = 0; i < num_frames; ++i)
        frames.push_back(Frame(Vec2_t(0.3 * i, 0.0), i));
    tf2_ros::TransformBroadcaster tf_broadcaster;

    ros::Rate loop_rate(10);

    while(ros::ok())
    {

        //publish
        publishLandmarks(cloud, landmarks_pub);
        for(const auto& frame : frames) {
            publishFramePose(frame, tf_broadcaster);
        }
        setImages(frames, cloud);
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}
