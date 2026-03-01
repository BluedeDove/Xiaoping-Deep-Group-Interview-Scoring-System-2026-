"""
主窗口
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QGroupBox, QMessageBox, QFileDialog,
    QApplication, QRadioButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from data.questions import get_question
from core.calculator import calculate_score, generate_report
from ui.criteria_panel import CriteriaPanel
from ui.score_grid import ScoreInputGrid
from ui.radar_chart import RadarChartWidget
from ui.ai_audit import AIAuditPanel


class MainWindow(QMainWindow):
    """面试评分系统主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("2026深度学习组 · 面试评分系统")
        self.setMinimumSize(1200, 800)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局 - 三栏式
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ========== 左栏：题目标准 ==========
        self.criteria_panel = CriteriaPanel()
        self.criteria_panel.setMinimumWidth(280)
        self.criteria_panel.setMaximumWidth(350)
        main_layout.addWidget(self.criteria_panel)

        # 题目切换时更新评分网格
        # 注意：criteria_panel 内部已处理按钮切换，这里只需响应其状态变化
        self.criteria_panel.radio_image.toggled.connect(self.on_question_changed)
        self.criteria_panel.radio_text.toggled.connect(self.on_question_changed)

        # ========== 中栏：评分输入 ==========
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.setSpacing(10)

        self.score_grid = ScoreInputGrid()
        middle_layout.addWidget(self.score_grid)

        # AI审计面板
        self.ai_audit = AIAuditPanel()
        self.ai_audit.factor_changed.connect(self.on_ai_factor_changed)
        middle_layout.addWidget(self.ai_audit)

        # 操作按钮
        button_layout = QHBoxLayout()

        self.calc_btn = QPushButton("计算得分")
        self.calc_btn.setMinimumHeight(40)
        self.calc_btn.clicked.connect(self.calculate_and_display)
        button_layout.addWidget(self.calc_btn)

        self.export_btn = QPushButton("导出报告")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.clicked.connect(self.export_report)
        button_layout.addWidget(self.export_btn)

        self.reset_btn = QPushButton("重置表单")
        self.reset_btn.setMinimumHeight(40)
        self.reset_btn.clicked.connect(self.reset_form)
        button_layout.addWidget(self.reset_btn)

        middle_layout.addLayout(button_layout)
        main_layout.addWidget(middle_widget, 2)

        # ========== 右栏：结果展示 ==========
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)

        # 雷达图
        radar_group = QGroupBox("能力雷达图")
        radar_layout = QVBoxLayout(radar_group)
        self.radar_chart = RadarChartWidget()
        radar_layout.addWidget(self.radar_chart)
        right_layout.addWidget(radar_group)

        # 分数展示
        result_group = QGroupBox("评分结果")
        result_layout = QVBoxLayout(result_group)

        self.base_score_label = QLabel("基础总分: --")
        self.base_score_label.setFont(QFont("Microsoft YaHei", 14))
        result_layout.addWidget(self.base_score_label)

        self.final_score_label = QLabel("最终得分: --")
        self.final_score_label.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        self.final_score_label.setStyleSheet("color: #2196F3;")
        result_layout.addWidget(self.final_score_label)

        self.ai_factor_label = QLabel("AI系数: 1.00")
        self.ai_factor_label.setFont(QFont("Microsoft YaHei", 11))
        result_layout.addWidget(self.ai_factor_label)

        result_layout.addStretch()
        right_layout.addWidget(result_group)

        right_widget.setMinimumWidth(300)
        right_widget.setMaximumWidth(400)
        main_layout.addWidget(right_widget, 1)

        # 初始化 - 手动加载第一个题目
        self._init_question()

    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #333333;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QLineEdit, QSpinBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border: 1px solid #2196F3;
            }
        """)

    def _init_question(self):
        """初始化题目"""
        question = get_question("image")
        if question:
            self.score_grid.set_question(question)
            self.criteria_panel.set_question("image")

    def on_question_changed(self, checked: bool = True):
        """题目切换时的处理"""
        # 只在按钮被选中时处理（避免取消选中时也触发）
        if not checked:
            return

        if self.criteria_panel.radio_image.isChecked():
            question_id = "image"
        else:
            question_id = "text"

        question = get_question(question_id)
        if question:
            self.score_grid.set_question(question)
            # 不再调用 criteria_panel.set_question()，
            # 因为 CriteriaPanel 自身的 toggled 处理器已处理
            self.reset_scores()

    def on_ai_factor_changed(self, factor: float, label: str):
        """AI系数改变时的处理"""
        self.ai_factor_label.setText(f"AI系数: {factor:.2f} ({label})")
        self.calculate_preview()

    def calculate_preview(self):
        """预览计算（实时更新雷达图）"""
        scores = self.score_grid.get_all_scores()
        weights = self.score_grid.get_weights()

        # 计算各维度平均分
        valid_scores = []
        for level_scores in scores.values():
            if sum(level_scores.values()) > 0:
                valid_scores.append(level_scores)

        if valid_scores:
            avg_code = sum(s["code"] for s in valid_scores) / len(valid_scores)
            avg_arch = sum(s["arch"] for s in valid_scores) / len(valid_scores)
            avg_math = sum(s["math"] for s in valid_scores) / len(valid_scores)
            avg_viz = sum(s["viz"] for s in valid_scores) / len(valid_scores)

            self.radar_chart.update_scores(avg_code, avg_arch, avg_math, avg_viz)

    def calculate_and_display(self):
        """计算并显示完整结果"""
        try:
            name, days = self.score_grid.get_student_info()
            if not name:
                QMessageBox.warning(self, "提示", "请输入学生姓名")
                return

            scores = self.score_grid.get_all_scores()
            weights = self.score_grid.get_weights()

            question = self.criteria_panel.get_current_question()
            if not question:
                QMessageBox.warning(self, "提示", "请先选择题目")
                return

            ai_factor = self.ai_audit.get_factor()
            ai_label = self.ai_audit.get_label()

            # 计算结果
            result = calculate_score(
                student_name=name,
                question_name=question.name,
                days_taken=days,
                scores=scores,
                weights=weights,
                ai_factor=ai_factor,
                ai_label=ai_label
            )

            # 更新显示
            self.base_score_label.setText(f"基础总分: {result.base_score:.1f}")
            self.final_score_label.setText(f"最终得分: {result.final_score:.2f} {'⭐' if ai_factor > 1.0 else ''}")

            # 更新雷达图
            dims = result.dimension_averages
            self.radar_chart.update_scores(
                dims["code"], dims["arch"], dims["math"], dims["viz"],
                result.final_score / 10  # 综合分数归一化到0-10
            )

            self.current_result = result
        except Exception as e:
            import traceback
            error_msg = f"计算出错:\n{str(e)}\n\n详细:\n{traceback.format_exc()}"
            QMessageBox.critical(self, "错误", error_msg)

    def export_report(self):
        """导出评分报告"""
        if not hasattr(self, 'current_result'):
            QMessageBox.warning(self, "提示", "请先计算得分")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出评分报告",
            f"{self.current_result.student_name}_面试评分报告.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )

        if file_path:
            try:
                report = generate_report(self.current_result)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                QMessageBox.information(self, "成功", f"报告已导出到:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败:\n{str(e)}")

    def reset_form(self):
        """重置表单"""
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要重置所有输入吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.reset_scores()

    def reset_scores(self):
        """重置分数输入"""
        self.score_grid.clear_all()
        self.base_score_label.setText("基础总分: --")
        self.final_score_label.setText("最终得分: --")
        self.ai_factor_label.setText("AI系数: 1.00")
        self.radar_chart.update_scores(0, 0, 0, 0)
        if hasattr(self, 'current_result'):
            delattr(self, 'current_result')
