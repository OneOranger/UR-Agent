import axios from 'axios';
import type {
  CreateResearchRunRequest,
  ResumeResearchRunRequest,
  ResearchRunResponse,
  ResearchRunDetail,
} from '../types/research';

const api = axios.create({
  baseURL: '/research',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 创建研究任务
export const createResearchRun = async (
  payload: CreateResearchRunRequest
): Promise<ResearchRunResponse> => {
  const response = await api.post<ResearchRunResponse>('/run', payload);
  return response.data;
};

// 恢复被中断任务（审批）
export const resumeResearchRun = async (
  payload: ResumeResearchRunRequest
): Promise<ResearchRunResponse> => {
  const response = await api.post<ResearchRunResponse>('/resume', payload);
  return response.data;
};

// 查询任务详情
export const getResearchRunDetail = async (
  runId: string
): Promise<ResearchRunDetail> => {
  const response = await api.get<ResearchRunDetail>(`/run/${runId}`);
  return response.data;
};

export default api;
