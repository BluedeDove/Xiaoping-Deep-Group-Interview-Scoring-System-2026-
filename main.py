"""
面试评分系统 - 程序入口

基于 PyQt6 + Matplotlib 的桌面评分工具
供面试官在现场答辩时使用
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.main_window import MainWindow


def main():
    """程序入口"""
    # 启用高分屏支持 - 兼容 1080p 到 4K 各种分辨率
    # PyQt6 默认启用高分屏支持，使用 PassThrough 策略让系统控制缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("面试评分系统")
    app.setApplicationVersion("1.0.0")

    # 设置全局字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
