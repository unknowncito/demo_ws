#!/usr/bin/env python3
 
import time
import json
import sys
import tty
import termios
import threading
import websocket
import rospy
 
WS_URL = "ws://localhost:8765"
 
 
# Map keyboard keys to velocities
key_to_cmd = {
    "w": (0.5, 0.0),
    "s": (-0.5, 0.0),
    "a": (0.0, 0.7),
    "d": (0.0, -0.7),
    "x": (0.0, 0.0),
}
 
 
##  not my code straight up claude
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
 
    try:
        tty.setcbreak(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
 
    return key.lower()
 
 
def run(ws_url: str) -> None:
    rospy.init_node("ws_server")
    # list so nested callbacks/threads can mutate
    ws_ref = [None]
 
    # by teyema
    def send_cmd(linear, angular):
        ws = ws_ref[0]
 
        if ws is None:
            rospy.logwarn("WebSocket not connected.")
            return
 
        payload = {
            "type": "cmd_vel",
            "data": {
                "linear": linear,
                "angular": angular
            }
        }
 
        try:
            ws.send(json.dumps(payload))
        except Exception as e:
            rospy.logerr(f"Failed to send command: {e}")
 
    def on_error(ws, error):
        rospy.logerr(f"WebSocket error: {error}")
 
    def on_close(ws, close_status_code, close_msg):
        rospy.logwarn(f"WebSocket closed ({close_status_code}): {close_msg}")
 
    def on_open(ws):
        rospy.loginfo(f"WebSocket connected to {ws_url}")
 
    def ws_thread():
        while not rospy.is_shutdown():
            try:
                ws = websocket.WebSocketApp(
                    ws_url,
                    on_error=on_error,
                    on_close=on_close,
                    on_open=on_open,
                )
                ws_ref[0] = ws
                ws.run_forever(ping_interval=20, ping_timeout=10)
            except Exception as e:
                rospy.logerr(f"WebSocket exception: {e}")
            if not rospy.is_shutdown():
                rospy.loginfo("WebSocket reconnecting in 3s...")
                time.sleep(3)
 
    # Run WebSocket in background thread, keyboard loop on main thread
    t = threading.Thread(target=ws_thread, daemon=True)
    t.start()
 
    rospy.loginfo("WASD keyboard controller started.")
    rospy.loginfo("W = Forward | S = Backward")
    rospy.loginfo("A = Left | D = Right")
    rospy.loginfo("X = Stop | Q = Quit")
 
    try:
        while not rospy.is_shutdown():
 
            key = get_key()
 
            if key == "q":
                break
 
            linear, angular = key_to_cmd.get(
                key, (0.0, 0.0)
            )
 
            send_cmd(linear, angular)
 
    except KeyboardInterrupt:
        pass
 
    finally:
        send_cmd(0.0, 0.0)
        rospy.loginfo("Stopping robot...")
        rospy.signal_shutdown("Keyboard controller stopped")
 
 
if __name__ == "__main__":
    try:
        run(WS_URL)
    except KeyboardInterrupt:
        print("\nStopped.")
