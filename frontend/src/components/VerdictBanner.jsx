import React from 'react';
import { AlertTriangle, ShieldAlert, ShieldCheck, HelpCircle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function VerdictBanner({ result }) {
  const { t } = useLanguage();
  if (!result) return null;

  const { verdict, explanation_simple, confidence, pii_masked, pii_types_found } = result;

  const config = {
    SCAM: {
      title: t('scam') || 'High Risk Scam Detected',
      badge: 'High Risk',
      icon: AlertTriangle,
      lightBg: 'bg-red-500/10 border-red-500/20 text-red-700 dark:text-red-300',
      iconColor: 'text-red-600 dark:text-red-400',
      badgeColor: 'bg-red-500/15 text-red-700 dark:text-red-300 border-red-500/30',
    },
    SUSPICIOUS: {
      title: t('suspicious') || 'Suspicious Offer',
      badge: 'Exercise Caution',
      icon: ShieldAlert,
      lightBg: 'bg-amber-500/10 border-amber-500/20 text-amber-800 dark:text-amber-300',
      iconColor: 'text-amber-600 dark:text-amber-400',
      badgeColor: 'bg-amber-500/15 text-amber-800 dark:text-amber-300 border-amber-500/30',
    },
    LIKELY_GENUINE: {
      title: t('genuine') || 'Likely Genuine Recruitment',
      badge: 'Legitimate',
      icon: ShieldCheck,
      lightBg: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-800 dark:text-emerald-300',
      iconColor: 'text-emerald-600 dark:text-emerald-400',
      badgeColor: 'bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 border-emerald-500/30',
    },
    UNSURE: {
      title: t('unsure') || 'Needs More Information',
      badge: 'Inconclusive',
      icon: HelpCircle,
      lightBg: 'bg-secondary border-border text-foreground',
      iconColor: 'text-muted-foreground',
      badgeColor: 'bg-secondary text-muted-foreground border-border',
    },
  };

  const current = config[verdict] || config.UNSURE;
  const Icon = current.icon;
  const confidencePercent = Math.round((confidence || 0.85) * 100);

  return (
    <div className={`rounded-2xl p-5 md:p-6 border ${current.lightBg} transition-all duration-200`}>
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-card border border-border/50 shadow-xs">
            <Icon className={`w-5 h-5 ${current.iconColor}`} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base sm:text-lg font-bold tracking-tight text-foreground">
                {current.title}
              </h3>
              <span className={`text-xs px-3 py-1 rounded-full font-semibold border ${current.badgeColor}`}>
                {current.badge}
              </span>
            </div>
            <p className="text-xs text-muted-foreground mt-0.5">
              Confidence: {confidencePercent}%
            </p>
          </div>
        </div>

        {pii_masked && (
          <span className="text-xs px-3.5 py-1.5 rounded-full bg-secondary text-muted-foreground border border-border font-medium">
            Contact details masked
          </span>
        )}
      </div>

      <div className="mt-2 text-xs sm:text-sm leading-relaxed text-muted-foreground">
        <p>{explanation_simple || "No detailed summary available."}</p>
      </div>
    </div>
  );
}
