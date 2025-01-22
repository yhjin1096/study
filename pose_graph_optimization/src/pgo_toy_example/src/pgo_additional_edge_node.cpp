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

enum TYPE
{
    PREV,
    OPT,
    ADDITIONAL
};

// prev poses (gray sphere).
visualization_msgs::MarkerArray prev_nodes;
visualization_msgs::MarkerArray prev_edges;

visualization_msgs::MarkerArray opt_nodes;
visualization_msgs::MarkerArray opt_edges;

visualization_msgs::MarkerArray addi_nodes;
visualization_msgs::MarkerArray addi_edges;

visualization_msgs::MarkerArray texts;

// Position of the first node.
double xinit, yinit, zinit;

void SetNodeForROS(PGOAdditionalEdge* pae, visualization_msgs::MarkerArray& nodes,
              std::string ns, int id, Vec4 rgba, TYPE type)
{
    visualization_msgs::Marker node;
    node.header.frame_id = "world";
    node.header.stamp = ros::Time::now();
    node.ns = ns;
    node.id = id;
    node.type = visualization_msgs::Marker::SPHERE;
    node.scale.x = node.scale.y = node.scale.z = 0.2;
    node.color.r = rgba[0]; node.color.g = rgba[1]; node.color.b = rgba[2]; node.color.a = rgba[3];

    if(type == PREV)
    {
        Eigen::Quaterniond q = (Eigen::Quaterniond)pae->GetOriginalPoses()[id].rotation();

        node.pose.position.x = pae->GetOriginalPoses()[id].translation()[0];
        node.pose.position.y = pae->GetOriginalPoses()[id].translation()[1];
        node.pose.position.z = pae->GetOriginalPoses()[id].translation()[2];
        node.pose.orientation.x = q.x();
        node.pose.orientation.y = q.y();
        node.pose.orientation.z = q.z();
        node.pose.orientation.w = q.w();

        if(node.pose.orientation.w < 0)
        {
            node.pose.orientation.x *= -1;
            node.pose.orientation.y *= -1;
            node.pose.orientation.z *= -1;
            node.pose.orientation.w *= -1;
        }
        nodes.markers.push_back(node);
    }
    else if(type == ADDITIONAL)
    {
        Eigen::Quaterniond q = (Eigen::Quaterniond)pae->GetAdditionalPoses()[id].rotation();

        node.pose.position.x = pae->GetAdditionalPoses()[id].translation()[0];
        node.pose.position.y = pae->GetAdditionalPoses()[id].translation()[1];
        node.pose.position.z = pae->GetAdditionalPoses()[id].translation()[2];
        node.pose.orientation.x = q.x();
        node.pose.orientation.y = q.y();
        node.pose.orientation.z = q.z();
        node.pose.orientation.w = q.w();

        if(node.pose.orientation.w < 0)
        {
            node.pose.orientation.x *= -1;
            node.pose.orientation.y *= -1;
            node.pose.orientation.z *= -1;
            node.pose.orientation.w *= -1;
        }
        nodes.markers.push_back(node);
    }
    else if(type == OPT)
    {
        g2o::VertexSE3Expmap* vtx = static_cast<g2o::VertexSE3Expmap*>(pae->GetOptimizer()->vertex(id));
        Eigen::Isometry3d opt_poses = vtx->estimate();
        Eigen::Quaterniond q = (Eigen::Quaterniond)opt_poses.rotation();

        if(id==0)
        {
            xinit = opt_poses.translation()[0];
            yinit = opt_poses.translation()[1];
            zinit = opt_poses.translation()[2];

            node.pose.position.x = 0;
            node.pose.position.y = 0;
            node.pose.position.z = 0;
        }

        node.pose.position.x = opt_poses.translation()[0]-xinit;
        node.pose.position.y = opt_poses.translation()[1]-yinit;
        node.pose.position.z = opt_poses.translation()[2]-zinit;

        node.pose.orientation.x = q.x();
        node.pose.orientation.y = q.y();
        node.pose.orientation.z = q.z();
        node.pose.orientation.w = q.w();

        if(node.pose.orientation.w < 0) {
        node.pose.orientation.x *= -1;
        node.pose.orientation.y *= -1;
        node.pose.orientation.z *= -1;
        node.pose.orientation.w *= -1;
        }
        nodes.markers.push_back(node);

        visualization_msgs::Marker opt_node_text;
        opt_node_text.header.frame_id = "world";
        opt_node_text.header.stamp = ros::Time();
        opt_node_text.ns = "opt_node_text";
        opt_node_text.id = id;
        opt_node_text.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
        opt_node_text.action = visualization_msgs::Marker::ADD;
        opt_node_text.scale.z = 0.1;
        opt_node_text.color.r =0.0; opt_node_text.color.g = 0.0; opt_node_text.color.b = 0.0; opt_node_text.color.a = 1.0;
        opt_node_text.pose.position.x = node.pose.position.x;
        opt_node_text.pose.position.y = node.pose.position.y;
        opt_node_text.pose.position.z = node.pose.position.z+0.2;
        std::string txt = "x" + std::to_string(id);
        opt_node_text.text = txt;
        texts.markers.push_back(opt_node_text);
    }
}

void SetEdgeForROS(PGOAdditionalEdge* pae, visualization_msgs::MarkerArray& edges,
             std::string ns, int id, int start, int end, Vec4 rgba, TYPE type)
{
    visualization_msgs::Marker edge;
    edge.header.frame_id = "world";
    edge.header.stamp = ros::Time::now();
    edge.ns = ns;
    edge.id = id;
    edge.type = visualization_msgs::Marker::LINE_LIST;
    edge.color.r = rgba[0]; edge.color.g = rgba[1]; edge.color.b = rgba[2]; edge.color.a = rgba[3];
    edge.pose.orientation.w = 1.0;
    edge.scale.x = 0.01;

    if(type == PREV)
    {
        geometry_msgs::Point p1;
        p1.x = pae->GetOriginalPoses()[start].translation()[0];
        p1.y = pae->GetOriginalPoses()[start].translation()[1];
        p1.z = pae->GetOriginalPoses()[start].translation()[2];
        edge.points.push_back(p1);

        geometry_msgs::Point p2;
        p2.x = pae->GetOriginalPoses()[end].translation()[0];
        p2.y = pae->GetOriginalPoses()[end].translation()[1];
        p2.z = pae->GetOriginalPoses()[end].translation()[2];
        edge.points.push_back(p2);

        edges.markers.push_back(edge);

        visualization_msgs::Marker prev_edge_text;
        prev_edge_text.header.frame_id = "world";
        prev_edge_text.header.stamp = ros::Time();
        prev_edge_text.ns = "prev_edge_text";
        prev_edge_text.id = id;
        prev_edge_text.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
        prev_edge_text.action = visualization_msgs::Marker::ADD;
        prev_edge_text.scale.z = 0.1;
        prev_edge_text.color.r = rgba[0]; prev_edge_text.color.g = rgba[1]; prev_edge_text.color.b = rgba[2]; prev_edge_text.color.a = rgba[3];
        prev_edge_text.pose.position.x = (p1.x+p2.x)/2.;
        prev_edge_text.pose.position.y = (p1.y+p2.y)/2.;
        prev_edge_text.pose.position.z = (p1.z+p2.z)/2. + 0.1;
        std::string txt = "zhat" + std::to_string(start) + std::to_string(end);
        prev_edge_text.text = txt;
        texts.markers.push_back(prev_edge_text);
    }
    else if(type == ADDITIONAL)
    {
        geometry_msgs::Point p1;
        p1.x = pae->GetAdditionalPoses()[start].translation()[0];
        p1.y = pae->GetAdditionalPoses()[start].translation()[1];
        p1.z = pae->GetAdditionalPoses()[start].translation()[2];
        edge.points.push_back(p1);

        geometry_msgs::Point p2;
        p2.x = pae->GetAdditionalPoses()[end].translation()[0];
        p2.y = pae->GetAdditionalPoses()[end].translation()[1];
        p2.z = pae->GetAdditionalPoses()[end].translation()[2];
        edge.points.push_back(p2);

        edges.markers.push_back(edge);

        visualization_msgs::Marker prev_edge_text;
        prev_edge_text.header.frame_id = "world";
        prev_edge_text.header.stamp = ros::Time();
        prev_edge_text.ns = "addi_edge_text";
        prev_edge_text.id = id;
        prev_edge_text.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
        prev_edge_text.action = visualization_msgs::Marker::ADD;
        prev_edge_text.scale.z = 0.1;
        prev_edge_text.color.r = rgba[0]; prev_edge_text.color.g = rgba[1]; prev_edge_text.color.b = rgba[2]; prev_edge_text.color.a = rgba[3];
        prev_edge_text.pose.position.x = (p1.x+p2.x)/2.;
        prev_edge_text.pose.position.y = (p1.y+p2.y)/2.;
        prev_edge_text.pose.position.z = (p1.z+p2.z)/2. + 0.1;
        std::string txt = "addi" + std::to_string(start) + std::to_string(end);
        prev_edge_text.text = txt;
        texts.markers.push_back(prev_edge_text);
    }
    else if (type == OPT)
    {
        g2o::VertexSE3Expmap* prev_vtx = static_cast<g2o::VertexSE3Expmap*>(pae->GetOptimizer()->vertex(start));
        g2o::VertexSE3Expmap* curr_vtx = static_cast<g2o::VertexSE3Expmap*>(pae->GetOptimizer()->vertex(end));
        Isometry prev_opt_poses = prev_vtx->estimate();
        Isometry curr_opt_poses = curr_vtx->estimate();

        // First opt_node.
        if(start == 0) {
        xinit = prev_opt_poses.translation()[0];
        yinit = prev_opt_poses.translation()[1];
        zinit = prev_opt_poses.translation()[2];
        }

        geometry_msgs::Point p1;
        p1.x = prev_opt_poses.translation()[0] -xinit;
        p1.y = prev_opt_poses.translation()[1] -yinit;
        p1.z = prev_opt_poses.translation()[2] -zinit;
        edge.points.push_back(p1);

        geometry_msgs::Point p2;
        p2.x = curr_opt_poses.translation()[0] -xinit;
        p2.y = curr_opt_poses.translation()[1] -yinit;
        p2.z = curr_opt_poses.translation()[2] -zinit;
        edge.points.push_back(p2);

        edges.markers.push_back(edge);

        visualization_msgs::Marker opt_edge_text;
        opt_edge_text.header.frame_id = "world";
        opt_edge_text.header.stamp = ros::Time();
        opt_edge_text.ns = "opt_edge_text";
        opt_edge_text.id = id;
        opt_edge_text.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
        opt_edge_text.action = visualization_msgs::Marker::ADD;
        opt_edge_text.scale.z = 0.1;
        opt_edge_text.color.r = 0.0; opt_edge_text.color.g = 0.0; opt_edge_text.color.b = 0.0; opt_edge_text.color.a = 1.0;
        opt_edge_text.pose.position.x = (p1.x+p2.x)/2.;
        opt_edge_text.pose.position.y = (p1.y+p2.y)/2.;
        opt_edge_text.pose.position.z = (p1.z+p2.z)/2. + 0.1;
        std::string txt = "z" + std::to_string(start) + std::to_string(end);
        opt_edge_text.text = txt;
        texts.markers.push_back(opt_edge_text);
  }
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "pgo_additional_edge");
    ros::NodeHandle nh, priv_nh("~");

    ros::Publisher opt_node_pub = nh.advertise<visualization_msgs::MarkerArray>("opt_nodes",1);
    ros::Publisher opt_edge_pub = nh.advertise<visualization_msgs::MarkerArray>("opt_edges",1);
    ros::Publisher prev_node_pub = nh.advertise<visualization_msgs::MarkerArray>("prev_nodes",1);
    ros::Publisher prev_edge_pub = nh.advertise<visualization_msgs::MarkerArray>("prev_edges",1);
    ros::Publisher addi_node_pub = nh.advertise<visualization_msgs::MarkerArray>("addi_nodes",1);
    ros::Publisher addi_edge_pub = nh.advertise<visualization_msgs::MarkerArray>("addi_edges",1);
    ros::Publisher text_pub = nh.advertise<visualization_msgs::MarkerArray>("texts",1);

    int _rate, _iter;
    priv_nh.param("loop_rate", _rate, 5);
    priv_nh.param("iteration", _iter, 20);

    PGOAdditionalEdge* pae = new PGOAdditionalEdge(true);
    ros::Rate loop_rate(_rate);

    while(ros::ok())
    {
        pae->Reset();

        int num_poses = pae->GetOriginalPosesSize();
        int count = 0;

        while(count < _iter)
        {
            for(int i = 0; i < num_poses; i++)
                SetNodeForROS(pae, prev_nodes, "prev_nodes", i, Eigen::Matrix<double, 4, 1>(0.0, 0.0, 0.0, 0.25), PREV);
            
            for(int i=1; i<num_poses; i++) 
              SetEdgeForROS(pae, prev_edges, "prev_edges", i, i-1, i, Vec4(0.0, 0.0, 0.0, 0.25), PREV);

            // SetEdgeForROS(pae, prev_edges, "prev_edges", 16, 5, 11, Vec4(0.0, 0.0, 0.0, 0.25), PREV);
            // SetEdgeForROS(pae, prev_edges, "prev_edges", 17, 3, 14, Vec4(0.0, 0.0, 0.0, 0.25), PREV);


            for(int i=0; i<num_poses; i++)
              SetNodeForROS(pae, opt_nodes, "opt_nodes", i, Eigen::Matrix<double, 4, 1>(0.0, 0.0, 0.0, 1.0), OPT);
            
            for(int i=1; i<num_poses; i++)
              SetEdgeForROS(pae, opt_edges, "opt_edges", i, i-1, i, Vec4(0.0, 0.0, 0.0, 1), OPT);

            // SetEdgeForROS(pae, opt_edges, "opt_edges", 16, 5, 11, Vec4(0.0, 0.0, 0.0, 1), OPT);
            // SetEdgeForROS(pae, opt_edges, "opt_edges", 17, 3, 14, Vec4(0.0, 0.0, 0.0, 1), OPT);


            for(int i=0; i<num_poses; i++)
              SetNodeForROS(pae, addi_nodes, "addi_nodes", i, Eigen::Matrix<double, 4, 1>(0.0, 0.0, 1.0, 0.25), ADDITIONAL);

            for(int i=1; i<num_poses; i++)
              SetEdgeForROS(pae, addi_edges, "addi_edges", i, i-1, i, Vec4(0.0, 0.0, 1.0, 0.25), ADDITIONAL);

            // SetEdgeForROS(pae, addi_edges, "addi_edges", 16, 5, 11, Vec4(0.0, 0.0, 1.0, 0.25), ADDITIONAL);
            // SetEdgeForROS(pae, addi_edges, "addi_edges", 17, 3, 14, Vec4(0.0, 0.0, 1.0, 0.25), ADDITIONAL);

            prev_node_pub.publish(prev_nodes);
            prev_edge_pub.publish(prev_edges);

            opt_node_pub.publish(opt_nodes);
            opt_edge_pub.publish(opt_edges);

            addi_node_pub.publish(addi_nodes);
            addi_edge_pub.publish(addi_edges);

            text_pub.publish(texts);

            loop_rate.sleep();

            pae->GetOptimizer()->optimize(1);

            count += 1;
            ros::spinOnce();
        }
        std::cout << std::endl;

        prev_nodes.markers.clear();
        prev_edges.markers.clear();
        opt_nodes.markers.clear();
        opt_edges.markers.clear();
        addi_nodes.markers.clear();
        addi_edges.markers.clear();
        texts.markers.clear();
    }

    ros::spin();    
    return 0;
}