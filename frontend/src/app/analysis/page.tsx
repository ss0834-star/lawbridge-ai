'use client';
import { useEffect, useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { docApi } from '@/lib/api';
import { FileText, Trash2, BarChart2, Upload, Loader2 } from 'lucide-react';
import { fmtDate, fmtSize } from '@/lib/utils';
import Link from 'next/link';

export default function AnalysisIndexPage() {
  const [docs, setDocs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { docApi.list().then(r => setDocs(r.data)).finally(() => setLoading(false)); }, []);

  const del = async (id: number) => {
    if (!confirm('Delete this document?')) return;
    await docApi.del(id);
    setDocs(p => p.filter(d => d.id !== id));
  };

  return (
    <AppShell>
      <div style={{ maxWidth: 900 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
          <div><h1 className="font-serif" style={{ fontSize: 26, fontWeight: 700, color: 'var(--navy)' }}>Document Files</h1>
            <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.5)' }}>{docs.length} document{docs.length !== 1 ? 's' : ''} in your case files</p></div>
          <Link href="/upload" className="btn-navy" style={{ fontSize: 13 }}><Upload size={14} /> Upload New</Link>
        </div>

        {loading && <div style={{ textAlign: 'center', padding: 60 }}><Loader2 size={24} className="animate-spin" style={{ color: 'rgba(20,33,61,0.3)' }} /></div>}

        {!loading && docs.length === 0 && (
          <div className="legal-card" style={{ padding: 60, textAlign: 'center' }}>
            <FileText size={40} style={{ color: 'rgba(20,33,61,0.2)', margin: '0 auto 12px' }} />
            <p className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: 'var(--navy)', marginBottom: 8 }}>No documents yet</p>
            <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.5)', marginBottom: 20 }}>Upload your first legal document to get started</p>
            <Link href="/upload" className="btn-navy"><Upload size={14} /> Upload document</Link>
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {docs.map(doc => (
            <div key={doc.id} className="file-folder-card" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', gap: 14 }}>
              <div style={{ width: 42, height: 42, borderRadius: 10, background: 'var(--parchment)', border: '1px solid rgba(201,162,39,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                <FileText size={18} style={{ color: 'var(--navy)' }} />
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <p style={{ fontSize: 14, fontWeight: 600, color: 'var(--navy)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{doc.original_filename || doc.filename}</p>
                <div style={{ display: 'flex', gap: 12, marginTop: 2 }}>
                  <span style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)' }}>{doc.document_type}</span>
                  <span style={{ fontSize: 11, color: 'rgba(20,33,61,0.4)' }}>·</span>
                  <span style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)' }}>{fmtDate(doc.created_at)}</span>
                  {doc.file_size && <><span style={{ fontSize: 11, color: 'rgba(20,33,61,0.4)' }}>·</span><span style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)' }}>{fmtSize(doc.file_size)}</span></>}
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
                <span style={{ fontSize: 11, padding: '3px 10px', borderRadius: 20, fontWeight: 600,
                  background: doc.status === 'analyzed' ? '#f0fdf4' : doc.status === 'analyzing' ? '#fffbeb' : '#f5f5f5',
                  color: doc.status === 'analyzed' ? '#16834A' : doc.status === 'analyzing' ? '#D97706' : '#666' }}>
                  {doc.status}
                </span>
                {doc.status === 'analyzed' ? (
                  <Link href={`/analysis/${doc.id}`} className="btn-ghost" style={{ fontSize: 12, padding: '6px 12px' }}><BarChart2 size={12} /> Report</Link>
                ) : (
                  <Link href="/upload" className="btn-navy" style={{ fontSize: 12, padding: '6px 12px' }}>Analyze</Link>
                )}
                <button onClick={() => del(doc.id)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'rgba(20,33,61,0.3)', padding: 4, borderRadius: 6, display: 'flex' }}>
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
