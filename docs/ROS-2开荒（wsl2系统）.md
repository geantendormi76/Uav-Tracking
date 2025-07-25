### **里程碑一：奠基 (The Foundation) - ROS 2 工作空间搭建**

**目标：** 在您已经完美配置的WSL2环境中，安装ROS 2，并利用`direnv`创建一个自动化的、隔离的、专业的ROS 2开发工作空间。

**核心理念：** 工作空间应该是自包含的(self-contained)。当您进入项目目录时，所有需要的环境（ROS 2路径、Python虚拟环境）都应自动激活，离开目录时自动卸载。这正是`direnv`的威力所在。

---

#### **第一步：安装ROS 2 Humble 核心组件**

即使您的开荒蓝图很完美，但我们还未正式安装ROS 2本身。现在，我们来完成这一步。

*   **行动指令 (在WSL2终端中执行)：**

**添加ROS 2官方软件源：**
```bash
# 确保您的系统支持UTF-8
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 添加ROS 2的GPG密钥
sudo apt install -y curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 将ROS 2的仓库地址写入apt源列表
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

```bash
sudo apt update
# 我们安装桌面完整版，因为它包含了后续里程碑需要的Rviz2等可视化工具
sudo apt install -y ros-humble-desktop

# 安装colcon构建工具和其他有用的开发包
sudo apt install -y ros-dev-tools
```

-  **如果节点问题导致出错了，可以换节点执行以下命令**

```bash
sudo dpkg --configure -a && sudo apt-get -f install -y && sudo apt install -y ros-humble-desktop ros-dev-tools
```

### **如果问题依旧存在：终极备用方案 - 更换ROS镜像源**

如果切换代理节点后，重试依然失败，那说明ROS官方源 (`packages.ros.org`) 可能与您所有代理节点的连接性都不佳。此时，最佳策略是切换到一个国内的、经过优化的镜像源，例如清华大学源。

*   **切换到清华源的指令：**
```bash
# 备份原始的ROS源文件
sudo cp /etc/apt/sources.list.d/ros2.list /etc/apt/sources.list.d/ros2.list.backup

# 将源地址替换为清华大学镜像源
sudo sed -i 's@packages.ros.org/ros2@mirrors.tuna.tsinghua.edu.cn/ros2@g' /etc/apt/sources.list.d/ros2.list

# 更新apt缓存并重试安装
sudo apt update
sudo apt install -y ros-humble-desktop ros-dev-tools ros-humble-moveit ros-humble-ackermann-msgs
```

## Python3.10构建 ROS 2 工作区

```zsh
cd ~
git clone https://github.com/isaac-sim/IsaacSim-ros_workspaces

# 获取您现有的 ROS 2 Humble 安装：
source /opt/ros/humble/setup.zsh

# 构建 ROS 2 工作区：
cd IsaacSim-ros_workspaces/humble_ws
colcon build

# 获取构建的工作区并从同一终端运行 Isaac Sim：
source humble_ws/install/setup.zsh
```