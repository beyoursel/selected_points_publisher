import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import sys

def load_point_cloud(txt_file):
    """ 读取点云数据 """
    data = np.loadtxt(txt_file, skiprows=1)  # 跳过第一行表头
    return data  # 返回数组 (N, 8)

def plot_histogram(data, column_index, title, xlabel):
    """ 画属性的直方图 """
    plt.figure(figsize=(8, 5))
    sns.histplot(data[:, column_index], bins=50, kde=True)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.grid(True)
    plt.show()

def plot_attr_radar(data, column_index, title="velocity_radar"):
    plt.figure(figsize=(10, 6))
    # 绘制散点图
    plt.scatter(range(len(data[:, column_index])), data[:, column_index], label=title, color='blue', s=20, alpha=0.8)
    # 添加标题和标签
    plt.title(title, fontsize=16)
    plt.xlabel('Step', fontsize=14)
    plt.ylabel(title, fontsize=14)
    
    # 添加网格和图例
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.show()

def plot_attr_radar_multi_file(data_ground, data_lift, column_index, title="velocity_radar"):
    plt.figure(figsize=(10, 6))
    # 绘制散点图
    plt.scatter(range(len(data_ground[:, column_index])), data_ground[:, column_index], label="ground", color='blue', s=20, alpha=0.8)
    plt.scatter(range(len(data_lift[:, column_index])), data_lift[:, column_index], label="lift-goods", color='red', s=20, alpha=0.8)
    # 添加标题和标签
    plt.title(title, fontsize=16)
    plt.xlabel('Step', fontsize=14)
    plt.ylabel(title, fontsize=14)
    
    # 添加网格和图例
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.show()

def plot_3d_scatter(data):
    """ 3D 可视化点云 """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=data[:, 3], cmap='viridis', s=1)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Point Cloud Visualization")
    plt.show()

def visualize_attributes(ground_file, lift_file):
    """ 读取并可视化点云的属性 """
    data_ground = load_point_cloud(ground_file)
    data_lift = load_point_cloud(lift_file)

    # 3D 散点图
    # plot_3d_scatter(data)

    # # 各属性直方图
    # plot_histogram(data, 3, "Confidence Distribution", "Confidence")
    # # plot_histogram(data, 7, "Curvature Distribution", "Curvature")
    # plot_histogram(data, 4, "Velocity Distribution", "Velocity")
    # plot_histogram(data, 5, "Rcs Distribution", "Rcs")
    # plot_histogram(data, 6, "Snr Distribution", "Snr")

    plot_attr_radar_multi_file(data_ground, data_lift, 4, "ground-lift velocity_radar")
    plot_attr_radar_multi_file(data_ground, data_lift, 5, "ground-lift rcs_radar")
    # plot_attr_radar(data, 6, "lift snr_radar")

def visualize_attributes_single(ground_file):
    """ 读取并可视化点云的属性 """
    data_ground = load_point_cloud(ground_file)

    plot_attr_radar(data_ground, 4, "velocity")

if __name__ == "__main__":
    """
        pt.x = xyz.x();
        pt.y = xyz.y();
        pt.z = xyz.z();
        pt.normal_x = ob->vel;
        pt.normal_y = ob->rcs;
        pt.normal_z = ob->snr;
        pt.intensity = ob->exist_confidence;
        pt.curvature = ob->flags;
    
    """
    if (len(sys.argv) < 3):
        print("Usage: python parse_ptc_distribution.py <ground_file> <lift_file>")
        exit(0)
    ground_file = sys.argv[1]
    lift_file = sys.argv[2]
    # visualize_attributes_single(ground_file)
    visualize_attributes(ground_file, lift_file)
