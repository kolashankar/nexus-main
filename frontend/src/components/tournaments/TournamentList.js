import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Trophy, Users, Calendar, DollarSign, Crown, Sword, Zap, TrendingUp, Clock, Award } from 'lucide-react';
import { useTournaments } from '../../hooks/useTournaments';
import { toast } from 'sonner';

const TournamentList = () => {
  const { tournaments, loading, registerForTournament, fetchActiveTournaments } = useTournaments();
  const [registering, setRegistering] = useState(null);

  useEffect(() => {
    fetchActiveTournaments();
  }, [fetchActiveTournaments]);

  const handleRegister = async (tournamentId) => {
    setRegistering(tournamentId);
    try {
      await registerForTournament(tournamentId);
      toast.success('Registered successfully!', {
        description: 'You are now registered for the tournament.',
      });
      await fetchActiveTournaments();
    } catch (error) {
      toast.error('Registration failed', {
        description: error.response?.data?.detail || 'Could not register for tournament.',
      });
    } finally {
      setRegistering(null);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      registration: 'bg-green-500',
      active: 'bg-blue-500',
      completed: 'bg-gray-500',
      upcoming: 'bg-yellow-500'
    };
    return colors[status] || 'bg-gray-500';
  };

  const getTournamentTypeIcon = (type) => {
    const icons = {
      pvp_combat: <Sword />,
      robot_battle: <Zap />,
      trading_competition: <TrendingUp />,
      quest_speedrun: <Clock />,
      creativity_contest: <Award />
    };
    return icons[type] || <Trophy />;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const canRegister = (tournament) => {
    const now = new Date();
    const regEnd = new Date(tournament.registration_end);
    return tournament.status === 'registration' && 
           now < regEnd && 
           tournament.total_registered < tournament.max_participants;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Tournaments</CardTitle>
        <CardDescription>Compete for glory and rewards</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : tournaments.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-center text-muted-foreground">
              <Trophy className="mx-auto w-12 h-12 mb-4" />
              <p className="font-semibold">No Active Tournaments</p>
              <p className="text-sm">Check back soon for upcoming competitions</p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {tournaments.map((tournament) => (
              <Card key={tournament.tournament_id} className="flex flex-col">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <CardTitle className="flex items-center gap-2">
                      {getTournamentTypeIcon(tournament.tournament_type)}
                      {tournament.name}
                    </CardTitle>
                    <Badge className={getStatusColor(tournament.status)}>
                      {tournament.status}
                    </Badge>
                  </div>
                  <CardDescription>
                    {tournament.description || 'No description'}
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex-grow space-y-4">
                  {/* Info Grid */}
                  <div className="grid grid-cols-3 gap-2 text-sm">
                    <div className="text-center">
                      <Users className="mx-auto" />
                      <p>{tournament.total_registered}/{tournament.max_participants}</p>
                    </div>
                    <div className="text-center">
                      <DollarSign className="mx-auto" />
                      <p>{tournament.prize_pool.toLocaleString()}</p>
                    </div>
                    <div className="text-center">
                      <Calendar className="mx-auto" />
                      <p>{formatDate(tournament.start_time)}</p>
                    </div>
                  </div>

                  {/* Requirements */}
                  {(tournament.min_level || tournament.min_karma || tournament.entry_fee > 0) && (
                    <div className="text-xs text-muted-foreground">
                      Requirements: Lvl {tournament.min_level}, Karma {tournament.min_karma}, {tournament.entry_fee} credits
                    </div>
                  )}

                  {/* Action Button */}
                  {canRegister(tournament) && (
                    <Button
                      onClick={() => handleRegister(tournament.tournament_id)}
                      disabled={registering === tournament.tournament_id}
                      className="w-full"
                    >
                      {registering === tournament.tournament_id ? 'Registering...' : 'Register'}
                    </Button>
                  )}
                  {tournament.status === 'active' && (
                    <Button variant="outline" className="w-full">
                      In Progress
                    </Button>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default TournamentList;