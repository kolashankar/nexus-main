import React from "react";
/**
 * Analytics and tracking utilities
 */

class Analytics {
  constructor() {
    this.enabled = process.env.NODE_ENV === 'production';
    this.events = [];
  }

  /**
   * Track a page view
   */
  trackPageView(path, title) {
    if (!this.enabled) {
      console.log('[Analytics] Page view:', path, title);
      return;
    }

    // Google Analytics
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('config', 'GA_MEASUREMENT_ID', {
        page_path: path,
        page_title: title,
      });
    }
  }

  /**
   * Track a custom event
   */
  trackEvent(event) {
    if (!this.enabled) {
      console.log('[Analytics] Event:', event);
      return;
    }

    this.events.push(event);

    // Google Analytics
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', event.action, {
        event_category: event.category,
        event_label: event.label,
        value: event.value,
      });
    }
  }

  /**
   * Track user actions
   */
  trackUserAction(action, category = 'User', label, value) {
    this.trackEvent({ category, action, label, value });
  }

  /**
   * Track quest events
   */
  trackQuestEvent(action, questId, questType) {
    this.trackEvent({
      category: 'Quest',
      action: action,
      label: `${questId}-${questType || ''}`,
    });
  }

  /**
   * Track combat events
   */
  trackCombatEvent(action, opponentId) {
    this.trackEvent({
      category: 'Combat',
      action: action,
      label: opponentId || '',
    });
  }

  /**
   * Track guild events
   */
  trackGuildEvent(action, guildId) {
    this.trackEvent({
      category: 'Guild',
      action: action,
      label: guildId || '',
    });
  }

  /**
   * Track marketplace transactions
   */
  trackTransaction(action, itemType, amount) {
    this.trackEvent({
      category: 'Marketplace',
      action: action,
      label: itemType,
      value: amount,
    });
  }

  /**
   * Track errors
   */
  trackError(error, category = 'Error', fatal = false) {
    this.trackEvent({
      category: category,
      action: fatal ? 'Fatal Error' : 'Error',
      label: error.message || error.toString(),
    });

    // Send to error tracking service
    if (typeof window !== 'undefined' && window.Sentry) {
      window.Sentry.captureException(error);
    }
  }

  /**
   * Track performance metrics
   */
  trackPerformance(metric, value) {
    if (!this.enabled) {
      console.log(`[Analytics] Performance - ${metric}:`, value);
      return;
    }

    this.trackEvent({
      category: 'Performance',
      action: metric,
      value: Math.round(value),
    });
  }

  /**
   * Track user timing
   */
  trackTiming(category, variable, time, label) {
    if (!this.enabled) {
      console.log(`[Analytics] Timing - ${category}.${variable}:`, time);
      return;
    }

    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'timing_complete', {
        name: variable,
        value: Math.round(time),
        event_category: category,
        event_label: label,
      });
    }
  }

  /**
   * Set user properties
   */
  setUserProperties(properties) {
    if (!this.enabled) {
      console.log('[Analytics] User properties:', properties);
      return;
    }

    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('set', 'user_properties', properties);
    }
  }

  /**
   * Get tracked events (for debugging)
   */
  getEvents() {
    return this.events;
  }

  /**
   * Clear tracked events
   */
  clearEvents() {
    this.events = [];
  }
}

// Singleton instance
export const analytics = new Analytics();

/**
 * React hook for analytics
 */
export function useAnalytics() {
  return {
    trackPageView: analytics.trackPageView.bind(analytics),
    trackEvent: analytics.trackEvent.bind(analytics),
    trackUserAction: analytics.trackUserAction.bind(analytics),
    trackQuestEvent: analytics.trackQuestEvent.bind(analytics),
    trackCombatEvent: analytics.trackCombatEvent.bind(analytics),
    trackGuildEvent: analytics.trackGuildEvent.bind(analytics),
    trackTransaction: analytics.trackTransaction.bind(analytics),
    trackError: analytics.trackError.bind(analytics),
    trackPerformance: analytics.trackPerformance.bind(analytics),
  };
}
