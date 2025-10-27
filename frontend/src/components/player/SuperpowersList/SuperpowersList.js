import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Button } from '../../ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';
import superpowersService from '../../../services/superpowers/superpowersService';
import SuperpowerCard from './SuperpowerCard';
import { toast } from 'sonner';

const SuperpowersList = () => {
  const [superpowers, setSuperpowers] = useState(null);
  const [availablePowers, setAvailablePowers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSuperpowers();
    fetchAvailablePowers();
  }, []);

  const fetchSuperpowers = async () => {
    try {
      const data = await superpowersService.getSuperpowers();
      setSuperpowers(data);
    } catch (error) {
      console.error('Failed to fetch superpowers', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailablePowers = async () => {
    try {
      const data = await superpowersService.getAvailablePowers();
      setAvailablePowers(data);
    } catch (error) {
      console.error('Failed to fetch available powers', error);
    }
  };

  const handleUnlockPower = async (powerId) => {
    try {
      await superpowersService.unlockPower(powerId);
      toast.success('Superpower unlocked!');
      fetchSuperpowers();
      fetchAvailablePowers();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to unlock power');
    }
  };

  const handleEquipPower = async (powerId) => {
    try {
      await superpowersService.equipPower(powerId);
      toast.success('Power equipped!');
      fetchSuperpowers();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to equip power');
    }
  };

  const handleUsePower = async (powerId) => {
    try {
      const result = await superpowersService.usePower(powerId);
      toast.success(result.message);
      fetchSuperpowers();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to use power');
    }
  };

  if (loading) {
    return <div>Loading superpowers...</div>;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex justify-between items-center">
          Superpowers
          {superpowers && (
            <Badge>
              Unlocked ({superpowers.unlocked_powers.length}/{superpowers.total_powers})
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="unlocked">
          <TabsList>
            <TabsTrigger value="unlocked">Unlocked Powers</TabsTrigger>
            <TabsTrigger value="available">Available Powers</TabsTrigger>
          </TabsList>
          <TabsContent value="unlocked" className="mt-4">
            {superpowers && superpowers.unlocked_powers.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {superpowers.unlocked_powers.map((power) => (
                  <SuperpowerCard
                    key={power.power_id}
                    power={power}
                    isEquipped={superpowers.equipped_powers.includes(power.power_id)}
                    onEquip={() => handleEquipPower(power.power_id)}
                    onUse={() => handleUsePower(power.power_id)}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                No superpowers unlocked yet. Meet requirements to unlock powers!
              </div>
            )}
          </TabsContent>
          <TabsContent value="available" className="mt-4">
            <div className="space-y-4">
              {availablePowers.map((power) => (
                <Card key={power.power_id} className="p-4">
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-bold">{power.name}</h3>
                      <Badge variant="outline">{power.tier.replace('tier_', 'T')}</Badge>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">{power.description}</p>
                      <div className="mt-2">
                        <p className="text-xs font-semibold">Requirements:</p>
                        <ul className="list-disc list-inside text-xs">
                          {Object.entries(power.requirements).map(([trait, value]) => (
                            <li key={trait}>
                              {trait}: {value}%
                            </li>
                          ))}
                        </ul>
                      </div>
                      {power.eligible && (
                        <Button
                          size="sm"
                          className="mt-2"
                          onClick={() => handleUnlockPower(power.power_id)}
                        >
                          Unlock Power
                        </Button>
                      )}
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default SuperpowersList;