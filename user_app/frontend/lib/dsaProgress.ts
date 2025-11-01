import AsyncStorage from '@react-native-async-storage/async-storage';

const DSA_PROGRESS_KEY = '@careerguide_dsa_progress';

export interface QuestionProgress {
  questionId: string;
  status: 'unsolved' | 'attempted' | 'solved';
  attempts: number;
  lastAttemptedAt?: string;
  solvedAt?: string;
  notes?: string;
}

export interface SheetProgress {
  sheetId: string;
  completedQuestions: string[];
  totalQuestions: number;
  startedAt: string;
  lastUpdatedAt: string;
}

export interface DSAStats {
  totalSolved: number;
  easySolved: number;
  mediumSolved: number;
  hardSolved: number;
  streak: number;
  lastSolvedDate?: string;
}

// Get all question progress
export const getAllQuestionProgress = async (): Promise<QuestionProgress[]> => {
  try {
    const progressJson = await AsyncStorage.getItem(`${DSA_PROGRESS_KEY}_questions`);
    return progressJson ? JSON.parse(progressJson) : [];
  } catch (error) {
    console.error('Error getting question progress:', error);
    return [];
  }
};

// Get progress for specific question
export const getQuestionProgress = async (
  questionId: string
): Promise<QuestionProgress | null> => {
  const allProgress = await getAllQuestionProgress();
  return allProgress.find((p) => p.questionId === questionId) || null;
};

// Update question progress
export const updateQuestionProgress = async (
  questionId: string,
  status: QuestionProgress['status'],
  notes?: string
): Promise<boolean> => {
  try {
    const allProgress = await getAllQuestionProgress();
    const existingIndex = allProgress.findIndex((p) => p.questionId === questionId);

    const now = new Date().toISOString();
    let progressItem: QuestionProgress;

    if (existingIndex >= 0) {
      const existing = allProgress[existingIndex];
      progressItem = {
        ...existing,
        status,
        attempts: existing.attempts + 1,
        lastAttemptedAt: now,
        solvedAt: status === 'solved' ? now : existing.solvedAt,
        notes: notes || existing.notes,
      };
      allProgress[existingIndex] = progressItem;
    } else {
      progressItem = {
        questionId,
        status,
        attempts: 1,
        lastAttemptedAt: now,
        solvedAt: status === 'solved' ? now : undefined,
        notes,
      };
      allProgress.push(progressItem);
    }

    await AsyncStorage.setItem(`${DSA_PROGRESS_KEY}_questions`, JSON.stringify(allProgress));
    return true;
  } catch (error) {
    console.error('Error updating question progress:', error);
    return false;
  }
};

// Get all sheet progress
export const getAllSheetProgress = async (): Promise<SheetProgress[]> => {
  try {
    const progressJson = await AsyncStorage.getItem(`${DSA_PROGRESS_KEY}_sheets`);
    return progressJson ? JSON.parse(progressJson) : [];
  } catch (error) {
    console.error('Error getting sheet progress:', error);
    return [];
  }
};

// Get progress for specific sheet
export const getSheetProgress = async (sheetId: string): Promise<SheetProgress | null> => {
  const allProgress = await getAllSheetProgress();
  return allProgress.find((p) => p.sheetId === sheetId) || null;
};

// Update sheet progress
export const updateSheetProgress = async (
  sheetId: string,
  questionId: string,
  totalQuestions: number
): Promise<boolean> => {
  try {
    const allProgress = await getAllSheetProgress();
    const existingIndex = allProgress.findIndex((p) => p.sheetId === sheetId);

    const now = new Date().toISOString();

    if (existingIndex >= 0) {
      const existing = allProgress[existingIndex];
      if (!existing.completedQuestions.includes(questionId)) {
        existing.completedQuestions.push(questionId);
      }
      existing.lastUpdatedAt = now;
      existing.totalQuestions = totalQuestions;
      allProgress[existingIndex] = existing;
    } else {
      const newProgress: SheetProgress = {
        sheetId,
        completedQuestions: [questionId],
        totalQuestions,
        startedAt: now,
        lastUpdatedAt: now,
      };
      allProgress.push(newProgress);
    }

    await AsyncStorage.setItem(`${DSA_PROGRESS_KEY}_sheets`, JSON.stringify(allProgress));
    return true;
  } catch (error) {
    console.error('Error updating sheet progress:', error);
    return false;
  }
};

// Calculate DSA statistics
export const getDSAStats = async (): Promise<DSAStats> => {
  try {
    const allProgress = await getAllQuestionProgress();
    const solved = allProgress.filter((p) => p.status === 'solved');

    // Calculate streak
    let streak = 0;
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const sortedSolved = solved
      .filter((p) => p.solvedAt)
      .sort((a, b) => new Date(b.solvedAt!).getTime() - new Date(a.solvedAt!).getTime());

    if (sortedSolved.length > 0) {
      const lastSolved = new Date(sortedSolved[0].solvedAt!);
      lastSolved.setHours(0, 0, 0, 0);

      const diffDays = Math.floor((today.getTime() - lastSolved.getTime()) / (1000 * 60 * 60 * 24));

      if (diffDays <= 1) {
        // Count consecutive days
        let currentDate = new Date(lastSolved);
        for (const progress of sortedSolved) {
          const solvedDate = new Date(progress.solvedAt!);
          solvedDate.setHours(0, 0, 0, 0);

          if (Math.abs(currentDate.getTime() - solvedDate.getTime()) <= 24 * 60 * 60 * 1000) {
            streak++;
            currentDate = solvedDate;
          } else {
            break;
          }
        }
      }
    }

    return {
      totalSolved: solved.length,
      easySolved: 0, // Would need difficulty from API
      mediumSolved: 0,
      hardSolved: 0,
      streak,
      lastSolvedDate: sortedSolved.length > 0 ? sortedSolved[0].solvedAt : undefined,
    };
  } catch (error) {
    console.error('Error calculating DSA stats:', error);
    return {
      totalSolved: 0,
      easySolved: 0,
      mediumSolved: 0,
      hardSolved: 0,
      streak: 0,
    };
  }
};

// Get question status
export const getQuestionStatus = async (
  questionId: string
): Promise<'unsolved' | 'attempted' | 'solved'> => {
  const progress = await getQuestionProgress(questionId);
  return progress?.status || 'unsolved';
};

// Record question submission
export const recordQuestionSubmission = async (
  questionId: string,
  questionTitle: string,
  status: 'attempted' | 'solved'
): Promise<boolean> => {
  return await updateQuestionProgress(questionId, status);
};

// Toggle question completion in sheet
export const toggleSheetQuestion = async (
  sheetId: string,
  questionId: string,
  totalQuestions: number
): Promise<boolean> => {
  try {
    const sheetProgress = await getSheetProgress(sheetId);
    
    if (sheetProgress) {
      const index = sheetProgress.completedQuestions.indexOf(questionId);
      if (index > -1) {
        // Remove from completed
        sheetProgress.completedQuestions.splice(index, 1);
      } else {
        // Add to completed
        sheetProgress.completedQuestions.push(questionId);
      }
      sheetProgress.lastUpdatedAt = new Date().toISOString();
      
      const allProgress = await getAllSheetProgress();
      const sheetIndex = allProgress.findIndex((p) => p.sheetId === sheetId);
      if (sheetIndex > -1) {
        allProgress[sheetIndex] = sheetProgress;
        await AsyncStorage.setItem(`${DSA_PROGRESS_KEY}_sheets`, JSON.stringify(allProgress));
      }
    } else {
      return await updateSheetProgress(sheetId, questionId, totalQuestions);
    }
    
    return true;
  } catch (error) {
    console.error('Error toggling sheet question:', error);
    return false;
  }
};

// Check if question is completed in a sheet
export const isQuestionCompletedInSheet = async (
  sheetId: string,
  questionId: string
): Promise<boolean> => {
  const sheetProgress = await getSheetProgress(sheetId);
  return sheetProgress?.completedQuestions.includes(questionId) || false;
};
