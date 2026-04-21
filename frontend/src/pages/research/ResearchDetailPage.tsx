




import React from 'react';
import { Tabs, Card, Spin, Alert, Tag, Descriptions, Button, Space } from 'antd';
import { useQuery } from 'react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { getResearchRunDetail } from '../../services/researchApi';
import { ArrowLeftOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import WorkflowProgress from '../../components/research/WorkflowProgress';
import ResearchOverview from '../../components/research/ResearchOverview';
import EvidenceList from '../../components/research/EvidenceList';
import ThemeList from '../../components/research/ThemeList';
import InsightList from '../../components/research/InsightList';
import PersonaList from '../../components/research/PersonaList';
import JourneyMapView from '../../components/research/JourneyMapView';
import RecommendationList from '../../components/research/RecommendationList';
import ReportView from '../../components/research/ReportView';
import ApprovalTimeline from '../../components/research/ApprovalTimeline';
import TraceViewer from '../../components/research/TraceViewer';
import EvalSummaryCard from '../../components/research/EvalSummaryCard';
import type { ResearchRunDetail } from '../../types/research';

const { TabPane } = Tabs;

const ResearchDetailPage: React.FC = () => {
  const { runId } = useParams<{ runId: string }>();
  const navigate = useNavigate();

  const { data, isLoading, error } = useQuery<ResearchRunDetail>(
    ['researchRun', runId],
    () => getResearchRunDetail(runId!),
    {
      enabled: !!runId,
      refetchInterval: (data) => {
        // 如果任务还在运行中，每3秒刷新一次
        const stage = data?.run?.current_stage;
        if (stage && stage !== 'completed' && stage !== 'approved_or_rejected') {
          return 3000;
        }
        return false;
      },
    }
  );

  if (isLoading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: '#F5F5F0'
      }}>
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div style={{ padding: 40, background: '#F5F5F0', minHeight: '100vh' }}>
        <Alert
          message="加载失败"
          description="无法获取研究任务详情"
          type="error"
          showIcon
        />
      </div>
    );
  }

  const getStatusTag = (stage: string) => {
    if (stage === 'completed') {
      return <Tag icon={<CheckCircleOutlined />} color="success">已完成</Tag>;
    }
    if (stage === 'interrupted' || stage === 'review') {
      return <Tag icon={<CloseCircleOutlined />} color="warning">待审批</Tag>;
    }
    return <Tag color="processing">{stage || '运行中'}</Tag>;
  };

  return (
    <div style={{ minHeight: '100vh', background: '#F5F5F0' }}>
      {/* 顶部导航 */}
      <div style={{ 
        background: '#FAF9F6', 
        padding: '16px 24px',
        borderBottom: '1px solid #E8E6E1',
        marginBottom: 24
      }}>
        <Space>
          <Button 
            icon={<ArrowLeftOutlined />} 
            onClick={() => navigate('/research/new')}
            style={{ borderRadius: 6 }}
          >
            返回
          </Button>
          <div>
            <h2 style={{ margin: 0, fontSize: 20, fontWeight: 600 }}>
              研究任务详情
            </h2>
            <div style={{ marginTop: 8 }}>
              {getStatusTag(data.run.current_stage)}
            </div>
          </div>
        </Space>
      </div>

      {/* 内容区域 */}
      <div style={{ padding: '0 24px 24px', maxWidth: 1400, margin: '0 auto' }}>
        {/* 流程进度显示 */}
        {!isLoading && data && (
          <WorkflowProgress 
            currentStage={data.run.current_stage} 
            status={data.run.current_stage === 'completed' || data.run.current_stage === 'approved_or_rejected' ? 'completed' : 
                   data.run.current_stage === 'review' ? 'interrupted' : 'running'}
          />
        )}

        {/* 概览信息 */}
        <Card 
          style={{ 
            marginBottom: 24, 
            borderRadius: 12,
            border: '1px solid #E8E6E1'
          }}
        >
          <Descriptions column={2} bordered size="small">
            <Descriptions.Item label="研究需求" span={2}>
              {data.run.user_request}
            </Descriptions.Item>
            <Descriptions.Item label="当前阶段">
              {data.run.current_stage}
            </Descriptions.Item>
            <Descriptions.Item label="研究目标">
              {data.run.research_goal || '-'}
            </Descriptions.Item>
          </Descriptions>
        </Card>

        {/* 如果需要审批,显示审批按钮 */}
        {(data.run.current_stage === 'interrupted' || data.run.current_stage === 'review') && (
          <div style={{ marginBottom: 24 }}>
            <Alert
              message="任务需要审批"
              description="当前研究任务已完成初步分析，等待您的审批以继续生成最终报告。"
              type="warning"
              showIcon
              style={{ marginBottom: 16, borderRadius: 8 }}
            />
            <Button
              type="primary"
              size="large"
              onClick={() => navigate(`/research/${runId}/review`)}
              style={{ 
                width: '100%',
                height: 48,
                borderRadius: 8,
                fontSize: 16,
                background: '#8B7355',
                border: 'none'
              }}
            >
              前往审批
            </Button>
          </div>
        )}

        {/* Tabs 内容 */}
        <Card 
          style={{ 
            borderRadius: 12,
            border: '1px solid #E8E6E1'
          }}
        >
          <Tabs defaultActiveKey="overview" size="large">
            <TabPane tab="概览" key="overview">
              <ResearchOverview data={data} />
            </TabPane>
            <TabPane tab={`证据 (${data.evidence_items.length})`} key="evidence">
              <EvidenceList items={data.evidence_items} />
            </TabPane>
            <TabPane tab={`主题 (${data.themes.length})`} key="themes">
              <ThemeList items={data.themes} />
            </TabPane>
            <TabPane tab={`洞察 (${data.insights.length})`} key="insights">
              <InsightList items={data.insights} />
            </TabPane>
            <TabPane tab={`画像 (${data.personas.length})`} key="personas">
              <PersonaList items={data.personas} />
            </TabPane>
            <TabPane tab={`旅程 (${data.journey_maps.length})`} key="journeys">
              <JourneyMapView items={data.journey_maps} />
            </TabPane>
            <TabPane tab={`建议 (${data.recommendations.length})`} key="recommendations">
              <RecommendationList items={data.recommendations} />
            </TabPane>
            <TabPane tab="报告" key="report">
              <ReportView report={data.report} />
            </TabPane>
            <TabPane tab={`审批 (${data.approvals.length})`} key="approvals">
              <ApprovalTimeline items={data.approvals} />
            </TabPane>
            <TabPane tab={`Trace (${data.traces.length})`} key="traces">
              <TraceViewer items={data.traces} />
            </TabPane>
            <TabPane tab="评估" key="evals">
              <EvalSummaryCard summary={data.eval_summary} records={data.eval_records} />
            </TabPane>
          </Tabs>
        </Card>
      </div>
    </div>
  );
};

export default ResearchDetailPage;
