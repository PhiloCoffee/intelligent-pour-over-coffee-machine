# Buglog for ECE445 Coffee System

## Servo Motor: PWM 输出
王杰
2024年5月4日

1. **Raspberry Pi 5 doesn't support the RPi.GPIO library**
- 从GPIO 迁移到gpiozero: https://gpiozero.readthedocs.io/en/stable/migrating_from_rpigpio.html
- 树莓派入门： https://blog.csdn.net/Naisu_kun/article/details/105288110
- SOC address 错误成因：
    - 官方论坛：不支持，https://forums.raspberrypi.com/viewtopic.php?t=361218
    - 一个很棒的reddit post, 解释了硬件库不支持的情况怎么办https://www.reddit.com/r/RASPBERRY_PI_PROJECTS/comments/188yynn/im_having_soc_problems_in_rpigpio_library_can_any/
        - 本质上是python & python3 两个冲突，然后硬件层面有bug
        - 似乎更换到32bit system 可以解决这个问题，不过还是算了

**最终：** https://gpiozero.readthedocs.io/en/latest/api_output.html#gpiozero.Servo