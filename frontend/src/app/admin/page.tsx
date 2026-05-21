'use client';
import { useEffect, useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { adminApi } from '@/lib/api';
import { Users, FileText, BarChart2, Shield, AlertTriangle, Scale } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const RISK_COLORS: Record<string, string> = { 'Low Risk': '#16834A', 'Medium Risk': '#D97706', 'High Risk': '#B86B4B', 'Critical Risk': '#B42318' };

export default function AdminPage() {
  const [stats, setStats] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [health, setHealth] = useState<any>(null);
  const [err, setErr] = useState('');

  useEffect(() => {
    Promise.all([adminApi.stats(), adminApi.users(), adminApi.health()])
      .then(([s, u, h]) => { setStats(s.data); setUsers(u.data); setHealth(h.data); })
      .catch(e => setErr(e.response?.data?.detail || 'Admin access required'));
  }, []);

  if (err) return (
    <AppShell>
      <div className="legal-card" style={{ padding: 60, textAlign: 'center', maxWidth: 500, margin: '40px auto' }}>
        <Shield size={40} style={{ color: 'var(--burgundy)', margin: '0 auto 16px' }} />
        <p className="font-serif" style={{ fontSize: 20, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>Access Denied</p>
        <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.6)' }}>{err}</p>
        <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.4)', marginTop: 8 }}>Login as admin@lawbridge.ai to access this panel</p>
      </div>
    </AppShell>
  );

  const riskData = stats?.risk_distribution ? Object.entries(stats.risk_distribution).map(([n, v]) => ({ name: n, value: v })) : [];
  const docData = stats?.document_types ? Object.entries(stats.document_types).map(([n, v]) => ({ name: n.replace(' Agreement', '').replace(' Contract', ''), value: v })) : [];

  return (
    <AppShell>
      <div style={{ maxWidth: 1100, animation: 'fadeUp 0.4s ease-out' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
          <div><h1 className="font-serif" style={{ fontSize: 26, fontWeight: 700, color: 'var(--navy)' }}>Operations Control Room</h1>
            <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.5)' }}>Platform analytics and system health</p></div>
          {health && <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 14px', background: health.status === 'operational' ? '#f0fdf4' : '#fef2f2', border: `1px solid ${health.status === 'operational' ? '#86efac' : '#fca5a5'}`, borderRadius: 20 }}>
            <div style={{ width: 8, height: 8, borderRadius: '50%', background: health.status === 'operational' ? '#16834A' : '#dc2626', animation: 'pulse 2s infinite' }} />
            <span style={{ fontSize: 12, fontWeight: 600, color: health.status === 'operational' ? '#16834A' : '#dc2626' }}>System {health.status}</span>
            <span style={{ fontSize: 11, color: 'rgba(20,33,61,0.4)' }}>DB: {health.database} · Redis: {health.redis}</span>
          </div>}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 12, marginBottom: 20 }}>
          {[
            { label: 'Users', value: stats?.total_users || 0, icon: Users, color: 'var(--navy)' },
            { label: 'Documents', value: stats?.total_documents || 0, icon: FileText, color: 'var(--gold)' },
            { label: 'Analyses', value: stats?.total_analyses || 0, icon: BarChart2, color: 'var(--forest)' },
            { label: 'Legal Queries', value: stats?.total_legal_queries || 0, icon: Scale, color: 'var(--terracotta)' },
            { label: 'Avg Risk Score', value: stats?.avg_risk_score || 0, icon: AlertTriangle, color: 'var(--burgundy)' },
          ].map(s => (
            <div key={s.label} className="legal-card" style={{ padding: '16px', textAlign: 'center' }}>
              <s.icon size={18} style={{ color: s.color, margin: '0 auto 8px' }} />
              <p style={{ fontSize: 22, fontWeight: 800, color: 'var(--navy)' }}>{s.value}</p>
              <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)' }}>{s.label}</p>
            </div>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
          <div className="legal-card" style={{ padding: 20 }}>
            <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: 'var(--navy)', marginBottom: 14 }}>Risk Distribution</h3>
            <ResponsiveContainer width="100%" height={180}>
              <PieChart><Pie data={riskData} cx="50%" cy="50%" outerRadius={70} dataKey="value" label={({ name, value }: any) => `${name?.split(' ')[0]}: ${value}`}>
                {riskData.map((entry: any, i) => <Cell key={i} fill={RISK_COLORS[entry.name] || 'var(--gold)'} />)}
              </Pie><Tooltip /></PieChart>
            </ResponsiveContainer>
          </div>
          <div className="legal-card" style={{ padding: 20 }}>
            <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: 'var(--navy)', marginBottom: 14 }}>Document Types</h3>
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={docData}><CartesianGrid stroke="#EDE3C8" strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fontSize: 9, fill: 'rgba(20,33,61,0.6)' }} />
                <YAxis tick={{ fontSize: 9, fill: 'rgba(20,33,61,0.6)' }} />
                <Tooltip /><Bar dataKey="value" fill="var(--gold)" radius={[4, 4, 0, 0]} /></BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="legal-card" style={{ padding: 20 }}>
          <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: 'var(--navy)', marginBottom: 14 }}>All Users ({users.length})</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr style={{ borderBottom: '1px solid rgba(201,162,39,0.2)' }}>
              {['Name', 'Email', 'Role', 'Joined'].map(h => <th key={h} style={{ textAlign: 'left', padding: '8px 12px', fontSize: 11, fontWeight: 700, color: 'rgba(20,33,61,0.5)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{h}</th>)}
            </tr></thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} style={{ borderBottom: '1px solid rgba(201,162,39,0.1)' }}>
                  <td style={{ padding: '10px 12px', fontSize: 13, fontWeight: 600, color: 'var(--navy)' }}>{u.name}</td>
                  <td style={{ padding: '10px 12px', fontSize: 13, color: 'rgba(20,33,61,0.7)' }}>{u.email}</td>
                  <td style={{ padding: '10px 12px' }}><span style={{ fontSize: 11, padding: '2px 8px', borderRadius: 10, fontWeight: 700, background: u.role === 'admin' ? '#fffbeb' : 'var(--parchment)', color: u.role === 'admin' ? 'var(--gold)' : 'rgba(20,33,61,0.6)', border: u.role === 'admin' ? '1px solid var(--gold)' : '1px solid rgba(20,33,61,0.15)' }}>{u.role}</span></td>
                  <td style={{ padding: '10px 12px', fontSize: 12, color: 'rgba(20,33,61,0.5)' }}>{new Date(u.created_at).toLocaleDateString('en-IN')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
