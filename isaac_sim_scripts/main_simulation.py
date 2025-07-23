# Uav-Tracking/isaac_sim_scripts/main_simulation.py (V17 - Final Integration of All Verified Components)

import carb
import asyncio
import omni.kit.app
import numpy as np

# --- 导入所有经过验证的、正确的模块 ---
from omni.isaac.core import World
from omni.isaac.core.utils import extensions
from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.core.prims import Articulation
from omni.isaac.core.utils.nucleus import get_assets_root_path
from isaacsim.core.api.objects import FixedCuboid

# -----------------------------------------------------------------------------
# 我们的核心场景搭建逻辑
# -----------------------------------------------------------------------------
async def setup_scene_logic():
    # 等待一帧，确保所有内容准备就绪
    await omni.kit.app.get_app().next_update_async()
    
    world = World() 
    
    # a. 添加地面
    world.scene.add_default_ground_plane(prim_path="/World/ground_plane", z_position=0)

    # b. 加载无人机
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        carb.log_error("Could not find Isaac Sim assets folder.")
        return
        
    drone_usd_path = assets_root_path + "/Isaac/Robots/Crazyflie/cf2x.usd"
    drone_prim_path = "/World/Crazyflie"
    
    add_reference_to_stage(usd_path=drone_usd_path, prim_path=drone_prim_path)
    
    drone_robot = world.scene.add(
        Articulation(
            prim_path=drone_prim_path,
            name="crazyflie_drone",
            position=np.array([0, 0, 1.0])
        )
    )

    # c. 启用ROS 2桥接
    extensions.enable_extension("omni.isaac.ros2.bridge")
    
    # d. 重置世界以应用所有更改并初始化物理
    await world.reset_async()
    
    # e. 在重置后初始化机器人
    if drone_robot:
        drone_robot.initialize()

    print("\n[SUCCESS] Scene setup complete via StartupHandler.")
    print("Press PLAY to start simulation and send ROS 2 commands.\n")

# -----------------------------------------------------------------------------
# 【经过验证的自启动框架】
# -----------------------------------------------------------------------------
class StartupHandler:
    def __init__(self):
        self.subscription = None
    def on_update(self, e: carb.events.IEvent):
        if omni.kit.app.get_app().is_app_ready():
            asyncio.ensure_future(setup_scene_logic())
            if self.subscription:
                self.subscription.unsubscribe()
                self.subscription = None

# --- 脚本主入口 ---
handler = StartupHandler()
update_stream = omni.kit.app.get_app().get_update_event_stream()
handler.subscription = update_stream.create_subscription_to_pop(handler.on_update, name="uav_tracking_startup")