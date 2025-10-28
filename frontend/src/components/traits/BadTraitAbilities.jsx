import React from 'react';
import { api } from '../../services/api';

const BadTraitAbilities = ({ player, onAbilityUsed }) => {
  const useEnvyAbility = async (targetId) => {
    try {
      const response = await api.post('/api/traits/bad/envy/use', {
        player_id: player.id,
        target_id: targetId,
        trait_level: player.traits?.bad?.find(t => t.name === 'Envy')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Envy ability failed:', error);
      throw error;
    }
  };

  const useWrathAbility = async () => {
    try {
      const response = await api.post('/api/traits/bad/wrath/use', {
        player_id: player.id,
        trait_level: player.traits?.bad?.find(t => t.name === 'Wrath')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Wrath ability failed:', error);
      throw error;
    }
  };

  const useSlothAbility = async (abilityName, targetId) => {
    try {
      const response = await api.post('/api/traits/bad/sloth/use', {
        player_id: player.id,
        ability_name: abilityName,
        target_id: targetId,
        trait_level: player.traits?.bad?.find(t => t.name === 'Sloth')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Sloth ability failed:', error);
      throw error;
    }
  };

  const usePrideAbility = async () => {
    try {
      const response = await api.post('/api/traits/bad/pride/use', {
        player_id: player.id,
        trait_level: player.traits?.bad?.find(t => t.name === 'Pride')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Pride ability failed:', error);
      throw error;
    }
  };

  return {
    useEnvyAbility,
    useWrathAbility,
    useSlothAbility,
    usePrideAbility
  };
};

export default BadTraitAbilities;