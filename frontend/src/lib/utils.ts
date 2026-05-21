export const DOC_TYPES = ['Rental Agreement','Employment Contract','NDA','Service Agreement','Loan Document','Legal Notice','Business Agreement','Freelance Contract','Property Document','General Agreement'];
export const LANGUAGES = ['English','Hindi','Tamil','Telugu','Kannada','Malayalam','Marathi','Bengali','Gujarati','Punjabi'];
export function getRiskClass(level: string) {
  const l = level?.toLowerCase();
  if (l?.includes('critical')) return 'critical';
  if (l?.includes('high')) return 'high';
  if (l?.includes('medium')) return 'medium';
  return 'low';
}
export function getRiskEmoji(level: string) {
  const l = level?.toLowerCase();
  if (l?.includes('critical')) return '⛔';
  if (l?.includes('high')) return '🔴';
  if (l?.includes('medium')) return '🟡';
  return '🟢';
}
export function getRiskColor(level: string) {
  const l = level?.toLowerCase();
  if (l?.includes('critical')) return 'text-red-800';
  if (l?.includes('high')) return 'text-orange-700';
  if (l?.includes('medium')) return 'text-amber-700';
  return 'text-green-700';
}
export function fmtDate(d: string) {
  return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}
export function fmtSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024*1024) return `${(bytes/1024).toFixed(1)} KB`;
  return `${(bytes/1024/1024).toFixed(1)} MB`;
}
export const DISCLAIMER = "Not legal advice. This tool explains documents and identifies possible risks. Always consult a qualified lawyer before making legal decisions. AI can make mistakes.";
