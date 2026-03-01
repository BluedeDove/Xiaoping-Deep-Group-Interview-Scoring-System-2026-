"""
题目数据定义
包含图像分类和文本分类两个题目的评分标准
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class DimensionCriteria:
    """单个维度的评分标准"""
    check_items: List[str]  # 检查项列表


@dataclass
class LevelCriteria:
    """单个层级的评分标准"""
    weight: float
    code: DimensionCriteria  # 工程代码
    arch: DimensionCriteria  # 架构设计
    math: DimensionCriteria  # 数理理论
    viz: DimensionCriteria  # 分析可视化
    killer_questions: List[str] = field(default_factory=list)  # 必问问题


@dataclass
class Question:
    """题目定义"""
    id: str
    name: str
    description: str
    levels: Dict[int, LevelCriteria]  # 1-4级


# ============== 图像场景分类题目 ==============
IMAGE_QUESTION = Question(
    id="image",
    name="图像场景分类",
    description="考察CNN、计算机视觉、模型可解释性",
    levels={
        1: LevelCriteria(
            weight=1.0,
            code=DimensionCriteria([
                "环境配置无误（PyTorch/TensorFlow）",
                "使用ImageFolder或类似方式加载数据",
                "代码能够跑通无报错"
            ]),
            arch=DimensionCriteria([
                "成功调用torchvision预训练模型",
                "跑通训练循环（Train/Val）",
                "有基本的模型保存/加载"
            ]),
            math=DimensionCriteria([
                "理解Train/Val/Test的区别",
                "知道Overfitting的基本概念",
                "能解释Accuracy的计算方式"
            ]),
            viz=DimensionCriteria([
                "终端打印Epoch/Loss信息",
                "能展示预测结果"
            ]),
            killer_questions=[
                "BatchSize设了多少？显存不够怎么改？",
                "ResNet18输出层维度为什么是6？怎么改的？"
            ]
        ),
        2: LevelCriteria(
            weight=1.2,
            code=DimensionCriteria([
                "代码模块化分离（data/model/train/utils）",
                "实现完整的模型保存/加载/断点续训",
                "有配置文件管理超参数"
            ]),
            arch=DimensionCriteria([
                "实现至少2种数据增强方法",
                "调整过学习率/优化器等超参数并有记录",
                "使用学习率调度器"
            ]),
            math=DimensionCriteria([
                "能推导Softmax和CrossEntropy",
                "理解Backpropagation基本原理",
                "能解释Conv2d参数量计算"
            ]),
            viz=DimensionCriteria([
                "绘制Loss/Acc曲线图",
                "可视化错误分类样例",
                "有tensorboard或类似日志"
            ]),
            killer_questions=[
                "数据增强后BatchSize还能增大吗？",
                "SGD和Adam的区别是什么？为什么选这个？"
            ]
        ),
        3: LevelCriteria(
            weight=1.5,
            code=DimensionCriteria([
                "实现自定义Dataset类",
                "多GPU训练或混合精度训练",
                "完整的日志系统和异常处理"
            ]),
            arch=DimensionCriteria([
                "实现模型集成（Ensemble）或知识蒸馏",
                "设计多尺度特征融合方案",
                "解决类别不平衡问题"
            ]),
            math=DimensionCriteria([
                "能推导BatchNorm前向和反向",
                "理解ResNet残差连接的作用",
                "能计算感受野大小"
            ]),
            viz=DimensionCriteria([
                "实现Grad-CAM等可解释性可视化",
                "绘制混淆矩阵并分析",
                "特征图可视化（Feature Map）"
            ]),
            killer_questions=[
                "BatchNorm在训练和测试时的区别？",
                "ResNet解决了什么问题？为什么有效？"
            ]
        ),
        4: LevelCriteria(
            weight=2.0,
            code=DimensionCriteria([
                "代码工程化（CI/CD、Docker化）",
                "实现分布式训练",
                "完整的单元测试覆盖"
            ]),
            arch=DimensionCriteria([
                "设计新的网络结构或改进现有架构",
                "实现AutoML或NAS相关方法",
                "模型量化/剪枝/蒸馏完整方案"
            ]),
            math=DimensionCriteria([
                "从数学角度分析模型收敛性",
                "能推导Attention机制",
                "理解流形学习在视觉中的应用"
            ]),
            viz=DimensionCriteria([
                "交互式可视化界面",
                "模型内部决策路径可视化",
                "高维数据降维可视化（t-SNE/UMAP）"
            ]),
            killer_questions=[
                "如果要将模型部署到移动端，你会怎么做？",
                "你的方法和SOTA的差距在哪里？如何改进？"
            ]
        )
    }
)

# ============== 新闻文本分类题目 ==============
TEXT_QUESTION = Question(
    id="text",
    name="新闻文本分类",
    description="考察NLP基础、Transformer、大模型应用",
    levels={
        1: LevelCriteria(
            weight=1.0,
            code=DimensionCriteria([
                "成功加载文本数据集",
                "实现基础的分词和词表构建",
                "跑通文本分类训练流程"
            ]),
            arch=DimensionCriteria([
                "使用简单的词袋模型或浅层神经网络",
                "理解Embedding层的作用",
                "有基本的文本预处理流程"
            ]),
            math=DimensionCriteria([
                "理解词向量的基本概念",
                "知道TF-IDF的计算方法",
                "能解释文本分类的评价指标"
            ]),
            viz=DimensionCriteria([
                "显示训练过程中的Loss变化",
                "展示分类结果示例",
                "词频统计可视化"
            ]),
            killer_questions=[
                "词表大小怎么确定的？OOV怎么处理？",
                "序列长度设多少？为什么？"
            ]
        ),
        2: LevelCriteria(
            weight=1.2,
            code=DimensionCriteria([
                "使用LSTM/GRU实现文本分类",
                "实现预训练词向量加载（Word2Vec/GloVe）",
                "代码模块化，数据加载优化"
            ]),
            arch=DimensionCriteria([
                "实现双向LSTM",
                "使用Attention机制",
                "正则化方法（Dropout/Weight Decay）"
            ]),
            math=DimensionCriteria([
                "理解RNN的梯度消失/爆炸问题",
                "能解释LSTM的门控机制",
                "理解Attention的Q/K/V机制"
            ]),
            viz=DimensionCriteria([
                "绘制Loss和F1-score曲线",
                "可视化Attention权重",
                "错误样本分析"
            ]),
            killer_questions=[
                "LSTM相比普通RNN解决了什么问题？",
                "Attention权重怎么解释？"
            ]
        ),
        3: LevelCriteria(
            weight=1.5,
            code=DimensionCriteria([
                "使用BERT等预训练模型",
                "实现Fine-tune最佳实践",
                "处理长文本（>512 tokens）"
            ]),
            arch=DimensionCriteria([
                "实现分层学习率",
                "多任务学习框架",
                "模型融合策略"
            ]),
            math=DimensionCriteria([
                "理解Transformer的Self-Attention",
                "能解释BERT的预训练任务",
                "理解位置编码的原理"
            ]),
            viz=DimensionCriteria([
                "BERT注意力头可视化",
                "词嵌入降维可视化",
                "混淆矩阵细粒度分析"
            ]),
            killer_questions=[
                "BERT的[CLS]token为什么能代表句子？",
                "Fine-tune时学习率为什么通常设得很小？"
            ]
        ),
        4: LevelCriteria(
            weight=2.0,
            code=DimensionCriteria([
                "使用大模型API或本地部署",
                "实现Prompt Engineering优化",
                "模型蒸馏到小模型"
            ]),
            arch=DimensionCriteria([
                "LoRA/Prefix-tuning等高效微调",
                "RAG检索增强架构",
                "多模态融合方案"
            ]),
            math=DimensionCriteria([
                "理解大模型的涌现能力",
                "能分析计算复杂度（FLOPs）",
                "理解对比学习的损失函数"
            ]),
            viz=DimensionCriteria([
                "Prompt效果对比可视化",
                "模型推理过程可视化",
                "错误类型聚类分析"
            ]),
            killer_questions=[
                "Prompt Engineering和Fine-tune各有什么优劣？",
                "如果要处理100万条数据，你会怎么设计流程？"
            ]
        )
    }
)

# 题目集合
QUESTIONS = {
    "image": IMAGE_QUESTION,
    "text": TEXT_QUESTION,
}

# AI审计系数选项
AI_AUDIT_FACTORS = {
    0.0: {"label": "AI傀儡", "icon": "[X]", "desc": "完全由AI生成，无个人理解"},
    0.5: {"label": "复制粘贴", "icon": "[!]", "desc": "大量复制AI代码，缺乏修改"},
    1.0: {"label": "正常工具", "icon": "[O]", "desc": "合理使用AI作为工具"},
    1.1: {"label": "人机协奏", "icon": "[*]", "desc": "AI辅助，有个人创新和优化"},
}


def get_question(question_id: str) -> Question:
    """获取指定题目"""
    return QUESTIONS.get(question_id)


def get_all_questions() -> Dict[str, Question]:
    """获取所有题目"""
    return QUESTIONS
