import React, { useState } from 'react';
import { Card, Input, Button, message, Space } from 'antd';
import { useNavigate } from 'react-router-dom';
import { useMutation } from 'react-query';
import { createResearchRun } from '../../services/researchApi';
import { LoadingOutlined, ArrowRightOutlined } from '@ant-design/icons';

const { TextArea } = Input;

const NewResearchPage: React.FC = () => {
  const navigate = useNavigate();
  const [userRequest, setUserRequest] = useState('');

  const createMutation = useMutation(createResearchRun, {
    onSuccess: (data) => {
      const runId = data.run_id;
      message.success('研究任务创建成功！正在执行...');
      
      // 保存状态到 localStorage
      localStorage.setItem(
        `research_${runId}`,
        JSON.stringify({
          runId,
          threadId: data.thread_id,
          status: 'running',
          currentStage: 'clarify_goal',
        })
      );
      
      // 跳转到详情页
      navigate(`/research/${runId}`);
    },
    onError: (error: any) => {
      message.error(`创建失败: ${error.response?.data?.detail || error.message}`);
    },
  });

  const handleSubmit = () => {
    if (!userRequest.trim()) {
      message.warning('请输入研究需求');
      return;
    }

    createMutation.mutate({ user_request: userRequest });
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #F5F5F0 0%, #FAF9F6 100%)',
      padding: '40px 20px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <Card 
        style={{ 
          maxWidth: 800, 
          width: '100%',
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
          border: '1px solid #E8E6E1'
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <h1 style={{ 
            fontSize: 32, 
            fontWeight: 600, 
            color: '#3D3D3D',
            marginBottom: 12
          }}>
            UR Agent
          </h1>
          <p style={{ 
            fontSize: 16, 
            color: '#6B6B6B',
            margin: 0
          }}>
            智能用户研究平台
          </p>
        </div>

        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <label style={{ 
              display: 'block', 
              marginBottom: 8, 
              fontWeight: 500,
              color: '#3D3D3D'
            }}>
              研究需求
            </label>
            <TextArea
              value={userRequest}
              onChange={(e) => setUserRequest(e.target.value)}
              placeholder="请描述您的研究需求，例如：为一个面向东京年轻白领的健身 App 做用户研究"
              rows={6}
              style={{ 
                borderRadius: 8,
                fontSize: 14,
                background: '#FAF9F6'
              }}
              disabled={createMutation.isLoading}
            />
          </div>

          <Button
            type="primary"
            size="large"
            onClick={handleSubmit}
            loading={createMutation.isLoading}
            icon={createMutation.isLoading ? <LoadingOutlined /> : <ArrowRightOutlined />}
            style={{ 
              width: '100%',
              height: 48,
              borderRadius: 8,
              fontSize: 16,
              fontWeight: 500,
              background: '#8B7355',
              border: 'none'
            }}
          >
            {createMutation.isLoading ? '创建中...' : '创建研究任务'}
          </Button>
        </Space>
      </Card>
    </div>
  );
};

export default NewResearchPage;
