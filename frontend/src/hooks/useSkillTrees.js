import React from "react";
import { useState, useEffect } from 'react';
import skillTreesService from '../services/skillTrees/skillTreesService';

export const useSkillTrees = () => {
  const [skillTrees, setSkillTrees] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSkillTrees = async () => {
    try {
      setLoading(true);
      const data = await skillTreesService.getSkillTrees();
      setSkillTrees(data);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillTrees();
  }, []);

  const unlockNode = async (traitName, nodeId) => {
    try {
      await skillTreesService.unlockNode({ trait_name: traitName, node_id: nodeId });
      await fetchSkillTrees();
      return { success: true };
    } catch (err) {
      return { success: false, error: err };
    }
  };

  const chooseBranch = async (traitName, branch) => {
    try {
      await skillTreesService.chooseBranch({ trait_name: traitName, branch });
      await fetchSkillTrees();
      return { success: true };
    } catch (err) {
      return { success: false, error: err };
    }
  };

  return {
    skillTrees,
    loading,
    error,
    refetch: fetchSkillTrees,
    unlockNode,
    chooseBranch,
  };
};
