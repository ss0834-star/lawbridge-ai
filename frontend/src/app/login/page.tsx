'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authApi } from '@/lib/api';
import { Scale, Eye, EyeOff, Loader2, AlertTriangle, ArrowRight } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [pwd, setPwd] = useState('');
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const [demoLoading, setDemoLoading] = useState(false);
  const [err, setErr] = useState('');

  const doLogin = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setErr('');
    try {
      const { data } = await authApi.login({ email, password: pwd });
      localStorage.setItem('lb_token', data.access_token);
      localStorage.setItem('lb_user', JSON.stringify(data.user));
      router.push('/dashboard');
    } catch (e: any) { setErr(e.response?.data?.detail || 'Invalid credentials'); }
    finally { setLoading(false); }
  };

  const doDemo = async () => {
    setDemoLoading(true); setErr('');
    try {
      const { data } = await authApi.demo();
      localStorage.setItem('lb_token', data.access_token);
      localStorage.setItem('lb_user', JSON.stringify(data.user));
      router.push('/dashboard');
    } catch (e: any) { setErr(e.response?.data?.detail || 'Demo failed'); }
    finally { setDemoLoading(false); }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', background: 'var(--ivory)' }}>
      {/* Left panel - brand story */}
      <div style={{ width: '42%', background: 'var(--navy)', display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '60px 48px', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', inset: 0, backgroundImage: 'radial-gradient(circle at 20% 80%, rgba(201,162,39,0.08) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(122,30,44,0.15) 0%, transparent 50%)' }} />
        <div style={{ position: 'relative' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 48 }}>
            <div style={{ width: 36, height: 36, borderRadius: 10, background: 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Scale size={18} color="var(--navy)" />
            </div>
            <span className="font-serif" style={{ fontSize: 22, fontWeight: 700, color: 'white' }}>LawBridge <span style={{ color: 'var(--gold)' }}>AI</span></span>
          </div>

          <div style={{ marginBottom: 40 }}>
            <div style={{ width: 60, height: 4, background: 'var(--gold)', borderRadius: 2, marginBottom: 28 }} />
            <blockquote className="font-serif" style={{ fontSize: 28, fontWeight: 600, color: 'white', lineHeight: 1.3, marginBottom: 16, fontStyle: 'italic' }}>
              "You should never sign a document you cannot understand."
            </blockquote>
            <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.5)' }}>— LawBridge AI guiding principle</p>
          </div>

          {/* Illustration - abstract legal document */}
          <div style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(201,162,39,0.2)', borderRadius: 12, padding: 20, marginBottom: 32 }}>
            <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.3)', fontFamily: 'JetBrains Mono, monospace', lineHeight: 2 }}>
              <div style={{ color: 'var(--gold)', marginBottom: 4, fontSize: 12 }}>📄 Employment Contract.pdf</div>
              <div><span style={{ background: '#B4231822', color: '#ff8080', padding: '1px 6px', borderRadius: 3 }}>HIGH RISK</span> Clause 5: Termination without cause</div>
              <div><span style={{ background: '#B86B4B22', color: '#ffaa80', padding: '1px 6px', borderRadius: 3 }}>MISSING</span> Severance / exit benefits</div>
              <div><span style={{ background: '#C9A22722', color: '#ffdd80', padding: '1px 6px', borderRadius: 3 }}>MEDIUM</span> 2-year non-compete clause</div>
              <div style={{ marginTop: 8, color: 'rgba(255,255,255,0.4)' }}>Risk Score: 72/100 — Lawyer review recommended</div>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {['Not legal advice — document education only', 'India-specific legal context', 'Private and secure document analysis', 'Free legal aid resources included'].map(t => (
              <div key={t} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12, color: 'rgba(255,255,255,0.5)' }}>
                <div style={{ width: 4, height: 4, borderRadius: '50%', background: 'var(--gold)' }} />
                {t}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right panel - login form */}
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '40px 24px' }}>
        <div style={{ width: '100%', maxWidth: 400 }}>
          <div style={{ marginBottom: 32 }}>
            <h1 className="font-serif" style={{ fontSize: 32, fontWeight: 700, color: 'var(--navy)', marginBottom: 6 }}>Welcome back</h1>
            <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.55)' }}>Sign into your private legal desk</p>
          </div>

          {err && (
            <div style={{ background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: 8, padding: '10px 14px', marginBottom: 16, fontSize: 13, color: '#dc2626', display: 'flex', gap: 8 }}>
              <AlertTriangle size={14} style={{ flexShrink: 0 }} /> {err}
            </div>
          )}

          <button onClick={doDemo} disabled={demoLoading}
            style={{ width: '100%', padding: '11px', background: '#fffbeb', border: '1.5px solid #fcd34d', borderRadius: 8, fontSize: 13, fontWeight: 600, color: '#92400e', cursor: 'pointer', marginBottom: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, transition: 'all 0.2s' }}>
            {demoLoading ? <Loader2 size={14} className="animate-spin" /> : '⚡'} Try Demo — no signup needed
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
            <div style={{ flex: 1, height: 1, background: 'rgba(20,33,61,0.1)' }} />
            <span style={{ fontSize: 11, color: 'rgba(20,33,61,0.4)', fontWeight: 500 }}>or sign in with email</span>
            <div style={{ flex: 1, height: 1, background: 'rgba(20,33,61,0.1)' }} />
          </div>

          <form onSubmit={doLogin} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div>
              <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Email address</label>
              <input className="lb-input" type="email" placeholder="you@email.com" value={email} onChange={e => setEmail(e.target.value)} required />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Password</label>
              <div style={{ position: 'relative' }}>
                <input className="lb-input" type={show ? 'text' : 'password'} placeholder="••••••••" value={pwd} onChange={e => setPwd(e.target.value)} required style={{ paddingRight: 40 }} />
                <button type="button" onClick={() => setShow(s => !s)} style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'rgba(20,33,61,0.4)' }}>
                  {show ? <EyeOff size={14} /> : <Eye size={14} />}
                </button>
              </div>
            </div>
            <button type="submit" disabled={loading} className="btn-navy" style={{ width: '100%', justifyContent: 'center', padding: '11px', opacity: loading ? 0.6 : 1 }}>
              {loading && <Loader2 size={14} className="animate-spin" />} Sign in <ArrowRight size={14} />
            </button>
          </form>

          <div style={{ background: 'var(--parchment)', borderRadius: 8, padding: '12px 14px', marginTop: 20, fontSize: 12, color: 'rgba(20,33,61,0.6)' }}>
            <p style={{ fontWeight: 600, marginBottom: 4 }}>Demo accounts:</p>
            <p>demo@lawbridge.ai / demo123</p>
            <p>admin@lawbridge.ai / admin123</p>
          </div>

          <p style={{ textAlign: 'center', fontSize: 13, color: 'rgba(20,33,61,0.55)', marginTop: 20 }}>
            New here? <Link href="/register" style={{ color: 'var(--gold)', fontWeight: 600, textDecoration: 'none' }}>Create a free account</Link>
          </p>

          <div className="disclaimer-ribbon" style={{ marginTop: 20, fontSize: 11 }}>
            <AlertTriangle size={11} className="flex-shrink-0" style={{ flexShrink: 0 }} />
            LawBridge AI is not a law firm and does not provide legal advice. For educational purposes only.
          </div>
        </div>
      </div>
    </div>
  );
}
