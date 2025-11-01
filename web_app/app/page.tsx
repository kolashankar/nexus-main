import Link from 'next/link';
import { Header } from '@/components/common/Header';
import { Footer } from '@/components/common/Footer';
import { Button } from '@/components/ui/Button';
import { Briefcase, BookOpen, Code, MapIcon, Users, MessageCircle, Linkedin, TrendingUp, FileText, Target, BarChart } from 'lucide-react';

export default function Home() {
  const communityLinks = [
    {
      icon: MessageCircle,
      title: 'WhatsApp',
      members: '46K+',
      href: '#',
      color: 'bg-green-500',
    },
    {
      icon: MessageCircle,
      title: 'Channel',
      members: '9K+',
      href: '#',
      color: 'bg-blue-500',
    },
    {
      icon: Linkedin,
      title: 'LinkedIn',
      members: '44K+',
      href: '#',
      color: 'bg-blue-600',
    },
  ];

  const quickAccessFeatures = [
    {
      icon: Briefcase,
      title: 'Find Jobs That Match Your Skills',
      description: 'Search through 50,000+ job opportunities from top companies.',
      ctaText: 'Browse Jobs',
      href: '/jobs',
      highlight: 'Adobe is hiring Software Development Engineer Freshers',
      highlightCompany: 'Adobe',
    },
    {
      icon: Code,
      title: 'Master Technical Interviews',
      description: 'Practice with 3000+ coding problems and company-specific questions.',
      ctaText: 'Start Practicing',
      href: '/dsa',
      highlight: 'Array',
      highlightCount: '1779',
    },
    {
      icon: FileText,
      title: 'AI-Powered Career Tools',
      description: 'Leverage cutting-edge AI to supercharge your job search.',
      ctaText: 'Resume Review',
      href: '/career-tools/resume-review',
      highlight: 'ATS-optimized',
      tools: ['Resume', 'Cover Letter', 'Auto Apply'],
    },
    {
      icon: Target,
      title: 'Track Your Progress & Build Profile',
      description: 'Monitor your job search journey and track applications.',
      ctaText: 'View Dashboard',
      href: '/profile',
      highlight: 'Your Applications',
    },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      
      <main className="flex-1">
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white py-20 md:py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold mb-6 leading-tight">
                India's #1 Freshers
                <br />
                <span className="text-yellow-300">Career Portal</span>
              </h1>
              <p className="text-xl md:text-2xl text-blue-100 mb-10 max-w-3xl mx-auto">
                Your one-stop platform for freshers jobs, internships, interview prep, and career growth.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/jobs">
                  <Button size="lg" className="w-full sm:w-auto bg-yellow-400 text-gray-900 hover:bg-yellow-300 font-semibold text-lg px-8 py-6">
                    Find Jobs
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Community Section */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-8 text-center">
              Join Our Community
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {communityLinks.map((link) => {
                const Icon = link.icon;
                return (
                  <Link
                    key={link.title}
                    href={link.href}
                    className="group p-8 bg-gradient-to-br from-gray-50 to-white rounded-2xl border-2 border-gray-200 hover:border-blue-500 hover:shadow-xl transition-all"
                  >
                    <div className={`${link.color} w-16 h-16 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                      <Icon className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {link.title}
                    </h3>
                    <p className="text-3xl font-extrabold text-blue-600">
                      {link.members}
                    </p>
                  </Link>
                );
              })}
            </div>
          </div>
        </section>

        {/* Quick Access Section */}
        <section className="py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12 text-center">
              Quick Access
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {quickAccessFeatures.map((feature) => {
                const Icon = feature.icon;
                return (
                  <div
                    key={feature.title}
                    className="bg-white rounded-2xl border border-gray-200 p-8 hover:shadow-xl transition-all"
                  >
                    <div className="flex items-start mb-6">
                      <div className="bg-blue-100 w-14 h-14 rounded-xl flex items-center justify-center mr-4">
                        <Icon className="h-7 w-7 text-blue-600" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">
                          {feature.title}
                        </h3>
                        <p className="text-gray-600 mb-4">
                          {feature.description}
                        </p>
                      </div>
                    </div>
                    
                    {feature.highlight && (
                      <div className="bg-blue-50 rounded-lg p-4 mb-4">
                        <p className="text-sm font-semibold text-blue-900">
                          {feature.highlight}
                          {feature.highlightCompany && (
                            <span className="ml-2 text-blue-600">{feature.highlightCompany}</span>
                          )}
                          {feature.highlightCount && (
                            <span className="ml-2 text-blue-600">{feature.highlightCount}</span>
                          )}
                        </p>
                      </div>
                    )}

                    {feature.tools && (
                      <div className="grid grid-cols-3 gap-3 mb-4">
                        {feature.tools.map((tool, idx) => (
                          <div key={tool} className={`text-center p-3 rounded-lg ${idx === 0 ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                            <p className="text-xs font-semibold">{tool}</p>
                            {idx === 0 && <p className="text-xs mt-1">ATS-optimized</p>}
                            {idx > 0 && <p className="text-xs mt-1">Coming Soon</p>}
                          </div>
                        ))}
                      </div>
                    )}
                    
                    <Link href={feature.href}>
                      <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold">
                        {feature.ctaText}
                      </Button>
                    </Link>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gradient-to-br from-gray-900 to-gray-800 text-white">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">
              Ready to Start Your Career Journey?
            </h2>
            <p className="text-xl text-gray-300 mb-10">
              Join thousands of students and professionals who found success with CareerGuide.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/jobs">
                <Button size="lg" className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white font-semibold text-lg px-8">
                  Find Jobs Now
                </Button>
              </Link>
              <Link href="/dsa">
                <Button size="lg" variant="outline" className="w-full sm:w-auto border-2 border-white text-white hover:bg-white hover:text-gray-900 font-semibold text-lg px-8">
                  Practice Coding
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
