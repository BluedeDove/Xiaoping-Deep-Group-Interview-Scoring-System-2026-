"""
AI审计系数选择面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton,
    QButtonGroup, QGroupBox, QSlider
)
from PyQt6.QtCore import Qt, pyqtSignal

from data.questions import AI_AUDIT_FACTORS


class AIAuditPanel(QGroupBox):
    """AI审计系数选择面板"""

    factor_changed = pyqtSignal(float, str)

    def __init__(self, parent=None):
        super().__init__("AI审计系数", parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # 使用按钮组
        self.button_group = QButtonGroup(self)

        for factor, info in sorted(AI_AUDIT_FACTORS.items()):
            radio = QRadioButton(f"{info['icon']} {factor:.1f} - {info['label']}")
            radio.setToolTip(info['desc'])
            radio.setProperty("factor", factor)
            radio.setProperty("label", info['label'])

            self.button_group.addButton(radio)
            layout.addWidget(radio)

            # 默认选中1.0
            if factor == 1.0:
                radio.setChecked(True)

        # 描述标签
        self.desc_label = QLabel("正常使用AI工具辅助开发")
        self.desc_label.setStyleSheet("color: #666666; font-size: 11px;")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

        # 连接信号
        self.button_group.buttonClicked.connect(self.on_selection_changed)

    def on_selection_changed(self, button):
        """选择改变时的处理"""
        factor = button.property("factor")
        label = button.property("label")
        desc = button.toolTip()
        self.desc_label.setText(desc)
        self.factor_changed.emit(factor, label)

    def get_factor(self) -> float:
        """获取当前选中的系数"""
        button = self.button_group.checkedButton()
        if button:
            return button.property("factor")
        return 1.0

    def get_label(self) -> str:
        """获取当前选中的标签"""
        button = self.button_group.checkedButton()
        if button:
            return button.property("label")
        return "正常工具"
