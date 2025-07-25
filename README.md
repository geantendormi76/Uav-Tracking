# Isaac Sim + ROS 2 自学探索之路

![Isaac Sim](https://img.shields.io/badge/Isaac%20Sim-4.5.0-brightgreen.svg)
![ROS 2](https://img.shields.io/badge/ROS%202-Humble-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2011%20%7C%20WSL2-lightgrey.svg)
[![GitHub stars](https://img.shields.io/github/stars/YourGitHubUsername/Uav-Tracking.svg?style=social)](https://github.com/YourGitHubUsername/Uav-Tracking/stargazers)

![键盘遥控演示](./docs/assets/ros2-teleop-keyboard-demo.gif)

---

## 📖 项目简介

本项目旨在记录并分享一个从零开始学习 **NVIDIA Isaac Sim** 与 **ROS 2 (Humble)** 集成开发的完整、可复现的自学路径。最初项目名为 `Uav-Tracking`，现已发展成为一个面向社区的、系统化的学习指南。

无论您是机器人领域的初学者，还是希望将ROS 2应用到先进物理仿真中的开发者，都可以通过本仓库提供的详细步骤，一步步搭建开发环境、完成官方核心教程，并最终构建属于自己的机器人仿真应用。

所有教程均基于NVIDIA官方文档，并融入了在实践中遇到的问题、详细的解读和经过验证的解决方案。

## 🚀 学习路径总览 (Learning Path)

本学习路径严格遵循官方推荐的学习流程，分为两大里程碑：**环境搭建** 和 **核心教程实践**。

---

### **里程碑 0：环境搭建 (Environment Setup) - 成功的基石**

在开始任何仿真之前，一个稳定、配置正确的开发环境是成功的关键。此阶段将指导您完成从操作系统到ROS 2工作空间的全部配置。**请务必严格按照顺序完成此里程碑中的所有步骤。**

*   **[第一部分：Windows 11 + WSL2 终极开发环境蓝图](./docs/00-Environment-Setup/01-Windows-Dev-Environment-Blueprint.md)**
    > 包含了从Windows系统设置、NVIDIA驱动、网络代理、终端美化到所有基础工具链的安装，为您构建一个极致稳定与高效的开发母舰。

*   **[第二部分：ROS 2 核心工作空间搭建](./docs/00-Environment-Setup/02-ROS2-Workspace-Setup.md)**
    > 指导您在配置好的WSL2环境中，安装ROS 2 Humble，并构建官方推荐的ROS 2工作区。

---

### **里程碑 1：核心教程实践 (Core Tutorial Practice)**

完成环境搭建后，我们将逐一攻克NVIDIA官方提供的核心教程。每一节都包含了官方文档链接和我的个人实践笔记（持续更新中）。

| 状态 | 教程主题 | 官方文档 | 
|:---:|:---|:---|
| ✅ | 1. Isaac Sim 快速入门 | [Quickstart](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/introduction/quickstart_isaacsim.html) 
| ✅ | 2. 机器人快速入门 | [Robot Quickstart](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/introduction/quickstart_isaacsim_robot.html)
| ✅ | 3. ROS & ROS 2 安装 | [Installation](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/installation/install_ros.html) 
| ✅ | 4. URDF 导入 (TurtleBot) | [URDF Import](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/ros2_tutorials/tutorial_ros2_turtlebot.html)
| ✅ | 5. Isaac Sim Omnigraph 教程 | [Omnigraph Tutorial](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/omnigraph/omnigraph_tutorial.html) 
| ✅ | 6. 自定义 Python 节点 | [Custom Python Nodes](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/omnigraph/custom-nodes.html) 
| ✅ | 7. 通过ROS2消息驱动TurtleBot | [Drive with ROS 2](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/ros2_tutorials/tutorial_ros2_drive_turtlebot.html) 
| ✅ | 8. ROS2 时钟同步 | [ROS 2 Clock](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/ros2_tutorials/tutorial_ros2_clock.html) 


* **图例:**
    * ✅: 已完成
    * ➡️: 正在进行
    * ⏳: 待学习

---

## 📂 项目结构

```
Uav-Tracking/
├── README.md                   # 本文档，项目总览
└── docs/
    ├── assets/                 # 文档中使用的图片资源
    ├── 00-Environment-Setup/   # 详细的环境搭建指南
    └── 01-Isaac-Sim-ROS2-Tutorials/ # 各个核心教程的学习笔记
```

## 🤝 贡献与反馈

本项目旨在为社区服务。如果您在复现过程中遇到任何问题，或对笔记内容有任何建议和补充，欢迎通过以下方式参与：

*   **提交 Issue:** 如果您发现文档中的错误、过时信息或有任何疑问，请[创建一个Issue](https://github.com/YourGitHubUsername/Uav-Tracking/issues)。
*   **发起 Pull Request:** 如果您想直接帮助改进文档内容，我们非常欢迎您[发起一个Pull Request](https://github.com/YourGitHubUsername/Uav-Tracking/pulls)。

让我们一起，让学习先进机器人技术的道路变得更加平坦！