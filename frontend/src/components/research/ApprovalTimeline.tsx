import React from 'react';
import { Timeline, Card, Tag } from 'antd';
import type { Approval } from '../../types/research';

interface ApprovalTimelineProps {
  items: Approval[];
}

const ApprovalTimeline: React.FC<ApprovalTimelineProps> = ({ items }) => {
  if (items.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无审批记录</div>;
  }

  const getDecisionColor = (decision: string) => {
    return decision === 'approved' ? 'green' : 'red';
  };

  const getDecisionText = (decision: string) => {
    return decision === 'approved' ? '通过' : '驳回';
  };

  return (
    <Card style={{ borderRadius: 8 }}>
      <Timeline>
        {items.map((item, index) => (
          <Timeline.Item key={index}>
            <div>
              <Tag color={getDecisionColor(item.decision)}>
                {getDecisionText(item.decision)}
              </Tag>
              <span style={{ marginLeft: 8, color: '#6B6B6B' }}>
                {item.approval_type}
              </span>
            </div>
            <p style={{ margin: '8px 0' }}>{item.comment}</p>
            <div style={{ fontSize: 12, color: '#999' }}>
              {item.stage_before} → {item.stage_after}
            </div>
          </Timeline.Item>
        ))}
      </Timeline>
    </Card>
  );
};

export default ApprovalTimeline;
