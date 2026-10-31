import React, { useState } from 'react';
import { PhoneCall, FileText, Copy, Check, ExternalLink, ShieldAlert, Loader2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function ReportPack({ text, messages, result }) {
  const { lang, t } = useLanguage();
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [copied, setCopied] = useState(false);
  const [victimName, setVictimName] = useState('');
  const [amountLost, setAmountLost] = useState('');

  const handleGenerateReport = async () => {
    setLoading(true);
    try {
      const payload = {
        text: text,
        messages: messages,
        victim_name: victimName || undefined,
        amount_lost: amountLost ? parseFloat(amountLost) : undefined,
        language: lang,
      };

      const res = await fetch('/api/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const data = await res.json();
        setReportData(data);
      }
    } catch (e) {
      console.error('Failed to generate report', e);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!reportData?.report_text) return;
    navigator.clipboard.writeText(reportData.report_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-5 md:p-6 transition-colors duration-200 space-y-5 shadow-xs">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-semibold text-red-700 dark:text-red-300 bg-red-500/10 px-3 py-1 rounded-full border border-red-500/20 inline-flex items-center gap-1.5">
              <ShieldAlert className="w-3.5 h-3.5 inline" />
              1930 Cybercrime Assistance
            </span>
          </div>
          <h3 className="text-base font-bold text-foreground mt-2">
            {t('reportPack') || 'Prepare Helpline 1930 Complaint Text'}
          </h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            Organizes suspect UPIs, phone numbers, and timeline into a clear complaint format
          </p>
        </div>

        <div className="flex items-center gap-2">
          <a
            href="tel:1930"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-xs font-semibold bg-red-600 hover:bg-red-700 text-white transition-all shadow-xs cursor-pointer active:scale-98"
          >
            <PhoneCall className="w-3.5 h-3.5" />
            <span>Call 1930 Free</span>
          </a>
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 px-4 py-2 rounded-full text-xs font-medium bg-secondary hover:bg-secondary/80 text-foreground border border-border transition-colors cursor-pointer"
          >
            <span>cybercrime.gov.in</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>

      {!reportData ? (
        <div className="bg-secondary/40 rounded-xl p-4 border border-border space-y-4">
          <p className="text-xs text-muted-foreground leading-relaxed">
            If you or someone you know transferred money or shared personal details, enter optional details below to format an incident report for 1930 or the Cyber Crime portal.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1">
                Your Name (Optional)
              </label>
              <input
                type="text"
                value={victimName}
                onChange={(e) => setVictimName(e.target.value)}
                placeholder="e.g. Rahul Sharma"
                className="w-full text-xs px-3.5 py-2.5 rounded-xl bg-card border border-border text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary transition-colors"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1">
                Amount Lost in ₹ (Optional)
              </label>
              <input
                type="number"
                value={amountLost}
                onChange={(e) => setAmountLost(e.target.value)}
                placeholder="e.g. 5000"
                className="w-full text-xs px-3.5 py-2.5 rounded-xl bg-card border border-border text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary transition-colors"
              />
            </div>
          </div>

          <div className="pt-1">
            <button
              onClick={handleGenerateReport}
              disabled={loading}
              className="w-full sm:w-auto px-7 py-3 rounded-full bg-primary text-primary-foreground font-semibold text-xs hover:bg-primary/90 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 active:scale-98 shadow-xs"
            >
              {loading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Preparing Draft...</span>
                </>
              ) : (
                <>
                  <FileText className="w-3.5 h-3.5" />
                  <span>Generate Complaint Draft</span>
                </>
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
              <Check className="w-3.5 h-3.5" /> Draft Ready
            </span>
            <button
              onClick={handleCopy}
              className="inline-flex items-center gap-1.5 px-5 py-2 rounded-full text-xs font-semibold bg-primary hover:bg-primary/90 text-primary-foreground transition-all cursor-pointer shadow-xs active:scale-98"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied to Clipboard!' : 'Copy Draft'}</span>
            </button>
          </div>

          <textarea
            readOnly
            rows={10}
            value={reportData.report_text}
            className="w-full font-mono text-xs p-4 rounded-xl bg-secondary/30 border border-border text-foreground focus:outline-none resize-none leading-relaxed"
          />

          <p className="text-[11px] text-muted-foreground">
            Tip: Call 1930 immediately to freeze the suspect's bank account or UPI ID before the money is withdrawn.
          </p>
        </div>
      )}
    </div>
  );
}
