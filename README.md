# ECE445/ME470: Intelligent Pour-Over Coffee Machine
> Team #15: Intelligent Coffee Team © PhiloCoffee Club

## coffee_system
Python-based control system for the senior design project


```python
smart_coffee_machine/
│
├── main.py               # 主控制脚本，程序入口
│
├── fsm.py                # 咖啡机操作系统，有限状态机维护用户交互程序
│
├── coffee.py             # 咖啡冲煮配置程序，自定义编程浅烘深烘方案
│
├── config.py             # 配置文件，包含设定参数如温度阈值、GPIO口等
│
├── hardware/             # 硬件控制模块
│   ├── __init__.py       # 初始化脚本，用于硬件模块导入
│   ├── sensor.py         # 传感器管理模块，如重量传感器
│   ├── pump.py           # 水泵驱动模块    
│   ├── motor.py          # 齿轮电机和舵机驱动模块
│   ├── servo_dict.json   # 舵机驱动值-角度对应字典
│   ├── display.py        # OLED 及四位数码管显示屏驱动模块
│   ├── led.py            # 四位LED数码管显示屏驱动模块
│   └── hx711_pi5.py      # 适用于Pi 5的HX711测压元件接口的自定驱动程序
│
├── utilities/            # 工具模块
│   ├── __init__.py       # 初始化脚本，用于工具模块导入
│   ├── logger.py         # 日志管理工具，用于记录系统日志
│   └── timer.py          # 定时器工具，用于处理时间相关的功能
│
└── communication/        # 通信模块(预留接口)
    ├── __init__.py       # 初始化脚本，用于通信模块导入
    ├── server.py         # 网络服务器模块，处理外部命令
    ├── chatgpt.py        # GPT agent 预留文件，用于更高级的HCI交互
    └── protocol.py       # 通信协议模块，定义数据交换格式和协议
```




## Todo List: 
1. Set up terminal right click 
(open terminal here, find it in the offical document)
2. Set up SSH. DON'T ASK GPT, find it out by Y2B / bilibili video 
& official doc
3. Set up the GPIO Program:
- [x] LED blink, same as lab 7 
- [x] timer 
- [x] display, OLED 
- [x] display, 4-digit
    - [X] 增加小数点

- [x] USER IO: terminal simulate the whole using process, 
without any hardware (first)

Jie Wang: take care of the electronic part
1. Servo Motor setup
- [x] Code
- [x] Mech setup 


## Final Week

- [x]  pump 电控代码 30min
    - [x]  测试pump 流速 30min
    - [x]  需求：电压变速 1h
    - [x]  数字电位计可以通过I2C或SPI通信协议与树莓派通信，实现类似传统滑动变阻器的功能，但其优点是可以通过软件控制。
    - **数字电位计**：比如AD5206或MCP4131。
    - **适配板**：以方便与树莓派的接口连接。
- [x]  motor 电控代码 30 min
    - [x]  需求：时间，力度控制
    - [x]  需求: 能正反转
    - [x]  确定电路设计
    - [x]  [树莓派4B|控制一路继电器，控制直流电机正反转（帮助自己记忆）_1路继电器控制直流电机csdn-CSDN博客](https://blog.csdn.net/abcde123qw123/article/details/114643980)
- [x]  servo 最终版代码
    - [x]  测试需要的差值dict
    - [x]  https://chat.openai.com/share/dd1c0a9b-0165-4884-93d3-91bdc7226a7d
- [x]  用户提示流程的文字
- [x]  咖啡冲煮方案的固定（找mzc 问冲煮流程）：
    - [x]  light roast
    - [x]  dark roast
    - [x]  hot water
    - [x]  bean-water-ratio 计算代码 func
- [x]  电源组装到一起
    - [x]  PCB?
    - [x]  测试FSM ： 从亮灯到亮电机
    
    耗时很长的程序忘加nohup就运行了怎么办？ - ipid君的回答 - 知乎
    https://www.zhihu.com/question/586298694/answer/2991647868
    
- [x]  固定整个工程的基座
    - [x]  固定各个UserIO 接口的位置

- [x]  写final report ： 成败和经验教训