import React from 'react';
import { Steps, Card } from 'antd';
import { 
  CheckCircleOutlined, 
  SyncOutlined, 
  ClockCircleOutlined,
  FileTextOutlined,
  TeamOutlined,
  ExperimentOutlined,
  UserOutlined,
  LineChartOutlined,
  BulbOutlined,
  ThunderboltOutlined,
  AuditOutlined
} from '@ant-design/icons';

interface WorkflowProgressProps {
  currentStage: string;
  status: 'running' | 'interrupted' | 'completed';
}

const WorkflowProgress: React.FC<WorkflowProgressProps> = ({ currentStage, status }) => {
  // 定义完整的流程节点
  const workflowSteps = [
    {
      title: '明确目标',
      key: 'clarify_goal',
      icon: <BulbOutlined />,
      description: '分析研究需求，明确研究目标'
    },
    {
      title: '制定计划',
      key: 'planner',
      icon: <FileTextOutlined />,
      description: '生成研究计划和方法论'
    },
    {
      title: '数据导入',
      key: 'ingest_uploaded_files',
      icon: <FileTextOutlined />,
      description: '导入和处理原始数据'
    },
    {
      title: '证据验证',
      key: 'evidence_validator',
      icon: <ExperimentOutlined />,
      description: '验证和整理研究证据'
    },
    {
      title: '主题提取',
      key: 'theme_extractor',
      icon: <TeamOutlined />,
      description: '从证据中提取关键主题'
    },
    {
      title: '洞察合成',
      key: 'insight_synthesizer',
      icon: <ThunderboltOutlined />,
      description: '综合生成用户洞察'
    },
    {
      title: '画像构建',
      key: 'persona_builder',
      icon: <UserOutlined />,
      description: '构建用户画像'
    },
    {
      title: '旅程映射',
      key: 'journey_mapper',
      icon: <LineChartOutlined />,
      description: '绘制用户旅程地图'
    },
    {
      title: '建议生成',
      key: 'recommendation_builder',
      icon: <BulbOutlined />,
      description: '生成产品建议'
    },
    {
      title: '报告生成',
      key: 'report_generator',
      icon: <FileTextOutlined />,
      description: '生成研究报告'
    },
    {
      title: '导出Markdown',
      key: 'markdown_export',
      icon: <FileTextOutlined />,
      description: '导出Markdown格式报告'
    },
    {
      title: '等待审批',
      key: 'review',
      icon: <AuditOutlined />,
      description: '等待人工审批'
    }
  ];

  // 找到当前步骤的索引
  const getCurrentStepIndex = () => {
    const index = workflowSteps.findIndex(step => step.key === currentStage);
    return index >= 0 ? index : 0;
  };

  // 确定每个步骤的状态
  const getStepStatus = (stepKey: string, index: number) => {
    const currentIndex = getCurrentStepIndex();

    // 如果是审批完成或全部完成状态，所有节点都显示为已完成
    if (status === 'completed' || currentStage === 'approved_or_rejected') {
      return 'finish';
    }

    if (index < currentIndex) {
      return 'finish'; // 已完成的步骤
    }

    if (index === currentIndex) {
      if (currentStage === 'review') {
        return 'wait'; // 等待审批
      }
      return status === 'running' ? 'process' : 'wait'; // 当前步骤
    }

    return 'wait'; // 未开始的步骤
  };

  const currentStepIndex = getCurrentStepIndex();
  const currentStep = workflowSteps[currentStepIndex];

  return (
    <Card 
      style={{ 
        marginBottom: 24, 
        borderRadius: 12,
        border: '1px solid #E8E6E1',
        background: '#FAF9F6'
      }}
    >
      <h3 style={{ marginTop: 0, marginBottom: 24, color: '#3D3D3D' }}>
        研究流程进度
      </h3>
      
      {/* 当前执行状态提示 */}
      {status === 'running' && currentStep && (
        <div style={{ 
          marginBottom: 24, 
          padding: 16, 
          background: '#FFF7E6', 
          borderRadius: 8,
          border: '1px solid #FFE7BA'
        }}>
          <SyncOutlined spin style={{ marginRight: 8, color: '#FA8C16' }} />
          <strong style={{ color: '#FA8C16' }}>正在执行: </strong>
          <span style={{ color: '#FA8C16' }}>{currentStep.title}</span>
          <div style={{ marginTop: 8, fontSize: 12, color: '#8C8C8C' }}>
            {currentStep.description}
          </div>
        </div>
      )}

      {currentStage === 'review' && (
        <div style={{ 
          marginBottom: 24, 
          padding: 16, 
          background: '#FFF1F0', 
          borderRadius: 8,
          border: '1px solid #FFCCC7'
        }}>
          <ClockCircleOutlined style={{ marginRight: 8, color: '#FF4D4F' }} />
          <strong style={{ color: '#FF4D4F' }}>等待审批: </strong>
          <span style={{ color: '#FF4D4F' }}>任务已暂停，等待您的审批</span>
        </div>
      )}

      {status === 'completed' && (
        <div style={{ 
          marginBottom: 24, 
          padding: 16, 
          background: '#F6FFED', 
          borderRadius: 8,
          border: '1px solid #B7EB8F'
        }}>
          <CheckCircleOutlined style={{ marginRight: 8, color: '#52C41A' }} />
          <strong style={{ color: '#52C41A' }}>已完成: </strong>
          <span style={{ color: '#52C41A' }}>研究流程已全部完成</span>
        </div>
      )}
      
      {/* 步骤条 */}
      <Steps
        direction="vertical"
        current={currentStepIndex}
        style={{ padding: '0 8px' }}
      >
        {workflowSteps.map((step, index) => (
          <Steps.Step
            key={step.key}
            title={
              <span style={{ fontSize: 14, fontWeight: 500 }}>
                {step.icon} {step.title}
              </span>
            }
            description={step.description}
            status={getStepStatus(step.key, index) as any}
          />
        ))}
      </Steps>
    </Card>
  );
};

export default WorkflowProgress;
