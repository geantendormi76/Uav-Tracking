# isaac_sim_scripts/managers/scene_manager.py

import carb
import os
import sys
import numpy as np
from isaacsim.core.api import World
from isaacsim.core.utils import stage
from isaacsim.core.utils.nucleus import get_assets_root_path
from isaacsim.core.prims import SingleArticulation

class SceneManager:
    """负责搭建和管理仿真场景中的所有资产。"""
    def __init__(self):
        self.assets_root_path = get_assets_root_path()
        if self.assets_root_path is None:
            carb.log_error("未能获取到资产根目录。")
            sys.exit(1)
        carb.log_info(f"成功获取到资产根目录: {self.assets_root_path}")
        
        self.drone_robot = None
        self.drone_prim_path = "/World/Crazyflie"

    def setup_scene(self, world: World):
        """搭建基础场景：地面和无人机。"""
        ground_plane_prim_path = "/World/ground_plane"
        crazyflie_usd_path = f"{self.assets_root_path}/Isaac/Robots/Crazyflie/cf2x.usd"
        
        if not os.path.exists(crazyflie_usd_path):
            carb.log_error(f"Crazyflie USD 文件未找到：{crazyflie_usd_path}")
            sys.exit(1)

        world.scene.add_default_ground_plane(prim_path=ground_plane_prim_path)
        stage.add_reference_to_stage(usd_path=crazyflie_usd_path, prim_path=self.drone_prim_path)
        
        self.drone_robot = world.scene.add(
            SingleArticulation(
                prim_path=self.drone_prim_path,
                name="crazyflie_drone",
                position=np.array([0, 0, 1.0])
            )
        )
        carb.log_info(f"场景搭建完成: 地面和无人机已加载。")