'use client';
import { useEffect, useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { docApi, analysisApi } from '@/lib/api';
import Link from 'next/link';
import { FileText, Upload, AlertTriangle, Clock, MessageSquare, Scale, ChevronRight, Loader2 } from 'lucide-react';
import { fmtDate, getRiskClass, getRiskEmoji } from '@/lib/utils';

export default function DashboardPage() {
  const [docs, setDocs] = useState<any[]>([]);
  const [user, setUser] = useState<any>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    try { setUser(JSON.parse(localStorage.getItem('lb_user') || '{}')); } catch {}
    docApi.list().then(r => setDocs(r.data)).finally(() => setLoading(false));
  }, []);

  const analyzed = docs.filter(d => d.status === 'analyzed');
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';

  return (
    <AppShell>
      <div style={{ maxWidth: 1100, animation: 'fadeUp 0.4s ease-out' }}>
        {/* Welcome + intake desk */}
        <div className="legal-card" style={{ padding: 28, marginBottom: 20 }}>
          <h1 className="font-serif" style={{ fontSize: 26, fontWeight: 700, color: 'var(--navy)', marginBottom: 4 }}>
            {greeting}, {user?.name?.split(' ')[0] || 'there'}.
          </h1>
          <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.55)', marginBottom: 20 }}>What legal document would you like to understand today?</p>
          <div style={{ background: 'var(--parchment)', border: '2px dashed rgba(201,162,39,0.4)', borderRadius: 12, padding: '24px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16, flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{ width: 44, height: 44, borderRadius: 12, background: 'var(--navy)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Upload size={20} color="var(--gold)" />
              </div>
              <div>
                <p style={{ fontSize: 14, fontWeight: 600, color: 'var(--navy)' }}>Analyze a legal document</p>
                <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.5)' }}>PDF, DOCX, or TXT — Max 10MB</p>
              </div>
            </div>
            <Link href="/upload" className="btn-gold">Upload & Analyze <ChevronRight size={14} /></Link>
          </div>
        </div>

        {/* Stats row */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14, marginBottom: 20 }}>
          {[
            { label: 'Documents Uploaded', value: docs.length, icon: FileText, color: 'var(--navy)' },
            { label: 'Analyses Complete', value: analyzed.length, icon: Scale, color: 'var(--gold)' },
            { label: 'Pending Review', value: docs.filter(d => d.status === 'uploaded').length, icon: Clock, color: 'var(--terracotta)' },
            { label: 'High Risk Found', value: analyzed.filter(d => d.status === 'analyzed').length, icon: AlertTriangle, color: 'var(--burgundy)' },
          ].map(s => (
            <div key={s.label} className="legal-card" style={{ padding: '16px', textAlign: 'center' }}>
              <s.icon size={18} style={{ color: s.color, margin: '0 auto 8px' }} />
              <p style={{ fontSize: 24, fontWeight: 800, color: 'var(--navy)' }}>{s.value}</p>
              <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)' }}>{s.label}</p>
            </div>
          ))}
        </div>

        {/* Main grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
          {/* Case files */}
          <div className="legal-card" style={{ padding: 20 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
              <h3 className="font-serif" style={{ fontSize: 18, fontWeight: 700, color: 'var(--navy)' }}>Active Case Files</h3>
              <Link href="/analysis" style={{ fontSize: 12, color: 'var(--gold)', textDecoration: 'none', fontWeight: 600, display: 'flex', alignItems: 'center', gap: 4 }}>
                View all <ChevronRight size={12} />
              </Link>
            </div>

            {loading && <div style={{ textAlign: 'center', padding: 32 }}><Loader2 size={24} style={{ color: 'rgba(20,33,61,0.3)' }} className="animate-spin" /></div>}

            {!loading && docs.length === 0 && (
              <div style={{ textAlign: 'center', padding: '32px 20px' }}>
                <FileText size={32} style={{ color: 'rgba(20,33,61,0.2)', margin: '0 auto 12px' }} />
                <p style={{ fontSize: 14, fontWeight: 600, color: 'var(--navy)', marginBottom: 4 }}>No documents yet</p>
                <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.5)', marginBottom: 16 }}>Upload your first legal document to get started</p>
                <Link href="/upload" className="btn-navy" style={{ fontSize: 12, padding: '8px 16px' }}>Upload document</Link>
              </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {docs.slice(0, 5).map(doc => (
                <div key={doc.id} className="file-folder-card" style={{ padding: '14px 16px', display: 'flex', alignItems: 'center', gap: 12 }}>
                  <div style={{ width: 36, height: 36, borderRadius: 8, background: 'var(--parchment)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                    <FileText size={16} style={{ color: 'var(--navy)' }} />
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <p style={{ fontSize: 13, fontWeight: 600, color: 'var(--navy)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{doc.original_filename || doc.filename}</p>
                    <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)' }}>{doc.document_type} · {fmtDate(doc.created_at)}</p>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
                    <span style={{ fontSize: 11, padding: '3px 8px', borderRadius: 20, fontWeight: 600,
                      background: doc.status === 'analyzed' ? '#f0fdf4' : doc.status === 'analyzing' ? '#fffbeb' : '#f5f5f5',
                      color: doc.status === 'analyzed' ? '#16834A' : doc.status === 'analyzing' ? '#D97706' : '#666' }}>
                      {doc.status}
                    </span>
                    {doc.status === 'analyzed' ? (
                      <Link href={`/analysis/${doc.id}`} style={{ fontSize: 11, color: 'var(--gold)', textDecoration: 'none', fontWeight: 600 }}>View →</Link>
                    ) : doc.status === 'uploaded' ? (
                      <Link href="/upload" style={{ fontSize: 11, color: 'var(--navy)', textDecoration: 'none', fontWeight: 600 }}>Analyze</Link>
                    ) : null}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right column */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {/* Ask LawBridge */}
            <div className="legal-card" style={{ padding: 18, background: 'var(--navy)' }}>
              <h4 className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: 'white', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
                <MessageSquare size={15} color="var(--gold)" /> Ask LawBridge AI
              </h4>
              <p style={{ fontSize: 12, color: 'rgba(255,255,255,0.6)', marginBottom: 14, lineHeight: 1.6 }}>
                Ask any Indian law question — tenant rights, employment disputes, consumer complaints, FIR procedure, and more.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 14 }}>
                {['What are my tenant rights?', 'How to file a consumer complaint?', 'Can my employer monitor my device?'].map(q => (
                  <Link key={q} href={`/chat?q=${encodeURIComponent(q)}`}
                    style={{ fontSize: 11, padding: '6px 10px', background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(201,162,39,0.2)', borderRadius: 6, color: 'rgba(255,255,255,0.7)', textDecoration: 'none', display: 'block', lineHeight: 1.4, transition: 'all 0.15s' }}>
                    {q}
                  </Link>
                ))}
              </div>
              <Link href="/chat" className="btn-gold" style={{ width: '100%', justifyContent: 'center', fontSize: 12 }}>Open Chat Desk</Link>
            </div>

            {/* Know Your Rights */}
            <div className="legal-card" style={{ padding: 18 }}>
              <h4 className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>Know Your Rights</h4>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                {[{ emoji: '🏠', label: 'Tenant', href: '/rights?cat=tenant' }, { emoji: '💼', label: 'Employee', href: '/rights?cat=employee' }, { emoji: '🛒', label: 'Consumer', href: '/rights?cat=consumer' }, { emoji: '🔐', label: 'Digital', href: '/rights?cat=digital' }].map(r => (
                  <Link key={r.label} href={r.href}
                    style={{ padding: '10px 8px', background: 'var(--parchment)', borderRadius: 8, textAlign: 'center', textDecoration: 'none', border: '1px solid rgba(201,162,39,0.2)', transition: 'all 0.15s' }}>
                    <div style={{ fontSize: 18, marginBottom: 4 }}>{r.emoji}</div>
                    <p style={{ fontSize: 11, fontWeight: 600, color: 'var(--navy)' }}>{r.label}</p>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
