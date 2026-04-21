import React from 'react';
import { List, Card, Collapse, Tag } from 'antd';
import type { JourneyMap } from '../../types/research';

const { Panel } = Collapse;

interface JourneyMapViewProps {
  items: JourneyMap[];
}

const JourneyMapView: React.FC<JourneyMapViewProps> = ({ items }) => {
  if (items.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无用户旅程</div>;
  }

  return (
    <List
      dataSource={items}
      renderItem={(item) => (
        <List.Item>
          <Card style={{ width: '100%', borderRadius: 8 }}>
            <h3 style={{ marginTop: 0 }}>{item.persona_name}</h3>
            <p style={{ marginBottom: 16, whiteSpace: 'pre-wrap' }}>{item.overview}</p>

            <h4>旅程阶段</h4>
            <Collapse>
              {item.stages.map((stage, index) => (
                <Panel header={`${index + 1}. ${stage.stage_name}`} key={index}>
                  <div style={{ marginBottom: 12 }}>
                    <strong>用户目标:</strong>
                    <p>{stage.user_goal}</p>
                  </div>
                  
                  <div style={{ marginBottom: 12 }}>
                    <strong>用户行为:</strong>
                    <ul>
                      {stage.user_actions.map((action, i) => (
                        <li key={i}>{action}</li>
                      ))}
                    </ul>
                  </div>

                  <div style={{ marginBottom: 12 }}>
                    <strong>接触点:</strong>
                    <div>
                      {stage.touchpoints.map((tp, i) => (
                        <Tag key={i}>{tp}</Tag>
                      ))}
                    </div>
                  </div>

                  <div style={{ marginBottom: 12 }}>
                    <strong>痛点:</strong>
                    <ul>
                      {stage.pain_points.map((pain, i) => (
                        <li key={i}>{pain}</li>
                      ))}
                    </ul>
                  </div>

                  <div style={{ marginBottom: 12 }}>
                    <strong>机会点:</strong>
                    <ul>
                      {stage.opportunities.map((opp, i) => (
                        <li key={i}>{opp}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <strong>情绪:</strong> {stage.emotion}
                  </div>
                </Panel>
              ))}
            </Collapse>
          </Card>
        </List.Item>
      )}
    />
  );
};

export default JourneyMapView;
