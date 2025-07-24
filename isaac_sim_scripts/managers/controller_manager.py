# isaac_sim_scripts/managers/controller_manager.py (V41 - FINAL GOLDEN STANDARD)

class ControllerManager:
    """负责为机器人定义控制器配置。"""
    def __init__(self, robot_prim_path: str):
        self.robot_prim_path = robot_prim_path

    def get_ros_control_graph_spec(self) -> dict:
        """返回用于创建ROS 2 Twist控制图的OmniGraph配置字典。"""
        import omni.graph.core as og
        
        # 【最终黄金标准】根据所有API迁移模式，这必须是正确的节点ID
        subscribe_twist_node_type = "isaacsim.ros2_bridge.ROS2SubscribeTwist"
        scale_node_type = "isaacsim.core.nodes.OgnIsaacScaleToFromStageUnit"
        articulation_controller_node_type = "isaacsim.core.nodes.IsaacArticulationController"
        
        graph_spec = {
            "graph_path": f"{self.robot_prim_path}/ROS_Control_Graph",
            "evaluator_name": "execution"
        }
        
        edit_commands = {
            og.Controller.Keys.CREATE_NODES: [
                ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
                ("ROS2Context", "isaacsim.ros2.bridge.ROS2Context"),
                ("SubscribeTwist", subscribe_twist_node_type),
                ("ScaleToFromStage", scale_node_type),
                ("ArticulationController", articulation_controller_node_type),
            ],
            og.Controller.Keys.CONNECT: [
                ("OnPlaybackTick.outputs:tick", "SubscribeTwist.inputs:execIn"),
                ("OnPlaybackTick.outputs:tick", "ArticulationController.inputs:execIn"),
                ("ROS2Context.outputs:context", "SubscribeTwist.inputs:context"),
                ("SubscribeTwist.outputs:linearVelocity", "ScaleToFromStage.inputs:value"),
                ("ScaleToFromStage.outputs:value", "ArticulationController.inputs:velocityCommand"),
            ],
            og.Controller.Keys.SET_VALUES: [
                ("ROS2Context.inputs:domain_id", 0),
                ("SubscribeTwist.inputs:topicName", "/cmd_vel"),
                ("ArticulationController.inputs:usePath", True),
                ("ArticulationController.inputs:robotPath", self.robot_prim_path),
            ],
        }
        
        return graph_spec, edit_commands