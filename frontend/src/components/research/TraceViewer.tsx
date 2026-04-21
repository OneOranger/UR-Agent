import React from 'react';
import { List, Card } from 'antd';
import type { Trace } from '../../types/research';

interface TraceViewerProps {
  items: Trace[];
}

const TraceViewer: React.FC<TraceViewerProps> = ({ items }) => {
  if (items.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无Trace记录</div>;
  }

  return (
    <List
      dataSource={items}
      renderItem={(item) => (
        <List.Item>
          <Card style={{ width: '100%', borderRadius: 8 }}>
            <h4 style={{ marginTop: 0, marginBottom: 12 }}>{item.event_name}</h4>
            <pre style={{ 
              background: '#FAF9F6', 
              padding: 12, 
              borderRadius: 6,
              overflow: 'auto',
              fontSize: 12
            }}>
              {JSON.stringify(item.payload, null, 2)}
            </pre>
          </Card>
        </List.Item>
      )}
    />
  );
};

export default TraceViewer;
