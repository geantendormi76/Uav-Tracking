# Uav-Tracking/isaac_sim_scripts/main_simulation.py (V27 - Golden Standard with Correct Variable Scope)

import carb
import os
import sys
import time

# 1. SimulationApp 是启动一切的根源
CONFIG = {"headless": False}
from isaacsim import SimulationApp
simulation_app = SimulationApp(CONFIG)

# 2. 导入所有需要的模块
from isaacsim.core.api import World
from isaacsim.core.utils import extensions, stage
from isaacsim.core.utils.nucleus import get_assets_root_path
from isaacsim.core.prims import SingleArticulation
import numpy as np

# 3. 主程序逻辑
def main():
    """自动化仿真的主函数"""
    # 核心修正：将所有配置变量的定义移入 main 函数的作用域内
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        carb.log_error("未能获取到资产根目录。")
        sys.exit(1)
    
    carb.log_info(f"成功获取到资产根目录: {assets_root_path}")

    crazyflie_usd_path = f"{assets_root_path}/Isaac/Robots/Crazyflie/cf2x.usd"
    crazyflie_prim_path = "/World/Crazyflie"
    ground_plane_prim_path = "/World/ground_plane"

    # 现在，函数内的所有代码都可以直接访问这些局部变量
    try:
        if not os.path.exists(crazyflie_usd_path):
            carb.log_error(f"Crazyflie USD 文件在动态路径下未找到：{crazyflie_usd_path}")
            sys.exit(1)

        extensions.enable_extension("isaacsim.ros2.bridge")
        
        world = World()
        
        world.scene.add_default_ground_plane(prim_path=ground_plane_prim_path)
        stage.add_reference_to_stage(usd_path=crazyflie_usd_path, prim_path=crazyflie_prim_path)
        
        crazyflie_robot = world.scene.add(
            SingleArticulation(
                prim_path=crazyflie_prim_path,
                name="crazyflie_drone",
                position=np.array([0, 0, 1.0])
            )
        )
        
        world.reset()

        crazyflie_robot.initialize()
        carb.log_info(f"Crazyflie 关节已初始化。自由度数量: {crazyflie_robot.num_dof}")

        print("\n" + "="*50)
        print("【里程碑达成】 自动化场景加载成功！")
        print("【下一步行动】 请在另一个 WSL2 终端中启动 ROS 2 控制节点。")
        print("                 仿真将持续运行，按 Ctrl+C 关闭此终端以结束。")
        print("="*50 + "\n")

        while simulation_app.is_running():
            world.step(render=True)

    except Exception as e:
        carb.log_error(f"主程序发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        simulation_app.close()

# 4. 脚本主入口
if __name__ == "__main__":
    main()