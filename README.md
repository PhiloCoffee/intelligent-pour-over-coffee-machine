# ECE445/ME470: Intelligent Pour-Over Coffee Machine
> Team #15: Intelligent Coffee Team © PhiloCoffee Club

- System Architecter: Jie Wang
- Program Manager: Jingyuan Huang
- Mechanical Architecter: Qiuxubin
- Financial Analyst: Rucheng Ke

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

## TODO:
1. Open source the mech design as well. 
2. Demo video and gif for the project
3. Project website construction
