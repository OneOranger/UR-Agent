import React from 'react';
import { List, Card, Tag } from 'antd';
import type { Recommendation } from '../../types/research';

interface RecommendationListProps {
  items: Recommendation[];
}

const RecommendationList: React.FC<RecommendationListProps> = ({ items }) => {
  if (items.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无建议</div>;
  }

  const getPriorityColor = (priority: string) => {
    switch(priority.toLowerCase()) {
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
              <Tag color={getPriorityColor(item.priority)}>优先级: {item.priority}</Tag>
            </div>
            <h3 style={{ marginTop: 0, marginBottom: 12 }}>{item.title}</h3>
            <p style={{ marginBottom: 12, whiteSpace: 'pre-wrap' }}>{item.description}</p>
            
            {item.rationale && (
              <div style={{ background: '#FAF9F6', padding: 12, borderRadius: 6, marginBottom: 12 }}>
                <strong>理由:</strong>
                <p style={{ margin: '8px 0 0 0', whiteSpace: 'pre-wrap' }}>{item.rationale}</p>
              </div>
            )}

            {item.related_opportunity_area && (
              <div>
                <strong>相关机会领域:</strong>
                <p style={{ margin: '8px 0 0 0', whiteSpace: 'pre-wrap' }}>{item.related_opportunity_area}</p>
              </div>
            )}
          </Card>
        </List.Item>
      )}
    />
  );
};

export default RecommendationList;
