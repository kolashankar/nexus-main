"""React hook for advanced tasks management."""

import { useState, useEffect, useCallback } from 'react';
import advancedTaskService from '../services/advancedTaskService';
import { toast } from 'react-hot-toast';

export const useAdvancedTasks = () => {
  const [tasks, setTasks] = useState([]);
  const [dailyTasks, setDailyTasks] = useState([]);
  const [cooldowns, setCooldowns] = useState({});
  const [difficulties, setDifficulties] = useState(null);
  const [skillLevels, setSkillLevels] = useState({});
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load player's skill levels
  const loadSkillLevels = useCallback(async () => {
    try {
      const data = await advancedTaskService.getSkillLevels();
      setSkillLevels(data.skill_levels || {});
    } catch (err) {
      console.error('Failed to load skill levels:', err);
    }
  }, []);

  // Load appropriate difficulties
  const loadDifficulties = useCallback(async () => {
    try {
      const data = await advancedTaskService.getAppropriateDifficulties();
      setDifficulties(data);
    } catch (err) {
      console.error('Failed to load difficulties:', err);
    }
  }, []);

  // Load daily tasks
  const loadDailyTasks = useCallback(async () => {
    try {
      const data = await advancedTaskService.getDailyTasks();
      setDailyTasks(data.tasks || []);
    } catch (err) {
      console.error('Failed to load daily tasks:', err);
    }
  }, []);

  // Load cooldowns
  const loadCooldowns = useCallback(async () => {
    try {
      const data = await advancedTaskService.getTaskCooldowns();
      setCooldowns(data.cooldowns || {});
    } catch (err) {
      console.error('Failed to load cooldowns:', err);
    }
  }, []);

  // Load all game locations
  const loadLocations = useCallback(async () => {
    try {
      const data = await advancedTaskService.getAllLocations();
      setLocations(data.locations || []);
    } catch (err) {
      console.error('Failed to load locations:', err);
    }
  }, []);

  // Generate tasks
  const generateTasks = useCallback(async (taskType, count = 1) => {
    try {
      setLoading(true);
      setError(null);
      const data = await advancedTaskService.generateTasks(taskType, count);
      setTasks(data.tasks || []);
      toast.success(`Generated ${data.tasks?.length || 0} ${taskType} tasks!`);
      return data.tasks;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to generate tasks';
      setError(errorMsg);
      toast.error(errorMsg);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  // Validate skill requirements
  const validateSkills = useCallback(async (skillRequirements) => {
    try {
      const data = await advancedTaskService.validateSkillRequirements(skillRequirements);
      return data;
    } catch (err) {
      console.error('Failed to validate skills:', err);
      return { meets_requirements: false, missing_skills: [] };
    }
  }, []);

  // Get nearby locations
  const getNearbyLocations = useCallback(async (playerPosition) => {
    try {
      const data = await advancedTaskService.getNearbyLocations(playerPosition);
      return data.locations || [];
    } catch (err) {
      console.error('Failed to get nearby locations:', err);
      return [];
    }
  }, []);

  // Check if task type is on cooldown
  const isOnCooldown = useCallback((taskType) => {
    const cooldown = cooldowns[taskType];
    return cooldown?.on_cooldown || false;
  }, [cooldowns]);

  // Get cooldown info for task type
  const getCooldownInfo = useCallback((taskType) => {
    return cooldowns[taskType] || null;
  }, [cooldowns]);

  // Initial load
  useEffect(() => {
    loadSkillLevels();
    loadDifficulties();
    loadDailyTasks();
    loadCooldowns();
    loadLocations();
  }, [loadSkillLevels, loadDifficulties, loadDailyTasks, loadCooldowns, loadLocations]);

  // Auto-refresh cooldowns every minute
  useEffect(() => {
    const interval = setInterval(() => {
      loadCooldowns();
    }, 60000); // 60 seconds

    return () => clearInterval(interval);
  }, [loadCooldowns]);

  return {
    tasks,
    dailyTasks,
    cooldowns,
    difficulties,
    skillLevels,
    locations,
    loading,
    error,
    generateTasks,
    validateSkills,
    getNearbyLocations,
    isOnCooldown,
    getCooldownInfo,
    refreshDailyTasks: loadDailyTasks,
    refreshCooldowns: loadCooldowns,
    refreshSkillLevels: loadSkillLevels
  };
};
