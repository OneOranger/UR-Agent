import React from 'react';
import { List, Card, Tag } from 'antd';
import type { EvidenceItem } from '../../types/research';

interface EvidenceListProps {
  items: EvidenceItem[];
}

const EvidenceList: React.FC<EvidenceListProps> = ({ items }) => {
  if (items.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无证据</div>;
  }

  return (
    <List
      dataSource={items}
      renderItem={(item) => (
        <List.Item>
          <Card style={{ width: '100%', borderRadius: 8 }}>
            <div style={{ marginBottom: 12 }}>
              <Tag color="blue">{item.source_type}</Tag>
              <Tag color={item.confidence > 0.7 ? 'green' : 'orange'}>
                置信度: {(item.confidence * 100).toFixed(0)}%
              </Tag>
              {item.is_simulated && <Tag color="red">模拟数据</Tag>}
            </div>
            <h4 style={{ margin: '8px 0' }}>{item.source_name}</h4>
            <p style={{ color: '#6B6B6B', whiteSpace: 'pre-wrap' }}>{item.raw_excerpt}</p>
            {item.tags.length > 0 && (
              <div style={{ marginTop: 8 }}>
                {item.tags.map((tag, index) => (
                  <Tag key={index}>{tag}</Tag>
                ))}
              </div>
            )}
          </Card>
        </List.Item>
      )}
    />
  );
};

export default EvidenceList;
