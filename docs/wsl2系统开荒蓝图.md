
```bash
# 快捷键设置黄金标准
C:\Windows\System32\cmd.exe /c start "" "D:\笔记"
```
### **《WSL2 系统开荒蓝图 V-Final-Classic》**

**目标：** 构建一个以Windows 11为图形与交互层，以WSL2（经典NAT模式）为Linux引擎层，并由Clash Verge进行智能网络调度的、极致稳定与高效的机器人与AI开发环境。

**核心架构：** Windows 11 (GUI) + WSL2 (NAT) + Docker Desktop + Clash Verge (系统代理) + Zsh

---

#### **阶段零：地基工程 - Windows 宿主机准备**

*此阶段在Windows上完成，为整个系统打下坚实基础。*

1.  **系统与驱动更新：**
    *   **Windows 更新：** 确保Windows 11已更新到最新版本 (`设置` -> `Windows 更新`)。
    *   **NVIDIA 驱动：** 从NVIDIA官网下载并**清洁安装**最新的 **Studio 驱动程序 (SD)**，以获得最佳的专业应用稳定性。

2.  **核心应用安装：**
    *   **Windows Terminal:** 从 Microsoft Store 安装。
    *   **Visual Studio Code:** 从官网安装。
    *   **Docker Desktop for Windows:** 从官网安装。
    *   **Clash Verge:** 从其GitHub Release页面下载并安装。

---

#### **第一阶段：网络环境 - 智能、稳健、一劳永逸**

*此阶段配置Clash Verge，使其成为整个系统的智能网络中枢。*

1.  **Clash Verge 最终配置 (经过验证的正确配置)：**
    *   启动Clash Verge。
    *   进入“**设置**”页面。
    *   **系统设置 -> 虚拟网卡模式：** **保持关闭！**
    *   **系统设置 -> 系统代理：** **保持开启！**
    *   **Clash 设置 -> 局域网连接 (Allow LAN)：** **保持开启！** (Windows防火墙弹出时，务必点击“允许访问”)
    *   **Clash 设置 -> DNS 覆写：** **保持开启**，并进入其详细设置，将“**增强模式**”设置为 **`redir-host`**。

2.  **配置智能分流规则 (The Brain of the Network)：**
    *   **创建强制直连白名单：**
        *   在Clash的配置文件夹下 (通常是`C:\Users\<YourUsername>\.config\clash-verge\profiles\<profile_name>`)，创建一个名为 **`my_rules_direct.txt`** 的文件。
        *   粘贴以下内容：
            ```
            # Personal Direct Whitelist V3.0
            mirrors.aliyun.com
            github.com
            ```

*   **行动指令 (在WSL2终端中执行)：**

    1.  **使用`visudo`安全地编辑配置文件：**
        `visudo`是专门用来编辑`sudoers`文件的命令，它会在保存时检查语法，防止您因为手误而锁死自己的`sudo`权限。**请务必使用`visudo`**。

        ```bash
        sudo visudo
        ```
        这会用默认的文本编辑器（通常是`nano`）打开`/etc/sudoers`文件。

    2.  **添加环境变量保留规则：**
        在打开的文件中，找到以`Defaults`开头的行。在这些行的下面，添加新的一行：

        ```
        Defaults    env_keep += "http_proxy https_proxy no_proxy"
        ```
        *   **解释：** 这行配置的意思是，在`sudo`默认保留的环境变量列表（`env_keep`）中，**追加(+)** 上`http_proxy`、`httpshttps_proxy`和`no_proxy`这三个变量。

    3.  **保存并退出：**
        *   在`nano`编辑器中，按 `Ctrl + O` (Write**O**ut)，然后按 `Enter` 确认保存。
        *   按 `Ctrl + X` 退出。


    *   **创建主规则集 `my_rules.yaml`：**
        *   在同一目录下，创建 **`my_rules.yaml`** 文件。
        *   粘贴以下内容：
            ```yaml
            # Main Ruleset V3.0
            rule-providers:
              my-direct: { type: file, behavior: domain, path: ./my_rules_direct.txt }
              reject: { type: http, behavior: domain, url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt", path: ./ruleset/reject.yaml, interval: 86400 }
              proxy: { type: http, behavior: classical, url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt", path: ./ruleset/proxy.yaml, interval: 86400 }
              direct: { type: http, behavior: classical, url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt", path: ./ruleset/direct.yaml, interval: 86400 }
              lan: { type: http, behavior: ipcidr, url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lan.txt", path: ./ruleset/lan.yaml, interval: 86400 }
              cnip: { type: http, behavior: ipcidr, url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cnip.txt", path: ./ruleset/cnip.yaml, interval: 86400 }
            
            rules:
              - RULE-SET,reject,REJECT
              - RULE-SET,lan,DIRECT
              - RULE-SET,my-direct,DIRECT  # 赋予我们的白名单高优先级
              - RULE-SET,cnip,DIRECT
              - RULE-SET,direct,DIRECT
              - RULE-SET,proxy,追云加速    # <--- 请将'追云加速'替换为您自己的策略组名称
              - GEOIP,CN,DIRECT
              - MATCH,追云加速            # <--- 请将'追云加速'替换为您自己的策略组名称
            ```
    *   **启用规则集：**
        *   进入Clash Verge的“**订阅**”页面，点击“全局扩展覆写配置”旁的【**Merge**】按钮。
        *   粘贴以下内容并保存：
            ```yaml
            prepend-rules-from:
              - ./my_rules.yaml
            ```

---

#### **第二阶段：引擎搭建 - WSL2 与自动化代理配置**

*此阶段在Windows Terminal中完成，构建Linux核心。*

1.  **安装WSL2与Ubuntu：**
    *   以**管理员身份**打开Windows Terminal，执行 `wsl --install -d Ubuntu-22.04`。
    *   重启后设置Linux用户名和密码。

2.  **回归经典NAT模式：**
    *   **确保 `C:\Users\<YourUsername>\.wslconfig` 文件不存在或内容为空。**

3.  **执行自动化代理配置脚本 (核心步骤)：**
    *   启动WSL2终端 (Ubuntu)。
    *   创建并执行脚本：
        ```bash
        nano ~/configure_proxy_nat.sh
        ```
        
    *   粘贴以下脚本内容进去，然后保存退出: Ctrl+X, Y, Enter
        
        ```bash
        #!/bin/bash
        HOST_IP=$(grep nameserver /etc/resolv.conf | awk '{print $2}')
        PROXY_PORT=7897
        PROXY_HTTP="http://${HOST_IP}:${PROXY_PORT}"
        echo "正在为当前用户配置 .bashrc ..."
        sed -i '/# PROXY-START/,/# PROXY-END/d' ~/.bashrc
        { echo ''; echo '# PROXY-START - NAT Mode Auto-Config'; echo "export http_proxy=\"${PROXY_HTTP}\""; echo "export https_proxy=\"${PROXY_HTTP}\""; echo "export no_proxy=\"localhost,127.0.0.1,*.local\""; echo '# PROXY-END'; } >> ~/.bashrc
        echo "正在为 'apt' 创建代理配置文件..."
        APT_PROXY_CONF_FILE="/etc/apt/apt.conf.d/99proxy.conf"
        echo "Acquire::http::Proxy \"${PROXY_HTTP}\";" | sudo tee ${APT_PROXY_CONF_FILE} > /dev/null
        echo "Acquire::https::Proxy \"${PROXY_HTTP}\";" | sudo tee -a ${APT_PROXY_CONF_FILE} > /dev/null
        echo "经典NAT模式网络配置完成！代理已指向: ${PROXY_HTTP}"
        
        # 赋予权限并执行
        chmod +x ~/configure_proxy_nat.sh
        ~/configure_proxy_nat.sh
        
        # 让配置在当前终端立即生效
        source ~/.bashrc
        ```

---

#### **第三阶段：终端环境终极进化 - Zsh + Oh My Zsh**

*此阶段在WSL2终端内完成，打造顶级的命令行体验。*

1.  **安装Zsh并设为默认Shell：**
    ```bash
    sudo apt install zsh -y
    chsh -s $(which zsh)
    # (需要关闭并重开终端以切换到Zsh)
    ```
2.  **安装Oh My Zsh框架：**
    ```bash
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```
3.  **迁移代理环境变量 (关键风险修复)：**
    ```bash
    sed -n '/# PROXY-START/,/# PROXY-END/p' ~/.bashrc >> ~/.zshrc
    ```
4.  **安装核心插件 (命令建议与语法高亮)：**
    ```bash
    ZSH_CUSTOM=${ZSH_CUSTOM:-~/.oh-my-zsh/custom}
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM}/plugins/zsh-autosuggestions
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM}/plugins/zsh-syntax-highlighting
    ```
5.  **启用插件：**
    *   用`nano ~/.zshrc`打开配置文件。
    *   找到`plugins=(git)`，修改为`plugins=(git zsh-autosuggestions zsh-syntax-highlighting)`。
    *   保存并退出。
6.  **让配置生效：** `source ~/.zshrc`

---

#### **第四阶段：容器、软件源与开发工具链**

*此阶段在WSL2终端内完成，安装所有必要的开发工具。*

1.  **Docker Desktop 集成与加速（wsl2系统不要安装docker，由windows系统安装Docker Desktop 并设置好 wsl 集成即可）：**
    *   **集成：** Docker Desktop -> `Settings` -> `Resources` -> `WSL Integration` -> **开启**对`Ubuntu-22.04`的集成。
    *   **配置阿里云镜像加速**（https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors）
```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "registry-mirrors": [
    "https://vebl37mq.mirror.aliyuncs.com"  # 这个是阿里云用户加速器
  ]
}
```
-  **验证配置是否生效** 在wsl2终端测试
```bash
docker pull hello-world
```


#### **第五阶段：开发环境 - 工具链安装 (WSL2内部)**

*   **配置Apt阿里云镜像源：**
    ```bash
    sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
    sudo sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
    sudo sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
    ```

*   **更新系统并安装基础工具：**
    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y build-essential git git-lfs curl wget python3-pip python3.10-venv python3-virtualenv
    sudo apt install zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev chromium-browser

    ```
*   **配置Git LFS：** `git lfs install`


*   **安装项目环境与包管理器 (`uv`)：**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

*   **安装环境自动激活工具 (`direnv`)：**
    ```bash
    sudo apt install -y direnv
    echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
    ```

*   **配置pip国内源 (由`uv`使用)：**
    ```bash
    # uv会自动读取pip的配置
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
    pip config set install.trusted-host mirrors.aliyun.com
    ```

*   **安装Rust (使用`rustup`，保持不变)：**
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
    ```

*   **常用快捷键**
    ```bash
    alias zo='find ~/ -type f \( -name "*:Zone.Identifier" -o -name "Thumbs.db" \) -delete'
    alias ]=clear
    alias 】=clear
    ```

### **第六阶段：核心依赖 - Isaac Sim 环境准备**

1.  **安装CUDA Toolkit (在WSL2内部)：**
    *   **重要：** 查阅您Isaac Sim版本的官方文档，确定需要的CUDA版本（例如12.2）。
    *   访问 [NVIDIA CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive)。
    *   选择 `Linux` -> `x86_64` -> `WSL-Ubuntu` -> `2.0` -> `deb (network)`。

    ```bash
    # 步骤一：下载并设置CUDA仓库的优先级，确保我们安装的是正确版本
    wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
    sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600

    # 步骤二：下载本地的CUDA仓库定义文件 (.deb)
    wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda-repo-wsl-ubuntu-12-4-local_12.4.1-1_amd64.deb

    # 步骤三：使用dpkg安装该.deb文件，将NVIDIA的本地仓库信息注册到系统中
    sudo dpkg -i cuda-repo-wsl-ubuntu-12-4-local_12.4.1-1_amd64.deb

    # 步骤四：从本地仓库中复制GPG密钥，让系统信任这个仓库
    sudo cp /var/cuda-repo-wsl-ubuntu-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/

    # 步骤五：更新apt的软件包列表，使其包含来自新仓库的CUDA Toolkit信息
    sudo apt-get update

    # 步骤六：正式安装CUDA Toolkit 12.4
    sudo apt-get -y install cuda-toolkit-12-4

    # 验证CUDA编译器
    exec "$SHELL"
    nvcc --version

    # 配置环境变量 (关键！)
    # 将CUDA路径添加到Zsh配置文件中
    echo '' >> ~/.zshrc
    echo '# CUDA Toolkit Paths' >> ~/.zshrc
    echo 'export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}' >> ~/.zshrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.zshrc

    # 立即让配置生效
    source ~/.zshrc
    ```


    *   严格按照官网提供的命令在WSL2终端中完成安装。

2.  **VS Code 无缝集成：**
    *   在Windows上打开VS Code，安装 **`Remote - WSL`** 扩展。
    *   点击左下角绿色图标，选择 `Connect to WSL`。
    *   **完成！** VS Code会自动处理所有路径问题，**无需也绝不应该**手动创建任何符号链接。


#### **步骤七：WSL2系统语言环境优化 (中文化)**

*   **目标：** 为WSL2添加完整的中文语言包支持，并将系统默认区域设置为中文。

*   **行动指令 (在WSL2终端中执行)：**

    1.  **安装中文语言包：**
        ```bash
        sudo apt-get update
        sudo apt-get install -y language-pack-zh-hans
        ```

    2.  **配置系统区域 (Locale)：**
        ```bash
        sudo locale-gen zh_CN.UTF-8
        sudo update-locale LANG=zh_CN.UTF-8
        ```        

    3.  **验证配置：**
        *   **关闭并重新打开**您的Windows Terminal。
        *   在新终端中执行以下命令：
            ```bash
            locale
            ```
        *   您应该能看到类似 `LANG=zh_CN.UTF-8` 的输出，以及其他所有 `LC_*` 变量也都设置为了 `zh_CN.UTF-8`。这意味着系统语言环境已成功切换。

#### **步骤八：系统状态最终检查**

*   **目标：** 确认所有关键组件都处于预期的工作状态。

*   **行动指令 (在WSL2终端中执行)：**

    1.  **网络代理检查：**
        ```bash
        # 检查是否能访问Google，验证代理是否对终端生效
        curl -I https://www.google.com
        
        # 检查是否能访问GitHub，验证自定义直连规则是否生效
        curl -I https://github.com
        ```
        第一个命令应该能快速返回HTTP头信息，第二个也应如此。

    2.  **Python环境检查：**
        ```bash
        python --version
        # 预期输出: Python 3.10.14
        
        pip --version
        # 预期输出: pip from ...python3.10...

        uv --version
        # 预期输出: uv 0.x.x
        ```

    3.  **Docker集成检查：**
        ```bash
        docker --version
        # 预期输出: Docker version ...
        
        docker run hello-world
        # 预期输出: Hello from Docker! ...
        ```

    4.  **CUDA检查：**
        ```bash
        nvcc --version
        # 预期输出: Cuda compilation tools, release 12.4, V12.4.x
        ```

#### **步骤 九：系统稳定性强化 - 根治时钟偏斜**

*   **目标：** 解决WSL2与Windows宿主机的时间差问题，避免编译工具因时间戳错乱而产生不可预知的构建错误。

*   **行动指令 (在WSL2终端中执行)：**

    1.  **安装时间同步工具：**
        ```bash
        sudo apt-get update && sudo apt-get install -y ntpdate
        ```

    2.  **配置WSL启动时自动同步：**
        ```bash
        echo -e '[boot]\ncommand = "ntpdate time.windows.com"' | sudo tee /etc/wsl.conf
        ```

    3.  **使配置生效：**
        *   在**管理员权限的PowerShell**中执行 `wsl --shutdown`。
        *   重新启动WSL终端即可。此后，时钟将自动同步。

---

这份最终版的《开荒蓝图》是您个人经验与业界最佳实践的完美结合。它逻辑严谨、步骤清晰、无任何信息遗漏，将是您未来在任何机器上都能精确复刻这套顶级开发环境的权威指南。





