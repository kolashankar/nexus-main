import React from 'react';
import Link from 'next/link';

export function Footer() {
  const currentYear = new Date().getFullYear();

  const links = {
    products: [
      { name: 'Resume Review', href: '/career-tools/resume-review' },
      { name: 'DSA Corner', href: '/dsa' },
      { name: 'Jobs', href: '/jobs' },
      { name: 'Internships', href: '/jobs?type=internship' },
      { name: 'Fresher Jobs', href: '/jobs?type=fresher' },
      { name: 'Roadmaps', href: '/roadmaps' },
    ],
    resources: [
      { name: 'Articles', href: '/learning' },
    ],
    support: [
      { name: 'Contact Us', href: '/contact' },
    ],
    dsaInterviewPrep: [
      { name: 'DSA Questions', href: '/dsa/questions' },
      { name: 'DSA Sheets', href: '/dsa/sheets' },
      { name: 'Company Questions', href: '/dsa/companies' },
      { name: 'Topics', href: '/dsa/topics' },
    ],
    company: [
      { name: 'About', href: '/about' },
      { name: 'Contact', href: '/contact' },
      { name: 'Advertisement', href: '/advertisement' },
    ],
    legal: [
      { name: 'Privacy Policy', href: '/privacy' },
      { name: 'Terms & Conditions', href: '/terms' },
    ],
  };

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Main Footer Content */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 mb-12">
          {/* Products */}
          <div>
            <h3 className="text-white font-bold text-sm mb-4">Products</h3>
            <ul className="space-y-3">
              {links.products.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-400 hover:text-blue-400 transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-white font-bold text-sm mb-4">Resources</h3>
            <ul className="space-y-3">
              {links.resources.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-400 hover:text-blue-400 transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-white font-bold text-sm mb-4">Support</h3>
            <ul className="space-y-3">
              {links.support.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-400 hover:text-blue-400 transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* DSA & Interview Prep */}
          <div>
            <h3 className="text-white font-bold text-sm mb-4">DSA & Interview Prep</h3>
            <ul className="space-y-3">
              {links.dsaInterviewPrep.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-400 hover:text-blue-400 transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-white font-bold text-sm mb-4">Company</h3>
            <ul className="space-y-3">
              {links.company.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-400 hover:text-blue-400 transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-white font-bold text-sm mb-4">Legal</h3>
            <ul className="space-y-3">
              {links.legal.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-400 hover:text-blue-400 transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Brand Section */}
        <div className="border-t border-gray-800 pt-8 mb-8">
          <Link href="/" className="inline-block mb-4">
            <span className="text-2xl font-bold text-white">CareerGuide</span>
          </Link>
          <p className="text-sm text-gray-400 max-w-md">
            Your trusted platform to ace any job interviews, craft the perfect resumes, and land your dream jobs.
          </p>
        </div>

        {/* Bottom Footer */}
        <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-gray-400 mb-4 md:mb-0">
            © {currentYear} CareerGuide.in - All rights reserved
          </p>
          <div className="flex flex-wrap gap-4 text-sm">
            <Link href="/privacy" className="text-gray-400 hover:text-blue-400 transition-colors">
              Privacy Policy
            </Link>
            <Link href="/terms" className="text-gray-400 hover:text-blue-400 transition-colors">
              Terms & Conditions
            </Link>
            <Link href="/dsa" className="text-gray-400 hover:text-blue-400 transition-colors">
              Coding Practice
            </Link>
            <Link href="/profile" className="text-gray-400 hover:text-blue-400 transition-colors">
              My Profile
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
