# UR Agent 前端平台 - 异步任务模式实现说明

## 🎯 实现目标

将研究任务创建从**同步模式**改为**异步模式**，并提供**实时流程进度可视化**。

## ✅ 已完成的修改

### 1. 后端修改 (`app/api/routes/research_runs.py`)

#### 修改前（同步模式）：
```python
@router.post("/run")
def create_research_run(request: CreateResearchRunRequest):
    # 等待整个流程完成
    raw_result = app_graph.invoke(state, config=config)
    # 返回完整结果
    return {
        "thread_id": thread_id,
        "status": "completed",
        "result": state_dict,
    }
```

#### 修改后（异步模式）：
```python
@router.post("/run")
async def create_research_run(request: CreateResearchRunRequest):
    # 立即返回 run_id
    # 后台异步执行整个流程
    asyncio.create_task(run_workflow())
    
    return {
        "run_id": run_id,
        "thread_id": thread_id,
        "status": "running",
        "message": "任务已创建，正在执行中...",
    }
```

**关键改进：**
- ✅ 立即返回，不等待完成
- ✅ 后台异步执行工作流
- ✅ 自动保存审批记录
- ✅ 任务完成后自动运行评估器
- ✅ 错误处理和日志记录

### 2. 前端修改

#### 2.1 类型定义更新 (`src/types/research.ts`)
```typescript
export interface ResearchRunResponse {
  run_id: string;          // 新增
  thread_id: string;
  status: 'running' | 'interrupted' | 'completed';  // 新增 'running'
  message?: string;        // 新增
  interrupts?: any[];
  result?: ResearchRunResult;
}
```

#### 2.2 新建任务页面 (`src/pages/research/NewResearchPage.tsx`)
```typescript
const createMutation = useMutation(createResearchRun, {
  onSuccess: (data) => {
    const runId = data.run_id;  // 直接使用 run_id
    message.success('研究任务创建成功！正在执行...');
    
    // 立即跳转到详情页
    navigate(`/research/${runId}`);
  },
});
```

**改进：**
- ✅ 创建后立即跳转，不再等待
- ✅ 用户体验更流畅

#### 2.3 新增流程进度组件 (`src/components/research/WorkflowProgress.tsx`)

**功能：**
- 📊 可视化显示12个流程节点
- 🔄 实时显示当前执行位置
- ✨ 动态状态指示（进行中/已完成/等待中）
- 💬 友好的状态提示信息

**流程节点：**
1. 明确目标 (clarify_goal)
2. 制定计划 (planner)
3. 数据导入 (ingest_uploaded_files)
4. 证据验证 (evidence_validator)
5. 主题提取 (theme_extractor)
6. 洞察合成 (insight_synthesizer)
7. 画像构建 (persona_builder)
8. 旅程映射 (journey_mapper)
9. 建议生成 (recommendation_builder)
10. 报告生成 (report_generator)
11. 导出Markdown (markdown_export)
12. 等待审批 (review)

#### 2.4 详情页优化 (`src/pages/research/ResearchDetailPage.tsx`)

```typescript
const { data, isLoading, error } = useQuery<ResearchRunDetail>(
  ['researchRun', runId],
  () => getResearchRunDetail(runId!),
  {
    enabled: !!runId,
    refetchInterval: (data) => {
      // 任务运行中，每3秒刷新一次
      if (data?.run?.current_stage && data.run.current_stage !== 'completed') {
        return 3000;
      }
      return false;
    },
  }
);
```

**改进：**
- ✅ 集成流程进度组件
- ✅ 自动轮询（3秒间隔）
- ✅ 任务完成后停止轮询
- ✅ 实时状态更新

##  完整流程说明

### 用户操作流程：

1. **创建任务**
   - 用户在首页输入研究需求
   - 点击"创建研究任务"
   - 立即跳转到详情页（不再等待）

2. **查看进度**
   - 详情页顶部显示流程进度条
   - 高亮显示当前执行节点
   - 每3秒自动刷新状态

3. **节点状态：**
   - 🟢 **已完成** - 绿色对勾
   - 🔵 **进行中** - 蓝色旋转图标
   - ⚪ **等待中** - 灰色时钟图标
   - 🟡 **待审批** - 黄色警告图标

4. **审批流程**
   - 流程执行到"等待审批"节点时暂停
   - 显示"前往审批"按钮
   - 用户审批后继续执行

5. **任务完成**
   - 所有节点显示为已完成
   - 显示评估结果
   - 可查看完整报告

## 🎨 UI/UX 设计

### 进度条状态提示：

**执行中：**
```
🔄 正在执行: 主题提取
   从证据中提取关键主题
```
背景色：淡黄色 (#FFF7E6)

**等待审批：**
```
⏰ 等待审批: 任务已暂停，等待您的审批
```
背景色：淡红色 (#FFF1F0)

**已完成：**
```
✅ 已完成: 研究流程已全部完成
```
背景色：淡绿色 (#F6FFED)

## 🔧 技术实现细节

### 后端异步执行：
```python
async def run_workflow():
    try:
        # 执行完整工作流
        raw_result = app_graph.invoke(state, config=config)
        state_dict, interrupts = normalize_graph_result(raw_result)
        
        # 保存到数据库
        await persist_state(thread_id, state_dict)
        
        # 如果是审批中断，保存审批记录
        if state_dict.get("current_stage") == "review":
            await persist_approval(...)
        
        # 如果完成，运行评估
        if not interrupts:
            await persist_evals(...)
            
    except Exception as e:
        # 错误处理
        log_event(event_name="research_run_error", ...)

# 启动后台任务
asyncio.create_task(run_workflow())
```

### 前端轮询机制：
```typescript
// React Query 自动轮询
refetchInterval: (data) => {
  if (data?.run?.current_stage !== 'completed') {
    return 3000;  // 3秒刷新
  }
  return false;   // 停止轮询
}
```

## 📊 性能优化

1. **减少等待时间：** 从2-5分钟 → 立即跳转
2. **合理的轮询间隔：** 3秒（平衡实时性和服务器压力）
3. **智能停止轮询：** 任务完成后自动停止
4. **错误处理：** 完善的异常捕获和日志记录

## 🚀 使用方法

### 启动服务：
```bash
# 方式1：使用启动脚本
.\start-all.ps1

# 方式2：手动启动
# 后端
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 前端
cd frontend
npm run dev
```

### 访问：
- 前端：http://localhost:3000
- 后端API文档：http://localhost:8000/docs

## ✨ 优势总结

### 用户体验：
- ✅ 无需长时间等待
- ✅ 实时看到进度
- ✅ 清晰的流程可视化
- ✅ 可以随时关闭页面

### 技术优势：
- ✅ 不会超时
- ✅ 支持任务恢复
- ✅ 完善的错误处理
- ✅ 可扩展性强

### 业务价值：
- ✅ 提高用户满意度
- ✅ 降低跳出率
- ✅ 提升平台专业度
- ✅ 更好的用户留存

## 📝 注意事项

1. **后端服务必须运行** - 否则前端无法获取进度
2. **数据库需要正常** - 状态保存在SQLite中
3. **LLM API需要可用** - 流程需要调用AI模型
4. **网络环境稳定** - 保证轮询正常进行

## 🔮 未来优化方向

1. WebSocket 实时推送（替代轮询）
2. 流程节点详情展开
3. 每个节点的执行时间统计
4. 任务暂停/恢复功能
5. 多任务并行执行
6. 任务优先级管理

---

**实现日期：** 2024-04-12
**版本：** v1.0
**状态：** ✅ 已完成并测试通过
