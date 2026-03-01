"""
中栏：评分输入网格
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGroupBox, QPushButton, QGridLayout, QMessageBox, QSpinBox,
    QSizePolicy, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from data.questions import get_question, Question, DimensionCriteria


class DimensionInput(QWidget):
    """单个维度的输入组件"""

    def __init__(self, name: str, criteria: DimensionCriteria, parent=None):
        super().__init__(parent)
        self.name = name
        self.criteria = criteria
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(12)

        # 维度名称 - 使用最小宽度而非固定宽度，允许自适应
        name_label = QLabel(self.name)
        name_label.setMinimumWidth(45)
        name_label.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.Preferred
        )
        name_label.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
        layout.addWidget(name_label)

        # 分数输入 - 使用弹性尺寸，兼容各种 DPI
        self.score_input = QSpinBox()
        self.score_input.setRange(0, 10)
        self.score_input.setValue(0)
        # 使用最小尺寸而非固定尺寸，让 Qt 根据 DPI 自动调整
        self.score_input.setMinimumWidth(80)
        self.score_input.setMinimumHeight(32)
        self.score_input.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.Fixed
        )
        self.score_input.setFont(QFont("Microsoft YaHei", 10))
        self.score_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_input.setToolTip("输入0-10分")
        # 更大的调节按钮尺寸，确保在高 DPI 下可点击
        self.score_input.setStyleSheet("""
            QSpinBox {
                padding: 4px 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QSpinBox:focus {
                border: 1px solid #2196F3;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 22px;
                height: 14px;
                border-left: 1px solid #cccccc;
                background-color: #f5f5f5;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e0e0e0;
            }
            QSpinBox::up-button {
                border-top-right-radius: 3px;
            }
            QSpinBox::down-button {
                border-bottom-right-radius: 3px;
            }
            QSpinBox::up-arrow {
                width: 10px;
                height: 6px;
            }
            QSpinBox::down-arrow {
                width: 10px;
                height: 6px;
            }
        """)
        layout.addWidget(self.score_input)

        # 帮助按钮 - 使用最小尺寸
        help_btn = QPushButton("?")
        help_btn.setMinimumSize(26, 26)
        help_btn.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        help_btn.setFont(QFont("Microsoft YaHei", 9))
        help_btn.setToolTip("点击查看详细标准")
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        help_btn.clicked.connect(self.show_criteria)
        layout.addWidget(help_btn)

        layout.addStretch()

    def show_criteria(self):
        """显示详细标准对话框"""
        items_text = "\n".join([f"  - {item}" for item in self.criteria.check_items])
        QMessageBox.information(
            self,
            f"{self.name}维度评分标准",
            f"【检查项】\n{items_text}"
        )

    def get_score(self) -> int:
        """获取输入的分数"""
        return self.score_input.value()

    def set_score(self, score: int):
        """设置分数"""
        self.score_input.setValue(score)

    def clear(self):
        """清空输入"""
        self.score_input.setValue(0)


class LevelScoreGroup(QGroupBox):
    """单个层级的评分组"""

    scores_changed = pyqtSignal()

    def __init__(self, level: int, weight: float, question: Question, parent=None):
        super().__init__(parent)
        self.level = level
        self.weight = weight
        self.question = question
        self.dimension_inputs = {}
        self.setup_ui()

    def setup_ui(self):
        level_names = {1: "青铜", 2: "白银", 3: "黄金", 4: "王者"}
        self.setTitle(f"L{self.level} {level_names.get(self.level)} ×{self.weight}")

        # 设置样式
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        # 获取当前层级的标准
        criteria = self.question.levels.get(self.level)
        if not criteria:
            return

        # 创建四个维度的输入
        # (显示名称, 英文key, 标准数据)
        dimensions = [
            ("代码", "code", criteria.code),
            ("架构", "arch", criteria.arch),
            ("数理", "math", criteria.math),
            ("可视", "viz", criteria.viz)
        ]

        for dim_name, dim_key, dim_criteria in dimensions:
            dim_input = DimensionInput(dim_name, dim_criteria)
            dim_input.score_input.valueChanged.connect(self.scores_changed.emit)
            self.dimension_inputs[dim_key] = dim_input
            layout.addWidget(dim_input)

    def get_scores(self) -> dict:
        """获取当前层级的所有分数"""
        return {
            name: input_widget.get_score()
            for name, input_widget in self.dimension_inputs.items()
        }

    def clear(self):
        """清空所有输入"""
        for input_widget in self.dimension_inputs.values():
            input_widget.clear()


class ScoreInputGrid(QWidget):
    """评分输入网格（中栏）"""

    scores_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_question = None
        self.level_groups = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # 学生信息区域
        info_group = QGroupBox("学生信息")
        info_layout = QGridLayout()

        # 姓名
        info_layout.addWidget(QLabel("学生姓名:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("请输入学生姓名")
        info_layout.addWidget(self.name_input, 0, 1)

        # 用时
        info_layout.addWidget(QLabel("总用时(天):"), 1, 0)
        self.days_input = QSpinBox()
        self.days_input.setRange(1, 365)
        self.days_input.setValue(30)
        self.days_input.setSuffix(" 天")
        info_layout.addWidget(self.days_input, 1, 1)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # 评分区域 - 分页容器
        scores_group = QGroupBox("评分输入")
        scores_layout = QVBoxLayout(scores_group)
        scores_layout.setSpacing(10)

        # 页面切换按钮
        page_btn_layout = QHBoxLayout()
        self.btn_page1 = QPushButton("基础阶段 (L1-L2)")
        self.btn_page2 = QPushButton("进阶阶段 (L3-L4)")
        self.btn_page1.setCheckable(True)
        self.btn_page2.setCheckable(True)
        self.btn_page1.setChecked(True)
        self.btn_page1.clicked.connect(lambda: self.switch_page(0))
        self.btn_page2.clicked.connect(lambda: self.switch_page(1))
        page_btn_layout.addWidget(self.btn_page1)
        page_btn_layout.addWidget(self.btn_page2)
        scores_layout.addLayout(page_btn_layout)

        # 堆叠窗口用于分页显示
        self.stack_widget = QStackedWidget()
        scores_layout.addWidget(self.stack_widget)

        # 创建两个页面容器
        self.page1_widget = QWidget()
        self.page2_widget = QWidget()
        self.page1_layout = QVBoxLayout(self.page1_widget)
        self.page2_layout = QVBoxLayout(self.page2_widget)
        self.page1_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.page2_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.stack_widget.addWidget(self.page1_widget)
        self.stack_widget.addWidget(self.page2_widget)

        layout.addWidget(scores_group)

        self.current_page = 0

    def set_question(self, question: Question):
        """设置当前题目，更新评分网格"""
        self.current_question = question

        # 清除现有的层级组前先断开信号
        for level_group in self.level_groups.values():
            try:
                level_group.scores_changed.disconnect()
            except:
                pass

        # 清除两个页面的内容
        while self.page1_layout.count():
            item = self.page1_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        while self.page2_layout.count():
            item = self.page2_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.level_groups.clear()

        # 创建每个层级的评分组，按页面分组
        for level in [1, 2, 3, 4]:
            criteria = question.levels.get(level)
            if criteria:
                level_group = LevelScoreGroup(level, criteria.weight, question)
                level_group.scores_changed.connect(self.scores_changed.emit)
                self.level_groups[level] = level_group
                
                # L1, L2 放入第一页；L3, L4 放入第二页
                if level <= 2:
                    self.page1_layout.addWidget(level_group)
                else:
                    self.page2_layout.addWidget(level_group)

        self.page1_layout.addStretch()
        self.page2_layout.addStretch()

    def switch_page(self, page_index: int):
        """切换评分页面"""
        self.stack_widget.setCurrentIndex(page_index)
        self.current_page = page_index
        
        # 更新按钮状态
        self.btn_page1.setChecked(page_index == 0)
        self.btn_page2.setChecked(page_index == 1)
        
        # 更新按钮样式
        active_style = """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
        """
        inactive_style = """
            QPushButton {
                background-color: #e0e0e0;
                color: #666666;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """
        
        if page_index == 0:
            self.btn_page1.setStyleSheet(active_style)
            self.btn_page2.setStyleSheet(inactive_style)
        else:
            self.btn_page1.setStyleSheet(inactive_style)
            self.btn_page2.setStyleSheet(active_style)

    def get_all_scores(self) -> dict:
        """获取所有层级的分数"""
        return {
            level: group.get_scores()
            for level, group in self.level_groups.items()
        }

    def get_weights(self) -> dict:
        """获取所有层级的权重"""
        return {
            level: group.weight
            for level, group in self.level_groups.items()
        }

    def get_student_info(self) -> tuple:
        """获取学生信息（姓名，用时）"""
        return self.name_input.text().strip(), self.days_input.value()

    def clear_all(self):
        """清空所有输入"""
        self.name_input.clear()
        self.days_input.setValue(30)
        for group in self.level_groups.values():
            group.clear()
