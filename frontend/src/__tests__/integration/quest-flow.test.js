import React from "react";
/**
 * Integration test for quest flow
 */

import { questService } from '../../services/questService';

import { apiClient } from '../../services/api/client';

// Mock API client
jest.mock('../../services/api/client', () => ({
  apiClient: {
    get: jest.fn(),
    post: jest.fn(),
  },
}));

const mockQuest = {
  _id: 'quest123',
  title: 'Test Quest',
  description: 'Test description',
  quest_type: 'daily',
  status: 'available',
  objectives: [
    {
      type: 'defeat',
      current: 0,
      required: 5,
      completed: false,
    },
  ],
  rewards: {
    xp: 100,
    karma: 10,
  },
  difficulty: 'medium',
};

describe('Quest Flow Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('completes full quest lifecycle', async () => {
    // 1. Get available quests
    apiClient.get.mockResolvedValueOnce({
      data: [mockQuest],
    });

    const availableQuests = await questService.getAvailableQuests();
    expect(availableQuests).toHaveLength(1);
    expect(availableQuests[0]._id).toBe('quest123');

    // 2. Accept quest
    apiClient.post.mockResolvedValueOnce({
      data: { success: true, quest: { ...mockQuest, status: 'active' } },
    });

    const acceptResult = await questService.acceptQuest('quest123');
    expect(acceptResult.success).toBe(true);
    expect(apiClient.post).toHaveBeenCalledWith('/api/quests/accept', { quest_id: 'quest123' });

    // 3. Get active quests
    apiClient.get.mockResolvedValueOnce({
      data: [{ ...mockQuest, status: 'active' }],
    });

    const activeQuests = await questService.getActiveQuests();
    expect(activeQuests).toHaveLength(1);
    expect(activeQuests[0].status).toBe('active');

    // 4. Complete quest objectives (simulated)
    // In real scenario, this would happen through gameplay

    // 5. Get completed quests
    apiClient.get.mockResolvedValueOnce({
      data: [{ ...mockQuest, status: 'completed' }],
    });

    const completedQuests = await questService.getCompletedQuests();
    expect(completedQuests).toHaveLength(1);
    expect(completedQuests[0].status).toBe('completed');
  });

  it('handles quest abandonment', async () => {
    // Accept quest
    apiClient.post.mockResolvedValueOnce({
      data: { success: true },
    });

    await questService.acceptQuest('quest123');

    // Abandon quest
    apiClient.post.mockResolvedValueOnce({
      data: { success: true },
    });

    const result = await questService.abandonQuest('quest123');
    expect(result).toBe(true);
    expect(apiClient.post).toHaveBeenCalledWith('/api/quests/abandon', { quest_id: 'quest123' });
  });

  it('fetches quest details', async () => {
    apiClient.get.mockResolvedValueOnce({
      data: mockQuest,
    });

    const quest = await questService.getQuestDetails('quest123');
    expect(quest._id).toBe('quest123');
    expect(apiClient.get).toHaveBeenCalledWith('/api/quests/quest123');
  });

  it('handles daily quests', async () => {
    apiClient.get.mockResolvedValueOnce({
      data: [{ ...mockQuest, quest_type: 'daily' }],
    });

    const dailyQuests = await questService.getDailyQuests();
    expect(dailyQuests).toHaveLength(1);
    expect(dailyQuests[0].quest_type).toBe('daily');
  });

  it('handles weekly quests', async () => {
    apiClient.get.mockResolvedValueOnce({
      data: [{ ...mockQuest, quest_type: 'weekly' }],
    });

    const weeklyQuests = await questService.getWeeklyQuests();
    expect(weeklyQuests).toHaveLength(1);
    expect(weeklyQuests[0].quest_type).toBe('weekly');
  });

  it('handles guild quests', async () => {
    apiClient.get.mockResolvedValueOnce({
      data: {
        available: [mockQuest],
        active: [],
      },
    });

    const guildQuests = await questService.getGuildQuests();
    expect(guildQuests.available).toHaveLength(1);
    expect(guildQuests.active).toHaveLength(0);
  });

  it('handles campaign flow', async () => {
    const mockCampaign = {
      _id: 'campaign123',
      title: 'Test Campaign',
      description: 'Campaign description',
      total_chapters: 5,
      difficulty: 'hard',
      category: 'main',
    };

    apiClient.get.mockResolvedValueOnce({
      data: [mockCampaign],
    });

    const campaigns = await questService.getCampaigns();
    expect(campaigns).toHaveLength(1);

    // Start campaign
    apiClient.post.mockResolvedValueOnce({
      data: { success: true, progress: { chapter: 1 } },
    });

    const startResult = await questService.startCampaign('campaign123');
    expect(startResult.success).toBe(true);

    // Get current chapter
    apiClient.get.mockResolvedValueOnce({
      data: {
        chapter_number: 1,
        title: 'Chapter 1',
        description: 'First chapter',
        story_text: 'Story...',
        objectives: [],
        choices: [],
      },
    });

    const chapter = await questService.getCurrentChapter('campaign123');
    expect(chapter.chapter_number).toBe(1);
  });
});
