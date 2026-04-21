import React from 'react';
import { List, Card, Progress } from 'antd';
import type { Theme } from '../../types/research';

interface ThemeListProps {
  items: Theme[];
}

const ThemeList: React.FC<ThemeListProps> = ({ items }) => {
  if (items.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无主题</div>;
  }

  return (
    <List
      dataSource={items}
      renderItem={(item) => (
        <List.Item>
          <Card style={{ width: '100%', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
              <h3 style={{ margin: 0 }}>{item.name}</h3>
              <Progress 
                type="circle" 
                percent={Math.round(item.confidence_score * 100)} 
                width={60}
                strokeColor="#8B7355"
              />
            </div>
            <p style={{ color: '#6B6B6B', whiteSpace: 'pre-wrap' }}>{item.description}</p>
          </Card>
        </List.Item>
      )}
    />
  );
};

export default ThemeList;
