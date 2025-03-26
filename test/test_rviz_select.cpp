// pointcloud_saver_node.cpp

#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <boost/filesystem.hpp>
#include <string>

class PointCloudSaver
{
public:
    PointCloudSaver()
        : nh_("~") // 使用私有命名空间
    {
        // 设置 PCD 文件的保存路径
        pcd_file_path_ = "saved_cloud.pcd";
        txt_file_path_ = "saved_cloud.txt";
        // 订阅 /rviz_selected_points 话题
        subscriber_ = nh_.subscribe<sensor_msgs::PointCloud2>("/rviz_selected_points", 10, &PointCloudSaver::pointcloudCallback, this);
    }

    void pointcloudCallback(const sensor_msgs::PointCloud2ConstPtr& cloud_msg)
    {
        // 将 sensor_msgs::PointCloud2 转换为 pcl::PointCloud<pcl::PointXYZINormal>
        pcl::PointCloud<pcl::PointXYZINormal>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZINormal>);

        pcl::fromROSMsg(*cloud_msg, *cloud);
        if (!cloud->empty()) {
            pcl::io::savePCDFileASCII(pcd_file_path_, *cloud);
            ROS_INFO("Saved pointcloud to %s and num: %d", pcd_file_path_.c_str(), cloud->points.size());
        } else {
            ROS_WARN("Empty pointcloud.");
        }

        std::ofstream out_file(txt_file_path_);
        if (!out_file.is_open()) {
            std::cerr << "Failed to open output file: " << txt_file_path_ << std::endl;
            return;
        }
    
        out_file << "x y z intensity normal_x normal_y normal_z curvature\n";
    
        // 遍历点云并写入 TXT 文件
        for (const auto& point : cloud->points) {
            out_file << point.x << " " << point.y << " " << point.z << " "
                     << point.intensity << " "
                     << point.normal_x << " " << point.normal_y << " " << point.normal_z << " "
                     << point.curvature << "\n";
        }
    
        out_file.close();
        std::cout << "Saved point cloud data to " << txt_file_path_ << std::endl;        

    }

private:
    ros::NodeHandle nh_;
    ros::Subscriber subscriber_;
    std::string current_dir_;      // 当前工作目录
    std::string pcd_file_path_;    // PCD 文件保存路径
    std::string txt_file_path_;    // TXT 文件保存路径
};

int main(int argc, char** argv)
{
    // 初始化 ROS 节点
    ros::init(argc, argv, "pointcloud_saver_node");

    // 创建节点对象
    PointCloudSaver saver;

    // 进入 ROS 循环
    ros::spin();

    return 0;
}