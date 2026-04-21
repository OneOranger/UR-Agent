/**
 * 进度追踪器组件
 * 用于在创建页面实时显示研究任务的执行进度
 */

import React, { useEffect, useState } from 'react';
import { useQuery } from 'react-query';
import { Card, Spin, Alert } from 'antd';
import { SyncOutlined, CheckCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';
import { getResearchRunDetail } from '../../services/researchApi';
import type { ResearchRunDetail } from '../../types/research';
import WorkflowProgress from './WorkflowProgress';

interface ProgressTrackerProps {
  runId: string;
}

const ProgressTracker: React.FC<ProgressTrackerProps> = ({ runId }) => {
  const [isCompleted, setIsCompleted] = useState(false);

  // 轮询查询任务状态
  const { data, isLoading, error } = useQuery<ResearchRunDetail>(
    ['researchRunProgress', runId],
    () => getResearchRunDetail(runId),
    {
      enabled: !!runId && !isCompleted,
      refetchInterval: (data) => {
        // 如果任务还在运行中，每2秒刷新一次
        if (data?.run?.current_stage && data.run.current_stage !== 'completed') {
          return 2000;
        }
        return false;
      },
      onSuccess: (data) => {
        if (data?.run?.current_stage === 'completed') {
          setIsCompleted(true);
        }
      },
    }
  );

  // 页面加载时滚动到进度区域
  useEffect(() => {
    if (runId) {
      setTimeout(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 100);
    }
  }, [runId]);

  if (isLoading && !data) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <Spin size="large" tip="正在加载任务状态..." />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="加载失败"
        description="无法获取任务状态，请检查网络连接"
        type="error"
        showIcon
        style={{ borderRadius: 8 }}
      />
    );
  }

  if (!data) {
    return null;
  }

  const currentStage = data.run.current_stage;
  const status = currentStage === 'completed' || currentStage === 'approved_or_rejected' ? 'completed' : 
                 currentStage === 'review' ? 'interrupted' : 'running';

  return (
    <div>
      {/* 状态提示 */}
      {status === 'running' && currentStage && (
        <Alert
          message={
            <span>
              <SyncOutlined spin style={{ marginRight: 8, color: '#FA8C16' }} />
              <strong>正在执行: </strong>
              {getStageDisplayName(currentStage)}
            </span>
          }
          description="请稍候，系统正在自动执行研究流程..."
          type="warning"
          showIcon={false}
          style={{ 
            marginBottom: 20, 
            borderRadius: 8,
            background: '#FFF7E6',
            border: '1px solid #FFD591'
          }}
        />
      )}

      {status === 'interrupted' && (
        <Alert
          message={
            <span>
              <ClockCircleOutlined style={{ marginRight: 8, color: '#FF4D4F' }} />
              <strong>等待审批</strong>
            </span>
          }
          description="研究流程已暂停，需要人工审批后才能继续"
          type="error"
          showIcon={false}
          style={{ 
            marginBottom: 20, 
            borderRadius: 8,
            background: '#FFF1F0',
            border: '1px solid #FFA39E'
          }}
        />
      )}

      {status === 'completed' && (
        <Alert
          message={
            <span>
              <CheckCircleOutlined style={{ marginRight: 8, color: '#52C41A' }} />
              <strong>研究完成</strong>
            </span>
          }
          description="所有流程已完成，您可以查看完整报告"
          type="success"
          showIcon={false}
          style={{ 
            marginBottom: 20, 
            borderRadius: 8,
            background: '#F6FFED',
            border: '1px solid #B7EB8F'
          }}
        />
      )}

      {/* 流程进度 */}
      <WorkflowProgress currentStage={currentStage} status={status} />

      {/* 统计数据 */}
      {data.eval_summary && (
        <Card 
          size="small" 
          style={{ 
            marginTop: 24, 
            borderRadius: 8,
            background: '#FAFAF9',
            border: '1px solid #E8E6E1'
          }}
        >
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontWeight: 600, color: '#8B7355' }}>
                {data.evidence_items?.length || 0}
              </div>
              <div style={{ fontSize: 12, color: '#6B6B6B', marginTop: 4 }}>
                证据条数
              </div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontWeight: 600, color: '#8B7355' }}>
                {data.themes?.length || 0}
              </div>
              <div style={{ fontSize: 12, color: '#6B6B6B', marginTop: 4 }}>
                主题数量
              </div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontWeight: 600, color: '#8B7355' }}>
                {data.insights?.length || 0}
              </div>
              <div style={{ fontSize: 12, color: '#6B6B6B', marginTop: 4 }}>
                洞察数量
              </div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontWeight: 600, color: '#8B7355' }}>
                {data.recommendations?.length || 0}
              </div>
              <div style={{ fontSize: 12, color: '#6B6B6B', marginTop: 4 }}>
                建议数量
              </div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

// 辅助函数：获取阶段的中文显示名称
function getStageDisplayName(stage: string): string {
  const stageMap: Record<string, string> = {
    'clarify_goal': '明确目标',
    'planner': '制定计划',
    'ingest_uploaded_files': '数据导入',
    'evidence_validator': '证据验证',
    'theme_extractor': '主题提取',
    'insight_synthesizer': '洞察合成',
    'persona_builder': '画像构建',
    'journey_mapper': '旅程映射',
    'recommendation_builder': '建议生成',
    'report_generator': '报告生成',
    'markdown_export': '导出Markdown',
    'review': '等待审批',
    'approved_or_rejected': '审批完成',
  };
  return stageMap[stage] || stage;
}

export default ProgressTracker;
