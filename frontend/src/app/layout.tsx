import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {
  title: 'LawBridge AI — India\'s Legal Document Intelligence Platform',
  description: 'Understand every clause before it becomes your problem. AI-powered legal document analysis for India.',
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
