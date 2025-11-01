import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CareerGuide Admin Dashboard',
  description: 'Admin dashboard for CareerGuide job portal',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
