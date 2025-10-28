import { useState, useCallback } from 'react';
import { toast } from 'react-toastify';
import SkillAbilities from '../components/traits/SkillAbilities';
import SuperpowerAbilities from '../components/traits/SuperpowerAbilities';
import GoodTraitAbilities from '../components/traits/GoodTraitAbilities';
import BadTraitAbilities from '../components/traits/BadTraitAbilities';
import MetaTraitAbilities from '../components/traits/MetaTraitAbilities';

export const useTraitAbilities = (player) => {
  const [isUsing, setIsUsing] = useState(false);
  const [lastUsedAbility, setLastUsedAbility] = useState(null);

  const handleAbilityUsed = useCallback((result) => {
    if (result.success) {
      toast.success(`Ability used successfully!`);
      setLastUsedAbility(result);
    } else {
      toast.error(result.message || 'Ability failed');
    }
    setIsUsing(false);
  }, []);

  const skillAbilities = SkillAbilities({ player, onAbilityUsed: handleAbilityUsed });
  const superpowerAbilities = SuperpowerAbilities({ player, onAbilityUsed: handleAbilityUsed });
  const goodTraitAbilities = GoodTraitAbilities({ player, onAbilityUsed: handleAbilityUsed });
  const badTraitAbilities = BadTraitAbilities({ player, onAbilityUsed: handleAbilityUsed });
  const metaTraitAbilities = MetaTraitAbilities({ player, onAbilityUsed: handleAbilityUsed });

  const useAbility = useCallback(async ({ traitName, abilityName, traitLevel, targets = [], params = {} }) => {
    if (isUsing) {
      toast.warn('Please wait for the current ability to complete');
      return;
    }

    setIsUsing(true);

    try {
      let result;

      // Route to appropriate ability handler based on trait name
      switch (traitName) {
        // Skills
        case 'Hacking':
          result = await skillAbilities.useHackingAbility(abilityName, targets[0]);
          break;
        case 'Negotiation':
          result = await skillAbilities.useNegotiationAbility(abilityName, targets);
          break;
        case 'Stealth':
          result = await skillAbilities.useStealthAbility(abilityName);
          break;
        case 'Leadership':
          result = await skillAbilities.useLeadershipAbility(abilityName, targets);
          break;

        // Superpowers
        case 'Meditation Superpower':
          result = await superpowerAbilities.useMeditationAbility(abilityName);
          break;
        case 'Telekinesis':
          result = await superpowerAbilities.useTelekinesisAbility(abilityName, targets, params);
          break;
        case 'Pyrokinesis':
          result = await superpowerAbilities.usePyrokinesisAbility(abilityName, targets, params);
          break;
        case 'Cryokinesis':
          result = await superpowerAbilities.useCryokinesisAbility(abilityName, targets, params);
          break;

        // Good Traits
        case 'Empathy':
          result = await goodTraitAbilities.useEmpathyAbility(abilityName, targets[0]);
          break;
        case 'Integrity':
          result = await goodTraitAbilities.useIntegrityAbility(abilityName);
          break;
        case 'Compassion':
          result = await goodTraitAbilities.useCompassionAbility(targets[0]);
          break;
        case 'Honesty':
          result = await goodTraitAbilities.useHonestyAbility(targets[0]);
          break;

        // Bad Traits
        case 'Envy':
          result = await badTraitAbilities.useEnvyAbility(targets[0]);
          break;
        case 'Wrath':
          result = await badTraitAbilities.useWrathAbility();
          break;
        case 'Sloth':
          result = await badTraitAbilities.useSlothAbility(abilityName, targets[0]);
          break;
        case 'Pride':
          result = await badTraitAbilities.usePrideAbility();
          break;

        // Meta Traits
        case 'Luck':
          result = await metaTraitAbilities.useLuckAbility(abilityName, params);
          break;
        case 'Resilience':
          result = await metaTraitAbilities.useResilienceAbility(abilityName, params);
          break;
        case 'Wisdom':
          result = await metaTraitAbilities.useWisdomAbility(abilityName, params);
          break;
        case 'Adaptability':
          result = await metaTraitAbilities.useAdaptabilityAbility(abilityName, params);
          break;

        default:
          throw new Error(`Unknown trait: ${traitName}`);
      }

      handleAbilityUsed(result);
      return result;
    } catch (error) {
      console.error('Failed to use ability:', error);
      toast.error(error.message || 'Failed to use ability');
      setIsUsing(false);
      throw error;
    }
  }, [isUsing, skillAbilities, superpowerAbilities, goodTraitAbilities, badTraitAbilities, metaTraitAbilities, handleAbilityUsed]);

  return {
    useAbility,
    isUsing,
    lastUsedAbility,
    ...skillAbilities,
    ...superpowerAbilities,
    ...goodTraitAbilities,
    ...badTraitAbilities,
    ...metaTraitAbilities
  };
};