'use client';
import Link from 'next/link';
import { useState } from 'react';
import { Scale, FileText, AlertTriangle, Shield, MapPin, BookOpen, ChevronRight, CheckCircle, ArrowRight, MessageSquare } from 'lucide-react';

const DOC_FOLDERS = [
  { type: 'Rental Agreement', color: '#1F5C4D', icon: '🏠', risks: 'Security deposit, eviction, lock-in' },
  { type: 'Employment Contract', color: '#14213D', icon: '💼', risks: 'Non-compete, bonds, IP ownership' },
  { type: 'NDA', color: '#C9A227', icon: '🔒', risks: 'Perpetual terms, broad scope, penalties' },
  { type: 'Legal Notice', color: '#7A1E2C', icon: '⚖️', risks: 'Deadlines, claims, required actions' },
  { type: 'Loan Document', color: '#B86B4B', icon: '💰', risks: 'Hidden charges, guarantors, default' },
  { type: 'Service Agreement', color: '#4A5568', icon: '📋', risks: 'Payment terms, IP, termination' },
];

const ANNOTATIONS = [
  { text: '⚠ HIGH RISK: One-sided termination clause — employer can exit immediately with no notice', color: '#7A1E2C', bg: '#fef2f2', top: '15%', x: 'right' },
  { text: '❌ MISSING: Notice period protection not specified for employee', color: '#B86B4B', bg: '#fff7ed', top: '38%', x: 'right' },
  { text: '💬 ASK LAWYER: Is this non-compete enforceable in your state?', color: '#1F5C4D', bg: '#f0fdf4', top: '60%', x: 'right' },
];

const STEPS = [
  { n: '01', title: 'Upload Document', desc: 'PDF, DOCX, or TXT. We extract and parse all text securely.' },
  { n: '02', title: 'AI Reads Every Clause', desc: 'India-specific risk patterns + LLM analysis + ML classifier.' },
  { n: '03', title: 'Risk Docket Generated', desc: 'Stamped risk score, clause breakdown, missing protections.' },
  { n: '04', title: 'Prepare for Your Lawyer', desc: 'Negotiation points, lawyer questions, plain-English explanations.' },
];

export default function LandingPage() {
  const [hovered, setHovered] = useState<number | null>(null);

  return (
    <div className="min-h-screen" style={{ background: 'var(--ivory)', fontFamily: 'Manrope, system-ui, sans-serif' }}>

      {/* Nav */}
      <nav style={{ background: 'white', borderBottom: '1px solid rgba(201,162,39,0.2)', position: 'sticky', top: 0, zIndex: 50 }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 24px', height: 64, display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{ width: 32, height: 32, borderRadius: 8, background: 'var(--navy)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Scale size={16} color="var(--gold)" />
            </div>
            <span className="font-serif" style={{ fontSize: 20, fontWeight: 600, color: 'var(--navy)' }}>LawBridge <span style={{ color: 'var(--gold)' }}>AI</span></span>
          </div>
          <div style={{ flex: 1, display: 'flex', justifyContent: 'center', gap: 32 }}>
            <a href="#how" style={{ fontSize: 13, color: 'rgba(20,33,61,0.6)', textDecoration: 'none', fontWeight: 500 }}>How it works</a>
            <a href="#documents" style={{ fontSize: 13, color: 'rgba(20,33,61,0.6)', textDecoration: 'none', fontWeight: 500 }}>Documents</a>
            <Link href="/rights" style={{ fontSize: 13, color: 'rgba(20,33,61,0.6)', textDecoration: 'none', fontWeight: 500 }}>Know Your Rights</Link>
            <Link href="/location" style={{ fontSize: 13, color: 'rgba(20,33,61,0.6)', textDecoration: 'none', fontWeight: 500 }}>Legal Help</Link>
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            <Link href="/login" className="btn-ghost" style={{ padding: '8px 16px', fontSize: 13 }}>Sign in</Link>
            <Link href="/register" className="btn-navy" style={{ padding: '8px 18px', fontSize: 13 }}>Get started free</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section style={{ padding: '80px 24px 60px', maxWidth: 1200, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, background: '#fffbeb', border: '1px solid #fcd34d', borderRadius: 20, padding: '4px 14px', fontSize: 12, color: '#92400e', fontWeight: 500, marginBottom: 24 }}>
            <AlertTriangle size={11} /> India-first legal document AI — not legal advice
          </div>
          <h1 className="font-serif" style={{ fontSize: 'clamp(36px, 5vw, 64px)', fontWeight: 700, color: 'var(--navy)', lineHeight: 1.1, marginBottom: 20 }}>
            Understand every clause<br />
            <span style={{ color: 'var(--gold)', fontStyle: 'italic' }}>before it becomes your problem.</span>
          </h1>
          <p style={{ fontSize: 16, color: 'rgba(20,33,61,0.65)', maxWidth: 600, margin: '0 auto 40px', lineHeight: 1.7 }}>
            Upload rental agreements, employment contracts, NDAs, or legal notices. Get plain-English risk analysis, missing protection alerts, and questions to ask your lawyer — in minutes.
          </p>

          {/* Intake desk */}
          <div style={{ maxWidth: 680, margin: '0 auto', background: 'white', border: '2px solid rgba(201,162,39,0.3)', borderRadius: 16, padding: 24, boxShadow: '0 8px 32px rgba(20,33,61,0.08)' }}>
            <div style={{ background: 'var(--parchment)', border: '2px dashed rgba(201,162,39,0.4)', borderRadius: 12, padding: '28px 20px', marginBottom: 16, textAlign: 'center' }}>
              <FileText size={28} color="var(--gold)" style={{ marginBottom: 8 }} />
              <p style={{ fontSize: 15, fontWeight: 600, color: 'var(--navy)', marginBottom: 4 }}>Drop your legal document here</p>
              <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.5)' }}>PDF · DOCX · TXT — Max 10MB</p>
            </div>
            <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
              <select className="lb-input" style={{ flex: 1 }}>
                <option>Select document type...</option>
                {DOC_FOLDERS.map(d => <option key={d.type}>{d.type}</option>)}
              </select>
              <select className="lb-input" style={{ width: 140, flexShrink: 0 }}>
                <option>English</option>
                <option>Hindi</option>
                <option>Tamil</option>
                <option>Telugu</option>
              </select>
              <Link href="/register" className="btn-navy" style={{ flexShrink: 0, whiteSpace: 'nowrap' }}>
                Analyze <ArrowRight size={14} />
              </Link>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', gap: 28, marginTop: 20 }}>
            {['Not legal advice', 'Built for India', 'Private & secure'].map(t => (
              <div key={t} style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12, color: 'rgba(20,33,61,0.5)' }}>
                <CheckCircle size={12} color="var(--forest)" /> {t}
              </div>
            ))}
          </div>
        </div>

        {/* Document annotation showcase */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, alignItems: 'center', marginTop: 40, background: 'white', borderRadius: 20, border: '1px solid rgba(201,162,39,0.2)', padding: 32, boxShadow: '0 4px 24px rgba(20,33,61,0.06)' }}>
          <div>
            <p style={{ fontSize: 11, fontWeight: 700, color: 'rgba(20,33,61,0.4)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 8 }}>Sample Analysis</p>
            <h2 className="font-serif" style={{ fontSize: 28, fontWeight: 700, color: 'var(--navy)', marginBottom: 4 }}>Employment Contract</h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 20 }}>
              <span className="risk-stamp high animate-stamp">🔴 HIGH RISK — Score: 71/100</span>
            </div>
            <div className="gold-rule" />
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {ANNOTATIONS.map((a, i) => (
                <div key={i} style={{ padding: '10px 14px', borderRadius: 8, background: a.bg, border: `1px solid ${a.color}33`, fontSize: 12, color: a.color, fontWeight: 500, lineHeight: 1.5 }}>
                  {a.text}
                </div>
              ))}
            </div>
            <div className="disclaimer-ribbon" style={{ marginTop: 16, fontSize: 11 }}>
              <AlertTriangle size={11} /> Not legal advice. Consult a lawyer before signing.
            </div>
          </div>
          <div style={{ background: 'var(--parchment)', borderRadius: 12, padding: 20, fontFamily: 'JetBrains Mono, monospace', fontSize: 11, color: 'rgba(20,33,61,0.7)', lineHeight: 1.8, position: 'relative', border: '1px solid rgba(201,162,39,0.2)' }}>
            <p style={{ fontFamily: 'Cormorant Garamond, serif', fontSize: 15, fontWeight: 600, color: 'var(--navy)', marginBottom: 12, borderBottom: '1px solid rgba(201,162,39,0.3)', paddingBottom: 10 }}>Employment Agreement</p>
            <p><span style={{ color: 'var(--gold)', fontWeight: 600 }}>Clause 5: Termination</span></p>
            <p style={{ background: '#fef2f266', borderLeft: '2px solid #B42318', paddingLeft: 8, marginBottom: 8 }}>The Company may terminate this agreement at any time without cause or prior notice...</p>
            <p><span style={{ color: 'var(--gold)', fontWeight: 600 }}>Clause 8: Non-Compete</span></p>
            <p style={{ background: '#fff7ed66', borderLeft: '2px solid #B86B4B', paddingLeft: 8, marginBottom: 8 }}>Employee shall not engage in any competing business for a period of 2 years...</p>
            <p><span style={{ color: 'var(--gold)', fontWeight: 600 }}>Clause 12: IP Ownership</span></p>
            <p style={{ background: '#fffef566', borderLeft: '2px solid #C9A227', paddingLeft: 8 }}>All inventions, designs, and work product shall be the exclusive property of the Company...</p>
          </div>
        </div>
      </section>

      {/* Document folder tiles */}
      <section id="documents" style={{ background: 'white', borderTop: '1px solid rgba(201,162,39,0.15)', borderBottom: '1px solid rgba(201,162,39,0.15)', padding: '60px 24px' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 40 }}>
            <h2 className="font-serif" style={{ fontSize: 36, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>Every document type covered</h2>
            <p style={{ fontSize: 14, color: 'rgba(20,33,61,0.6)' }}>India-specific risk patterns for each document category</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 16 }}>
            {DOC_FOLDERS.map((f, i) => (
              <div key={f.type} className="file-folder-card" style={{ '--folder-color': f.color, padding: '20px 16px', cursor: 'pointer' } as any}
                onMouseEnter={() => setHovered(i)} onMouseLeave={() => setHovered(null)}>
                <div style={{ fontSize: 24, marginBottom: 8 }}>{f.icon}</div>
                <p style={{ fontSize: 13, fontWeight: 700, color: 'var(--navy)', marginBottom: 4 }}>{f.type}</p>
                <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)', lineHeight: 1.5 }}>{f.risks}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how" style={{ padding: '80px 24px', maxWidth: 1200, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <h2 className="font-serif" style={{ fontSize: 36, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>How LawBridge thinks</h2>
          <p style={{ fontSize: 14, color: 'rgba(20,33,61,0.6)' }}>A legal workflow — not a tech pipeline</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 0, position: 'relative' }}>
          <div style={{ position: 'absolute', top: 20, left: '10%', right: '10%', height: 2, background: 'linear-gradient(to right, var(--gold), rgba(201,162,39,0.3))', zIndex: 0 }} />
          {STEPS.map((s, i) => (
            <div key={s.n} style={{ flex: 1, textAlign: 'center', padding: '0 12px', position: 'relative', zIndex: 1 }}>
              <div style={{ width: 40, height: 40, borderRadius: '50%', background: 'var(--navy)', color: 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, fontWeight: 700, margin: '0 auto 16px', border: '3px solid var(--ivory)' }}>
                {i + 1}
              </div>
              <p className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: 'var(--navy)', marginBottom: 6 }}>{s.title}</p>
              <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.6)', lineHeight: 1.6 }}>{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Expanded features */}
      <section style={{ background: 'var(--navy)', padding: '80px 24px' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 48 }}>
            <h2 className="font-serif" style={{ fontSize: 36, fontWeight: 700, color: 'white', marginBottom: 8 }}>More than document checking</h2>
            <p style={{ fontSize: 14, color: 'rgba(255,255,255,0.6)' }}>India's complete legal intelligence companion</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 20 }}>
            {[
              { icon: FileText, title: 'Document Analysis', desc: 'Upload any legal document. Get risk score, clause breakdown, missing protections, and negotiation points.' },
              { icon: MessageSquare, title: 'General Legal Q&A', desc: 'Ask any Indian law question — tenant rights, consumer complaints, employment disputes, FIR procedure, RTI.' },
              { icon: BookOpen, title: 'Know Your Rights', desc: 'Browse India law by category — Tenant, Employee, Consumer, Digital. Plain-English rights explanation.' },
              { icon: MapPin, title: 'Legal Help Near Me', desc: 'Find NALSA, state legal aid, and free legal resources near you based on your city/state.' },
            ].map(f => (
              <div key={f.title} style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(201,162,39,0.2)', borderRadius: 14, padding: 24 }}>
                <div style={{ width: 40, height: 40, borderRadius: 10, background: 'rgba(201,162,39,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 14 }}>
                  <f.icon size={18} color="var(--gold)" />
                </div>
                <p className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: 'white', marginBottom: 8 }}>{f.title}</p>
                <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.6)', lineHeight: 1.6 }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Disclaimer */}
      <section style={{ background: '#fffbeb', borderTop: '1px solid #fcd34d', borderBottom: '1px solid #fcd34d', padding: '40px 24px' }}>
        <div style={{ maxWidth: 700, margin: '0 auto', textAlign: 'center' }}>
          <AlertTriangle size={28} color="#d97706" style={{ margin: '0 auto 12px' }} />
          <h3 className="font-serif" style={{ fontSize: 22, fontWeight: 700, color: '#78350f', marginBottom: 10 }}>Important Disclaimer</h3>
          <p style={{ fontSize: 14, color: '#92400e', lineHeight: 1.8 }}>
            LawBridge AI is an <strong>educational and document-understanding tool</strong>, not a law firm. We do not provide legal advice. We do not replace a lawyer. We help you understand what documents say and identify potential risks so you can have better conversations with qualified legal professionals. <strong>Always consult a lawyer before signing or taking legal action.</strong>
          </p>
        </div>
      </section>

      {/* CTA */}
      <section style={{ padding: '80px 24px', textAlign: 'center' }}>
        <h2 className="font-serif" style={{ fontSize: 'clamp(28px, 4vw, 52px)', fontWeight: 700, color: 'var(--navy)', marginBottom: 12 }}>
          Don't sign what you don't understand.
        </h2>
        <p style={{ fontSize: 16, color: 'rgba(20,33,61,0.6)', marginBottom: 32 }}>Analyze your first document free. No credit card required.</p>
        <div style={{ display: 'flex', gap: 14, justifyContent: 'center' }}>
          <Link href="/register" className="btn-navy" style={{ fontSize: 15, padding: '12px 28px' }}>
            Analyze your first document <ArrowRight size={16} />
          </Link>
          <Link href="/login" className="btn-ghost" style={{ fontSize: 15, padding: '12px 28px' }}>Try demo</Link>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ background: 'var(--navy)', padding: '24px', borderTop: '1px solid rgba(201,162,39,0.2)' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <Scale size={16} color="var(--gold)" />
            <span className="font-serif" style={{ color: 'white', fontWeight: 600 }}>LawBridge AI</span>
            <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: 12 }}>— Not a law firm. Not legal advice.</span>
          </div>
          <div style={{ display: 'flex', gap: 20 }}>
            {['Login', 'Register', 'API Docs'].map(l => (
              <Link key={l} href={l === 'Login' ? '/login' : l === 'Register' ? '/register' : 'http://localhost:8000/docs'}
                style={{ color: 'rgba(255,255,255,0.4)', fontSize: 12, textDecoration: 'none' }}>{l}</Link>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}
