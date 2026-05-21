'use client';
import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useRouter } from 'next/navigation';
import AppShell from '@/components/layout/AppShell';
import { docApi, analysisApi } from '@/lib/api';
import { Upload, FileText, AlertTriangle, Loader2, CheckCircle, ChevronRight } from 'lucide-react';
import { DOC_TYPES, LANGUAGES } from '@/lib/utils';

const STEPS = ['Upload Document', 'Document Type', 'Language', 'Accept Disclaimer', 'Analyze'];

export default function UploadPage() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [file, setFile] = useState<File | null>(null);
  const [docType, setDocType] = useState('');
  const [language, setLanguage] = useState('English');
  const [accepted, setAccepted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const [progress, setProgress] = useState('');

  const onDrop = useCallback((accepted: File[]) => {
    if (accepted.length) { setFile(accepted[0]); setErr(''); if (step === 0) setStep(1); }
  }, [step]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'], 'text/plain': ['.txt'] }, maxFiles: 1
  });

  const analyze = async () => {
    if (!file) return;
    setLoading(true); setErr('');
    try {
      setProgress('Uploading document...');
      const { data: doc } = await docApi.upload(file, docType || undefined, language);
      setProgress('Extracting text and detecting clauses...');
      const { data: analysis } = await analysisApi.start(doc.id);
      setProgress('Analysis complete!');
      router.push(`/analysis/${doc.id}`);
    } catch (e: any) { setErr(e.response?.data?.detail || 'Analysis failed'); setLoading(false); setProgress(''); }
  };

  return (
    <AppShell>
      <div style={{ maxWidth: 800, animation: 'fadeUp 0.4s ease-out' }}>
        <h1 className="font-serif" style={{ fontSize: 28, fontWeight: 700, color: 'var(--navy)', marginBottom: 4 }}>Document Intake Desk</h1>
        <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.55)', marginBottom: 24 }}>Upload a legal document to receive comprehensive risk analysis</p>

        {/* Stepper */}
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 28, overflowX: 'auto', paddingBottom: 4 }}>
          {STEPS.map((s, i) => (
            <div key={s} style={{ display: 'flex', alignItems: 'center', flexShrink: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{ width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 12, fontWeight: 700, flexShrink: 0,
                  background: i < step ? 'var(--forest)' : i === step ? 'var(--navy)' : 'var(--parchment)',
                  color: i < step || i === step ? 'white' : 'rgba(20,33,61,0.4)', border: i === step ? '2px solid var(--gold)' : 'none' }}>
                  {i < step ? '✓' : i + 1}
                </div>
                <span style={{ fontSize: 12, fontWeight: i === step ? 600 : 400, color: i === step ? 'var(--navy)' : 'rgba(20,33,61,0.4)', whiteSpace: 'nowrap' }}>{s}</span>
              </div>
              {i < STEPS.length - 1 && <div style={{ width: 24, height: 1, background: i < step ? 'var(--forest)' : 'rgba(20,33,61,0.15)', margin: '0 8px', flexShrink: 0 }} />}
            </div>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: 20 }}>
          <div className="legal-card" style={{ padding: 28 }}>
            {/* Step 0 & 1: Upload + type */}
            <div {...getRootProps()} style={{ border: `2px dashed ${file ? 'var(--forest)' : isDragActive ? 'var(--gold)' : 'rgba(201,162,39,0.4)'}`, borderRadius: 12, padding: 36, textAlign: 'center', cursor: 'pointer', background: file ? '#f0fdf4' : isDragActive ? '#fffbeb' : 'var(--parchment)', marginBottom: 20, transition: 'all 0.2s' }}>
              <input {...getInputProps()} />
              {file ? (
                <div><CheckCircle size={32} style={{ color: 'var(--forest)', margin: '0 auto 10px' }} />
                <p style={{ fontWeight: 600, color: 'var(--forest)' }}>{file.name}</p>
                <p style={{ fontSize: 12, color: 'var(--forest)', opacity: 0.8 }}>{(file.size/1024).toFixed(1)} KB — Click to replace</p></div>
              ) : (
                <div><Upload size={28} style={{ color: 'rgba(20,33,61,0.3)', margin: '0 auto 10px' }} />
                <p style={{ fontWeight: 600, color: 'var(--navy)', marginBottom: 4 }}>{isDragActive ? 'Drop here' : 'Drop your document or click to browse'}</p>
                <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.5)' }}>PDF · DOCX · TXT — Max 10MB</p></div>
              )}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginBottom: 20 }}>
              <div>
                <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Document Type</label>
                <select className="lb-input" value={docType} onChange={e => { setDocType(e.target.value); if(step < 2) setStep(2); }}>
                  <option value="">Auto-detect</option>
                  {DOC_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: 'rgba(20,33,61,0.6)', marginBottom: 6 }}>Language</label>
                <select className="lb-input" value={language} onChange={e => { setLanguage(e.target.value); if(step < 3) setStep(3); }}>
                  {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
                </select>
              </div>
            </div>

            <div style={{ background: '#fffbeb', border: '1px solid #fcd34d', borderRadius: 10, padding: '14px 16px', marginBottom: 20 }}>
              <p style={{ fontSize: 12, color: '#78350f', marginBottom: 8, lineHeight: 1.6 }}>
                <strong>Disclaimer:</strong> This analysis identifies possible risks. It is not legal advice. Your document is processed securely. Always consult a qualified lawyer before signing.
              </p>
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
                <input type="checkbox" checked={accepted} onChange={e => { setAccepted(e.target.checked); if(e.target.checked && step < 4) setStep(4); }} />
                <span style={{ fontSize: 12, fontWeight: 600, color: '#92400e' }}>I understand this is not legal advice</span>
              </label>
            </div>

            {err && <div style={{ background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: 8, padding: '10px 14px', marginBottom: 14, fontSize: 13, color: '#dc2626', display: 'flex', gap: 8 }}>
              <AlertTriangle size={14} /> {err}
            </div>}

            {loading && progress && <div style={{ textAlign: 'center', padding: '16px', background: 'var(--parchment)', borderRadius: 10, marginBottom: 14 }}>
              <Loader2 size={20} style={{ color: 'var(--gold)', margin: '0 auto 8px' }} className="animate-spin" />
              <p style={{ fontSize: 13, color: 'var(--navy)', fontWeight: 500 }}>{progress}</p>
              <p style={{ fontSize: 11, color: 'rgba(20,33,61,0.5)' }}>This may take 30-60 seconds</p>
            </div>}

            <button onClick={analyze} disabled={!file || !accepted || loading} className="btn-navy"
              style={{ width: '100%', justifyContent: 'center', padding: 13, opacity: (!file || !accepted || loading) ? 0.5 : 1, cursor: (!file || !accepted || loading) ? 'not-allowed' : 'pointer' }}>
              {loading ? <Loader2 size={15} className="animate-spin" /> : <FileText size={15} />}
              {loading ? 'Analyzing...' : 'Analyze Document'} {!loading && <ChevronRight size={15} />}
            </button>
          </div>

          {/* What we check */}
          <div>
            <div className="legal-card" style={{ padding: 18, marginBottom: 14 }}>
              <h4 className="font-serif" style={{ fontSize: 15, fontWeight: 700, color: 'var(--navy)', marginBottom: 12 }}>What we analyze</h4>
              {['Overall risk score (0-100)', 'Clause-by-clause explanation', 'India-specific risk patterns', 'Missing clause detection', 'Negotiation suggestions', 'Important deadlines', 'Financial obligations', 'Lawyer questions', 'State-specific checklist'].map(item => (
                <div key={item} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 7, fontSize: 12, color: 'rgba(20,33,61,0.7)' }}>
                  <CheckCircle size={11} style={{ color: 'var(--forest)', flexShrink: 0 }} /> {item}
                </div>
              ))}
            </div>

            <div style={{ background: 'var(--navy)', borderRadius: 12, padding: 16 }}>
              <p style={{ fontSize: 12, fontWeight: 600, color: 'var(--gold)', marginBottom: 6 }}>Supported formats</p>
              {[['📄 PDF', 'Best quality'], ['📝 DOCX', 'Word documents'], ['📃 TXT', 'Plain text']].map(([f, d]) => (
                <div key={f} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'rgba(255,255,255,0.7)', marginBottom: 6 }}>
                  <span>{f}</span><span style={{ color: 'rgba(255,255,255,0.4)' }}>{d}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
