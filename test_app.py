"""
测试脚本 - 验证评分系统功能
无需GUI即可运行
"""

from data.questions import get_question, QUESTIONS
from core.calculator import calculate_score, generate_report


def test_questions_data():
    """测试题目数据"""
    print("=" * 50)
    print("测试题目数据加载")
    print("=" * 50)

    print(f"题目数量: {len(QUESTIONS)}")

    for qid, question in QUESTIONS.items():
        print(f"\n题目: {question.name} (ID: {qid})")
        print(f"  描述: {question.description}")
        print(f"  层级数: {len(question.levels)}")

        for level, criteria in question.levels.items():
            print(f"    L{level}: 权重×{criteria.weight}")
            print(f"      - 代码检查项: {len(criteria.code.check_items)}")
            print(f"      - 必问问题: {len(criteria.killer_questions)}")

    print("\n[PASS] 题目数据测试通过\n")


def test_scoring_calculation():
    """测试评分计算 - 使用plan.md中的小明案例"""
    print("=" * 50)
    print("测试评分计算（小明案例）")
    print("=" * 50)

    scores = {
        1: {'code': 10, 'arch': 10, 'math': 10, 'viz': 10},
        2: {'code': 8, 'arch': 8, 'math': 6, 'viz': 10},
        3: {'code': 0, 'arch': 0, 'math': 0, 'viz': 8},
        4: {'code': 0, 'arch': 0, 'math': 0, 'viz': 0},
    }
    weights = {1: 1.0, 2: 1.2, 3: 1.5, 4: 2.0}

    result = calculate_score(
        student_name='小明',
        question_name='图像场景分类',
        days_taken=45,
        scores=scores,
        weights=weights,
        ai_factor=1.05,
        ai_label='人机协奏'
    )

    print(f"学生: {result.student_name}")
    print(f"题目: {result.question_name}")
    print(f"基础总分: {result.base_score:.2f}")
    print(f"AI系数: {result.ai_factor}")
    print(f"最终得分: {result.final_score:.2f}")
    print(f"期望得分: 94.92")
    print(f"误差: {abs(result.final_score - 94.92):.4f}")

    # 验证各层级
    print("\n各层级得分:")
    for ls in result.level_scores:
        print(f"  L{ls.level}: {ls.subtotal:.1f} × {ls.weight} = {ls.weighted:.2f}")

    # 验证维度平均
    dims = result.dimension_averages
    print(f"\n各维度平均:")
    print(f"  代码: {dims['code']:.2f}")
    print(f"  架构: {dims['arch']:.2f}")
    print(f"  数理: {dims['math']:.2f}")
    print(f"  可视: {dims['viz']:.2f}")

    assert abs(result.final_score - 94.92) < 0.01, "计算结果与预期不符！"
    print("\n[PASS] 评分计算测试通过\n")


def test_report_generation():
    """测试报告生成"""
    print("=" * 50)
    print("测试报告生成")
    print("=" * 50)

    scores = {
        1: {'code': 10, 'arch': 10, 'math': 10, 'viz': 10},
        2: {'code': 8, 'arch': 8, 'math': 6, 'viz': 10},
        3: {'code': 0, 'arch': 0, 'math': 0, 'viz': 8},
        4: {'code': 0, 'arch': 0, 'math': 0, 'viz': 0},
    }
    weights = {1: 1.0, 2: 1.2, 3: 1.5, 4: 2.0}

    result = calculate_score(
        student_name='小明',
        question_name='图像场景分类',
        days_taken=45,
        scores=scores,
        weights=weights,
        ai_factor=1.05,
        ai_label='人机协奏'
    )

    report = generate_report(result)
    print(report[:800] + "...\n")
    print("[PASS] 报告生成测试通过\n")


def test_ai_factors():
    """测试AI审计系数"""
    print("=" * 50)
    print("测试AI审计系数")
    print("=" * 50)

    from data.questions import AI_AUDIT_FACTORS

    print("AI审计系数选项:")
    for factor, info in sorted(AI_AUDIT_FACTORS.items()):
        print(f"  {factor:.1f} - {info['label']}: {info['desc']}")

    print("\n[PASS] AI审计系数测试通过\n")


def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("面试评分系统 - 功能测试")
    print("=" * 50 + "\n")

    try:
        test_questions_data()
        test_scoring_calculation()
        test_report_generation()
        test_ai_factors()

        print("=" * 50)
        print("所有测试通过！")
        print("=" * 50)
        return 0

    except AssertionError as e:
        print(f"\n[FAIL] 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
