'use client';
import { useEffect, useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { locationApi } from '@/lib/api';
import { MapPin, Phone, Globe, Scale, CheckCircle, AlertTriangle, Building } from 'lucide-react';
import { DOC_TYPES } from '@/lib/utils';

export default function LocationPage() {
  const [states, setStates] = useState<string[]>([]);
  const [state, setState] = useState('');
  const [docType, setDocType] = useState('Rental Agreement');
  const [resources, setResources] = useState<any[]>([]);
  const [checklist, setChecklist] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => { locationApi.states().then(r => setStates(r.data.states)); }, []);

  const search = async () => {
    if (!state) return;
    setLoading(true);
    try {
      const [r, c] = await Promise.all([locationApi.resources(state), locationApi.checklist(state, docType)]);
      setResources(r.data); setChecklist(c.data.checklist || []);
      await locationApi.update(state);
    } finally { setLoading(false); }
  };

  return (
    <AppShell>
      <div style={{ maxWidth: 900, animation: 'fadeUp 0.4s ease-out' }}>
        <h1 className="font-serif" style={{ fontSize: 26, fontWeight: 700, color: 'var(--navy)', marginBottom: 4 }}>Legal Help Near Me</h1>
        <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.55)', marginBottom: 20 }}>Find free legal aid and state-specific requirements for your documents</p>

        <div className="legal-card" style={{ padding: 20, marginBottom: 16 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: 12, alignItems: 'end' }}>
            <div>
              <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Your State</label>
              <select className="lb-input" value={state} onChange={e => setState(e.target.value)}>
                <option value="">Select your state</option>
                {states.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Document Type</label>
              <select className="lb-input" value={docType} onChange={e => setDocType(e.target.value)}>
                {DOC_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <button onClick={search} disabled={!state || loading} className="btn-navy" style={{ opacity: !state ? 0.5 : 1, whiteSpace: 'nowrap' }}>
              <MapPin size={14} /> Find Help
            </button>
          </div>
        </div>

        {checklist.length > 0 && (
          <div className="legal-card" style={{ padding: 20, marginBottom: 16, borderLeft: '4px solid var(--gold)' }}>
            <h3 className="font-serif" style={{ fontSize: 18, fontWeight: 700, color: 'var(--navy)', marginBottom: 12 }}>
              {state} — {docType} Checklist
            </h3>
            {checklist.map((item, i) => (
              <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 10, padding: '10px 14px', background: '#fffbeb', border: '1px solid #fcd34d', borderRadius: 8 }}>
                <AlertTriangle size={13} style={{ color: '#D97706', flexShrink: 0, marginTop: 1 }} />
                <p style={{ fontSize: 13, color: '#78350f', lineHeight: 1.6 }}>{item}</p>
              </div>
            ))}
          </div>
        )}

        {resources.length > 0 && (
          <div className="legal-card" style={{ padding: 20, marginBottom: 16 }}>
            <h3 className="font-serif" style={{ fontSize: 18, fontWeight: 700, color: 'var(--navy)', marginBottom: 16 }}>Free Legal Aid Resources</h3>
            {resources.map((r: any) => (
              <div key={r.id} style={{ padding: '16px', border: '1px solid rgba(201,162,39,0.2)', borderRadius: 10, marginBottom: 10, display: 'flex', gap: 14 }}>
                <div style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--navy)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  <Building size={16} style={{ color: 'var(--gold)' }} />
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                    <p style={{ fontSize: 14, fontWeight: 700, color: 'var(--navy)' }}>{r.name}</p>
                    {r.is_free && <span style={{ fontSize: 10, padding: '2px 8px', background: '#f0fdf4', color: '#16834A', border: '1px solid #86efac', borderRadius: 10, fontWeight: 700 }}>FREE</span>}
                  </div>
                  <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.6)', marginBottom: 8, lineHeight: 1.5 }}>{r.description}</p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12, fontSize: 12, color: 'rgba(20,33,61,0.5)' }}>
                    {r.address && <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><MapPin size={10} />{r.address}</span>}
                    {r.phone && <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><Phone size={10} />{r.phone}</span>}
                    {r.website && <a href={`https://${r.website}`} target="_blank" style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'var(--gold)', textDecoration: 'none' }}><Globe size={10} />{r.website}</a>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        <div style={{ background: 'var(--navy)', borderRadius: 12, padding: 20 }}>
          <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: 'white', marginBottom: 8 }}>National Legal Services Authority (NALSA)</h3>
          <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.6)', marginBottom: 12, lineHeight: 1.6 }}>Free legal services for SC/ST, women, children, persons with disabilities, and those below poverty line.</p>
          <div style={{ display: 'flex', gap: 10 }}>
            <a href="tel:15100" style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '8px 14px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(201,162,39,0.3)', borderRadius: 8, color: 'white', textDecoration: 'none', fontSize: 13, fontWeight: 600 }}>
              <Phone size={13} style={{ color: 'var(--gold)' }} /> 15100 Helpline
            </a>
            <a href="https://nalsa.gov.in" target="_blank" style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '8px 14px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(201,162,39,0.3)', borderRadius: 8, color: 'white', textDecoration: 'none', fontSize: 13, fontWeight: 600 }}>
              <Globe size={13} style={{ color: 'var(--gold)' }} /> nalsa.gov.in
            </a>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
