'use client';
import { Suspense } from 'react';
import { useEffect, useState, useRef } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import AppShell from '@/components/layout/AppShell';
import { chatApi, qaApi, docApi } from '@/lib/api';
import { Send, Loader2, MessageSquare, AlertTriangle, Bot, User, Scale, BookOpen, Plus } from 'lucide-react';
import { LANGUAGES } from '@/lib/utils';

const SUGGESTED_DOC = ["What are the main risks in this document?","Explain the termination clause in simple terms","What should I ask my lawyer?","What happens if I break the lock-in period?","Summarize the financial obligations"];
const SUGGESTED_GENERAL = ["What are my rights as a tenant in India?","Can my employer force me to work overtime?","How do I file a consumer complaint?","Is a non-compete clause enforceable in India?","What should I do if police refuse to file my FIR?","What documents do I need to buy a flat?"];

function ChatContent() {
  const searchParams = useSearchParams();
  const sessionParam = searchParams.get('session');
  const qParam = searchParams.get('q');
  const [mode, setMode] = useState<'document' | 'general'>('general');
  const [sessions, setSessions] = useState<any[]>([]);
  const [activeSession, setActiveSession] = useState<any>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState(qParam || '');
  const [sending, setSending] = useState(false);
  const [language, setLanguage] = useState('English');
  const [docs, setDocs] = useState<any[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<number | null>(null);
  const [qaHistory, setQaHistory] = useState<any[]>([]);
  const [qaInput, setQaInput] = useState(qParam || '');
  const [qaLoading, setQaLoading] = useState(false);
  const [qaMessages, setQaMessages] = useState<any[]>([]);
  const messagesEnd = useRef<HTMLDivElement>(null);

  useEffect(() => {
    Promise.all([chatApi.sessions(), docApi.list(), qaApi.popular()]).then(([s, d, p]) => {
      setSessions(s.data); setDocs(d.data.filter((doc: any) => doc.status === 'analyzed'));
      if (p.data.questions) setQaMessages([{ role: 'system', content: 'popular', questions: p.data.questions }]);
    });
    if (sessionParam) {
      chatApi.getSession(Number(sessionParam)).then(r => { setActiveSession(r.data); setMessages(r.data.messages || []); setMode('document'); });
    } else if (qParam) {
      setMode('general'); setTimeout(() => sendQA(qParam), 500);
    }
  }, []);

  useEffect(() => { messagesEnd.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, qaMessages]);

  const createDocSession = async () => {
    const { data } = await chatApi.createSession(selectedDoc || undefined, language, 'document');
    setActiveSession(data); setMessages([]); setSessions(p => [data, ...p]);
  };

  const sendDocMsg = async () => {
    if (!input.trim() || !activeSession || sending) return;
    const um = { role: 'user', content: input, created_at: new Date().toISOString() };
    setMessages(p => [...p, um]); setInput(''); setSending(true);
    try {
      const { data } = await chatApi.send(activeSession.id, um.content, language);
      setMessages(p => [...p, data]);
    } catch { setMessages(p => [...p, { role: 'assistant', content: 'Sorry, an error occurred. Please try again.' }]); }
    finally { setSending(false); }
  };

  const sendQA = async (q?: string) => {
    const question = q || qaInput.trim();
    if (!question) return;
    const um = { role: 'user', content: question };
    setQaMessages(p => p.filter(m => m.role !== 'system').concat([um]));
    setQaInput(''); setQaLoading(true);
    try {
      const { data } = await qaApi.ask(question, language, '', 'General');
      setQaMessages(p => [...p, { role: 'assistant', content: data.answer }]);
    } catch { setQaMessages(p => [...p, { role: 'assistant', content: 'Sorry, could not get an answer. Please try again.' }]); }
    finally { setQaLoading(false); }
  };

  return (
    <AppShell>
      <div style={{ maxWidth: 1100, height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column', animation: 'fadeUp 0.4s ease-out' }}>
        <div style={{ display: 'flex', gap: 10, marginBottom: 16 }}>
          <button onClick={() => setMode('general')} className={mode === 'general' ? 'btn-navy' : 'btn-ghost'} style={{ fontSize: 13, padding: '8px 16px' }}>
            <BookOpen size={14} /> General Legal Q&A
          </button>
          <button onClick={() => setMode('document')} className={mode === 'document' ? 'btn-navy' : 'btn-ghost'} style={{ fontSize: 13, padding: '8px 16px' }}>
            <MessageSquare size={14} /> Document Chat
          </button>
          <select className="lb-input" style={{ width: 130, marginLeft: 'auto' }} value={language} onChange={e => setLanguage(e.target.value)}>
            {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
          </select>
        </div>

        <div style={{ flex: 1, display: 'flex', gap: 14, minHeight: 0 }}>
          {mode === 'general' ? (
            /* General Q&A mode */
            <div className="legal-card" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ padding: '16px 20px', borderBottom: '1px solid rgba(201,162,39,0.15)', background: 'var(--navy)', borderRadius: '11px 11px 0 0', display: 'flex', alignItems: 'center', gap: 10 }}>
                <Scale size={16} style={{ color: 'var(--gold)' }} />
                <div>
                  <p className="font-serif" style={{ fontSize: 15, fontWeight: 700, color: 'white' }}>Legal Q&A — Ask anything about Indian law</p>
                  <p style={{ fontSize: 11, color: 'rgba(255,255,255,0.5)' }}>No document upload required</p>
                </div>
              </div>
              <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px', display: 'flex', flexDirection: 'column', gap: 12 }}>
                {qaMessages.length === 0 || (qaMessages.length === 1 && qaMessages[0].role === 'system') ? (
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 10 }}>
                    <p style={{ fontSize: 12, color: 'rgba(20,33,61,0.5)', textAlign: 'center', marginBottom: 8 }}>Popular questions:</p>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                      {SUGGESTED_GENERAL.map(q => (
                        <button key={q} onClick={() => sendQA(q)} style={{ textAlign: 'left', padding: '10px 12px', background: 'var(--parchment)', border: '1px solid rgba(201,162,39,0.2)', borderRadius: 8, fontSize: 12, color: 'var(--navy)', cursor: 'pointer', lineHeight: 1.5, transition: 'all 0.15s' }}>
                          {q}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  qaMessages.filter(m => m.role !== 'system').map((msg, i) => (
                    <div key={i} style={{ display: 'flex', gap: 10, flexDirection: msg.role === 'user' ? 'row-reverse' : 'row', alignItems: 'flex-start' }}>
                      <div style={{ width: 28, height: 28, borderRadius: '50%', background: msg.role === 'user' ? 'var(--navy)' : 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                        {msg.role === 'user' ? <User size={14} style={{ color: 'white' }} /> : <Bot size={14} style={{ color: 'white' }} />}
                      </div>
                      <div className={msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'} style={{ maxWidth: '75%', fontSize: 13, lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>
                        {msg.content}
                      </div>
                    </div>
                  ))
                )}
                {qaLoading && (
                  <div style={{ display: 'flex', gap: 10, alignItems: 'flex-start' }}>
                    <div style={{ width: 28, height: 28, borderRadius: '50%', background: 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <Bot size={14} style={{ color: 'white' }} />
                    </div>
                    <div className="chat-bubble-ai" style={{ padding: '12px 16px' }}><Loader2 size={14} className="animate-spin" style={{ color: 'var(--navy)' }} /></div>
                  </div>
                )}
                <div ref={messagesEnd} />
              </div>
              <div style={{ padding: '12px 16px', borderTop: '1px solid rgba(201,162,39,0.15)' }}>
                <div className="disclaimer-ribbon" style={{ fontSize: 11, marginBottom: 10 }}>
                  <AlertTriangle size={11} style={{ flexShrink: 0 }} /> Not legal advice — for education only. Consult a lawyer for your specific situation.
                </div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <input className="lb-input" style={{ flex: 1 }} placeholder="Ask any Indian law question..." value={qaInput}
                    onChange={e => setQaInput(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendQA(); } }} />
                  <button onClick={() => sendQA()} disabled={!qaInput.trim() || qaLoading} className="btn-navy" style={{ padding: '9px 14px', opacity: !qaInput.trim() || qaLoading ? 0.5 : 1 }}>
                    {qaLoading ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
                  </button>
                </div>
              </div>
            </div>
          ) : (
            /* Document chat mode */
            <>
              <div style={{ width: 200, display: 'flex', flexDirection: 'column', gap: 10 }}>
                <div className="legal-card" style={{ padding: 14 }}>
                  <p style={{ fontSize: 11, fontWeight: 700, color: 'rgba(20,33,61,0.5)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.06em' }}>New Chat</p>
                  <select className="lb-input" style={{ fontSize: 12, marginBottom: 8 }} value={selectedDoc || ''} onChange={e => setSelectedDoc(e.target.value ? Number(e.target.value) : null)}>
                    <option value="">General legal question</option>
                    {docs.map(d => <option key={d.id} value={d.id}>{d.original_filename?.slice(0, 22)}...</option>)}
                  </select>
                  <button onClick={createDocSession} className="btn-navy" style={{ width: '100%', justifyContent: 'center', fontSize: 12, padding: 8 }}>
                    <Plus size={12} /> New Session
                  </button>
                </div>
                <div style={{ flex: 1, overflowY: 'auto' }}>
                  {sessions.map(s => (
                    <button key={s.id} onClick={() => { setActiveSession(s); chatApi.getSession(s.id).then(r => setMessages(r.data.messages || [])); }}
                      style={{ width: '100%', textAlign: 'left', padding: '10px 12px', borderRadius: 8, border: 'none', cursor: 'pointer', marginBottom: 4, fontSize: 12, fontWeight: activeSession?.id === s.id ? 600 : 400, background: activeSession?.id === s.id ? 'var(--navy)' : 'transparent', color: activeSession?.id === s.id ? 'white' : 'rgba(20,33,61,0.7)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {s.title}
                    </button>
                  ))}
                </div>
              </div>

              <div className="legal-card" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                {!activeSession ? (
                  <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 12, padding: 40, textAlign: 'center' }}>
                    <Scale size={32} style={{ color: 'var(--gold)' }} />
                    <p className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: 'var(--navy)' }}>Document Consultation Desk</p>
                    <p style={{ fontSize: 13, color: 'rgba(20,33,61,0.5)', maxWidth: 300, lineHeight: 1.6 }}>Create a new session to chat about an uploaded document or ask general legal questions.</p>
                  </div>
                ) : (
                  <>
                    <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px', display: 'flex', flexDirection: 'column', gap: 12 }}>
                      {messages.length === 0 && (
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                          {SUGGESTED_DOC.map(q => (
                            <button key={q} onClick={() => setInput(q)} style={{ padding: '8px 12px', background: 'var(--parchment)', border: '1px solid rgba(201,162,39,0.2)', borderRadius: 20, fontSize: 12, color: 'var(--navy)', cursor: 'pointer' }}>{q}</button>
                          ))}
                        </div>
                      )}
                      {messages.map((msg, i) => (
                        <div key={i} style={{ display: 'flex', gap: 10, flexDirection: msg.role === 'user' ? 'row-reverse' : 'row', alignItems: 'flex-start' }}>
                          <div style={{ width: 28, height: 28, borderRadius: '50%', background: msg.role === 'user' ? 'var(--navy)' : 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                            {msg.role === 'user' ? <User size={14} style={{ color: 'white' }} /> : <Bot size={14} style={{ color: 'white' }} />}
                          </div>
                          <div className={msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'} style={{ maxWidth: '75%', fontSize: 13, lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                        </div>
                      ))}
                      {sending && <div style={{ display: 'flex', gap: 10 }}><div style={{ width: 28, height: 28, borderRadius: '50%', background: 'var(--gold)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Bot size={14} style={{ color: 'white' }} /></div><div className="chat-bubble-ai"><Loader2 size={14} className="animate-spin" /></div></div>}
                      <div ref={messagesEnd} />
                    </div>
                    <div style={{ padding: '12px 16px', borderTop: '1px solid rgba(201,162,39,0.15)' }}>
                      <div className="disclaimer-ribbon" style={{ fontSize: 11, marginBottom: 10 }}><AlertTriangle size={11} style={{ flexShrink: 0 }} /> Not legal advice.</div>
                      <div style={{ display: 'flex', gap: 8 }}>
                        <input className="lb-input" style={{ flex: 1 }} placeholder="Ask about your document..." value={input}
                          onChange={e => setInput(e.target.value)}
                          onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendDocMsg(); } }} />
                        <button onClick={sendDocMsg} disabled={!input.trim() || sending} className="btn-navy" style={{ padding: '9px 14px', opacity: !input.trim() || sending ? 0.5 : 1 }}>
                          {sending ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </AppShell>
  );
}

export default function ChatPage() {
  return <Suspense fallback={<div style={{ display: 'flex', justifyContent: 'center', padding: 60 }}><Loader2 size={24} className="animate-spin" style={{ color: 'var(--navy)' }} /></div>}><ChatContent /></Suspense>;
}
