import React from 'react';
import { Card, Row, Col, Statistic, Tag, List } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import type { EvalSummary, EvalRecord } from '../../types/research';

interface EvalSummaryCardProps {
  summary: EvalSummary;
  records: EvalRecord[];
}

const EvalSummaryCard: React.FC<EvalSummaryCardProps> = ({ summary, records }) => {
  return (
    <div>
      <Card style={{ marginBottom: 16, borderRadius: 8 }}>
        <h3 style={{ marginTop: 0, marginBottom: 16 }}>评估汇总</h3>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12} md={8}>
            <Statistic 
              title="总体评分" 
              value={summary.overall_eval_score} 
              precision={2}
              suffix="/ 1.0"
            />
          </Col>
          <Col xs={24} sm={12} md={8}>
            <div>
              <div style={{ color: '#6B6B6B', marginBottom: 8 }}>通过状态</div>
              <Tag 
                icon={summary.overall_passed ? <CheckCircleOutlined /> : <CloseCircleOutlined />}
                color={summary.overall_passed ? 'success' : 'error'}
                style={{ fontSize: 14, padding: '4px 12px' }}
              >
                {summary.overall_passed ? '已通过' : '未通过'}
              </Tag>
            </div>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Statistic 
              title="评估器数量" 
              value={summary.evaluator_count} 
              suffix="个"
            />
          </Col>
        </Row>
      </Card>

      <Card style={{ borderRadius: 8 }}>
        <h3 style={{ marginTop: 0, marginBottom: 16 }}>评估详情</h3>
        <List
          dataSource={records}
          renderItem={(record) => (
            <List.Item>
              <Card style={{ width: '100%', borderRadius: 6 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                  <h4 style={{ margin: 0 }}>{record.evaluator_name}</h4>
                  <Tag 
                    icon={record.passed ? <CheckCircleOutlined /> : <CloseCircleOutlined />}
                    color={record.passed ? 'success' : 'error'}
                  >
                    {record.passed ? '通过' : '未通过'}
                  </Tag>
                </div>
                <Statistic 
                  title="分数" 
                  value={record.score} 
                  precision={2}
                  valueStyle={{ fontSize: 18 }}
                />
                {record.detail && (
                  <pre style={{ 
                    background: '#FAF9F6', 
                    padding: 12, 
                    borderRadius: 6,
                    marginTop: 12,
                    overflow: 'auto',
                    fontSize: 12
                  }}>
                    {JSON.stringify(record.detail, null, 2)}
                  </pre>
                )}
              </Card>
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default EvalSummaryCard;
