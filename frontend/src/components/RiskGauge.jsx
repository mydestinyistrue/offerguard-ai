import React from 'react';
import { useLanguage } from '../context/LanguageContext';

export default function RiskGauge({ score }) {
  const { t } = useLanguage();
  const radius = 46;
  const circumference = 2 * Math.PI * radius;
  const validScore = Math.min(Math.max(score || 0, 0), 100);
  const strokeDashoffset = circumference - (validScore / 100) * circumference;

  let strokeColor = '#16a34a'; // green
  let severityLabel = 'Safe / Low Risk';
  let severityBg = 'text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-800';

  if (validScore >= 70) {
    strokeColor = '#dc2626'; // red
    severityLabel = 'High Scam Risk';
    severityBg = 'text-red-700 dark:text-red-300 bg-red-50 dark:bg-red-950/40 border-red-200 dark:border-red-800';
  } else if (validScore >= 40) {
    strokeColor = '#d97706'; // amber
    severityLabel = 'Suspicious / Caution';
    severityBg = 'text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 border-amber-200 dark:border-amber-800';
  }

  return (
    <div className="bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 flex flex-col items-center justify-center text-center relative transition-colors duration-200 shadow-xs">
      <h3 className="text-xs uppercase font-bold tracking-wider text-slate-500 dark:text-slate-400 mb-2">
        {t('riskScore') || 'Threat Level'}
      </h3>

      <div className="relative w-32 h-32 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
          {/* Background circle with clear greyness */}
          <circle
            cx="60"
            cy="60"
            r={radius}
            className="stroke-gray-300 dark:stroke-neutral-700"
            strokeWidth="9"
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx="60"
            cy="60"
            r={radius}
            stroke={strokeColor}
            strokeWidth="9"
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-700 ease-out"
          />
        </svg>

        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            {validScore}%
          </span>
          <span className="text-[10px] uppercase font-semibold text-slate-400">
            Probability
          </span>
        </div>
      </div>

      <div className={`mt-3 px-3 py-1 rounded-full text-xs font-semibold border ${severityBg}`}>
        {severityLabel}
      </div>
    </div>
  );
}
