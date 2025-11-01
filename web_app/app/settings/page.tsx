"use client";

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { 
  ArrowLeft, 
  User, 
  Bell, 
  Shield, 
  Database, 
  Palette,
  Mail,
  Lock,
  Trash2,
  Moon,
  Sun,
  Globe,
  Clock
} from 'lucide-react';
import toast from 'react-hot-toast';

type SettingsSection = 'account' | 'notifications' | 'privacy' | 'data' | 'preferences';

export default function SettingsPage() {
  const router = useRouter();
  const { user, isAuthenticated, logout } = useAuthStore();
  const [activeSection, setActiveSection] = useState<SettingsSection>('account');
  const [settings, setSettings] = useState({
    // Notifications
    emailNotifications: true,
    jobAlerts: true,
    articleUpdates: false,
    dsaReminders: true,
    
    // Privacy
    profileVisibility: 'public',
    dataSharing: false,
    cookies: true,
    
    // Preferences
    theme: 'system',
    language: 'en',
    timezone: 'UTC',
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  const handleSettingChange = (key: string, value: any) => {
    setSettings({ ...settings, [key]: value });
    toast.success('Setting updated successfully');
  };

  const handleClearCache = () => {
    localStorage.clear();
    toast.success('Cache cleared successfully');
  };

  const handleClearSearchHistory = () => {
    toast.success('Search history cleared');
  };

  const handleDownloadData = () => {
    toast.success('Data download started');
  };

  const handleDeleteAccount = () => {
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      logout();
      toast.success('Account deletion requested');
      router.push('/');
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  const sections = [
    { id: 'account', label: 'Account', icon: User },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'privacy', label: 'Privacy', icon: Shield },
    { id: 'data', label: 'Data & Storage', icon: Database },
    { id: 'preferences', label: 'Preferences', icon: Palette },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-4">
            <Link href="/profile" className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-4 sticky top-24">
              <nav className="space-y-2">
                {sections.map((section) => {
                  const Icon = section.icon;
                  return (
                    <button
                      key={section.id}
                      onClick={() => setActiveSection(section.id as SettingsSection)}
                      className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                        activeSection === section.id
                          ? 'bg-indigo-50 text-indigo-600'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="font-medium">{section.label}</span>
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>

          {/* Content */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-md p-6">
              {/* Account Section */}
              {activeSection === 'account' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Account Settings</h2>
                    <p className="text-gray-600 mb-6">Manage your account information and preferences</p>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                      <input
                        type="text"
                        value={user?.name || ''}
                        disabled
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                      <div className="flex items-center space-x-2">
                        <Mail className="w-5 h-5 text-gray-400" />
                        <input
                          type="email"
                          value={user?.email || ''}
                          disabled
                          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"
                        />
                      </div>
                    </div>

                    <div className="pt-4 border-t">
                      <button className="flex items-center text-indigo-600 hover:text-indigo-700 font-medium">
                        <Lock className="w-4 h-4 mr-2" />
                        Change Password
                      </button>
                    </div>

                    <div className="pt-4 border-t">
                      <button
                        onClick={handleDeleteAccount}
                        className="flex items-center text-red-600 hover:text-red-700 font-medium"
                      >
                        <Trash2 className="w-4 h-4 mr-2" />
                        Delete Account
                      </button>
                      <p className="text-sm text-gray-500 mt-2">Permanently delete your account and all data</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications Section */}
              {activeSection === 'notifications' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Notification Settings</h2>
                    <p className="text-gray-600 mb-6">Manage how you receive notifications</p>
                  </div>

                  <div className="space-y-4">
                    {[
                      { key: 'emailNotifications', label: 'Email Notifications', description: 'Receive notifications via email' },
                      { key: 'jobAlerts', label: 'Job Alerts', description: 'Get notified about new job postings' },
                      { key: 'articleUpdates', label: 'Article Updates', description: 'Updates on your favorite topics' },
                      { key: 'dsaReminders', label: 'DSA Challenge Reminders', description: 'Daily coding challenge reminders' },
                    ].map((item) => (
                      <div key={item.key} className="flex items-center justify-between py-3 border-b">
                        <div>
                          <p className="font-medium text-gray-900">{item.label}</p>
                          <p className="text-sm text-gray-500">{item.description}</p>
                        </div>
                        <button
                          onClick={() => handleSettingChange(item.key, !settings[item.key as keyof typeof settings])}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            settings[item.key as keyof typeof settings] ? 'bg-indigo-600' : 'bg-gray-200'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              settings[item.key as keyof typeof settings] ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Privacy Section */}
              {activeSection === 'privacy' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Privacy Settings</h2>
                    <p className="text-gray-600 mb-6">Control your privacy and data sharing</p>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Profile Visibility</label>
                      <select
                        value={settings.profileVisibility}
                        onChange={(e) => handleSettingChange('profileVisibility', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="public">Public</option>
                        <option value="private">Private</option>
                        <option value="friends">Friends Only</option>
                      </select>
                    </div>

                    {[
                      { key: 'dataSharing', label: 'Data Sharing', description: 'Share analytics data for improvement' },
                      { key: 'cookies', label: 'Cookie Preferences', description: 'Allow cookies for better experience' },
                    ].map((item) => (
                      <div key={item.key} className="flex items-center justify-between py-3 border-b">
                        <div>
                          <p className="font-medium text-gray-900">{item.label}</p>
                          <p className="text-sm text-gray-500">{item.description}</p>
                        </div>
                        <button
                          onClick={() => handleSettingChange(item.key, !settings[item.key as keyof typeof settings])}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            settings[item.key as keyof typeof settings] ? 'bg-indigo-600' : 'bg-gray-200'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              settings[item.key as keyof typeof settings] ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Data & Storage Section */}
              {activeSection === 'data' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Data & Storage</h2>
                    <p className="text-gray-600 mb-6">Manage your data and storage</p>
                  </div>

                  <div className="space-y-4">
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-sm font-medium text-gray-700 mb-2">Storage Usage</p>
                      <p className="text-2xl font-bold text-gray-900">2.3 MB</p>
                    </div>

                    <button
                      onClick={handleClearCache}
                      className="w-full py-3 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-left"
                    >
                      <p className="font-medium text-gray-900">Clear Cache</p>
                      <p className="text-sm text-gray-500">Remove temporary files and data</p>
                    </button>

                    <button
                      onClick={handleClearSearchHistory}
                      className="w-full py-3 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-left"
                    >
                      <p className="font-medium text-gray-900">Clear Search History</p>
                      <p className="text-sm text-gray-500">Remove all search history</p>
                    </button>

                    <button
                      onClick={handleDownloadData}
                      className="w-full py-3 px-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                    >
                      Download My Data
                    </button>
                  </div>
                </div>
              )}

              {/* Preferences Section */}
              {activeSection === 'preferences' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Preferences</h2>
                    <p className="text-gray-600 mb-6">Customize your experience</p>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                        <Moon className="w-4 h-4 mr-2" />
                        Theme
                      </label>
                      <select
                        value={settings.theme}
                        onChange={(e) => handleSettingChange('theme', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                        <option value="system">System</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                        <Globe className="w-4 h-4 mr-2" />
                        Language
                      </label>
                      <select
                        value={settings.language}
                        onChange={(e) => handleSettingChange('language', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                        <Clock className="w-4 h-4 mr-2" />
                        Timezone
                      </label>
                      <select
                        value={settings.timezone}
                        onChange={(e) => handleSettingChange('timezone', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="UTC">UTC</option>
                        <option value="EST">Eastern Time</option>
                        <option value="PST">Pacific Time</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* About Section */}
            <div className="mt-8 bg-white rounded-lg shadow-md p-6">
              <h3 className="font-bold text-gray-900 mb-4">About CareerGuide</h3>
              <div className="space-y-2 text-sm text-gray-600">
                <p><strong>Version:</strong> 1.0.0</p>
                <div className="flex space-x-4 pt-2">
                  <Link href="/privacy" className="text-indigo-600 hover:text-indigo-700">Privacy Policy</Link>
                  <Link href="/terms" className="text-indigo-600 hover:text-indigo-700">Terms of Service</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
