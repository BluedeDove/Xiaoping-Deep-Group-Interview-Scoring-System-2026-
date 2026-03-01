"""
右栏：雷达图组件
"""

import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class RadarChart(FigureCanvas):
    """雷达图组件"""

    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111, polar=True)
        super().__init__(self.fig)
        self.setParent(parent)

        # 维度标签
        self.labels = ['代码', '架构', '数理', '可视', '综合']
        self.num_vars = len(self.labels)

        # 计算角度
        self.angles = np.linspace(0, 2 * np.pi, self.num_vars, endpoint=False).tolist()
        self.angles += self.angles[:1]  # 闭合

        # 初始化空数据
        self.update_data([0, 0, 0, 0, 0])

    def update_data(self, scores: list):
        """
        更新雷达图数据

        Args:
            scores: [代码, 架构, 数理, 可视, 综合] 五个维度的分数
        """
        self.ax.clear()

        # 数据闭合
        values = scores + scores[:1]

        # 绘制雷达图
        self.ax.plot(self.angles, values, 'o-', linewidth=2, color='#2196F3', label='能力值')
        self.ax.fill(self.angles, values, alpha=0.25, color='#2196F3')

        # 设置刻度标签
        self.ax.set_xticks(self.angles[:-1])
        self.ax.set_xticklabels(self.labels, fontsize=11)

        # 设置径向刻度
        self.ax.set_ylim(0, 10)
        self.ax.set_yticks([2, 4, 6, 8, 10])
        self.ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8)

        # 添加网格
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # 在每个点上标注数值
        for angle, value, label in zip(self.angles[:-1], scores, self.labels):
            self.ax.text(angle, value + 0.5, f'{value:.1f}',
                        ha='center', va='center', fontsize=9, fontweight='bold')

        self.fig.tight_layout()
        self.draw()


class RadarChartWidget(QWidget):
    """雷达图包装组件（包含标题等）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.chart = RadarChart()
        layout.addWidget(self.chart)

    def update_scores(self, code: float, arch: float, math: float, viz: float, overall: float = None):
        """
        更新雷达图分数

        Args:
            code: 代码维度分数
            arch: 架构维度分数
            math: 数理维度分数
            viz: 可视化维度分数
            overall: 综合分数（可选，默认可视化分数）
        """
        if overall is None:
            overall = (code + arch + math + viz) / 4

        scores = [code, arch, math, viz, overall]
        self.chart.update_data(scores)
