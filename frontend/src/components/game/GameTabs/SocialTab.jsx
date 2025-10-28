import React, { useState } from 'react';
import { Users, UserPlus, MessageCircle, Shield, Swords, Heart, Trophy } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

/**
 * SocialTab - Friends, alliances, and social interactions
 */
const SocialTab = ({ player }) => {
  const [activeSection, setActiveSection] = useState('friends');

  // Sample data
  const onlinePlayers = [
    { id: 1, username: 'Virtuous Victor', level: 45, karma: 1250, status: 'In Combat' },
    { id: 2, username: 'Cunning Carl', level: 38, karma: -300, status: 'Trading' },
    { id: 3, username: 'Innocent Ivy', level: 22, karma: 800, status: 'Exploring' },
    { id: 4, username: 'Tactical Tara', level: 41, karma: 150, status: 'Online' },
  ];

  const friends = [
    { id: 1, username: 'Virtuous Victor', level: 45, online: true, lastSeen: 'Now' },
    { id: 3, username: 'Innocent Ivy', level: 22, online: true, lastSeen: 'Now' },
  ];

  const alliances = [
    { id: 1, name: 'Circle of Balance', members: 5, leader: 'Virtuous Victor', formed: '2 weeks ago' },
  ];

  const getKarmaColor = (karma) => {
    if (karma > 500) return 'text-green-400';
    if (karma < -200) return 'text-red-400';
    return 'text-yellow-400';
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Users className="w-5 h-5 text-blue-400" />
        <h3 className="text-xl font-bold text-white">Social</h3>
      </div>

      {/* Section Tabs */}
      <div className="flex gap-2 mb-4">
        <Button
          onClick={() => setActiveSection('friends')}
          variant={activeSection === 'friends' ? 'default' : 'outline'}
          size="sm"
          className="flex items-center gap-2"
        >
          <Heart className="w-4 h-4" />
          Friends
        </Button>
        <Button
          onClick={() => setActiveSection('online')}
          variant={activeSection === 'online' ? 'default' : 'outline'}
          size="sm"
          className="flex items-center gap-2"
        >
          <Users className="w-4 h-4" />
          Online
        </Button>
        <Button
          onClick={() => setActiveSection('alliances')}
          variant={activeSection === 'alliances' ? 'default' : 'outline'}
          size="sm"
          className="flex items-center gap-2"
        >
          <Shield className="w-4 h-4" />
          Alliances
        </Button>
      </div>

      {/* Friends Section */}
      {activeSection === 'friends' && (
        <div className="space-y-2">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-lg font-semibold text-white">Your Friends ({friends.length})</h4>
            <Button size="sm" variant="outline">
              <UserPlus className="w-4 h-4 mr-2" />
              Add Friend
            </Button>
          </div>

          {friends.map((friend) => (
            <Card key={friend.id} className="bg-gray-900/50 p-3 hover:bg-gray-800/50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center">
                      <span className="text-white font-bold">{friend.username[0]}</span>
                    </div>
                    {friend.online && (
                      <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-gray-900" />
                    )}
                  </div>
                  <div>
                    <h5 className="font-semibold text-white">{friend.username}</h5>
                    <p className="text-sm text-gray-400">Level {friend.level} • {friend.lastSeen}</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button size="sm" variant="outline">
                    <MessageCircle className="w-4 h-4" />
                  </Button>
                  <Button size="sm" variant="outline">
                    <Trophy className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Online Players Section */}
      {activeSection === 'online' && (
        <div className="space-y-2">
          <h4 className="text-lg font-semibold text-white mb-3">Online Players ({onlinePlayers.length})</h4>
          {onlinePlayers.map((playerItem) => (
            <Card key={playerItem.id} className="bg-gray-900/50 p-3 hover:bg-gray-800/50 transition-colors cursor-pointer">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold">{playerItem.username[0]}</span>
                  </div>
                  <div>
                    <h5 className="font-semibold text-white">{playerItem.username}</h5>
                    <p className="text-sm text-gray-400">Level {playerItem.level}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`text-sm font-semibold ${getKarmaColor(playerItem.karma)}`}>
                    Karma: {playerItem.karma}
                  </p>
                  <p className="text-xs text-gray-400">{playerItem.status}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Alliances Section */}
      {activeSection === 'alliances' && (
        <div className="space-y-2">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-lg font-semibold text-white">Your Alliances ({alliances.length})</h4>
            <Button size="sm" variant="outline">
              <Shield className="w-4 h-4 mr-2" />
              Form Alliance
            </Button>
          </div>

          {alliances.map((alliance) => (
            <Card key={alliance.id} className="bg-purple-900/30 border-purple-500/50 p-4">
              <div className="flex items-center gap-3 mb-3">
                <Shield className="w-6 h-6 text-purple-400" />
                <div>
                  <h5 className="font-bold text-white text-lg">{alliance.name}</h5>
                  <p className="text-sm text-gray-400">Led by {alliance.leader}</p>
                </div>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-300">{alliance.members} members</span>
                <span className="text-gray-400">Formed {alliance.formed}</span>
              </div>
              <div className="flex gap-2 mt-3">
                <Button size="sm" variant="outline" className="flex-1">
                  <MessageCircle className="w-4 h-4 mr-2" />
                  Chat
                </Button>
                <Button size="sm" variant="outline" className="flex-1">
                  <Swords className="w-4 h-4 mr-2" />
                  Activities
                </Button>
              </div>
            </Card>
          ))}

          {alliances.length === 0 && (
            <Card className="bg-gray-900/50 p-6 text-center">
              <Shield className="w-12 h-12 text-gray-600 mx-auto mb-3" />
              <p className="text-gray-400">You're not in any alliances yet</p>
              <p className="text-sm text-gray-500 mt-1">Form or join an alliance to gain strategic advantages</p>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

export default SocialTab;
