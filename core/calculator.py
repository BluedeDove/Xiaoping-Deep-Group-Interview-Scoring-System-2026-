"""
评分计算逻辑
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class LevelScore:
    """单个层级的评分结果"""
    level: int
    weight: float
    code: float
    arch: float
    math: float
    viz: float

    @property
    def subtotal(self) -> float:
        """小计（未加权）"""
        return self.code + self.arch + self.math + self.viz

    @property
    def weighted(self) -> float:
        """加权后得分"""
        return self.subtotal * self.weight


@dataclass
class ScoreResult:
    """完整评分结果"""
    student_name: str
    question_name: str
    days_taken: int
    level_scores: List[LevelScore]
    ai_factor: float
    ai_label: str

    @property
    def base_score(self) -> float:
        """基础总分（未乘AI系数）"""
        return sum(ls.weighted for ls in self.level_scores)

    @property
    def final_score(self) -> float:
        """最终得分（乘AI系数后）"""
        return self.base_score * self.ai_factor

    @property
    def dimension_averages(self) -> Dict[str, float]:
        """各维度平均分"""
        valid_scores = [ls for ls in self.level_scores if ls.subtotal > 0]
        if not valid_scores:
            return {"code": 0, "arch": 0, "math": 0, "viz": 0}

        return {
            "code": sum(ls.code for ls in valid_scores) / len(valid_scores),
            "arch": sum(ls.arch for ls in valid_scores) / len(valid_scores),
            "math": sum(ls.math for ls in valid_scores) / len(valid_scores),
            "viz": sum(ls.viz for ls in valid_scores) / len(valid_scores),
        }


def calculate_score(
    student_name: str,
    question_name: str,
    days_taken: int,
    scores: Dict[int, Dict[str, float]],
    weights: Dict[int, float],
    ai_factor: float,
    ai_label: str
) -> ScoreResult:
    """
    计算最终得分

    Args:
        student_name: 学生姓名
        question_name: 题目名称
        days_taken: 用时（天）
        scores: {层级: {维度: 分数}}，维度包括 code, arch, math, viz
        weights: {层级: 权重}
        ai_factor: AI审计系数
        ai_label: AI审计标签

    Returns:
        ScoreResult: 完整的评分结果
    """
    level_scores = []
    for level in [1, 2, 3, 4]:
        level_data = scores.get(level, {})
        level_scores.append(LevelScore(
            level=level,
            weight=weights.get(level, 1.0),
            code=level_data.get("code", 0),
            arch=level_data.get("arch", 0),
            math=level_data.get("math", 0),
            viz=level_data.get("viz", 0),
        ))

    return ScoreResult(
        student_name=student_name,
        question_name=question_name,
        days_taken=days_taken,
        level_scores=level_scores,
        ai_factor=ai_factor,
        ai_label=ai_label
    )


def generate_report(result: ScoreResult) -> str:
    """生成文本格式的评分报告"""
    lines = []
    lines.append("=" * 50)
    lines.append("       2026深度学习组 · 面试评分报告")
    lines.append("=" * 50)
    lines.append(f"学生姓名: {result.student_name}")
    lines.append(f"答辩题目: {result.question_name}")
    lines.append(f"总用时: {result.days_taken}天")
    lines.append("")
    lines.append("【评分详情】")
    lines.append("+------+------+------+------+------+--------+--------+")
    lines.append("| 层级 | 代码 | 架构 | 数理 | 可视 |  小计  |  加权  |")
    lines.append("+------+------+------+------+------+--------+--------+")

    for ls in result.level_scores:
        lines.append(
            f"| L{ls.level}   |  {ls.code:2.0f}  |  {ls.arch:2.0f}  |  {ls.math:2.0f}  |  {ls.viz:2.0f}  | "
            f"{ls.subtotal:5.1f}  | {ls.weighted:6.1f} |"
        )

    lines.append("+------+------+------+------+------+--------+--------+")
    lines.append("")
    lines.append(f"基础总分: {result.base_score:.1f}")
    lines.append(f"AI审计系数: {result.ai_factor:.2f} ({result.ai_label})")
    lines.append(f"最终得分: {result.final_score:.2f}")
    lines.append("")
    lines.append("【雷达图能力分析】")

    dims = result.dimension_averages
    for name, value in [("代码", dims["code"]), ("架构", dims["arch"]),
                        ("数理", dims["math"]), ("可视", dims["viz"])]:
        bar = "#" * int(value) + "-" * (10 - int(value))
        lines.append(f"{name}: [{bar}] {value:.1f}")

    lines.append("")
    lines.append("【评语】")
    lines.append(generate_comment(dims))
    lines.append("")
    lines.append("面试官签名: ___________")
    lines.append(f"日期: 2026-03-01")
    lines.append("=" * 50)

    return "\n".join(lines)


def generate_comment(dims: Dict[str, float]) -> str:
    """根据维度得分生成评语"""
    comments = []

    avg = sum(dims.values()) / len(dims)

    if avg >= 8:
        comments.append("综合能力优秀，各维度表现均衡。")
    elif avg >= 6:
        comments.append("综合能力良好，有进一步发展潜力。")
    else:
        comments.append("基础能力有待加强，需要更多练习。")

    # 找出强弱项
    sorted_dims = sorted(dims.items(), key=lambda x: x[1], reverse=True)

    if sorted_dims[0][1] - sorted_dims[-1][1] > 3:
        strong = {"code": "代码能力", "arch": "架构设计",
                  "math": "数理基础", "viz": "可视化"}[sorted_dims[0][0]]
        weak = {"code": "代码能力", "arch": "架构设计",
                "math": "数理基础", "viz": "可视化"}[sorted_dims[-1][0]]
        comments.append(f"{strong}突出，{weak}需加强。")

    return "".join(comments)
