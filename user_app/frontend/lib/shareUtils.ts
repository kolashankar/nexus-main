import * as Sharing from 'expo-sharing';
import * as FileSystem from 'expo-file-system';

export interface ShareContent {
  title: string;
  message: string;
  url?: string;
}

// Share text content
export const shareText = async (content: ShareContent): Promise<boolean> => {
  try {
    const isAvailable = await Sharing.isAvailableAsync();
    if (!isAvailable) {
      console.log('Sharing is not available on this device');
      return false;
    }

    const shareMessage = `${content.title}\n\n${content.message}${content.url ? `\n\n${content.url}` : ''}`;

    // Create a temporary text file
    const fileUri = `${FileSystem.cacheDirectory}share.txt`;
    await FileSystem.writeAsStringAsync(fileUri, shareMessage);

    await Sharing.shareAsync(fileUri, {
      mimeType: 'text/plain',
      dialogTitle: content.title,
    });

    return true;
  } catch (error) {
    console.error('Error sharing text:', error);
    return false;
  }
};

// Share job posting
export const shareJob = async (job: any): Promise<boolean> => {
  const content: ShareContent = {
    title: `Job: ${job.title} at ${job.company}`,
    message: `Check out this job opportunity!\n\nPosition: ${job.title}\nCompany: ${job.company}\nLocation: ${job.location}\nType: ${job.job_type}\nSalary: ${job.salary_range || 'Not specified'}\n\nFind it on CareerGuide app!`,
  };
  return await shareText(content);
};

// Share internship
export const shareInternship = async (internship: any): Promise<boolean> => {
  const content: ShareContent = {
    title: `Internship: ${internship.title} at ${internship.company}`,
    message: `Check out this internship opportunity!\n\nPosition: ${internship.title}\nCompany: ${internship.company}\nDuration: ${internship.duration}\nStipend: ${internship.stipend || 'Not specified'}\nType: ${internship.internship_type}\n\nFind it on CareerGuide app!`,
  };
  return await shareText(content);
};

// Share scholarship
export const shareScholarship = async (scholarship: any): Promise<boolean> => {
  const content: ShareContent = {
    title: `Scholarship: ${scholarship.title}`,
    message: `Check out this scholarship opportunity!\n\nName: ${scholarship.title}\nAmount: ${scholarship.amount}\nProvider: ${scholarship.provider}\nCountry: ${scholarship.country}\nEducation Level: ${scholarship.education_level}\n\nFind it on CareerGuide app!`,
  };
  return await shareText(content);
};

// Share article
export const shareArticle = async (article: any): Promise<boolean> => {
  const content: ShareContent = {
    title: article.title,
    message: `${article.excerpt}\n\nCategory: ${article.category}\nRead Time: ${article.read_time} min\n\nRead more on CareerGuide app!`,
  };
  return await shareText(content);
};

// Share DSA question
export const shareDSAQuestion = async (question: any): Promise<boolean> => {
  const content: ShareContent = {
    title: `DSA: ${question.title}`,
    message: `Check out this coding problem!\n\nProblem: ${question.title}\nDifficulty: ${question.difficulty}\nTopics: ${question.topics?.join(', ') || 'N/A'}\n\nPractice on CareerGuide app!`,
  };
  return await shareText(content);
};

// Share roadmap
export const shareRoadmap = async (roadmap: any): Promise<boolean> => {
  const content: ShareContent = {
    title: `Roadmap: ${roadmap.title}`,
    message: `Check out this learning roadmap!\n\nTitle: ${roadmap.title}\nCategory: ${roadmap.category}\nLevel: ${roadmap.level}\nEstimated Time: ${roadmap.estimated_time}\n\nExplore on CareerGuide app!`,
  };
  return await shareText(content);
};

// Share achievement/progress
export const shareAchievement = async (achievement: string, stats: any): Promise<boolean> => {
  const content: ShareContent = {
    title: 'My CareerGuide Progress',
    message: `${achievement}\n\n📊 My Stats:\n${Object.entries(stats).map(([key, value]) => `• ${key}: ${value}`).join('\n')}\n\nJoin me on CareerGuide app!`,
  };
  return await shareText(content);
};
