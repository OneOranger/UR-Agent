import React from 'react';
import { Button, Spin, Alert } from 'antd';
import { useQuery } from 'react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { getResearchRunDetail } from '../../services/researchApi';
import { ArrowLeftOutlined } from '@ant-design/icons';
import ReportView from '../../components/research/ReportView';

const ReportPage: React.FC = () => {
  const { runId } = useParams<{ runId: string }>();
  const navigate = useNavigate();

  const { data, isLoading, error } = useQuery(
    ['researchRun', runId],
    () => getResearchRunDetail(runId!),
    {
      enabled: !!runId,
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
        <Spin size="large" tip="加载报告中..." />
      </div>
    );
  }

  if (error || !data?.report) {
    return (
      <div style={{ padding: 40, background: '#F5F5F0', minHeight: '100vh' }}>
        <Alert
          message="报告不可用"
          description="该研究任务还没有生成报告"
          type="warning"
          showIcon
        />
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: '#F5F5F0' }}>
      {/* 顶部导航 */}
      <div style={{ 
        background: '#FAF9F6', 
        padding: '16px 24px',
        borderBottom: '1px solid #E8E6E1',
        marginBottom: 24
      }}>
        <Button 
          icon={<ArrowLeftOutlined />} 
          onClick={() => navigate(`/research/${runId}`)}
          style={{ borderRadius: 6 }}
        >
          返回详情页
        </Button>
      </div>

      {/* 报告内容 */}
      <div style={{ padding: '0 24px 40px', maxWidth: 1200, margin: '0 auto' }}>
        <ReportView report={data.report} />
      </div>
    </div>
  );
};

export default ReportPage;
