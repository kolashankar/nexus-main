import React from 'react';
import { api } from '../../services/api';

const GoodTraitAbilities = ({ player, onAbilityUsed }) => {
  const useEmpathyAbility = async (abilityName, targetId) => {
    try {
      const response = await api.post('/api/traits/good/empathy/use', {
        player_id: player.id,
        ability_name: abilityName,
        target_id: targetId,
        trait_level: player.traits?.good?.find(t => t.name === 'Empathy')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Empathy ability failed:', error);
      throw error;
    }
  };

  const useIntegrityAbility = async (abilityName) => {
    try {
      const response = await api.post('/api/traits/good/integrity/use', {
        player_id: player.id,
        ability_name: abilityName,
        trait_level: player.traits?.good?.find(t => t.name === 'Integrity')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Integrity ability failed:', error);
      throw error;
    }
  };

  const useCompassionAbility = async (targetId) => {
    try {
      const response = await api.post('/api/traits/good/compassion/use', {
        player_id: player.id,
        target_id: targetId,
        trait_level: player.traits?.good?.find(t => t.name === 'Compassion')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Compassion ability failed:', error);
      throw error;
    }
  };

  const useHonestyAbility = async (targetId) => {
    try {
      const response = await api.post('/api/traits/good/honesty/use', {
        player_id: player.id,
        target_id: targetId,
        trait_level: player.traits?.good?.find(t => t.name === 'Honesty')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Honesty ability failed:', error);
      throw error;
    }
  };

  return {
    useEmpathyAbility,
    useIntegrityAbility,
    useCompassionAbility,
    useHonestyAbility
  };
};

export default GoodTraitAbilities;