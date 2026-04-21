"""
过渡兼容文件

说明：
1. 旧版 prompt helper 暂时保留
2. 新增节点一律不要再写到这里
3. 已迁移节点应改用 app/llm/prompt_loader.py
4. 等全部节点迁移完成后，再删除本文件
"""


def get_clarify_goal_prompt(user_request: str) -> str:
    """
    生成“研究目标澄清”提示词
    """
    return f"""
你是专业的用户研究负责人。
请根据用户需求，输出结构化的研究目标定义。

用户需求：
{user_request}

要求：
1. research_goal 要清晰、专业、可执行
2. target_users 必须是用户群体列表
3. key_questions 是这次研究最该回答的问题
4. 不要输出解释性废话
""".strip()


def get_research_plan_prompt(user_request: str, research_goal: str) -> str:
    """
    生成“研究计划”提示词
    """
    return f"""
你是专业的用户研究规划专家。
请根据以下信息生成一份精简但专业的研究计划。

用户需求：
{user_request}

研究目标：
{research_goal}

要求：
1. method 给出最合适的方法
2. steps 给出清晰执行步骤
3. human_checkpoints 给出必须人工审核的节点
4. risks 给出潜在风险
""".strip()


def get_insight_synthesis_prompt(evidence_texts: list[str]) -> str:
    """
    生成“洞察提炼”提示词
    """
    joined = "\n\n".join(
        [f"证据{i+1}:\n{text}" for i, text in enumerate(evidence_texts)]
    )

    return f"""
你是专业的用户研究分析师。
请基于以下真实证据，提炼结构化洞察。

证据：
{joined}

要求：
1. 只根据证据生成洞察，不要编造
2. 每条洞察要简洁明确
3. severity 只能是 low / medium / high
4. confidence_score 在 0 到 1 之间
5. 不要输出无证据支持的结论
""".strip()

def get_theme_extraction_prompt(evidence_texts: list[str]) -> str:
    """
    生成主题提取提示词
    """
    joined = "\n\n".join(
        [f"证据{i+1}:\n{text}" for i, text in enumerate(evidence_texts)]
    )

    return f"""
你是专业的用户研究分析师。
请基于以下真实证据，先提炼“研究主题（themes）”，不要直接输出最终产品建议。

证据：
{joined}

要求：
1. 主题要比原始证据更抽象，但不要过度概括
2. 每个主题都要有清晰名称和说明
3. 主题数量控制在 2 到 5 个
4. 只根据证据生成，不要编造
5. confidence_score 在 0 到 1 之间
""".strip()

def get_persona_builder_prompt(theme_text: str, insight_text: str, evidence_texts: list[str]) -> str:
    """
    生成 Persona 提取提示词
    """
    evidence_joined = "\n\n".join(
        [f"证据{i+1}:\n{text}" for i, text in enumerate(evidence_texts)]
    )

    return f"""
你是专业的用户研究分析师。
请基于以下研究主题、洞察和证据，提炼 1 到 3 个用户画像（Persona）。

研究主题：
{theme_text}

研究洞察：
{insight_text}

原始证据：
{evidence_joined}

要求：
1. Persona 必须是“典型用户类型”的抽象，不是某个真实个人
2. 每个 Persona 必须包含：
   - name
   - summary
   - goals
   - pain_points
   - behaviors
   - motivations
3. 不要编造与研究材料无关的内容
4. 画像数量控制在 1 到 3 个
5. 输出要结构化，不要写解释性废话
""".strip()

def get_journey_mapper_prompt(persona_text: str, theme_text: str, insight_text: str) -> str:
    """
    生成旅程图提示词
    """
    return f"""
你是专业的用户研究与体验分析师。
请基于以下 Persona、研究主题和洞察，生成一条结构化的用户旅程图（Journey Map）。

Persona：
{persona_text}

研究主题：
{theme_text}

研究洞察：
{insight_text}

要求：
1. 旅程阶段控制在 4 到 6 个
2. 每个阶段都必须包含：
   - stage_name
   - user_goal
   - user_actions
   - touchpoints
   - pain_points
   - opportunities
   - emotion
3. 阶段应该符合用户使用健身 App 的真实过程
4. 不要编造与研究材料无关的内容
5. 输出结构化结果，不要写多余解释
""".strip()

def get_recommendation_builder_prompt(
    theme_text: str,
    insight_text: str,
    persona_text: str,
    journey_text: str,
) -> str:
    """
    生成建议构建提示词
    """
    return f"""
你是专业的用户研究与产品策略分析师。
请基于以下研究主题、洞察、Persona 和 Journey Map，输出结构化的产品建议。

研究主题：
{theme_text}

研究洞察：
{insight_text}

Persona：
{persona_text}

Journey Map：
{journey_text}

要求：
1. 建议必须具体、可执行，不能空泛
2. 每条建议都必须包含：
   - title
   - description
   - priority（只能是 high / medium / low）
   - rationale
   - related_opportunity_area
3. 建议数量控制在 3 到 5 条
4. 不要输出与研究材料无关的建议
5. 优先输出对产品设计和体验优化最有价值的建议
""".strip()