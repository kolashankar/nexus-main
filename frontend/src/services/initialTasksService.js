/**
 * Initial tasks service for API calls
 */
import apiClient from './api/client';

class InitialTasksService {
  async getInitialTasks() {
    const response = await apiClient.get('/api/tasks/initial-tasks/');
    return response.data;
  }

  async completeTask(taskId, choiceIndex) {
    const response = await apiClient.post('/api/tasks/initial-tasks/complete', {
      task_id: taskId,
      choice_index: choiceIndex
    });
    return response.data;
  }

  async getProgress() {
    const response = await apiClient.get('/api/tasks/initial-tasks/progress');
    return response.data;
  }
}

export default new InitialTasksService();
