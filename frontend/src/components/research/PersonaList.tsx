import React from 'react';
import { List, Card, Tag, Collapse } from 'antd';
import type { Persona } from '../../types/research';

const { Panel } = Collapse;

interface PersonaListProps {
  items: Persona[];
}

const PersonaList: React.FC<PersonaListProps> = ({ items }) => {
  if (items.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无用户画像</div>;
  }

  return (
    <List
      dataSource={items}
      renderItem={(item) => (
        <List.Item>
          <Card style={{ width: '100%', borderRadius: 8 }}>
            <h3 style={{ marginTop: 0, marginBottom: 16 }}>{item.name}</h3>
            <p style={{ marginBottom: 16, whiteSpace: 'pre-wrap' }}>{item.summary}</p>
            
            <Collapse defaultActiveKey={[]}>
              <Panel header="目标" key="goals">
                <ul>
                  {item.goals.map((goal, index) => (
                    <li key={index}>{goal}</li>
                  ))}
                </ul>
              </Panel>
              <Panel header="痛点" key="pain_points">
                <ul>
                  {item.pain_points.map((pain, index) => (
                    <li key={index}>{pain}</li>
                  ))}
                </ul>
              </Panel>
              <Panel header="行为特征" key="behaviors">
                <ul>
                  {item.behaviors.map((behavior, index) => (
                    <li key={index}>{behavior}</li>
                  ))}
                </ul>
              </Panel>
              <Panel header="动机" key="motivations">
                <ul>
                  {item.motivations.map((motivation, index) => (
                    <li key={index}>{motivation}</li>
                  ))}
                </ul>
              </Panel>
            </Collapse>
          </Card>
        </List.Item>
      )}
    />
  );
};

export default PersonaList;
