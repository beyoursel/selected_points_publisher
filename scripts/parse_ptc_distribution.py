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

def visualize_attributes(txt_file):
    """ 读取并可视化点云的属性 """
    data = load_point_cloud(txt_file)

    # 3D 散点图
    # plot_3d_scatter(data)

    # 各属性直方图
    plot_histogram(data, 3, "Confidence Distribution", "Confidence")
    # plot_histogram(data, 7, "Curvature Distribution", "Curvature")
    plot_histogram(data, 4, "Velocity Distribution", "Velocity")
    plot_histogram(data, 5, "Rcs Distribution", "Rcs")
    plot_histogram(data, 6, "Snr Distribution", "Snr")

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
    if (len(sys.argv) < 2):
        print("Usage: python parse_ptc_distribution.py <txt_file>")
        exit(0)
    txt_file = sys.argv[-1]
    visualize_attributes(txt_file)
