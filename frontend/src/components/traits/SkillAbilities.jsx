import React from 'react';
import { apiClient as api } from '../../services/api/client';

const SkillAbilities = ({ player, onAbilityUsed }) => {
  const useHackingAbility = async (abilityName, targetId) => {
    try {
      const response = await api.post('/api/traits/skills/hacking/use', {
        player_id: player.id,
        ability_name: abilityName,
        target_id: targetId,
        trait_level: player.traits?.skills?.find(s => s.name === 'Hacking')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Hacking ability failed:', error);
      throw error;
    }
  };

  const useNegotiationAbility = async (abilityName, targets) => {
    try {
      const response = await api.post('/api/traits/skills/negotiation/use', {
        player_id: player.id,
        ability_name: abilityName,
        targets: targets,
        trait_level: player.traits?.skills?.find(s => s.name === 'Negotiation')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Negotiation ability failed:', error);
      throw error;
    }
  };

  const useStealthAbility = async (abilityName) => {
    try {
      const response = await api.post('/api/traits/skills/stealth/use', {
        player_id: player.id,
        ability_name: abilityName,
        trait_level: player.traits?.skills?.find(s => s.name === 'Stealth')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Stealth ability failed:', error);
      throw error;
    }
  };

  const useLeadershipAbility = async (abilityName, targets) => {
    try {
      const response = await api.post('/api/traits/skills/leadership/use', {
        player_id: player.id,
        ability_name: abilityName,
        targets: targets,
        trait_level: player.traits?.skills?.find(s => s.name === 'Leadership')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Leadership ability failed:', error);
      throw error;
    }
  };

  return {
    useHackingAbility,
    useNegotiationAbility,
    useStealthAbility,
    useLeadershipAbility
  };
};

export default SkillAbilities;