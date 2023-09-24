import glm
from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions, delay_until, omen_color
from ff_draw.gui.text import TextPosition
from ff_draw.plugins import FFDrawPlugin
from ff_draw import mem as memm
map_ex = raid_utils.MapTrigger.get(1141)


#更新日志
#1、四风调色，冰刀调色
#2、增加一陨2穿1无损安全点位
is_enable = map_ex.add_value(raid_utils.BoolCheckBox('四风调色，冰刀调色 By Chany/enable', True))
map_ex.decorators.append(lambda f: (lambda *args, **kwargs: f(*args, **kwargs) if is_enable.value else None))
_冰刀 = [33889]
_风球 = [33880, 33881, 33882, 33883]
冰刀填充颜色 = glm.vec4(0.0, 0.2, 1.0, .5)
风球填充颜色 = glm.vec4(0.0, 0.2, 1.0, .5)
冰刀边缘线颜色 = glm.vec4(1.0, 1.0, 1.0, 1.0)
近战贪刀点 = glm.vec4(0, 1, 0, .3)
第一次陨石是否结束 = 0
for _a in _冰刀:
    omen_color[_a] = 冰刀填充颜色, 冰刀边缘线颜色
     
#四风调色
#四风顺序    
omen_color[33880] = glm.vec4(1, 0, 0, .7), glm.vec4(1.0, 1.0, 1.0, .7)
omen_color[33881] = glm.vec4(1, 0, 0, .5), glm.vec4(1.0, 1.0, 1.0, .7)
omen_color[33882] = glm.vec4(1, 0, 0, .4), glm.vec4(1.0, 1.0, 1.0, .7)
omen_color[33883] = glm.vec4(1, 0, 0, .7), glm.vec4(1.0, 1.0, 1.0, .7)

@map_ex.on_cast(33880, 33881, 33882, 33883)
def on_cast_radial_flagration(evt: 'NetworkMessage[zone_server.ActorCast]'):
    raid_utils.sleep(evt.message.cast_time - 4)
    cast_time = min(evt.message.cast_time, 4)
    source = raid_utils.NActor.by_id(evt.header.source_id)

    def _draw(actor: raid_utils.NActor):
        return raid_utils.draw_rect(
            width=3, length=3,
            pos=source,
            #facing=lambda _: glm.polar(actor.update().pos - source.update().pos).y,
            duration=evt.message.cast_time,
            line_color=冰刀边缘线颜色,
            surface_color=冰刀填充颜色
        )

    _draw(source)
    
@map_ex.on_reset
def clean_all_triggermsg(ect):
    global 第一次陨石是否结束
    print("CColourful Draw: 任务已重置")
    第一次陨石是否结束 = 0
@map_ex.on_cast(33956)
def on_cast_radial_flagration(evt: 'NetworkMessage[zone_server.ActorCast]'):
    global 第一次陨石是否结束
    raid_utils.sleep(evt.message.cast_time - 4)
    cast_time = min(evt.message.cast_time, 2)
    source = raid_utils.NActor.by_id(evt.header.source_id)
    第一次陨石是否结束 += 1
    #print(第一次陨石是否结束)
    def _draw(actor: raid_utils.NActor):
        global 第一次陨石是否结束
        positions = [
            glm.vec3(100, 0, 107),
            glm.vec3(100, 0, 108.8),
            glm.vec3(100, 0, 93),
            glm.vec3(100, 0, 91.3)            
        ]

        for pos in positions:
            if 第一次陨石是否结束 == 1:
                raid_utils.draw_circle(
                    radius=0.3,
                    pos=pos,
                    line_color=冰刀边缘线颜色,
                    surface_color=近战贪刀点,
                    duration=12
                )
    _draw(source)
map_ex.clear_decorators()