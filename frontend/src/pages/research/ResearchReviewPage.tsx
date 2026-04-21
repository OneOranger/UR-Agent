import React, { useState } from 'react';
import { Card, Button, Input, message, Space, Alert } from 'antd';
import { useMutation } from 'react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { resumeResearchRun, getResearchRunDetail } from '../../services/researchApi';
import { CheckOutlined, CloseOutlined, ArrowLeftOutlined } from '@ant-design/icons';

const { TextArea } = Input;

const ResearchReviewPage: React.FC = () => {
  const { runId } = useParams<{ runId: string }>();
  const navigate = useNavigate();
  const [comment, setComment] = useState('');

  // 获取任务详情
  const [taskData, setTaskData] = React.useState<any>(null);

  React.useEffect(() => {
    if (runId) {
      getResearchRunDetail(runId).then((data) => {
        setTaskData(data);
      }).catch((err) => {
        message.error('获取任务详情失败');
      });
    }
  }, [runId]);

  const resumeMutation = useMutation(resumeResearchRun, {
    onSuccess: () => {
      message.success('审批成功！');
      navigate(`/research/${runId}`);
    },
    onError: (error: any) => {
      message.error(`审批失败: ${error.response?.data?.detail || error.message}`);
    },
  });

  const handleApprove = () => {
    if (!taskData?.run?.thread_id) {
      message.error('缺少 thread_id');
      return;
    }

    resumeMutation.mutate({
      thread_id: taskData.run.thread_id,
      decision: 'approved',
      comment: comment || '通过',
    });
  };

  const handleReject = () => {
    if (!taskData?.run?.thread_id) {
      message.error('缺少 thread_id');
      return;
    }

    if (!comment.trim()) {
      message.warning('驳回时请填写备注');
      return;
    }

    resumeMutation.mutate({
      thread_id: taskData.run.thread_id,
      decision: 'rejected',
      comment,
    });
  };

  return (
    <div style={{ minHeight: '100vh', background: '#F5F5F0', padding: '24px' }}>
      <div style={{ maxWidth: 1000, margin: '0 auto' }}>
        {/* 返回按钮 */}
        <Button 
          icon={<ArrowLeftOutlined />} 
          onClick={() => navigate(`/research/${runId}`)}
          style={{ marginBottom: 24, borderRadius: 6 }}
        >
          返回详情页
        </Button>

        {/* 审批卡片 */}
        <Card 
          title="任务审批" 
          style={{ 
            borderRadius: 12,
            border: '1px solid #E8E6E1',
            marginBottom: 24
          }}
        >
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            {/* 任务信息 */}
            <Alert
              message="待审批任务"
              description={
                <div>
                  <p style={{ margin: '8px 0' }}><strong>研究需求:</strong> {taskData?.run?.user_request}</p>
                  <p style={{ margin: '8px 0' }}><strong>当前阶段:</strong> {taskData?.run?.current_stage}</p>
                  {taskData?.report && (
                    <div style={{ marginTop: 16 }}>
                      <p style={{ margin: '8px 0' }}><strong>执行摘要:</strong></p>
                      <p style={{ whiteSpace: 'pre-wrap' }}>{taskData.report.executive_summary}</p>
                    </div>
                  )}
                </div>
              }
              type="info"
              showIcon
            />

            {/* 审批备注 */}
            <div>
              <label style={{ 
                display: 'block', 
                marginBottom: 8, 
                fontWeight: 500 
              }}>
                审批备注 {taskData?.run?.current_stage === 'interrupted' && <span style={{ color: '#ff4d4f' }}>*</span>}
              </label>
              <TextArea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="请输入审批备注..."
                rows={4}
                style={{ borderRadius: 8 }}
              />
            </div>

            {/* 审批按钮 */}
            <Space style={{ width: '100%', justifyContent: 'center' }} size="large">
              <Button
                type="primary"
                size="large"
                icon={<CheckOutlined />}
                onClick={handleApprove}
                loading={resumeMutation.isLoading}
                disabled={!taskData?.run?.thread_id}
                style={{ 
                  width: 160,
                  height: 48,
                  borderRadius: 8,
                  fontSize: 16,
                  background: '#52c41a',
                  border: 'none'
                }}
              >
                通过
              </Button>
              <Button
                size="large"
                icon={<CloseOutlined />}
                onClick={handleReject}
                loading={resumeMutation.isLoading}
                disabled={!taskData?.run?.thread_id || !comment.trim()}
                style={{ 
                  width: 160,
                  height: 48,
                  borderRadius: 8,
                  fontSize: 16,
                  background: '#ff4d4f',
                  border: 'none',
                  color: '#fff'
                }}
              >
                驳回
              </Button>
            </Space>
          </Space>
        </Card>
      </div>
    </div>
  );
};

export default ResearchReviewPage;
