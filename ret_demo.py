import time
from avp_stream import VisionProStreamer

from orca_core import OrcaHand
from orca_retargeter.retargeter import Retargeter

### NOTE: Please double check these paths

# MODEL_PATH = "/home/kywch/workspace/orca_core/orca_core/models/orcahand_v1_left"
MODEL_PATH = "/home/kywch/workspace/orca_core/orca_core/models/orcahand_v1_right"

avp_ip = "172.30.1.61"

hand = OrcaHand(MODEL_PATH)
status = hand.connect()
print(status)
# hand.calibrate()

retargeter = Retargeter(MODEL_PATH)

print("Retargeter initialized...")

s = VisionProStreamer(ip = avp_ip, record = True)

time.sleep(5)

which_hand = "right" if "right" in MODEL_PATH else "left"
wrist_offset = 40 if which_hand == "left" else 0

while True:
    r = s.latest
    joint_angles, _ = retargeter.retarget(r, hand=which_hand)

    joint_angles['thumb_abd'] = joint_angles['thumb_abd'] + 10
    joint_angles['thumb_mcp'] = joint_angles['thumb_mcp'] 

    joint_angles['wrist'] = joint_angles['wrist'] + wrist_offset
    #joint_angles['wrist'] = -20.0

    hand.set_joint_pos(joint_angles) 

    
#hand.calibrate()

hand.set_joint_pos({'wrist': -20.0})

# Set the desired joint positions to 0
# hand.set_joint_pos({joint: 0 for joint in hand.joint_ids})

