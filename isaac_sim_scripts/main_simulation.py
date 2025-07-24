# isaac_sim_scripts/main_simulation.py (V41 - FINAL GOLDEN STANDARD)

import carb
import sys

# 1. SimulationApp 是启动一切的根源
CONFIG = {"headless": False}
from isaacsim import SimulationApp
simulation_app = SimulationApp(CONFIG)

# 2. 在 SimulationApp 实例化后，安全地导入所有其他模块
import omni.graph.core as og
from isaacsim.core.api import World
from isaacsim.core.utils import extensions
from managers.scene_manager import SceneManager
from managers.controller_manager import ControllerManager

# -----------------------------------------------------------------------------
# 主程序逻辑
# -----------------------------------------------------------------------------
def main():
    """自动化仿真的主函数，负责协调各个模块。"""
    try:
        # a. 严格使用官方 Extensions API 列表中的正确扩展ID
        extensions.enable_extension("isaacsim.ros2.bridge")
        extensions.enable_extension("isaacsim.core.nodes")

        # b. 让应用先空跑几帧，确保所有扩展完成内部注册
        for _ in range(5):
            simulation_app.update()
        
        # c. 创建 World 实例
        world = World()
        
        # d. 搭建场景
        scene_manager = SceneManager()
        scene_manager.setup_scene(world)
        
        # e. 在 main 函数的上下文中，直接创建 OmniGraph
        controller_manager = ControllerManager(robot_prim_path=scene_manager.drone_prim_path)
        graph_spec, edit_commands = controller_manager.get_ros_control_graph_spec()
        
        og.Controller.edit(graph_spec, edit_commands)
        
        # f. 重置世界并初始化机器人
        world.reset()
        
        scene_manager.drone_robot.initialize()
        
        print("\n" + "="*50)
        print("【里程碑达成】 最终模块化架构加载成功！")
        print("【下一步行动】 请在另一个 WSL2 终端中启动 ROS 2 控制节点。")
        print("                 观察无人机是否起飞。")
        print("="*50 + "\n")

        # g. 进入仿真循环
        while simulation_app.is_running():
            world.step(render=True)

    except Exception as e:
        carb.log_error(f"主程序发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        simulation_app.close()

# 脚本主入口
if __name__ == "__main__":
    main()