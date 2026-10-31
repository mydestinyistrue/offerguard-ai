import React from 'react';
import { 
  Building2, 
  Globe, 
  ExternalLink, 
  CheckCircle, 
  AlertTriangle, 
  XCircle, 
  ShieldAlert, 
  ShieldCheck, 
  ShieldQuestion 
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function CompanyCheck({ company }) {
  const { t } = useLanguage();
  if (!company) return null;

  const {
    name,
    cin,
    status,
    verification_outcome,
    domain_signals = [],
    virustotal,
  } = company;

  const isFound = company.mca_match === true;

  // Determine if a meaningful company name was provided in the message
  const hasCompany = Boolean(
    name && 
    name.trim() !== '' && 
    name.trim().toLowerCase() !== 'unknown' && 
    name.trim().toLowerCase() !== 'none' &&
    name.trim().toLowerCase() !== 'no registered company name mentioned'
  );

  // Determine if any domain or external link was found
  const hasDomain = Boolean(
    (virustotal && virustotal.status && virustotal.status !== 'NOT_CONFIGURED' && virustotal.url) ||
    (domain_signals && domain_signals.length > 0)
  );

  // Case 1: Neither company nor domain was included in the message
  if (!hasCompany && !hasDomain) {
    return (
      <div className="bg-card border border-border rounded-2xl p-5 md:p-6 transition-colors duration-200 shadow-xs space-y-3">
        <h3 className="text-sm md:text-base font-bold text-foreground flex items-center gap-2">
          <Building2 className="w-4 h-4 text-primary" />
          Company Status
        </h3>
        <div className="bg-secondary/40 rounded-xl p-4 border border-border">
          <p className="text-xs sm:text-sm text-muted-foreground">
            No registered company name mentioned
          </p>
        </div>
      </div>
    );
  }

  // Case 2: Either company, domain, or both are present
  return (
    <div className="bg-card border border-border rounded-2xl p-5 md:p-6 transition-colors duration-200 space-y-4 shadow-xs">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm md:text-base font-bold text-foreground flex items-center gap-2">
            <Building2 className="w-4 h-4 text-primary" />
            {hasDomain ? 'Company Status & Link Safety' : 'Company Status'}
          </h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            Verified against Government of India corporate registry
          </p>
        </div>

        {hasCompany && (
          <a
            href="https://www.mca.gov.in"
            target="_blank"
            rel="noreferrer"
            className="text-xs text-primary hover:underline inline-flex items-center gap-1 font-semibold"
          >
            MCA Portal <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>

      <div className={`grid grid-cols-1 ${hasDomain ? 'md:grid-cols-2' : ''} gap-4`}>
        {/* Left: Company Status */}
        <div className="bg-secondary/40 rounded-xl p-4 border border-border space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Company Status
            </span>
            {hasCompany && (
              isFound ? (
                <span className="inline-flex items-center gap-1 text-[11px] font-bold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20">
                  <CheckCircle className="w-3 h-3" /> Registered
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 text-[11px] font-bold px-3 py-1 rounded-full bg-secondary text-muted-foreground border border-border">
                  <XCircle className="w-3 h-3" /> Unregistered
                </span>
              )
            )}
          </div>

          {!hasCompany ? (
            <p className="text-xs sm:text-sm text-muted-foreground pt-1">
              No registered company name mentioned
            </p>
          ) : (
            <>
              <div>
                <div className="text-xs text-muted-foreground">Claimed Employer</div>
                <div className="font-bold text-foreground text-sm">
                  {name}
                </div>
              </div>

              {cin && (
                <div>
                  <div className="text-[11px] text-muted-foreground">Corporate ID (CIN)</div>
                  <div className="font-mono text-xs text-foreground font-semibold">{cin}</div>
                </div>
              )}

              <div className="text-xs text-muted-foreground pt-1 border-t border-border">
                <span className="font-semibold text-foreground">Registry Check: </span>
                {verification_outcome || (isFound ? "Active company found in official records." : "No registered company match found.")}
              </div>
            </>
          )}
        </div>

        {/* Right: Domain & VirusTotal URL Analysis (Only if links exist) */}
        {hasDomain && (
          <div className="bg-secondary/40 rounded-xl p-4 border border-border space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
                <Globe className="w-3.5 h-3.5" /> Link Safety
              </span>
            </div>

            {virustotal && virustotal.status !== "NOT_CONFIGURED" ? (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  {virustotal.status === "MALICIOUS" ? (
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold px-3 py-1 rounded-full bg-red-500/10 text-red-700 dark:text-red-300 border border-red-500/20">
                      <ShieldAlert className="w-3 h-3" /> Reported Dangerous ({virustotal.malicious} vendors)
                    </span>
                  ) : virustotal.status === "SUSPICIOUS" ? (
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold px-3 py-1 rounded-full bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20">
                      <AlertTriangle className="w-3 h-3" /> Suspicious Link
                    </span>
                  ) : virustotal.status === "CLEAN" ? (
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20">
                      <ShieldCheck className="w-3 h-3" /> Verified Safe
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold px-3 py-1 rounded-full bg-secondary text-muted-foreground border border-border">
                      <ShieldQuestion className="w-3 h-3" /> Newly Registered Domain
                    </span>
                  )}
                </div>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {virustotal.reason}
                </p>
              </div>
            ) : (
              <p className="text-xs text-muted-foreground">
                No suspicious external links found in this message.
              </p>
            )}

            {domain_signals.length > 0 && (
              <div className="pt-2 border-t border-border space-y-1">
                <span className="text-[11px] font-semibold text-muted-foreground">Link Notes:</span>
                <ul className="text-xs text-muted-foreground space-y-1">
                  {domain_signals.map((sig, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="text-primary font-bold">•</span>
                      <span>{sig}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
