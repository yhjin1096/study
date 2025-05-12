#ifndef SAVE_HPP
#define SAVE_HPP

#include <local_ba_g2o/type.h>
#include <local_ba_g2o/landmark.hpp>
#include <local_ba_g2o/frame.hpp>

#include <fstream>
class DataIO
{
    public:
        static void save(const std::vector<Frame>& frames, const std::vector<Landmark>& gt_landmarks, const std::vector<Landmark>& noise_landmarks, const std::string& data_path)
        {
            std::ofstream file(data_path);

            file << "intrinsic" << std::endl;
            file << frames[0].intrinsic_(0, 0) << " " << frames[0].intrinsic_(0, 1) << " " << frames[0].intrinsic_(0, 2) << " " 
                 << frames[0].intrinsic_(1, 0) << " " << frames[0].intrinsic_(1, 1) << " " << frames[0].intrinsic_(1, 2) << " " 
                 << frames[0].intrinsic_(2, 0) << " " << frames[0].intrinsic_(2, 1) << " " << frames[0].intrinsic_(2, 2) << std::endl;

            file << "gt_landmarks" << std::endl;
            for(const auto& gt_landmark : gt_landmarks)
            {
                file << gt_landmark.id_ << " " << gt_landmark.pos_(0) << " " << gt_landmark.pos_(1) << " " << gt_landmark.pos_(2) << std::endl;
            }

            file << "noise_landmarks" << std::endl;
            for(const auto& noise_landmark : noise_landmarks)
            {
                file << noise_landmark.id_ << " " << noise_landmark.pos_(0) << " " << noise_landmark.pos_(1) << " " << noise_landmark.pos_(2) << std::endl;
            }

            file << "frames" << std::endl;
            for(const auto& frame : frames)
            {
                file << frame.id_ << " " 
                     << frame.pose_w2c_(0, 0) << " " << frame.pose_w2c_(0, 1) << " " << frame.pose_w2c_(0, 2) << " " << frame.pose_w2c_(0, 3) << " " 
                     << frame.pose_w2c_(1, 0) << " " << frame.pose_w2c_(1, 1) << " " << frame.pose_w2c_(1, 2) << " " << frame.pose_w2c_(1, 3) << " " 
                     << frame.pose_w2c_(2, 0) << " " << frame.pose_w2c_(2, 1) << " " << frame.pose_w2c_(2, 2) << " " << frame.pose_w2c_(2, 3) << std::endl;
            }

            file << "gt_observations" << std::endl;
            for(const auto& frame : frames)
            {
                for(const auto& gt_observation : frame.gt_observations_)
                {
                    file << frame.id_ << " " << gt_observation.first << " " << gt_observation.second(0) << " " << gt_observation.second(1) << std::endl;
                }
            }

            file << "noise_observations" << std::endl;
            for(const auto& frame : frames)
            {
                for(const auto& noise_observation : frame.observations_)
                {
                    file << frame.id_ << " " << noise_observation.first << " " << noise_observation.second(0) << " " << noise_observation.second(1) << std::endl;
                }
            }

            file.close();
            std::cout << "Data saved to " << data_path << std::endl;
        }

        static void load(std::vector<Frame>& frames, std::vector<Landmark>& gt_landmarks, std::vector<Landmark>& noise_landmarks, const std::string& data_path)
        {
            std::ifstream file(data_path);
            if(!file.is_open())
            {
                std::cerr << "Failed to open file: " << data_path << std::endl;
                return;
            }

            std::string line;
            Mat33_t intrinsic = Mat33_t::Identity();
            frames.clear();
            gt_landmarks.clear();
            noise_landmarks.clear();

            while(std::getline(file, line))
            {
                std::cout << "line: " << line << std::endl;
                if(line == "intrinsic")
                {
                    std::getline(file, line);
                    std::stringstream ss(line);
                    for(int i = 0; i < 3; i++)
                    {
                        for(int j = 0; j < 3; j++)
                        {
                            ss >> intrinsic(i, j);
                        }
                    }
                }
                else if(line == "gt_landmarks")
                {
                    std::cout << "Reading gt_landmarks section..." << std::endl;
                    while(std::getline(file, line) && !line.empty())
                    {
                        if(line == "noise_landmarks" || line == "frames" || 
                           line == "gt_observations" || line == "noise_observations") {
                            file.seekg(file.tellg() - static_cast<std::streamoff>(line.length() + 1));
                            break;
                        }
                        std::stringstream ss(line);
                        int id;
                        double x, y, z;
                        ss >> id >> x >> y >> z;
                        gt_landmarks.push_back(Landmark(Vec3_t(x, y, z), id));
                    }
                }
                else if(line == "noise_landmarks")
                {
                    while(std::getline(file, line) && !line.empty())
                    {
                        if(line == "frames" || 
                           line == "gt_observations" || line == "noise_observations") {
                            file.seekg(file.tellg() - static_cast<std::streamoff>(line.length() + 1));
                            break;
                        }
                        std::stringstream ss(line);
                        int id;
                        double x, y, z;
                        ss >> id >> x >> y >> z;
                        noise_landmarks.push_back(Landmark(Vec3_t(x, y, z), id));
                    }
                }
                else if(line == "frames")
                {
                    while(std::getline(file, line) && !line.empty())
                    {
                        if(line == "gt_observations" || line == "noise_observations") {
                            file.seekg(file.tellg() - static_cast<std::streamoff>(line.length() + 1));
                            break;
                        }
                        std::stringstream ss(line);
                        int id;
                        Mat44_t pose = Mat44_t::Identity();
                        ss >> id;
                        for(int i = 0; i < 3; i++)
                        {
                            for(int j = 0; j < 4; j++)
                            {
                                ss >> pose(i, j);
                            }
                        }
                        // pose에서 translation 부분만 추출하여 Vec2_t로 전달
                        Vec2_t translation(pose(0,3), pose(1,3));
                        frames.push_back(Frame(translation, id, gt_landmarks.size()));
                        frames.back().intrinsic_ = intrinsic;
                        frames.back().pose_w2c_ = pose;
                        frames.back().pose_c2w_ = pose.inverse();
                    }
                }
                else if(line == "gt_observations")
                {
                    while(std::getline(file, line) && !line.empty())
                    {
                        if(line == "gt_observations" || line == "noise_observations") {
                            file.seekg(file.tellg() - static_cast<std::streamoff>(line.length() + 1));
                            break;
                        }
                        std::stringstream ss(line);
                        int frame_id, landmark_id;
                        double x, y;
                        ss >> frame_id >> landmark_id >> x >> y;
                        if(frame_id < frames.size())
                        {
                            frames[frame_id].addGTObservation(landmark_id, Vec2_t(x, y));
                        }
                    }
                }
                else if(line == "noise_observations")
                {
                    while(std::getline(file, line) && !line.empty())
                    {
                        std::stringstream ss(line);
                        int frame_id, landmark_id;
                        double x, y;
                        ss >> frame_id >> landmark_id >> x >> y;
                        if(frame_id < frames.size())
                        {
                            frames[frame_id].addObservation(landmark_id, Vec2_t(x, y));
                        }
                    }
                }
            }
            file.close();
            
            std::cout << "Data loaded from " << std::string(PROJECT_SOURCE_DIR) + "/data.txt" << std::endl;
            std::cout << "Loaded " << frames.size() << " frames, " 
                      << gt_landmarks.size() << " GT landmarks, and " 
                      << noise_landmarks.size() << " noise landmarks" << std::endl;
            for(auto& frame : frames)
            {
                std::cout << "frame.id_: " << frame.id_ << ", noise_observations: " << frame.observations_.size() << ", gt_observations: " << frame.gt_observations_.size() << std::endl;
                frame.observed_image_ = cv::Mat::zeros(frame.intrinsic_(1,2) * 2, frame.intrinsic_(0,2) * 2, CV_8UC3);
                frame.gt_image_ = cv::Mat::zeros(frame.intrinsic_(1,2) * 2, frame.intrinsic_(0,2) * 2, CV_8UC3);
            }
        }
};
#endif