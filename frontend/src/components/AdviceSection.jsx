import React from 'react';
import { ShieldAlert, ShieldCheck } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function AdviceSection({ advice = [], verdict }) {
  const { t } = useLanguage();

  if (!advice || advice.length === 0) return null;

  const isScam = verdict === 'SCAM';
  const isGenuine = verdict === 'LIKELY_GENUINE';

  return (
    <div className="bg-card border border-border rounded-2xl p-5 md:p-6 transition-colors duration-200 space-y-3 shadow-xs">
      <div className="flex items-center gap-3">
        <div className={`p-2.5 rounded-xl ${
          isScam
            ? 'bg-red-500/10 text-red-600 dark:text-red-400'
            : isGenuine
            ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
            : 'bg-amber-500/10 text-amber-600 dark:text-amber-400'
        }`}>
          {isGenuine ? <ShieldCheck className="w-5 h-5" /> : <ShieldAlert className="w-5 h-5" />}
        </div>
        <div>
          <h3 className="text-sm md:text-base font-bold text-foreground">
            {t('advice') || 'Recommended Next Steps'}
          </h3>
          <p className="text-xs text-muted-foreground">
            {isGenuine
              ? 'Best practices for onboarding and official documentation'
              : 'Steps to take right now to protect your money and accounts'}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-2 pt-1">
        {advice.map((item, idx) => (
          <div
            key={idx}
            className="flex items-start gap-3 p-3.5 rounded-xl bg-secondary/40 border border-border text-xs sm:text-sm text-foreground"
          >
            <div className="w-5 h-5 rounded-full bg-secondary text-foreground font-bold flex items-center justify-center shrink-0 text-xs mt-0.5 border border-border">
              {idx + 1}
            </div>
            <p className="leading-relaxed text-muted-foreground">{item}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
