import sys

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import Parallel
from direct.interval.IntervalGlobal import LerpPosHprInterval
from direct.interval.IntervalGlobal import LerpFunc
from direct.interval.IntervalGlobal import SoundInterval

from panda3d.core import AntialiasAttrib
from panda3d.core import Shader
from panda3d.core import Vec3

from pathlib import Path


asset_path = Path(__file__).parents[1] / 'assets' 


class RainbowSplash:
    def __init__(self):
        pass

    def setup(self):
        base.win.set_clear_color((0,0,0,1))
        cam_dist = 2
        base.cam.set_pos(0, -2.2 * cam_dist, 0)
        base.cam.node().get_lens().set_fov(45/cam_dist)

        self.logo_animation = Actor(asset_path / "panda3d_logo.bam")
        self.logo_animation.reparent_to(render)
        self.logo_animation.set_two_sided(True)

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex=asset_path / "panda3d_logo.vert",
            fragment=asset_path / "panda3d_logo.frag",
        )
        self.logo_animation.set_shader(shader)
        self.logo_animation.set_shader_input("fade", 0.0)
        self.logo_sound = base.loader.loadSfx(asset_path / "panda3d_logo.wav")

        # Build interval
        def shader_time(t):
            self.logo_animation.set_shader_input("time", t)
        def add_antialiasing(t):
            render.set_antialias(AntialiasAttrib.MMultisample)
        def fade_background_to_white(t):
            base.win.set_clear_color((t,t,t,1))
            self.logo_animation.set_shader_input("time", t/3.878)
            self.logo_animation.set_shader_input("fade", t)
        effects = Parallel(
            self.logo_animation.actorInterval(
                "splash",
                loop=False,
            ),
            SoundInterval(
                self.logo_sound,
                loop=False,
            ),
            Sequence(
                LerpFunc(
                    shader_time,
                    fromData=0,
                    toData=1,
                    duration=3.878,
                ),
                LerpFunc(
                    add_antialiasing,
                    fromData=0,
                    toData=1,
                    duration=0,
                ),
                LerpFunc(
                    fade_background_to_white,
                    fromData=0,
                    toData=1,
                    duration=1.0,
                ),
            ),
        )
        return effects

    def teardown(self):
        self.logo_animation.cleanup()
        # FIXME: Destroy self.logo_sound
