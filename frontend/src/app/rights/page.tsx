'use client';
import { useEffect, useState } from 'react';
import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import AppShell from '@/components/layout/AppShell';
import { rightsApi, qaApi } from '@/lib/api';
import { BookOpen, ChevronRight, Scale, Loader2, MessageSquare } from 'lucide-react';
import { useRouter } from 'next/navigation';

const CAT_COLORS: Record<string, string> = { tenant: 'var(--forest)', employee: 'var(--navy)', consumer: 'var(--gold)', digital: 'var(--burgundy)' };

function RightsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const catParam = searchParams.get('cat');
  const [categories, setCategories] = useState<any[]>([]);
  const [activeCategory, setActiveCategory] = useState<string>(catParam || '');
  const [rights, setRights] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { rightsApi.categories().then(r => setCategories(r.data.categories)); }, []);

  useEffect(() => {
    if (activeCategory) {
      setLoading(true);
      rightsApi.get(activeCategory).then(r => setRights(r.data)).finally(() => setLoading(false));
    }
  }, [activeCategory]);

  const askAboutRight = (right: string) => {
    router.push(`/chat?q=${encodeURIComponent(`Tell me more about: ${right}`)}`);
  };

  return (
    <AppShell>
      <div style={{ maxWidth: 1000, animation: 'fadeUp 0.4s ease-out' }}>
        <div style={{ marginBottom: 24 }}>
          <h1 className="font-serif" style={{ fontSize: 28, fontWeight: 700, color: 'var(--navy)', marginBottom: 4 }}>Know Your Rights</h1>
          <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.55)' }}>Browse Indian law by category — plain-English explanations of your legal rights</p>
        </div>

        {/* Category tabs */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 24 }}>
          {categories.map(cat => (
            <button key={cat.key} onClick={() => setActiveCategory(cat.key)}
              style={{ padding: '16px', borderRadius: 12, border: `2px solid ${activeCategory === cat.key ? CAT_COLORS[cat.key] : 'rgba(20,33,61,0.1)'}`, background: activeCategory === cat.key ? CAT_COLORS[cat.key] : 'white', cursor: 'pointer', transition: 'all 0.2s', textAlign: 'left' }}>
              <div style={{ fontSize: 24, marginBottom: 6 }}>{cat.icon}</div>
              <p style={{ fontSize: 13, fontWeight: 700, color: activeCategory === cat.key ? 'white' : 'var(--navy)', marginBottom: 3 }}>{cat.title}</p>
              <p style={{ fontSize: 11, color: activeCategory === cat.key ? 'rgba(255,255,255,0.7)' : 'rgba(20,33,61,0.5)', lineHeight: 1.4 }}>{cat.description}</p>
            </button>
          ))}
        </div>

        {!activeCategory && (
          <div className="legal-card" style={{ padding: '48px', textAlign: 'center' }}>
            <BookOpen size={40} style={{ color: 'rgba(20,33,61,0.2)', margin: '0 auto 16px' }} />
            <p className="font-serif" style={{ fontSize: 20, fontWeight: 600, color: 'var(--navy)', marginBottom: 8 }}>Select a category</p>
            <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.5)' }}>Choose a rights category above to explore your legal protections under Indian law</p>
          </div>
        )}

        {loading && <div style={{ textAlign: 'center', padding: 60 }}><Loader2 size={28} className="animate-spin" style={{ color: 'var(--navy)' }} /></div>}

        {rights && !loading && (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20, padding: '16px 20px', background: CAT_COLORS[activeCategory], borderRadius: 12 }}>
              <Scale size={20} style={{ color: 'white', flexShrink: 0 }} />
              <div>
                <h2 className="font-serif" style={{ fontSize: 20, fontWeight: 700, color: 'white' }}>{rights.title}</h2>
                <p style={{ fontSize: 11, color: 'rgba(255,255,255,0.6)' }}>Under Indian law — for educational purposes only</p>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {rights.rights?.map((right: any, i: number) => (
                <div key={i} className="legal-card" style={{ padding: '20px', borderLeft: `4px solid ${CAT_COLORS[activeCategory]}` }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 12, marginBottom: 10 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <span style={{ width: 26, height: 26, borderRadius: '50%', background: CAT_COLORS[activeCategory], color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>{i + 1}</span>
                      <h3 className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: 'var(--navy)' }}>{right.title}</h3>
                    </div>
                    <button onClick={() => askAboutRight(right.title)} style={{ background: 'none', border: '1px solid rgba(201,162,39,0.4)', borderRadius: 6, padding: '4px 10px', fontSize: 11, color: 'var(--gold)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 4, flexShrink: 0, fontWeight: 600 }}>
                      <MessageSquare size={10} /> Ask AI
                    </button>
                  </div>
                  <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.75)', lineHeight: 1.8, marginLeft: 36 }}>{right.description}</p>
                  {right.law && <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.4)', marginLeft: 36, marginTop: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                    <Scale size={10} /> {right.law}
                  </p>}
                </div>
              ))}
            </div>

            <div style={{ background: '#fffbeb', border: '1px solid #fcd34d', borderRadius: 10, padding: '14px 16px', marginTop: 20, fontSize: 12, color: '#78350f', lineHeight: 1.6 }}>
              <strong>Important:</strong> This information is for general education about Indian law. Laws may vary by state and individual circumstances differ. Always consult a qualified lawyer for advice specific to your situation. For free legal aid, call NALSA helpline: <strong>15100</strong>.
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}

export default function RightsPage() {
  return <Suspense fallback={<div style={{ display: 'flex', justifyContent: 'center', padding: 60 }}><Loader2 size={24} className="animate-spin" /></div>}><RightsContent /></Suspense>;
}
