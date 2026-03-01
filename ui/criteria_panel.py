"""
左栏：题目标准展示面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup,
    QGroupBox, QScrollArea, QFrame, QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from data.questions import get_question, Question, LevelCriteria, DimensionCriteria


class CriteriaPanel(QWidget):
    """题目标准展示面板（左栏）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_question = None
        self.highlighted_level = 1
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # 题目选择区域
        question_group = QGroupBox("题目选择")
        question_layout = QVBoxLayout()

        self.question_group = QButtonGroup(self)
        self.radio_image = QRadioButton("图像场景分类")
        self.radio_text = QRadioButton("新闻文本分类")
        self.radio_image.setChecked(True)

        self.question_group.addButton(self.radio_image, 0)
        self.question_group.addButton(self.radio_text, 1)

        question_layout.addWidget(self.radio_image)
        question_layout.addWidget(self.radio_text)
        question_group.setLayout(question_layout)
        layout.addWidget(question_group)

        # 连接信号
        self.radio_image.toggled.connect(lambda: self.on_question_changed("image"))
        self.radio_text.toggled.connect(lambda: self.on_question_changed("text"))

        # 标准展示区域（可滚动）
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.criteria_widget = QWidget()
        self.criteria_layout = QVBoxLayout(self.criteria_widget)
        self.criteria_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.criteria_widget)
        layout.addWidget(scroll)

        # 初始加载
        self.set_question("image")

    def on_question_changed(self, question_id: str):
        """题目切换时的处理"""
        sender = self.sender()
        if isinstance(sender, QRadioButton) and sender.isChecked():
            self.set_question(question_id)

    def set_question(self, question_id: str):
        """设置当前题目并更新显示"""
        question = get_question(question_id)
        if not question:
            return

        self.current_question = question
        self.update_criteria_display()

    def highlight_level(self, level: int):
        """高亮显示指定层级"""
        self.highlighted_level = level
        self.update_criteria_display()

    def update_criteria_display(self):
        """更新标准显示"""
        # 清空现有内容
        while self.criteria_layout.count():
            item = self.criteria_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.current_question:
            return

        # 显示每个层级的标准
        for level in [1, 2, 3, 4]:
            criteria = self.current_question.levels.get(level)
            if criteria:
                level_widget = self.create_level_widget(level, criteria)
                self.criteria_layout.addWidget(level_widget)

        self.criteria_layout.addStretch()

    def create_level_widget(self, level: int, criteria: LevelCriteria) -> QGroupBox:
        """创建单个层级的标准显示组件"""
        level_names = {1: "L1 青铜", 2: "L2 白银", 3: "L3 黄金", 4: "L4 王者"}
        group = QGroupBox(f"{level_names.get(level, f'L{level}')} ×{criteria.weight}")

        # 高亮当前层级
        if level == self.highlighted_level:
            group.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #2196F3;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    color: #2196F3;
                }
            """)
        else:
            group.setStyleSheet("""
                QGroupBox {
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

        layout = QVBoxLayout()
        layout.setSpacing(5)

        # 验收标准
        standards_label = QLabel("[验收标准]")
        standards_label.setFont(QFont("Microsoft YaHei", 9, QFont.Weight.Bold))
        layout.addWidget(standards_label)

        # 各维度标准
        dimensions = [
            ("代码", criteria.code),
            ("架构", criteria.arch),
            ("数理", criteria.math),
            ("可视", criteria.viz)
        ]

        for dim_name, dim_criteria in dimensions:
            dim_widget = self.create_dimension_widget(dim_name, dim_criteria)
            layout.addWidget(dim_widget)

        # 必问问题
        if criteria.killer_questions:
            questions_label = QLabel("[必问问题]")
            questions_label.setFont(QFont("Microsoft YaHei", 9, QFont.Weight.Bold))
            layout.addWidget(questions_label)

            for q in criteria.killer_questions:
                q_label = QLabel(f'  "{q}"')
                q_label.setStyleSheet("color: #E65100; padding-left: 10px;")
                q_label.setWordWrap(True)
                layout.addWidget(q_label)

        group.setLayout(layout)
        return group

    def create_dimension_widget(self, name: str, criteria: DimensionCriteria) -> QWidget:
        """创建单个维度的标准显示"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(2)
        layout.setContentsMargins(10, 2, 2, 2)

        # 维度名称
        name_label = QLabel(f"【{name}】")
        name_label.setFont(QFont("Microsoft YaHei", 8, QFont.Weight.Bold))
        layout.addWidget(name_label)

        # 检查项
        for item in criteria.check_items:
            item_label = QLabel(f"  [OK] {item}")
            item_label.setStyleSheet("color: #666666; font-size: 11px;")
            item_label.setWordWrap(True)
            layout.addWidget(item_label)

        return widget

    def get_current_question(self) -> Question:
        """获取当前选中的题目"""
        return self.current_question
