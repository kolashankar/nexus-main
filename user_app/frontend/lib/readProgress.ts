import AsyncStorage from '@react-native-async-storage/async-storage';

const READ_PROGRESS_KEY = '@careerguide_read_progress';

export interface ReadProgress {
  articleId: string;
  progress: number; // 0-100
  lastReadAt: string;
  completed: boolean;
}

export interface ArticleProgress {
  articleId: string;
  articleTitle: string;
  articleAuthor?: string;
  scrollProgress?: number; // 0-1
  lastReadAt: number;
  completedAt?: number;
}

// Get all read progress
export const getAllReadProgress = async (): Promise<ReadProgress[]> => {
  try {
    const progressJson = await AsyncStorage.getItem(READ_PROGRESS_KEY);
    return progressJson ? JSON.parse(progressJson) : [];
  } catch (error) {
    console.error('Error getting read progress:', error);
    return [];
  }
};

// Get progress for specific article
export const getArticleProgress = async (articleId: string): Promise<ReadProgress | null> => {
  const allProgress = await getAllReadProgress();
  return allProgress.find((p) => p.articleId === articleId) || null;
};

// Update read progress
export const updateReadProgress = async (
  articleId: string,
  progress: number
): Promise<boolean> => {
  try {
    const allProgress = await getAllReadProgress();
    const existingIndex = allProgress.findIndex((p) => p.articleId === articleId);

    const progressItem: ReadProgress = {
      articleId,
      progress,
      lastReadAt: new Date().toISOString(),
      completed: progress >= 90, // Consider 90% as completed
    };

    if (existingIndex >= 0) {
      allProgress[existingIndex] = progressItem;
    } else {
      allProgress.push(progressItem);
    }

    await AsyncStorage.setItem(READ_PROGRESS_KEY, JSON.stringify(allProgress));
    return true;
  } catch (error) {
    console.error('Error updating read progress:', error);
    return false;
  }
};

// Mark article as read
export const markAsRead = async (articleId: string): Promise<boolean> => {
  return await updateReadProgress(articleId, 100);
};

// Clear article progress
export const clearArticleProgress = async (articleId: string): Promise<boolean> => {
  try {
    const allProgress = await getAllReadProgress();
    const filtered = allProgress.filter((p) => p.articleId !== articleId);
    await AsyncStorage.setItem(READ_PROGRESS_KEY, JSON.stringify(filtered));
    return true;
  } catch (error) {
    console.error('Error clearing article progress:', error);
    return false;
  }
};

// Convert ReadProgress to ArticleProgress format for reading history
const convertToArticleProgress = (rp: ReadProgress, articleData?: any): ArticleProgress => {
  return {
    articleId: rp.articleId,
    articleTitle: articleData?.title || 'Article',
    articleAuthor: articleData?.author,
    scrollProgress: rp.progress / 100,
    lastReadAt: new Date(rp.lastReadAt).getTime(),
    completedAt: rp.completed ? new Date(rp.lastReadAt).getTime() : undefined,
  };
};

// Get in-progress articles with full info
export const getInProgressArticles = async (): Promise<ArticleProgress[]> => {
  const allProgress = await getAllReadProgress();
  return allProgress
    .filter((p) => !p.completed && p.progress > 0)
    .map(p => convertToArticleProgress(p))
    .sort((a, b) => b.lastReadAt - a.lastReadAt);
};

// Get completed articles with full info
export const getCompletedArticles = async (): Promise<ArticleProgress[]> => {
  const allProgress = await getAllReadProgress();
  return allProgress
    .filter((p) => p.completed)
    .map(p => convertToArticleProgress(p))
    .sort((a, b) => b.lastReadAt - a.lastReadAt);
};
