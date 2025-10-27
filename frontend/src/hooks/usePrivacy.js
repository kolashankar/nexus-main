import React from "react";
import { useState, useEffect } from 'react';
import { privacyService } from '../services/privacy/privacyService';

export const usePrivacy = () => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const data = await privacyService.getPrivacySettings();
      setSettings(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const updateSettings = async (newSettings) => {
    setLoading(true);
    try {
      const result = await privacyService.updatePrivacySettings(newSettings);
      setSettings(result);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const changeTier = async (tier) => {
    setLoading(true);
    try {
      const result = await privacyService.changePrivacyTier(tier);
      setSettings(result);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  return {
    settings,
    loading,
    error,
    updateSettings,
    changeTier,
    refreshSettings: fetchSettings,
  };
};
