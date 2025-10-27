import React from "react";
import { useState, useEffect } from 'react';
import { toast } from '../ui/sonner';
import { Bell, CheckCircle2, XCircle, Info } from 'lucide-react';

export const QuestNotifications = () => {
  // eslint-disable-next-line no-unused-vars
  const [notifications, setNotifications] = useState([]);

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'quest_completed':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case 'quest_failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'quest_available':
      case 'objective_progress':
        return <Info className="w-5 h-5 text-blue-500" />;
      default:
        return <Bell className="w-5 h-5" />;
    }
  };

  const showToast = (notification) => {
    const icon = getNotificationIcon(notification.type);
    
    switch (notification.priority) {
      case 'high':
        toast.success(notification.title, {
          description: notification.message,
          icon,
        });
        break;
      case 'medium':
        toast.info(notification.title, {
          description: notification.message,
          icon,
        });
        break;
      case 'low':
      default:
        toast(notification.title, {
          description: notification.message,
          icon,
        });
        break;
    }
  };
  
  const createNotificationFromEvent = (event) => {
    switch (event.type) {
      case 'quest_completed':
        return {
          type: event.type,
          title: "Action",
          message: event.message,
          quest_id: event.quest_id,
          priority: 'high',
          timestamp: new Date().toISOString()
        };
      case 'objective_progress':
        return {
          type: event.type,
          title: "Action",
          message: event.message,
          quest_id: event.quest_id,
          priority: 'low',
          timestamp: new Date().toISOString()
        };
      case 'quest_available':
        return {
          type: event.type,
          title: "Action",
          message: event.message,
          quest_id: event.quest_id,
          priority: 'medium',
          timestamp: new Date().toISOString()
        };
      default:
        return null;
    }
  };
  
  useEffect(() => {
    // Listen for quest events via WebSocket or polling
    const handleQuestEvent = (event) => {
      const notification = createNotificationFromEvent(event);
      if (notification) {
        setNotifications(prev => [notification, ...prev.slice(0, 9)]);
        showToast(notification);
      }
    };
    
    // Example of triggering an event for demonstration
    // In a real app, this would come from a WebSocket or API call
    const timer = setTimeout(() => handleQuestEvent({type: 'quest_available', message: 'A new adventure awaits!', quest_id: 'q123'}), 2000);

    // Subscribe to quest events
    // window.addEventListener('quest_event', handleQuestEvent);

    return () => {
      // window.removeEventListener('quest_event', handleQuestEvent);
      clearTimeout(timer);
    };
  }, [showToast]);



  return null; // This component handles notifications via toasts
};

export const useQuestNotifications = () => {
  const notify = {
    questCompleted: (quest, rewards) => {
      toast.success('Quest Completed!', {
        description: `+${rewards.xp} XP, +${rewards.credits} Credits`,
        icon: <CheckCircle2 />,
      });
    },
    
    questAccepted: (quest) => {
      toast.info('Quest Accepted', {
        description: `Started: ${quest.title}`,
        icon: <Info />,
      });
    },
    
    questFailed: (quest) => {
      toast.error('Quest Failed', {
        description: `You failed: ${quest.title}`,
        icon: <XCircle />,
      });
    },
    
    objectiveProgress: (quest, objective, current, required) => {
      toast(`Objective Progress`, {
        description: `${objective}: ${current}/${required}`,
        icon: <Info />,
      });
    },
    
    hiddenQuestDiscovered: (quest) => {
      toast.success('Secret Discovered!', {
        description: `You found a hidden quest: ${quest.title}`,
        icon: <Info />,
      });
    }
  };

  return notify;
};
