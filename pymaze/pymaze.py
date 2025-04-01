from direct.showbase.ShowBase import ShowBase
from panda3d.core import LVector3, CardMaker, ClockObject, loadPrcFileData

loadPrcFileData("", "audio-library-name null")  # no audio
loadPrcFileData("", "load-display tinydisplay")  # software rendering
loadPrcFileData("", "input-device-configuration false")


# Get global clock for frame time updates
globalClock = ClockObject.get_global_clock()


class MazeGame(ShowBase):
    def __init__(self):
        super().__init__()

        # Create a simple flat plane as the ground
        ground = CardMaker("ground")
        ground.set_frame(-10, 10, -10, 10)
        ground_node = self.render.attach_new_node(ground.generate())
        ground_node.set_p(-90)
        ground_node.set_scale(10)

        # Set initial camera position
        self.camera.set_pos(0, -5, 2)  # Start behind the center
        self.camera.look_at(0, 0, 0)  # Look towards the center

        # Movement Variables
        self.movement = {
            "forward": 0,
            "backward": 0,
            "left": 0,
            "right": 0,
            "turn_left": 0,
            "turn_right": 0,
        }
        self.speed = 5
        self.turn_speed = 50

        # Key bindings
        self.accept("w", self.set_movement, ["forward", 1])
        self.accept("w-up", self.set_movement, ["forward", 0])
        self.accept("s", self.set_movement, ["backward", 1])
        self.accept("s-up", self.set_movement, ["backward", 0])
        self.accept("a", self.set_movement, ["left", 1])
        self.accept("a-up", self.set_movement, ["left", 0])
        self.accept("d", self.set_movement, ["right", 1])
        self.accept("d-up", self.set_movement, ["right", 0])
        self.accept("q", self.set_movement, ["turn_left", 1])
        self.accept("q-up", self.set_movement, ["turn_left", 0])
        self.accept("e", self.set_movement, ["turn_right", 1])
        self.accept("e-up", self.set_movement, ["turn_right", 0])

        # Update movement every frame
        self.taskMgr.add(self.update_movement, "update_movement")

    def set_movement(self, key, value):
        self.movement[key] = value

    def update_movement(self, task):
        dt = globalClock.get_dt()

        # Get current position and direction
        pos = self.camera.get_pos()
        h = self.camera.get_h()
        direction = LVector3(0, 1, 0).rotated_around(LVector3.up(), h)

        # Apply movement
        if self.movement["forward"]:
            pos += direction * self.speed * dt
        if self.movement["backward"]:
            pos -= direction * self.speed * dt
        if self.movement["left"]:
            pos -= direction.cross(LVector3.up()) * self.speed * dt
        if self.movement["right"]:
            pos += direction.cross(LVector3.up()) * self.speed * dt
        if self.movement["turn_left"]:
            self.camera.set_h(h + self.turn_speed * dt)
        if self.movement["turn_right"]:
            self.camera.set_h(h - self.turn_speed * dt)

        self.camera.set_pos(pos)

        return task.cont


if __name__ == "__main__":
    game = MazeGame()


def start():
    MazeGame()
