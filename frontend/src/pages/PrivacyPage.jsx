import React from 'react';
import { Calendar, MapPin, Mail, ShieldCheck, Lock, EyeOff, FileText, CheckCircle2, AlertTriangle, ExternalLink } from 'lucide-react';

export default function PrivacyPage() {
  const currentDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12 space-y-8">
      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <img src="/emblem.png" alt="OfferGuard AI" className="w-10 h-10 object-contain rounded-xl shadow-xs" />
          <h1 className="text-3xl sm:text-4xl font-extrabold text-foreground tracking-tight">
            Privacy Policy
          </h1>
        </div>

        {/* Metadata Badges */}
        <div className="flex flex-wrap gap-4 md:gap-6 text-xs sm:text-sm text-muted-foreground pt-1">
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-primary" />
            <span>Last Updated: {currentDate}</span>
          </div>
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-primary" />
            <span>India · National Scope</span>
          </div>
          <div className="flex items-center gap-2">
            <Mail className="w-4 h-4 text-primary" />
            <a href="https://cybercrime.gov.in" target="_blank" rel="noreferrer" className="hover:text-foreground underline">
              cybercrime.gov.in
            </a>
          </div>
        </div>
      </div>

      {/* Main Privacy Card */}
      <div className="bg-card rounded-2xl md:rounded-3xl border border-border shadow-sm p-6 sm:p-10 space-y-8 text-foreground">
        {/* 1. Introduction */}
        <div className="space-y-3">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
            1. Introduction & Core Philosophy
          </h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Welcome to OfferGuard AI. We believe that verifying suspicious employment communications, task schemes, and appointment letters must never compromise the privacy of job seekers, students, and citizens.
          </p>
          <p className="text-sm text-muted-foreground leading-relaxed">
            OfferGuard AI is built from the ground up on a <strong className="text-foreground">zero-retention, privacy-first architecture</strong>. We do not store your chats, do not save your uploaded screenshots, and do not create user tracking profiles.
          </p>
        </div>

        {/* 2. What We Do NOT Collect */}
        <div className="space-y-4 pt-4 border-t border-border">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
            2. Information We Do NOT Collect
          </h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Unlike typical web platforms, OfferGuard AI enforces strict negative data collection boundaries:
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-1.5">
              <span className="font-semibold text-xs text-foreground flex items-center gap-1.5">
                <span className="text-red-500 font-bold">✗</span> No Chat History or Database Logs
              </span>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Raw messages and chat logs are processed in temporary memory and completely discarded after analysis.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-1.5">
              <span className="font-semibold text-xs text-foreground flex items-center gap-1.5">
                <span className="text-red-500 font-bold">✗</span> No Image File Storage
              </span>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Screenshot OCR runs directly in your browser using client-side WebAssembly. Image pixels are never saved to our server disks.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-1.5">
              <span className="font-semibold text-xs text-foreground flex items-center gap-1.5">
                <span className="text-red-500 font-bold">✗</span> No Advertising or Tracking Cookies
              </span>
              <p className="text-xs text-muted-foreground leading-relaxed">
                We do not use advertising networks, behavioral tracking pixels, or cross-site tracking scripts.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-1.5">
              <span className="font-semibold text-xs text-foreground flex items-center gap-1.5">
                <span className="text-red-500 font-bold">✗</span> No Personal Identity Harvesting
              </span>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Indian phone numbers, UPI handles, PAN cards, and Aadhaar numbers are automatically masked during scanning.
              </p>
            </div>
          </div>
        </div>

        {/* 3. Ephemeral Processing */}
        <div className="space-y-3 pt-4 border-t border-border">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
            3. How We Process Submitted Data
          </h2>
          <ul className="space-y-2.5 text-sm text-muted-foreground list-disc pl-5">
            <li>
              <strong className="text-foreground">In-Memory Analysis:</strong> When you click "Run Check", the submitted text is evaluated in temporary server memory against deterministic scam pattern banks and verified registry data.
            </li>
            <li>
              <strong className="text-foreground">Client-Side OCR:</strong> If you upload a screenshot, recognition is performed locally on your device via Tesseract.js WASM.
            </li>
            <li>
              <strong className="text-foreground">PII Redaction:</strong> Sensitive identifiers (such as personal phone numbers and payment handles) are masked before analysis to safeguard candidate confidentiality.
            </li>
            <li>
              <strong className="text-foreground">1930 Report Generation:</strong> Any complaint draft generated through the 1930 Helper is produced on-demand in your session and is not logged.
            </li>
          </ul>
        </div>

        {/* 4. External Services & Government Feeds */}
        <div className="space-y-3 pt-4 border-t border-border">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
            4. External Verification & Official Sources
          </h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            To provide accurate verification, OfferGuard AI references the following public and security intelligence feeds:
          </p>

          <div className="space-y-3 text-xs sm:text-sm text-muted-foreground">
            <div className="p-3.5 rounded-xl bg-secondary/30 border border-border">
              <span className="font-bold text-foreground block mb-0.5">Ministry of Corporate Affairs (MCA) Snapshot</span>
              <span>Used exclusively for read-only verification of company names, ROC status, and Corporate Identification Numbers (CIN).</span>
            </div>
            <div className="p-3.5 rounded-xl bg-secondary/30 border border-border">
              <span className="font-bold text-foreground block mb-0.5">VirusTotal Intelligence API</span>
              <span>External recruiter websites and short links found in messages are queried to check for malicious phishing or malware status.</span>
            </div>
            <div className="p-3.5 rounded-xl bg-secondary/30 border border-border">
              <span className="font-bold text-foreground block mb-0.5">National Cyber Crime Reporting Helpline (1930)</span>
              <span>OfferGuard AI provides speed-dial shortcuts and formats complaint text for victims reporting financial fraud to cybercrime.gov.in.</span>
            </div>
          </div>
        </div>

        {/* 5. Your Rights */}
        <div className="space-y-3 pt-4 border-t border-border">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
            5. User Rights & Data Retention
          </h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Because we do not store chat logs or maintain user accounts, you have complete control over your session:
          </p>
          <ul className="space-y-2 text-sm text-muted-foreground list-disc pl-5">
            <li>No sign-up or phone number login is required to use OfferGuard AI.</li>
            <li>Clicking "Clear" or refreshing your browser immediately flushes all in-memory data.</li>
            <li>No copy of your communication remains on our servers after your request finishes.</li>
          </ul>
        </div>

        {/* 6. Contact & Emergency Assistance */}
        <div className="space-y-3 pt-4 border-t border-border">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
            6. Emergency Helpline & Assistance
          </h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            If you have transferred funds to an employment or task scammer, time is critical. Immediately contact:
          </p>
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-xs sm:text-sm text-red-700 dark:text-red-300 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 shrink-0 text-red-600 dark:text-red-400" />
              <span>National Cyber Crime Helpline: <strong>Dial 1930</strong> (Toll Free across India)</span>
            </div>
            <a
              href="https://cybercrime.gov.in"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 font-bold underline hover:opacity-80"
            >
              cybercrime.gov.in <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
