import React from 'react';
import { api } from '../../services/api';

const SuperpowerAbilities = ({ player, onAbilityUsed }) => {
  const useMeditationAbility = async (abilityName) => {
    try {
      const response = await api.post('/api/traits/superpowers/meditation/use', {
        player_id: player.id,
        ability_name: abilityName,
        trait_level: player.traits?.superpower_tools?.find(s => s.name === 'Meditation Superpower')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Meditation ability failed:', error);
      throw error;
    }
  };

  const useTelekinesisAbility = async (abilityName, targets, params = {}) => {
    try {
      const response = await api.post('/api/traits/superpowers/telekinesis/use', {
        player_id: player.id,
        ability_name: abilityName,
        targets: targets,
        params: params,
        trait_level: player.traits?.superpower_tools?.find(s => s.name === 'Telekinesis')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Telekinesis ability failed:', error);
      throw error;
    }
  };

  const usePyrokinesisAbility = async (abilityName, targets, params = {}) => {
    try {
      const response = await api.post('/api/traits/superpowers/pyrokinesis/use', {
        player_id: player.id,
        ability_name: abilityName,
        targets: targets,
        params: params,
        trait_level: player.traits?.superpower_tools?.find(s => s.name === 'Pyrokinesis')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Pyrokinesis ability failed:', error);
      throw error;
    }
  };

  const useCryokinesisAbility = async (abilityName, targets, params = {}) => {
    try {
      const response = await api.post('/api/traits/superpowers/cryokinesis/use', {
        player_id: player.id,
        ability_name: abilityName,
        targets: targets,
        params: params,
        trait_level: player.traits?.superpower_tools?.find(s => s.name === 'Cryokinesis')?.level || 1
      });

      onAbilityUsed && onAbilityUsed(response.data);
      return response.data;
    } catch (error) {
      console.error('Cryokinesis ability failed:', error);
      throw error;
    }
  };

  return {
    useMeditationAbility,
    useTelekinesisAbility,
    usePyrokinesisAbility,
    useCryokinesisAbility
  };
};

export default SuperpowerAbilities;