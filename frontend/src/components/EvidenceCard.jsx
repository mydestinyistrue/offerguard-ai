import React from 'react';
import { Quote, Tag, CheckCircle2, AlertOctagon } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function EvidenceCard({ signals = [] }) {
  const { t } = useLanguage();

  if (!signals || signals.length === 0) {
    return (
      <div className="bg-card border border-border rounded-2xl p-5 text-center text-muted-foreground text-xs">
        No warning signals found in this text.
      </div>
    );
  }

  const formatSignalId = (id) => {
    return id.replace(/_/g, ' ');
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-5 md:p-6 transition-colors duration-200 space-y-4 shadow-xs">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm md:text-base font-bold text-foreground flex items-center gap-2">
            <Tag className="w-4 h-4 text-primary" />
            {t('evidence') || 'Warning Signals Found'}
          </h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            Key phrases extracted from the submitted message
          </p>
        </div>

        <span className="text-xs font-semibold px-3 py-1 rounded-full bg-secondary text-muted-foreground border border-border">
          {signals.length} Signals
        </span>
      </div>

      <div className="grid grid-cols-1 gap-2.5">
        {signals.map((sig, idx) => {
          const isNegative = sig.weight < 0;
          const isHighWeight = Math.abs(sig.weight) >= 30;

          let cardStyle = "bg-secondary/40 border-border";
          let badgeStyle = "bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-500/20";

          if (isNegative) {
            cardStyle = "bg-emerald-500/5 border-emerald-500/20";
            badgeStyle = "bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border-emerald-500/20";
          } else if (isHighWeight) {
            cardStyle = "bg-red-500/5 border-red-500/20";
            badgeStyle = "bg-red-500/10 text-red-700 dark:text-red-300 border-red-500/20";
          }

          return (
            <div
              key={idx}
              className={`rounded-xl p-3.5 border transition-all ${cardStyle}`}
            >
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2">
                  {isNegative ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                  ) : (
                    <AlertOctagon className="w-4 h-4 text-red-600 dark:text-red-400" />
                  )}
                  <span className="font-semibold text-xs text-foreground capitalize">
                    {formatSignalId(sig.id)}
                  </span>
                </div>

                <span className={`text-[10px] font-mono px-2.5 py-0.5 rounded-full border ${badgeStyle}`}>
                  {sig.weight > 0 ? `+${sig.weight}` : sig.weight} Weight
                </span>
              </div>

              {sig.evidence && (
                <div className="flex items-start gap-2 bg-card rounded-lg p-2.5 border border-border text-xs text-muted-foreground italic mt-2">
                  <Quote className="w-3.5 h-3.5 text-muted-foreground/60 shrink-0 mt-0.5" />
                  <span>"{sig.evidence}"</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
