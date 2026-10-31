import React from 'react';
import { Eye, ArrowRight, AlertTriangle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function NextMoveCard({ nextMove, verdict }) {
  const { t } = useLanguage();
  if (!nextMove || verdict === 'LIKELY_GENUINE') return null;

  return (
    <div className="bg-amber-500/10 border border-amber-500/20 rounded-2xl p-5 md:p-6 transition-colors duration-200 shadow-xs">
      <div className="flex items-start gap-4">
        <div className="p-2.5 rounded-xl bg-amber-500/15 text-amber-700 dark:text-amber-300 shrink-0 mt-0.5">
          <Eye className="w-5 h-5" />
        </div>

        <div className="space-y-2 flex-1">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-semibold text-amber-800 dark:text-amber-300 bg-amber-500/20 px-3 py-1 rounded-full border border-amber-500/30 flex items-center gap-1">
              <AlertTriangle className="w-3 h-3 inline" />
              Expected Next Step
            </span>
          </div>

          <h3 className="text-base font-bold text-foreground">
            {t('whatNext') || 'What the sender will likely ask for next'}
          </h3>

          <div className="p-3.5 rounded-xl bg-card border border-border text-foreground text-xs sm:text-sm leading-relaxed font-medium shadow-2xs">
            "{nextMove}"
          </div>

          <p className="text-xs text-muted-foreground pt-0.5 flex items-center gap-1.5">
            <ArrowRight className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400 shrink-0" />
            Do not send money or bank details if they make this request.
          </p>
        </div>
      </div>
    </div>
  );
}
