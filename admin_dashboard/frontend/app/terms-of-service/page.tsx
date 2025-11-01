'use client';

import React from 'react';
import { FileText, Scale, AlertCircle, CheckCircle, XCircle } from 'lucide-react';

export default function TermsOfService() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-sm p-8 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <Scale className="w-10 h-10 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">Terms of Service</h1>
          </div>
          <p className="text-gray-600 text-lg">Last updated: {new Date().toLocaleDateString()}</p>
        </div>

        {/* Content */}
        <div className="bg-white rounded-xl shadow-sm p-8 space-y-8">
          
          {/* Introduction */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Agreement to Terms</h2>
            <p className="text-gray-700 leading-relaxed">
              By accessing or using CareerGuide, you agree to be bound by these Terms of Service and all applicable 
              laws and regulations. If you do not agree with any of these terms, you are prohibited from using or 
              accessing this platform.
            </p>
          </section>

          {/* Account Registration */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle className="w-6 h-6 text-green-600" />
              <h2 className="text-2xl font-semibold text-gray-900">Account Registration</h2>
            </div>
            <div className="space-y-3 text-gray-700">
              <p>When you create an account with us, you agree to:</p>
              <ul className="list-disc list-inside space-y-2 ml-4">
                <li>Provide accurate, current, and complete information</li>
                <li>Maintain and promptly update your account information</li>
                <li>Maintain the security of your password and account</li>
                <li>Accept responsibility for all activities under your account</li>
                <li>Notify us immediately of any unauthorized use</li>
              </ul>
            </div>
          </section>

          {/* Use of Service */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Acceptable Use</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-medium text-gray-800 mb-2 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  You May:
                </h3>
                <ul className="list-disc list-inside space-y-2 ml-4 text-gray-700">
                  <li>Use the platform to search and apply for jobs</li>
                  <li>Create and manage your professional profile</li>
                  <li>Access career resources and learning materials</li>
                  <li>Interact with career tools and AI features</li>
                  <li>Contact support for assistance</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-xl font-medium text-gray-800 mb-2 flex items-center gap-2">
                  <XCircle className="w-5 h-5 text-red-600" />
                  You May Not:
                </h3>
                <ul className="list-disc list-inside space-y-2 ml-4 text-gray-700">
                  <li>Use the platform for any illegal purpose</li>
                  <li>Transmit any viruses, malware, or harmful code</li>
                  <li>Attempt to gain unauthorized access to the platform</li>
                  <li>Scrape or harvest data from the platform</li>
                  <li>Impersonate another person or entity</li>
                  <li>Submit false or misleading information</li>
                  <li>Spam or harass other users</li>
                  <li>Violate any intellectual property rights</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Intellectual Property */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-6 h-6 text-blue-600" />
              <h2 className="text-2xl font-semibold text-gray-900">Intellectual Property</h2>
            </div>
            <div className="space-y-3 text-gray-700">
              <p>
                The platform and its original content, features, and functionality are owned by CareerGuide and are 
                protected by international copyright, trademark, patent, trade secret, and other intellectual property laws.
              </p>
              <p>
                You retain ownership of content you submit to the platform (such as your resume and profile information), 
                but grant us a license to use, display, and process this content to provide our services.
              </p>
            </div>
          </section>

          {/* AI Services */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">AI-Powered Features</h2>
            <div className="space-y-3 text-gray-700">
              <p>
                Our platform uses AI technology (powered by Gemini) to provide career tools such as resume reviews, 
                cover letter generation, and ATS optimization.
              </p>
              <ul className="list-disc list-inside space-y-2 ml-4">
                <li>AI-generated content is provided for guidance purposes only</li>
                <li>You are responsible for reviewing and verifying all AI-generated content</li>
                <li>We do not guarantee the accuracy or suitability of AI-generated content</li>
                <li>Your use of AI features is subject to fair use policies</li>
              </ul>
            </div>
          </section>

          {/* Payment and Subscriptions */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Payment Terms</h2>
            <div className="space-y-3 text-gray-700">
              <p>If you subscribe to premium features:</p>
              <ul className="list-disc list-inside space-y-2 ml-4">
                <li>Payment is required in advance for subscription periods</li>
                <li>Subscriptions auto-renew unless cancelled</li>
                <li>Refunds are subject to our refund policy</li>
                <li>We reserve the right to change pricing with notice</li>
              </ul>
            </div>
          </section>

          {/* Limitation of Liability */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle className="w-6 h-6 text-orange-600" />
              <h2 className="text-2xl font-semibold text-gray-900">Limitation of Liability</h2>
            </div>
            <p className="text-gray-700 leading-relaxed">
              CareerGuide shall not be liable for any indirect, incidental, special, consequential, or punitive damages 
              resulting from your use of or inability to use the service. We do not guarantee job placement or interview 
              opportunities. Job listings are provided by third-party employers, and we are not responsible for their accuracy.
            </p>
          </section>

          {/* Termination */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Termination</h2>
            <div className="space-y-3 text-gray-700">
              <p>
                We may terminate or suspend your account and access to the platform immediately, without prior notice or 
                liability, for any reason, including breach of these Terms.
              </p>
              <p>
                Upon termination, your right to use the platform will cease immediately. You may close your account at 
                any time by contacting us.
              </p>
            </div>
          </section>

          {/* Changes to Terms */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Changes to Terms</h2>
            <p className="text-gray-700 leading-relaxed">
              We reserve the right to modify these terms at any time. We will notify you of any changes by posting the 
              new Terms of Service on this page and updating the "Last updated" date. Your continued use of the platform 
              after changes constitutes acceptance of the new terms.
            </p>
          </section>

          {/* Governing Law */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Governing Law</h2>
            <p className="text-gray-700 leading-relaxed">
              These Terms shall be governed by and construed in accordance with the laws of the jurisdiction in which 
              CareerGuide operates, without regard to its conflict of law provisions.
            </p>
          </section>

          {/* Contact */}
          <section className="bg-blue-50 rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Contact Information</h2>
            <p className="text-gray-700 leading-relaxed mb-3">
              If you have any questions about these Terms of Service, please contact us:
            </p>
            <ul className="space-y-2 text-gray-700">
              <li><strong>Email:</strong> legal@careerguide.com</li>
              <li><strong>Phone:</strong> +1 (555) 123-4567</li>
              <li><strong>Address:</strong> 123 Career Street, Business District, City, Country</li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
}