# UR Agent - 用户研究智能体系统

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange.svg)](https://www.langchain.com/langgraph)
[![React](https://img.shields.io/badge/React-18.3+-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 项目简介

UR Agent 是一个基于 **LangGraph** 和 **FastAPI** 构建的生产级用户研究智能体系统。该系统通过 AI 驱动的自动化工作流，实现从用户需求到研究报告的全流程智能化处理，包括证据收集、主题提取、洞察合成、用户画像构建、旅程图生成和推荐策略制定。

### ✨ 核心特性

- 🔄 **自动化研究工作流**：基于 LangGraph 的状态机驱动，实现完整的研究流程自动化
- 🤖 **AI 增强分析**：集成 LLM 进行证据验证、主题提取和洞察合成
- 👥 **用户画像生成**：自动生成基于数据的用户画像和旅程地图
- 📊 **智能推荐系统**：基于研究结果生成数据驱动的策略推荐
- 🔍 **质量保障**：内置护栏系统，确保输出质量和准确性
- 👁️ **可追溯性**：完整的 LangSmith 集成，支持全链路追踪和调试
- 🎯 **人机协作**：支持人工审核节点，确保关键决策的可控性
- 📈 **评估体系**：内置多维度评估器，自动评估研究质量
- 🌐 **前后端分离**：现代化的 React + FastAPI 架构

## 🏗️ 系统架构

### 后端架构

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI Server                        │
├─────────────────────────────────────────────────────────────┤
│  API Routes  │  Core Config  │  Logger  │  Guardrails       │
├─────────────────────────────────────────────────────────────┤
│                    LangGraph Workflow                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Clarify  │→│ Planner  │→│ Ingest   │→│ Analyze  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Synthesize│→│  Report  │→│  Review  │→│  Export  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Domain Models  │  Storage Repos  │  LLM Executor          │
├─────────────────────────────────────────────────────────────┤
│                    SQLite Database                           │
└─────────────────────────────────────────────────────────────┘
```

### 研究工作流

UR Agent 的研究流程包含以下关键节点：

1. **目标澄清** (`clarify_goal`)：明确研究目标和范围
2. **研究规划** (`planner`)：制定详细的研究计划
3. **数据摄入** (`ingest_uploaded_files`)：处理上传的研究数据
4. **证据验证** (`evidence_validator`)：验证和整理证据
5. **主题提取** (`theme_extractor`)：从证据中提取关键主题
6. **洞察合成** (`insight_synthesizer`)：合成深度洞察
7. **用户画像** (`persona_builder`)：构建用户画像
8. **旅程地图** (`journey_mapper`)：生成用户旅程地图
9. **推荐生成** (`recommendation_builder`)：制定策略推荐
10. **报告生成** (`report_generator`)：生成研究报告
11. **人工审核** (`request_final_approval`)：人工审核节点（支持中断/恢复）
12. **报告导出** (`markdown_export`)：导出 Markdown 格式报告

## 🛠️ 技术栈

### 后端

- **Python 3.11+**：核心开发语言
- **FastAPI**：高性能异步 Web 框架
- **LangGraph**：状态机驱动的工作流引擎
- **LangChain**：LLM 集成框架
- **Pydantic**：数据验证和序列化
- **SQLite + aiosqlite**：异步数据库存储
- **LangSmith**：追踪和可观测性平台

### 前端

- **React 18**：用户界面框架
- **TypeScript**：类型安全的 JavaScript
- **Ant Design**：企业级 UI 组件库
- **Vite**：现代化的前端构建工具
- **React Query**：数据获取和状态管理
- **Axios**：HTTP 客户端
- **React Router**：路由管理

## 📦 安装与部署

### 前置要求

- Python 3.11 或更高版本
- Node.js 18+ 和 npm
- Git

### 后端安装

1. **克隆仓库**

```bash
git clone https://github.com/OneOranger/UR-Agent.git
cd UR-Agent
```

2. **创建虚拟环境**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows
```

3. **安装依赖**

```bash
pip install -e .
```

4. **配置环境变量**

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置必要的环境变量：

```env
# OpenAI API 配置
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.your-provider.com/v1

# LangSmith（可选，用于调试和追踪）
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-langsmith-key-here
LANGSMITH_PROJECT=ur-agent-dev
```

5. **初始化数据库**

```bash
python scripts/init_db.py
```

6. **启动后端服务**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

访问 API 文档：http://localhost:8000/docs

### 前端安装

1. **进入前端目录**

```bash
cd frontend
```

2. **安装依赖**

```bash
npm install
```

3. **启动开发服务器**

```bash
npm run dev
```

访问前端应用：http://localhost:5173

### 一键启动

Windows 用户可以使用提供的启动脚本：

```powershell
.\start-all.ps1
```

## 🚀 快速开始

### 1. 创建研究任务

通过 API 创建新的研究任务：

```bash
curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "user_request": "研究用户对某产品的使用体验和改进建议"
  }'
```

返回示例：

```json
{
  "run_id": "uuid-here",
  "thread_id": "uuid-here",
  "status": "running",
  "message": "任务已创建，正在执行中..."
}
```

### 2. 查询任务进度

```bash
curl "http://localhost:8000/run/{run_id}"
```

### 3. 人工审核（如需要）

当流程到达审核节点时，会中断等待人工决策：

```bash
curl -X POST "http://localhost:8000/resume" \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "your-thread-id",
    "decision": "approved",
    "comment": "报告质量良好，同意发布"
  }'
```

## 📚 API 文档

### 核心端点

| 方法 | 路径 | 描述 |
|------|------|------|
| `POST` | `/run` | 创建并启动研究任务 |
| `GET` | `/run/{run_id}` | 查询任务详情和结果 |
| `POST` | `/resume` | 恢复中断的任务（人工审核） |
| `GET` | `/health` | 健康检查 |
| `GET` | `/` | 服务信息 |

完整的 API 文档可在服务启动后访问：http://localhost:8000/docs

## 🗂️ 项目结构

```
UR-Agent/
├── app/                          # 后端应用代码
│   ├── api/                      # API 路由
│   │   └── routes/               # 路由处理器
│   ├── core/                     # 核心配置和日志
│   ├── domain/                   # 领域模型
│   │   ├── models/               # Pydantic 模型
│   │   └── schemas/              # API 请求/响应模式
│   ├── evals/                    # 评估器
│   │   ├── evaluators/           # 具体评估器实现
│   │   └── runners/              # 评估运行器
│   ├── graph/                    # LangGraph 工作流
│   ├── guardrails/               # 护栏系统
│   │   ├── input/                # 输入验证
│   │   └── output/               # 输出验证
│   ├── llm/                      # LLM 集成
│   ├── nodes/                    # 工作流节点
│   │   ├── analysis/             # 分析节点
│   │   ├── clarify/              # 目标澄清
│   │   ├── ingestion/            # 数据摄入
│   │   ├── planning/             # 规划节点
│   │   ├── reporting/            # 报告生成
│   │   ├── review/               # 审核节点
│   │   └── synthesis/            # 合成节点
│   ├── observability/            # 可观测性
│   ├── prompts/                  # Prompt 模板
│   │   ├── blocks/               # Prompt 块
│   │   ├── system/               # 系统 Prompt
│   │   └── tasks/                # 任务 Prompt
│   ├── storage/                  # 数据存储
│   │   ├── repositories/         # 数据访问层
│   │   └── sqlite/               # SQLite 实现
│   ├── tools/                    # 工具集
│   └── main.py                   # 应用入口
├── frontend/                     # 前端应用
│   ├── src/                      # 源代码
│   │   ├── components/           # React 组件
│   │   ├── pages/                # 页面组件
│   │   ├── services/             # API 服务
│   │   └── types/                # TypeScript 类型
│   └── package.json
├── scripts/                      # 工具脚本
├── data/                         # 数据目录
│   ├── raw_uploads/              # 原始上传文件
│   └── reports/                  # 生成的报告
├── tests/                        # 测试文件
├── .env.example                  # 环境变量示例
├── pyproject.toml                # Python 项目配置
└── README.md                     # 项目文档
```

## 🔬 评估系统

UR Agent 内置多个评估器，自动评估研究质量：

- **证据覆盖率评估** (`evidence_coverage`)：评估证据的完整性
- **推荐数量检查** (`recommendation_count_check`)：验证推荐数量是否合理
- **无支持声明率** (`unsupported_claim_rate`)：检查 unsupported claims 的比例

评估结果会自动保存到数据库，并可通过 API 查询。

## 🛡️ 护栏系统

系统内置多层护栏，确保输出质量：

### 输入护栏

- **PII 检查** (`pii_check`)：检测和过滤个人敏感信息
- **模拟数据检查** (`simulated_data_check`)：识别和警告模拟数据

### 输出护栏

- **无支持声明检查** (`unsupported_claim_check`)：验证所有声明都有证据支持
- **发布前验证** (`validate_before_publish`)：最终发布前的全面检查

## 🔍 可观测性

集成 LangSmith 提供完整的可观测性：

- **节点级追踪**：每个工作流节点的输入输出
- **LLM 调用追踪**：记录所有 LLM 交互
- **性能指标**：监控各节点执行时间
- **调试支持**：快速定位问题

## 🧪 测试

运行测试套件：

```bash
python -m pytest tests/ -v
```

运行特定测试：

```bash
python scripts/test_full_flow.py      # 测试完整工作流
python scripts/test_langgraph_state.py # 测试 LangGraph 状态管理
python scripts/test_llm.py            # 测试 LLM 集成
```

## 📖 使用示例

### 示例 1：用户体验研究

```python
import requests

# 创建研究任务
response = requests.post("http://localhost:8000/run", json={
    "user_request": "研究用户对我们新移动应用的体验，识别主要痛点和改进机会"
})

run_id = response.json()["run_id"]

# 轮询查询进度
import time
while True:
    result = requests.get(f"http://localhost:8000/run/{run_id}")
    data = result.json()
    
    if data["run"]["current_stage"] == "completed":
        print("研究完成！")
        print(f"报告: {data['report']}")
        break
    
    time.sleep(3)
```

### 示例 2：产品策略研究

```python
# 创建产品策略研究
response = requests.post("http://localhost:8000/run", json={
    "user_request": "分析目标市场的产品定位和竞争策略建议"
})

# 如果需要人工审核
requests.post("http://localhost:8000/resume", json={
    "thread_id": response.json()["thread_id"],
    "decision": "approved",
    "comment": "策略分析全面，同意发布"
})
```

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 为所有公共函数和类编写文档字符串
- 添加相应的单元测试
- 确保所有测试通过后再提交 PR

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用框架
- [LangGraph](https://www.langchain.com/langgraph) - 状态机工作流引擎
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Web 框架
- [React](https://reactjs.org/) - 用户界面库

## 📧 联系方式

- 项目主页：https://github.com/OneOranger/UR-Agent
- 问题反馈：https://github.com/OneOranger/UR-Agent/issues

---

⭐ 如果这个项目对你有帮助，请考虑给一个 Star！
