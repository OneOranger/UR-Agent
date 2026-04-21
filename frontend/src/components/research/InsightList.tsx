import React from 'react';
import { List, Card, Tag } from 'antd';
import type { Insight } from '../../types/research';

interface InsightListProps {
  items: Insight[];
}

const InsightList: React.FC<InsightListProps> = ({ items }) => {
  if (items.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无洞察</div>;
  }

  const getSeverityColor = (severity: string) => {
    switch(severity.toLowerCase()) {
      case 'high': return 'red';
      case 'medium': return 'orange';
      case 'low': return 'green';
      default: return 'default';
    }
  };

  return (
    <List
      dataSource={items}
      renderItem={(item) => (
        <List.Item>
          <Card style={{ width: '100%', borderRadius: 8 }}>
            <div style={{ marginBottom: 12 }}>
              <Tag color={getSeverityColor(item.severity)}>严重程度: {item.severity}</Tag>
              <Tag color="blue">置信度: {Math.round(item.confidence_score * 100)}%</Tag>
            </div>
            <p style={{ fontSize: 16, marginBottom: 12, whiteSpace: 'pre-wrap' }}>{item.statement}</p>
            {item.opportunity_area && (
              <div style={{ background: '#FAF9F6', padding: 12, borderRadius: 6 }}>
                <strong>机会领域:</strong>
                <p style={{ margin: '8px 0 0 0', whiteSpace: 'pre-wrap' }}>{item.opportunity_area}</p>
              </div>
            )}
          </Card>
        </List.Item>
      )}
    />
  );
};

export default InsightList;
