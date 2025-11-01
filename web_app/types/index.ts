export interface User {
  id: string;
  email: string;
  full_name: string;
  role?: string;
  created_at: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data: {
    token: string;
    user: User;
  };
}

export interface Job {
  id: string;
  title: string;
  company: string;
  company_logo?: string;
  location: string;
  job_type: string;
  category: string;
  experience_level: string;
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  description: string;
  skills: string[];
  qualifications: string[];
  responsibilities: string[];
  benefits?: string[];
  application_url: string;
  is_active: boolean;
  posted_at: string;
  created_at: string;
}

export interface Internship {
  id: string;
  title: string;
  company: string;
  company_logo?: string;
  location: string;
  internship_type: string;
  category: string;
  duration_months: number;
  stipend_min?: number;
  stipend_max?: number;
  stipend_currency?: string;
  description: string;
  skills: string[];
  qualifications: string[];
  learning_outcomes?: string[];
  responsibilities: string[];
  application_url: string;
  is_active: boolean;
  posted_at: string;
  created_at: string;
}

export interface Scholarship {
  id: string;
  title: string;
  provider: string;
  provider_logo?: string;
  country: string;
  scholarship_type: string;
  education_level: string;
  field_of_study: string;
  amount_min?: number;
  amount_max?: number;
  amount_currency?: string;
  description: string;
  eligibility_criteria: string[];
  benefits: string[];
  application_process: string[];
  application_url: string;
  deadline: string;
  is_active: boolean;
  created_at: string;
}

export interface Article {
  id: string;
  title: string;
  content: string;
  excerpt: string;
  author: string;
  author_avatar?: string;
  tags: string[];
  category: string;
  cover_image?: string;
  read_time: number;
  is_published: boolean;
  views_count: number;
  created_at: string;
  updated_at: string;
}

// DSA Types
export interface DSATopic {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  parent_topic?: string;
  question_count: number;
  is_active: boolean;
  created_at: string;
}

export interface DSAQuestion {
  id: string;
  title: string;
  description: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  topics: string[];
  companies: string[];
  examples: Array<{
    input: string;
    output: string;
    explanation?: string;
  }>;
  constraints?: string[];
  solution_approach?: string;
  code_solutions: Array<{
    language: string;
    code: string;
  }>;
  hints?: string[];
  time_complexity?: string;
  space_complexity?: string;
  acceptance_rate?: number;
  is_premium?: boolean;
  created_at: string;
}

export interface DSASheet {
  id: string;
  name: string;
  description: string;
  author: string;
  questions: Array<{
    question_id: string;
    order: number;
  }>;
  difficulty_breakdown: {
    easy: number;
    medium: number;
    hard: number;
  };
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  tags: string[];
  is_published: boolean;
  created_at: string;
  updated_at: string;
}

export interface DSACompany {
  id: string;
  name: string;
  logo?: string;
  industry: string;
  problem_count: number;
  job_count: number;
  is_active: boolean;
  created_at: string;
}

// Roadmap Types
export interface RoadmapNode {
  id: string;
  title: string;
  description: string;
  type: 'content' | 'roadmap_link' | 'article_link';
  position_x: number;
  position_y: number;
  content?: string;
  video_url?: string;
  resources?: Array<{
    title: string;
    url: string;
    type: string;
  }>;
  linked_roadmap_id?: string;
  linked_article_id?: string;
  connections: string[];
  is_completed?: boolean;
}

export interface Roadmap {
  id: string;
  title: string;
  description: string;
  category: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  estimated_time_hours: number;
  reading_time: number;
  nodes: RoadmapNode[];
  topics_covered: string[];
  is_published: boolean;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data: T;
  total?: number;
  page?: number;
  limit?: number;
}
