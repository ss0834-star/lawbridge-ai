'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import AppShell from '@/components/layout/AppShell';
import { analysisApi, chatApi } from '@/lib/api';
import { AlertTriangle, MessageSquare, Scale, Loader2, FileText, Shield, ChevronRight, XCircle, CheckCircle } from 'lucide-react';
import { getRiskClass, getRiskEmoji, fmtDate } from '@/lib/utils';
import Link from 'next/link';

export default function AnalysisPage() {
  const { id } = useParams();
  const router = useRouter();
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeClause, setActiveClause] = useState<any>(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [err, setErr] = useState('');

  useEffect(() => {
    if (!id) return;
    analysisApi.get(Number(id)).then(r => { setAnalysis(r.data); if (r.data.clauses?.length) setActiveClause(r.data.clauses[0]); })
      .catch(e => setErr(e.response?.data?.detail || 'Analysis not found')).finally(() => setLoading(false));
  }, [id]);

  const startChat = async () => {
    const { data } = await chatApi.createSession(Number(id), 'English', 'document');
    router.push(`/chat?session=${data.id}`);
  };

  if (loading) return <AppShell><div style={{ display: 'flex', justifyContent: 'center', padding: 60 }}><Loader2 size={28} style={{ color: 'var(--navy)' }} className="animate-spin" /></div></AppShell>;
  if (err || !analysis) return <AppShell><div style={{ textAlign: 'center', padding: 60 }}><p style={{ color: '#dc2626' }}>{err || 'Not found'}</p><Link href="/upload" className="btn-navy" style={{ marginTop: 16, display: 'inline-flex' }}>Upload document</Link></div></AppShell>;

  const rc = getRiskClass(analysis.risk_category);

  return (
    <AppShell>
      {/* Top bar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h1 className="font-serif" style={{ fontSize: 22, fontWeight: 700, color: 'var(--navy)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            Analysis Report
          </h1>
          <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.5)' }}>Completed · {fmtDate(analysis.created_at)}</p>
        </div>
        <span className={`risk-stamp ${rc} animate-stamp`}>{getRiskEmoji(rc)} {analysis.risk_category} — {Math.round(analysis.overall_risk_score)}/100</span>
        <button onClick={startChat} className="btn-gold" style={{ fontSize: 12, padding: '8px 14px' }}><MessageSquare size={13} /> Ask AI about this</button>
      </div>

      {/* Score breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10, marginBottom: 16 }}>
        {[
          { label: 'Overall Score', value: Math.round(analysis.overall_risk_score), sub: analysis.risk_category },
          { label: 'Rule-based', value: Math.round(analysis.rule_based_score || 0), sub: 'India-specific checks' },
          { label: 'AI Analysis', value: Math.round(analysis.llm_score || 0), sub: 'LLM risk assessment' },
          { label: 'ML Score', value: Math.round(analysis.ml_score || 0), sub: 'Pattern detection' },
        ].map(s => (
          <div key={s.label} className="legal-card" style={{ padding: '12px 16px', textAlign: 'center' }}>
            <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)', marginBottom: 4 }}>{s.label}</p>
            <p style={{ fontSize: 26, fontWeight: 800, color: s.value >= 61 ? 'var(--burgundy)' : s.value >= 31 ? 'var(--terracotta)' : 'var(--forest)' }}>{s.value}</p>
            <p style={{ fontSize: 10, color: 'rgba(20,33,61,0.4)' }}>{s.sub}</p>
          </div>
        ))}
      </div>

      {/* Three-column workspace */}
      <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr 300px', gap: 14, height: 'calc(100vh - 340px)', minHeight: 500 }}>
        {/* Left: outline */}
        <div className="legal-card" style={{ padding: 16, overflowY: 'auto' }}>
          <p style={{ fontSize: 11, fontWeight: 700, color: 'rgba(20,33,61,0.4)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 12 }}>Document Outline</p>
          {[
            { key: 'overview', label: '📋 Summary', count: 0 },
            { key: 'clauses', label: '📄 Clauses', count: analysis.clauses?.length || 0 },
            { key: 'risks', label: '⚠️ Risks', count: analysis.risk_findings?.length || 0 },
            { key: 'missing', label: '❌ Missing', count: analysis.missing_clauses?.length || 0 },
            { key: 'negotiate', label: '🤝 Negotiate', count: analysis.negotiation_points?.length || 0 },
            { key: 'questions', label: '❓ Lawyer Qs', count: analysis.lawyer_questions?.length || 0 },
          ].map(item => (
            <button key={item.key} onClick={() => setActiveTab(item.key)}
              style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 10px', borderRadius: 8, marginBottom: 2, border: 'none', cursor: 'pointer', fontSize: 12, fontWeight: activeTab === item.key ? 600 : 400,
                background: activeTab === item.key ? 'var(--navy)' : 'transparent',
                color: activeTab === item.key ? 'white' : 'rgba(20,33,61,0.7)' }}>
              <span>{item.label}</span>
              {item.count > 0 && <span style={{ fontSize: 10, padding: '1px 6px', borderRadius: 10, background: activeTab === item.key ? 'rgba(255,255,255,0.2)' : 'var(--parchment)', color: activeTab === item.key ? 'white' : 'var(--navy)' }}>{item.count}</span>}
            </button>
          ))}

          <div className="gold-rule" />
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {analysis.clauses?.slice(0, 8).map((c: any) => (
              <button key={c.id} onClick={() => setActiveClause(c)}
                style={{ width: '100%', textAlign: 'left', padding: '6px 8px', borderRadius: 6, border: 'none', cursor: 'pointer', fontSize: 11, background: activeClause?.id === c.id ? 'var(--parchment)' : 'transparent',
                  borderLeft: `3px solid ${c.risk_level === 'critical' ? '#B42318' : c.risk_level === 'high' ? 'var(--terracotta)' : c.risk_level === 'medium' ? 'var(--gold)' : 'var(--forest)'}` }}>
                <span style={{ color: 'var(--navy)', fontWeight: 500 }}>§{c.clause_number} {c.title}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Center: main content */}
        <div className="legal-card" style={{ padding: 20, overflowY: 'auto' }}>
          {activeTab === 'overview' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div><h3 className="font-serif" style={{ fontSize: 18, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>Executive Summary</h3>
                <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.75)', lineHeight: 1.8 }}>{analysis.executive_summary}</p></div>
              <div className="gold-rule" />
              <div><h4 className="font-serif" style={{ fontSize: 15, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>What this means for you</h4>
                <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.75)', lineHeight: 1.8 }}>{analysis.what_it_means}</p></div>
              {analysis.important_dates?.length > 0 && (
                <div><h4 className="font-serif" style={{ fontSize: 15, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>⏰ Important Deadlines</h4>
                  {analysis.important_dates.map((d: any, i: number) => (
                    <div key={i} style={{ padding: '8px 12px', background: '#fffbeb', border: '1px solid #fcd34d', borderRadius: 6, fontSize: 12, color: '#92400e', marginBottom: 6 }}>{d.description}</div>
                  ))}</div>
              )}
              {analysis.financial_obligations?.length > 0 && (
                <div><h4 className="font-serif" style={{ fontSize: 15, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>💰 Financial Obligations</h4>
                  {analysis.financial_obligations.map((f: any, i: number) => (
                    <div key={i} style={{ padding: '8px 12px', background: '#f0fdf4', border: '1px solid #86efac', borderRadius: 6, fontSize: 12, color: '#166534', marginBottom: 6 }}>₹{f.amount} — {f.description}</div>
                  ))}</div>
              )}
            </div>
          )}

          {activeTab === 'clauses' && (
            <div>{analysis.clauses?.map((c: any) => (
              <div key={c.id} className={`clause-card ${c.risk_level}`} style={{ marginBottom: 12 }} onClick={() => setActiveClause(c)}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--navy)' }}>§{c.clause_number} {c.title}</p>
                  <span className={`risk-stamp ${c.risk_level}`}>{c.risk_level}</span>
                </div>
                <div style={{ background: 'var(--parchment)', borderRadius: 6, padding: '8px 12px', marginBottom: 8, fontSize: 12, fontFamily: 'JetBrains Mono, monospace', color: 'rgba(20,33,61,0.7)', lineHeight: 1.7 }}>{c.original_text?.slice(0, 200)}...</div>
                {c.risk_reason && <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.6)', display: 'flex', alignItems: 'center', gap: 4 }}><AlertTriangle size={10} />{c.risk_reason}</p>}
              </div>
            ))}</div>
          )}

          {activeTab === 'risks' && (
            <div>{analysis.risk_findings?.length === 0 && <div style={{ textAlign: 'center', padding: 40 }}><CheckCircle size={32} style={{ color: 'var(--forest)', margin: '0 auto 8px' }} /><p style={{ color: 'rgba(20,33,61,0.5)' }}>No specific risk patterns detected by rule engine.</p></div>}
              {analysis.risk_findings?.map((r: any) => (
                <div key={r.id} style={{ padding: '14px 16px', borderRadius: 10, marginBottom: 10, border: '1px solid', background: r.severity === 'critical' ? '#fef2f2' : r.severity === 'high' ? '#fff7ed' : r.severity === 'medium' ? '#fffbeb' : '#f0fdf4', borderColor: r.severity === 'critical' ? '#fca5a5' : r.severity === 'high' ? '#fdba74' : r.severity === 'medium' ? '#fcd34d' : '#86efac' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                    <span className={`risk-stamp ${r.severity}`}>{r.severity}</span>
                    <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--navy)' }}>{r.title}</p>
                  </div>
                  <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.7)', lineHeight: 1.6 }}>{r.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'missing' && (
            <div>{analysis.missing_clauses?.length === 0 && <p style={{ textAlign: 'center', color: 'rgba(20,33,61,0.5)', padding: 40 }}>No missing clauses detected.</p>}
              {analysis.missing_clauses?.map((m: any) => (
                <div key={m.id} style={{ padding: '14px 16px', background: '#fff7ed', border: '1px solid #fdba74', borderRadius: 10, marginBottom: 10 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                    <XCircle size={14} style={{ color: 'var(--terracotta)', flexShrink: 0 }} />
                    <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--navy)' }}>{m.clause_name}</p>
                    <span style={{ fontSize: 10, padding: '2px 6px', borderRadius: 10, background: 'var(--terracotta)', color: 'white', fontWeight: 700 }}>{m.priority}</span>
                  </div>
                  <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.7)', lineHeight: 1.6 }}>{m.why_important}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'negotiate' && (
            <div>{analysis.negotiation_points?.map((n: any) => (
              <div key={n.id} style={{ padding: '14px 16px', border: '1px solid rgba(201,162,39,0.3)', borderRadius: 10, marginBottom: 10, background: 'white' }}>
                <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--navy)', marginBottom: 10 }}>{n.title}</p>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 8 }}>
                  <div style={{ padding: '8px 10px', background: '#fef2f2', borderRadius: 6 }}>
                    <p style={{ fontSize: 10, fontWeight: 700, color: '#dc2626', marginBottom: 4 }}>CURRENT</p>
                    <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.7)', lineHeight: 1.5 }}>{n.current_text || 'As stated in document'}</p>
                  </div>
                  <div style={{ padding: '8px 10px', background: '#f0fdf4', borderRadius: 6 }}>
                    <p style={{ fontSize: 10, fontWeight: 700, color: '#16834A', marginBottom: 4 }}>SUGGESTED</p>
                    <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.7)', lineHeight: 1.5 }}>{n.suggested_change}</p>
                  </div>
                </div>
                {n.reason && <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.55)', lineHeight: 1.5 }}>{n.reason}</p>}
              </div>
            ))}</div>
          )}

          {activeTab === 'questions' && (
            <div>
              <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.5)', marginBottom: 16 }}>Bring these questions to your lawyer consultation:</p>
              {analysis.lawyer_questions?.map((q: any, i: number) => (
                <div key={q.id} style={{ display: 'flex', gap: 12, padding: '12px', background: 'var(--parchment)', borderRadius: 8, marginBottom: 8 }}>
                  <span style={{ width: 24, height: 24, borderRadius: '50%', background: 'var(--navy)', color: 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>{i + 1}</span>
                  <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.8)', lineHeight: 1.6 }}>{q.question}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right: AI brief panel */}
        <div className="legal-card" style={{ padding: 18, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div>
            <p style={{ fontSize: 11, fontWeight: 700, color: 'rgba(20,33,61,0.4)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 10 }}>AI Legal Brief</p>
            {activeClause ? (
              <div>
                <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>§{activeClause.clause_number} {activeClause.title}</p>
                <span className={`risk-stamp ${activeClause.risk_level}`} style={{ display: 'inline-flex', marginBottom: 10 }}>{activeClause.risk_level}</span>
                <div style={{ background: 'var(--parchment)', borderRadius: 8, padding: '10px 12px', marginBottom: 12 }}>
                  <p style={{ fontSize: 11, fontWeight: 700, color: 'rgba(20,33,61,0.5)', marginBottom: 4 }}>Plain English</p>
                  <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.8)', lineHeight: 1.7 }}>{activeClause.plain_english}</p>
                </div>
                {activeClause.risk_reason && (
                  <div style={{ padding: '8px 12px', background: '#fffbeb', border: '1px solid #fcd34d', borderRadius: 6, marginBottom: 12 }}>
                    <p style={{ fontSize: 11, fontWeight: 700, color: '#92400e', marginBottom: 4 }}>Why this matters</p>
                    <p style={{ fontSize: 12, color: '#78350f', lineHeight: 1.6 }}>{activeClause.risk_reason}</p>
                  </div>
                )}
                {activeClause.lawyer_review_recommended && (
                  <div style={{ padding: '8px 12px', background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: 6, display: 'flex', gap: 6, alignItems: 'center' }}>
                    <Shield size={12} style={{ color: '#dc2626', flexShrink: 0 }} />
                    <p style={{ fontSize: 11, color: '#dc2626', fontWeight: 600 }}>Lawyer review recommended for this clause</p>
                  </div>
                )}
                <button onClick={startChat} className="btn-navy" style={{ width: '100%', justifyContent: 'center', fontSize: 12, padding: '8px', marginTop: 10 }}>
                  <MessageSquare size={12} /> Ask about this clause
                </button>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: 24, color: 'rgba(20,33,61,0.4)' }}>
                <FileText size={24} style={{ margin: '0 auto 8px' }} />
                <p style={{ fontSize: 12 }}>Click a clause to see AI explanation</p>
              </div>
            )}
          </div>

          <div className="gold-rule" />

          <div>
            <p style={{ fontSize: 11, fontWeight: 700, color: 'rgba(20,33,61,0.4)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 8 }}>Quick Actions</p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              <button onClick={startChat} className="btn-gold" style={{ width: '100%', justifyContent: 'center', fontSize: 12, padding: '8px' }}>
                <MessageSquare size={12} /> Chat about this document
              </button>
              <Link href="/location" className="btn-ghost" style={{ width: '100%', justifyContent: 'center', fontSize: 12, padding: '8px', textDecoration: 'none' }}>
                <Scale size={12} /> Find a lawyer near me
              </Link>
            </div>
          </div>

          <div className="disclaimer-ribbon" style={{ fontSize: 11 }}>
            <AlertTriangle size={11} style={{ flexShrink: 0 }} />
            Not legal advice. Consult a qualified lawyer before signing.
          </div>
        </div>
      </div>
    </AppShell>
  );
}
