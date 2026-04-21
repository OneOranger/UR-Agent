import React from 'react';
import { Card, Row, Col, Statistic, Tag, Alert } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, FileTextOutlined } from '@ant-design/icons';
import type { ResearchRunDetail } from '../../types/research';

interface ResearchOverviewProps {
  data: ResearchRunDetail;
}

const ResearchOverview: React.FC<ResearchOverviewProps> = ({ data }) => {
  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic 
              title="证据数量" 
              value={data.evidence_items.length} 
              suffix="条"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic 
              title="主题数量" 
              value={data.themes.length} 
              suffix="个"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic 
              title="洞察数量" 
              value={data.insights.length} 
              suffix="条"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic 
              title="建议数量" 
              value={data.recommendations.length} 
              suffix="条"
            />
          </Card>
        </Col>
      </Row>

      <Card style={{ marginTop: 16 }}>
        <h3 style={{ marginBottom: 16 }}>评估结果</h3>
        {data.eval_summary.evaluator_count === 0 ? (
          <Alert
            message="暂无评估数据"
            description="评估将在任务完成后自动生成"
            type="info"
            showIcon
          />
        ) : (
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} md={8}>
              <Statistic 
                title="总体评分" 
                value={data.eval_summary.overall_eval_score} 
                precision={2}
                suffix="/ 1.0"
              />
            </Col>
            <Col xs={24} sm={12} md={8}>
              <div>
                <div style={{ color: '#6B6B6B', marginBottom: 8 }}>通过状态</div>
                <Tag 
                  icon={data.eval_summary.overall_passed ? <CheckCircleOutlined /> : <CloseCircleOutlined />}
                  color={data.eval_summary.overall_passed ? 'success' : 'error'}
                  style={{ fontSize: 14, padding: '4px 12px' }}
                >
                  {data.eval_summary.overall_passed ? '已通过' : '未通过'}
                </Tag>
              </div>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Statistic 
                title="评估器数量" 
                value={data.eval_summary.evaluator_count} 
                suffix="个"
              />
            </Col>
          </Row>
        )}
      </Card>

      {data.report && (
        <Card style={{ marginTop: 16 }}>
          <h3 style={{ marginBottom: 16 }}>报告摘要</h3>
          <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>
            <p><strong>标题:</strong> {data.report.title}</p>
            <p><strong>执行摘要:</strong> {data.report.executive_summary}</p>
          </div>
        </Card>
      )}
    </div>
  );
};

export default ResearchOverview;
