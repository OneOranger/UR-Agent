import React from 'react';
import { Card, Divider } from 'antd';
import type { Report } from '../../types/research';

interface ReportViewProps {
  report: Report | null;
}

const ReportView: React.FC<ReportViewProps> = ({ report }) => {
  if (!report) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#6B6B6B' }}>暂无报告</div>;
  }

  return (
    <Card style={{ borderRadius: 12 }}>
      <h1 style={{ marginTop: 0, marginBottom: 24 }}>{report.title}</h1>

      <section style={{ marginBottom: 32 }}>
        <h2>背景</h2>
        <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>{report.background}</p>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>研究目标</h2>
        <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>{report.research_goal}</p>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>执行摘要</h2>
        <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>{report.executive_summary}</p>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>关键发现</h2>
        <ul>
          {report.key_findings.map((finding, index) => (
            <li key={index} style={{ marginBottom: 8, lineHeight: 1.8 }}>{finding}</li>
          ))}
        </ul>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>主题总结</h2>
        <ul>
          {report.themes_summary.map((theme, index) => (
            <li key={index} style={{ marginBottom: 8, lineHeight: 1.8 }}>{theme}</li>
          ))}
        </ul>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>用户画像总结</h2>
        <ul>
          {report.personas_summary.map((persona, index) => (
            <li key={index} style={{ marginBottom: 8, lineHeight: 1.8 }}>{persona}</li>
          ))}
        </ul>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>用户旅程总结</h2>
        <ul>
          {report.journey_summary.map((journey, index) => (
            <li key={index} style={{ marginBottom: 8, lineHeight: 1.8 }}>{journey}</li>
          ))}
        </ul>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>建议</h2>
        <ul>
          {report.recommendations.map((rec, index) => (
            <li key={index} style={{ marginBottom: 8, lineHeight: 1.8 }}>{rec}</li>
          ))}
        </ul>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>方法论</h2>
        <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>{report.methodology}</p>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>局限性</h2>
        <ul>
          {report.limitations.map((limitation, index) => (
            <li key={index} style={{ marginBottom: 8, lineHeight: 1.8 }}>{limitation}</li>
          ))}
        </ul>
      </section>

      <Divider />

      <section style={{ marginBottom: 32 }}>
        <h2>下一步</h2>
        <ul>
          {report.next_steps.map((step, index) => (
            <li key={index} style={{ marginBottom: 8, lineHeight: 1.8 }}>{step}</li>
          ))}
        </ul>
      </section>
    </Card>
  );
};

export default ReportView;
