'use client';

import React, { useState } from 'react';
import { MessageCircle, Mail, Phone, Clock, HelpCircle, Book, Video, Send } from 'lucide-react';

export default function Support() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    alert('Support ticket submitted! We will get back to you soon.');
    setFormData({ name: '', email: '', subject: '', message: '' });
  };

  const faqs = [
    {
      question: 'How do I create a job posting?',
      answer: 'Navigate to Jobs > Create Job, fill in the required details, and click Save. You can also use AI generation for faster creation.'
    },
    {
      question: 'How do I use AI-powered career tools?',
      answer: 'Sign in to your account, go to Career Tools section, and select the tool you need (Resume Review, Cover Letter Generator, etc.). You must be authenticated to use these features.'
    },
    {
      question: 'Can I import jobs in bulk?',
      answer: 'Yes! Go to Bulk Operations > Import Jobs, and upload your CSV file with job data. Download our template for the correct format.'
    },
    {
      question: 'How do I manage user permissions?',
      answer: 'As an admin, navigate to Settings > User Management to add sub-admins, assign roles, and manage permissions.'
    },
    {
      question: 'How can I view analytics?',
      answer: 'Access the Analytics Dashboard from the main menu to view user engagement, job statistics, and API usage metrics.'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-sm p-8 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <MessageCircle className="w-10 h-10 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">Support Center</h1>
          </div>
          <p className="text-gray-600 text-lg">We're here to help! Get answers to your questions or contact our support team.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {/* Contact Methods */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-4">
              <Mail className="w-8 h-8 text-blue-600" />
              <h3 className="text-xl font-semibold text-gray-900">Email Support</h3>
            </div>
            <p className="text-gray-700 mb-2">support@careerguide.com</p>
            <p className="text-sm text-gray-500">Response within 24 hours</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-4">
              <Phone className="w-8 h-8 text-green-600" />
              <h3 className="text-xl font-semibold text-gray-900">Phone Support</h3>
            </div>
            <p className="text-gray-700 mb-2">+1 (555) 123-4567</p>
            <p className="text-sm text-gray-500">Mon-Fri, 9 AM - 6 PM EST</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-4">
              <Clock className="w-8 h-8 text-purple-600" />
              <h3 className="text-xl font-semibold text-gray-900">Live Chat</h3>
            </div>
            <p className="text-gray-700 mb-2">Available 24/7</p>
            <button className="text-blue-600 hover:text-blue-700 font-medium text-sm">
              Start Chat →
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* FAQ Section */}
          <div className="bg-white rounded-xl shadow-sm p-8">
            <div className="flex items-center gap-3 mb-6">
              <HelpCircle className="w-8 h-8 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-900">Frequently Asked Questions</h2>
            </div>
            
            <div className="space-y-4">
              {faqs.map((faq, index) => (
                <details key={index} className="group">
                  <summary className="cursor-pointer list-none">
                    <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{faq.question}</h3>
                      </div>
                      <span className="text-gray-500 group-open:rotate-180 transition-transform">▼</span>
                    </div>
                  </summary>
                  <div className="p-4 text-gray-700 bg-white border-l-4 border-blue-600 ml-4 mt-2">
                    {faq.answer}
                  </div>
                </details>
              ))}
            </div>

            {/* Resources */}
            <div className="mt-8 space-y-3">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Additional Resources</h3>
              <a href="#" className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
                <Book className="w-5 h-5 text-blue-600" />
                <span className="text-blue-700 font-medium">Documentation</span>
              </a>
              <a href="#" className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
                <Video className="w-5 h-5 text-purple-600" />
                <span className="text-purple-700 font-medium">Video Tutorials</span>
              </a>
            </div>
          </div>

          {/* Contact Form */}
          <div className="bg-white rounded-xl shadow-sm p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Send us a Message</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Your name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email *
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="your.email@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Subject *
                </label>
                <select
                  required
                  value={formData.subject}
                  onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select a subject</option>
                  <option value="technical">Technical Issue</option>
                  <option value="billing">Billing Question</option>
                  <option value="feature">Feature Request</option>
                  <option value="account">Account Management</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Message *
                </label>
                <textarea
                  required
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  rows={6}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Describe your issue or question..."
                />
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
              >
                <Send className="w-5 h-5" />
                Send Message
              </button>
            </form>

            <p className="text-sm text-gray-500 mt-4 text-center">
              We typically respond within 24 hours during business days.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}