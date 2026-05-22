'use client';
import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { LayoutDashboard, FileText, MessageSquare, MapPin, Shield, Scale, Settings, LogOut, Upload, BookOpen, AlertTriangle, ChevronRight } from 'lucide-react';

const RAIL = [
  { href: '/dashboard', icon: LayoutDashboard, label: 'Legal Desk' },
  { href: '/upload', icon: Upload, label: 'Upload Document' },
  { href: '/analysis', icon: FileText, label: 'Documents' },
  { href: '/chat', icon: MessageSquare, label: 'Ask LawBridge' },
  { href: '/rights', icon: BookOpen, label: 'Know Your Rights' },
  { href: '/location', icon: MapPin, label: 'Legal Help Near Me' },
];

const TABS: Record<string, { label: string; tabs: { href: string; label: string }[] }> = {
  '/dashboard': { label: 'Legal Desk', tabs: [] },
  '/upload': { label: 'Upload Document', tabs: [] },
  '/analysis': { label: 'Documents', tabs: [{ href: '/analysis', label: 'All Documents' }] },
  '/chat': { label: 'Ask LawBridge', tabs: [{ href: '/chat?mode=general', label: 'General Legal Q&A' }, { href: '/chat?mode=document', label: 'Document Chat' }] },
  '/rights': { label: 'Know Your Rights', tabs: [] },
  '/location': { label: 'Legal Help Near Me', tabs: [] },
};

export default function AppShell({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<any>({});
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (!localStorage.getItem('lb_token')) { router.push('/login'); return; }
    try { setUser(JSON.parse(localStorage.getItem('lb_user') || '{}')); } catch {}
  }, [router]);

  const logout = () => {
    localStorage.removeItem('lb_token'); localStorage.removeItem('lb_user');
    router.push('/login');
  };

  const currentBase = '/' + pathname.split('/')[1];
  const currentSection = TABS[currentBase] || { label: 'LawBridge AI', tabs: [] };

  if (!mounted) return null;

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {/* Top command bar */}
      <div className="top-command-bar flex-shrink-0">
        <div className="flex items-center gap-2.5 flex-shrink-0">
          <div className="w-7 h-7 rounded-lg bg-gold flex items-center justify-center">
            <Scale size={14} className="text-navy" />
          </div>
          <span className="font-serif text-white text-lg font-semibold">LawBridge <span className="text-gold">AI</span></span>
        </div>
        <div className="w-px h-5 bg-white/10 mx-2 flex-shrink-0" />
        <span className="text-white/50 text-xs font-medium flex-shrink-0">My Legal Desk</span>
        <div className="flex-1" />
        <Link href="/upload" className="btn-gold py-1.5 px-3 text-xs flex-shrink-0">
          <Upload size={12} /> Upload
        </Link>
        <div className="flex items-center gap-2 ml-2">
          <div className="w-7 h-7 rounded-full bg-white/10 flex items-center justify-center text-white text-xs font-semibold flex-shrink-0">
            {user?.name?.[0] || 'U'}
          </div>
          <span className="text-white/70 text-xs hidden md:block">{user?.name || 'User'}</span>
          <button onClick={logout} className="text-white/40 hover:text-white/70 transition-colors ml-1 flex-shrink-0">
            <LogOut size={14} />
          </button>
        </div>
      </div>

      {/* Main area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Icon rail */}
        <div className="icon-rail flex-shrink-0">
          {RAIL.map(item => {
            const active = pathname === item.href || pathname.startsWith(item.href + '/');
            return (
              <Link key={item.href} href={item.href} title={item.label}
                className={`icon-rail-btn ${active ? 'active' : ''}`}>
                <item.icon size={18} />
              </Link>
            );
          })}
          <div className="flex-1" />
          {user?.role === 'admin' && (
            <Link href="/admin" title="Admin" className={`icon-rail-btn ${pathname.startsWith('/admin') ? 'active' : ''}`}>
              <Shield size={18} />
            </Link>
          )}
          <Link href="/dashboard" title="Settings" className="icon-rail-btn">
            <Settings size={18} />
          </Link>
        </div>

        {/* Content area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Workspace tabs */}
          {currentSection.tabs.length > 0 && (
            <div className="workspace-tabs flex-shrink-0">
              {currentSection.tabs.map(tab => (
                <Link key={tab.href} href={tab.href}
                  className={`workspace-tab ${pathname === tab.href ? 'active' : ''}`}>
                  {tab.label}
                </Link>
              ))}
            </div>
          )}

          {/* Disclaimer ribbon */}
          <div className="px-5 pt-3 flex-shrink-0">
            <div className="disclaimer-ribbon">
              <AlertTriangle size={12} className="flex-shrink-0 mt-0.5 text-amber-600" />
              <span>Not legal advice — this tool explains documents and identifies possible risks. Consult a qualified lawyer before making legal decisions.</span>
            </div>
          </div>

          {/* Page content */}
          <main className="flex-1 overflow-y-auto px-5 py-4">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
