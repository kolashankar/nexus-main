import React from 'react';
import { api } from '../../services/api';

const MetaTraitAbilities = ({ player, onAbilityUsed }) => {
  const useLuckAbility = async (abilityName, params = {}) => {
    try {
      const response = await api.post('/api/traits/meta/luck/use', {
        player_id: player.id,
        ability_name: abilityName,
        params: params,
        trait_level: player.traits?.meta?.find(t => t.name === 'Luck')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Luck ability failed:', error);
      throw error;
    }
  };

  const useResilienceAbility = async (abilityName, params = {}) => {
    try {
      const response = await api.post('/api/traits/meta/resilience/use', {
        player_id: player.id,
        ability_name: abilityName,
        params: params,
        trait_level: player.traits?.meta?.find(t => t.name === 'Resilience')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Resilience ability failed:', error);
      throw error;
    }
  };

  const useWisdomAbility = async (abilityName, params = {}) => {
    try {
      const response = await api.post('/api/traits/meta/wisdom/use', {
        player_id: player.id,
        ability_name: abilityName,
        params: params,
        trait_level: player.traits?.meta?.find(t => t.name === 'Wisdom')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Wisdom ability failed:', error);
      throw error;
    }
  };

  const useAdaptabilityAbility = async (abilityName, params = {}) => {
    try {
      const response = await api.post('/api/traits/meta/adaptability/use', {
        player_id: player.id,
        ability_name: abilityName,
        params: params,
        trait_level: player.traits?.meta?.find(t => t.name === 'Adaptability')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Adaptability ability failed:', error);
      throw error;
    }
  };

  return {
    useLuckAbility,
    useResilienceAbility,
    useWisdomAbility,
    useAdaptabilityAbility
  };
};

export default MetaTraitAbilities;