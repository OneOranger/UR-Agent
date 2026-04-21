// 研究任务相关类型定义

export interface ResearchTaskState {
  runId: string;
  threadId: string;
  status: 'running' | 'interrupted' | 'completed';
  currentStage?: string;
  detail?: ResearchRunDetail;
}

export interface CreateResearchRunRequest {
  user_request: string;
}

export interface ResumeResearchRunRequest {
  thread_id: string;
  decision: 'approved' | 'rejected';
  comment: string;
}

export interface ResearchRunResponse {
  run_id: string;
  thread_id: string;
  status: 'running' | 'interrupted' | 'completed';
  message?: string;
  interrupts?: any[];
  result?: ResearchRunResult;
}

export interface ResearchRunResult {
  run_id: string;
  thread_id: string;
  current_stage: string;
  research_goal?: string;
  markdown_report_path?: string;
}

export interface ResearchRunDetail {
  run: {
    run_id: string;
    thread_id: string;
    user_request: string;
    current_stage: string;
    research_goal: string;
    markdown_report_path: string;
  };
  evidence_items: EvidenceItem[];
  themes: Theme[];
  insights: Insight[];
  personas: Persona[];
  journey_maps: JourneyMap[];
  recommendations: Recommendation[];
  report: Report | null;
  approvals: Approval[];
  traces: Trace[];
  eval_summary: EvalSummary;
  eval_records: EvalRecord[];
}

export interface EvidenceItem {
  evidence_id: string;
  source_type: string;
  source_name: string;
  raw_excerpt: string;
  normalized_text: string;
  confidence: number;
  is_simulated: boolean;
  tags: string[];
}

export interface Theme {
  theme_id: string;
  name: string;
  description: string;
  supporting_evidence_ids: string[];
  confidence_score: number;
}

export interface Insight {
  insight_id: string;
  statement: string;
  supporting_evidence_ids: string[];
  counter_evidence_ids: string[];
  confidence_score: number;
  severity: string;
  opportunity_area: string;
}

export interface Persona {
  persona_id: string;
  name: string;
  summary: string;
  goals: string[];
  pain_points: string[];
  behaviors: string[];
  motivations: string[];
  supporting_evidence_ids: string[];
}

export interface JourneyStage {
  stage_name: string;
  user_goal: string;
  user_actions: string[];
  touchpoints: string[];
  pain_points: string[];
  opportunities: string[];
  emotion: string;
}

export interface JourneyMap {
  journey_id: string;
  persona_name: string;
  overview: string;
  stages: JourneyStage[];
  supporting_evidence_ids: string[];
}

export interface Recommendation {
  recommendation_id: string;
  title: string;
  description: string;
  priority: string;
  rationale: string;
  related_opportunity_area: string;
  supporting_evidence_ids: string[];
}

export interface Report {
  title: string;
  background: string;
  research_goal: string;
  executive_summary: string;
  key_findings: string[];
  themes_summary: string[];
  personas_summary: string[];
  journey_summary: string[];
  methodology: string;
  recommendations: string[];
  limitations: string[];
  next_steps: string[];
}

export interface Approval {
  approval_type: string;
  decision: string;
  comment: string;
  stage_before: string;
  stage_after: string;
}

export interface Trace {
  event_name: string;
  payload: any;
}

export interface EvalSummary {
  overall_eval_score: number;
  overall_passed: boolean;
  evaluator_count: number;
}

export interface EvalRecord {
  evaluator_name: string;
  score: number;
  passed: boolean;
  detail: any;
}
