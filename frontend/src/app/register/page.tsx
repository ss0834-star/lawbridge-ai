'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authApi } from '@/lib/api';
import { Scale, Eye, EyeOff, Loader2, AlertTriangle, CheckCircle } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [show, setShow] = useState(false);
  const [accepted, setAccepted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');

  const doRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!accepted) { setErr('Please accept the disclaimer to continue'); return; }
    if (form.password.length < 6) { setErr('Password must be at least 6 characters'); return; }
    setLoading(true); setErr('');
    try {
      const { data } = await authApi.register(form);
      localStorage.setItem('lb_token', data.access_token);
      localStorage.setItem('lb_user', JSON.stringify(data.user));
      await authApi.acceptDisclaimer();
      router.push('/dashboard');
    } catch (e: any) { setErr(e.response?.data?.detail || 'Registration failed'); }
    finally { setLoading(false); }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', background: 'var(--ivory)' }}>
      {/* Left panel */}
      <div style={{ width: '42%', background: 'var(--navy)', display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '60px 48px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 48 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Scale size={18} color="var(--navy)" />
          </div>
          <span className="font-serif" style={{ fontSize: 22, fontWeight: 700, color: 'white' }}>LawBridge <span style={{ color: 'var(--gold)' }}>AI</span></span>
        </div>
        <h2 className="font-serif" style={{ fontSize: 32, fontWeight: 700, color: 'white', marginBottom: 16, lineHeight: 1.2 }}>
          Your private legal reading room
        </h2>
        <p style={{ fontSize: 14, color: 'rgba(255,255,255,0.6)', lineHeight: 1.8, marginBottom: 40 }}>
          Join thousands of Indians who understand their legal documents before signing. Never be blindsided by a clause again.
        </p>
        {['Free to use — always', 'India-specific legal checks', 'Private document storage', 'General legal Q&A included', 'Know Your Rights library', 'Free legal aid finder'].map(f => (
          <div key={f} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
            <CheckCircle size={14} color="var(--gold)" style={{ flexShrink: 0 }} />
            <span style={{ fontSize: 13, color: 'rgba(255,255,255,0.7)' }}>{f}</span>
          </div>
        ))}
      </div>

      {/* Right panel */}
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '40px 24px' }}>
        <div style={{ width: '100%', maxWidth: 400 }}>
          <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 700, color: 'var(--navy)', marginBottom: 6 }}>Create your account</h1>
          <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.55)', marginBottom: 28 }}>Start understanding your legal documents today</p>

          {err && (
            <div style={{ background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: 8, padding: '10px 14px', marginBottom: 16, fontSize: 13, color: '#dc2626', display: 'flex', gap: 8 }}>
              <AlertTriangle size={14} style={{ flexShrink: 0 }} /> {err}
            </div>
          )}

          <form onSubmit={doRegister} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div>
              <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Full Name</label>
              <input className="lb-input" placeholder="Priya Sharma" value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} required />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Email</label>
              <input className="lb-input" type="email" placeholder="you@email.com" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} required />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Password</label>
              <div style={{ position: 'relative' }}>
                <input className="lb-input" type={show ? 'text' : 'password'} placeholder="Min. 6 characters" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} required style={{ paddingRight: 40 }} />
                <button type="button" onClick={() => setShow(s => !s)} style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'rgba(20,33,61,0.4)' }}>
                  {show ? <EyeOff size={14} /> : <Eye size={14} />}
                </button>
              </div>
            </div>

            <div style={{ background: '#fffbeb', border: '1px solid #fcd34d', borderRadius: 10, padding: '14px 16px' }}>
              <p style={{ fontSize: 12, color: '#78350f', lineHeight: 1.6, marginBottom: 10 }}>
                <strong>Disclaimer:</strong> LawBridge AI provides document explanations and risk awareness only — not legal advice. AI can make mistakes. Always consult a qualified lawyer before signing any legal document.
              </p>
              <label style={{ display: 'flex', alignItems: 'flex-start', gap: 8, cursor: 'pointer' }}>
                <input type="checkbox" checked={accepted} onChange={e => setAccepted(e.target.checked)} style={{ marginTop: 2 }} />
                <span style={{ fontSize: 12, color: '#92400e', fontWeight: 600 }}>I understand this is not legal advice</span>
              </label>
            </div>

            <button type="submit" disabled={loading || !accepted} className="btn-navy" style={{ width: '100%', justifyContent: 'center', padding: '11px', opacity: loading || !accepted ? 0.6 : 1 }}>
              {loading ? <Loader2 size={14} className="animate-spin" /> : <CheckCircle size={14} />} Create account
            </button>
          </form>

          <p style={{ textAlign: 'center', fontSize: 13, color: 'rgba(20,33,61,0.55)', marginTop: 20 }}>
            Already have an account? <Link href="/login" style={{ color: 'var(--gold)', fontWeight: 600, textDecoration: 'none' }}>Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
