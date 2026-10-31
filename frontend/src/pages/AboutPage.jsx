import React from 'react';
import { Link } from 'react-router-dom';
import { 
  ShieldCheck, 
  Building2, 
  Globe, 
  Layers, 
  Lock, 
  FileText, 
  PhoneCall, 
  ExternalLink, 
  Calendar, 
  MapPin, 
  CheckCircle2, 
  Cpu, 
  ArrowRight 
} from 'lucide-react';

export default function AboutPage() {
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
          <img 
            src="/emblem.png" 
            alt="OfferGuard AI Emblem" 
            className="w-10 h-10 object-contain rounded-xl shadow-xs" 
          />
          <h1 className="text-3xl sm:text-4xl font-extrabold text-foreground tracking-tight">
            About OfferGuard AI
          </h1>
        </div>

        {/* Metadata Badges */}
        <div className="flex flex-wrap gap-4 md:gap-6 text-xs sm:text-sm text-muted-foreground pt-1">
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-primary" />
            <span>Updated: {currentDate}</span>
          </div>
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-primary" />
            <span>India · National Scope</span>
          </div>
          <div className="flex items-center gap-2">
            <PhoneCall className="w-4 h-4 text-primary" />
            <span>Emergency: Helpline 1930</span>
          </div>
        </div>
      </div>

      {/* Main Container */}
      <div className="bg-card rounded-2xl md:rounded-3xl border border-border shadow-sm p-6 sm:p-10 space-y-10 text-foreground">
        
        {/* Section: Core Mission */}
        <div className="space-y-3">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground flex items-center gap-2.5">
            <ShieldCheck className="w-5 h-5 text-primary" />
            Core Mission & Citizen Protection
          </h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            OfferGuard AI is a free citizen verification service created to shield job seekers, students, and working professionals across India from employment fraud, part-time task scams, and fake appointment letters before any money is transferred.
          </p>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Every day, thousands of victims are targeted with unsolicited WhatsApp and Telegram messages promising high daily wages for trivial actions like liking YouTube videos, rating hotels, or reviewing apps. Fraud syndicates systematically transfer an initial small payout (₹150 to ₹300) to establish false trust, then trick victims into depositing thousands into fake prepaid merchant accounts. OfferGuard AI identifies these traps instantly and provides safe, actionable guidance.
          </p>
        </div>

        {/* Section: 5 Decoupled Verification Modules */}
        <div className="space-y-4 pt-4 border-t border-border">
          <div className="space-y-1">
            <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground flex items-center gap-2.5">
              <Layers className="w-5 h-5 text-primary" />
              Five Decoupled Verification Modules
            </h2>
            <p className="text-sm text-muted-foreground">
              OfferGuard AI is built with five standalone modules that run independently or in tandem:
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 pt-2">
            {/* Module 1 */}
            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-foreground">Module 1: Scam Pattern Engine</span>
                <span className="text-[10px] font-semibold text-muted-foreground">Deterministic</span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Applies heuristic pattern matching to detect upfront fee demands, daily wage lures, high-pressure urgency flags, and fake onboarding fees.
              </p>
            </div>

            {/* Module 2 */}
            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-foreground">Module 2: MCA Corporate Verifier</span>
                <span className="text-[10px] font-semibold text-muted-foreground">Registry Search</span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Matches claimed company names against official Ministry of Corporate Affairs (data.gov.in) records using fuzzy name resolution and CIN verification.
              </p>
            </div>

            {/* Module 3 */}
            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-foreground">Module 3: Link & Domain Safety</span>
                <span className="text-[10px] font-semibold text-muted-foreground">Threat Feeds</span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Queries VirusTotal intelligence feeds to identify spoofed recruiter domains, newly created websites, and malicious phishing redirects.
              </p>
            </div>

            {/* Module 4 */}
            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-foreground">Module 4: Scam Stage Classifier</span>
                <span className="text-[10px] font-semibold text-muted-foreground">Timeline Stepper</span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Maps conversational progression to the 5 stages of task fraud (Stage 0: Bait to Stage 4: Secondary Extortion).
              </p>
            </div>

            {/* Module 5 */}
            <div className="p-4 rounded-xl bg-secondary/40 border border-border space-y-2 md:col-span-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-foreground">Module 5: Victim Protection & 1930 Helper</span>
                <span className="text-[10px] font-semibold text-muted-foreground">Emergency FIR</span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Formats formal cybercrime.gov.in complaint drafts, extracts suspect UPI handles and phone numbers, and provides the step-by-step checklist to initiate the 1930 Golden Hour financial freeze.
              </p>
            </div>
          </div>
        </div>

        {/* Section: Privacy & Zero Retention */}
        <div className="space-y-4 pt-4 border-t border-border">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground flex items-center gap-2.5">
            <Lock className="w-5 h-5 text-primary" />
            Privacy & Zero-Retention Architecture
          </h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Privacy is an immutable architectural requirement across all systems:
          </p>
          <ul className="space-y-2.5 text-sm text-muted-foreground list-disc pl-5">
            <li>
              <strong className="text-foreground font-semibold">In-Browser OCR:</strong> Screenshot processing runs locally inside your browser using Tesseract.js WebAssembly. Image pixels never touch server disks or leave your device.
            </li>
            <li>
              <strong className="text-foreground font-semibold">No Chat Database:</strong> Messages and uploaded files are processed in ephemeral server memory and discarded immediately upon response completion.
            </li>
            <li>
              <strong className="text-foreground font-semibold">Automatic PII Masking:</strong> Sensitive identifiers like personal phone numbers, bank accounts, and UPI handles are automatically masked prior to any evaluation.
            </li>
          </ul>
        </div>

        {/* Section: Public Feeds & Verified Registries */}
        <div className="space-y-4 pt-4 border-t border-border">
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground flex items-center gap-2.5">
            <Cpu className="w-5 h-5 text-primary" />
            Official Registries & Technical Stack
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs pt-1">
            <div className="p-3.5 rounded-xl bg-secondary/30 border border-border space-y-1">
              <span className="font-bold text-foreground block text-sm">Ministry of Corporate Affairs (MCA)</span>
              <span className="text-muted-foreground leading-relaxed block">
                Official Government of India corporate registry dataset from data.gov.in.
              </span>
            </div>
            <div className="p-3.5 rounded-xl bg-secondary/30 border border-border space-y-1">
              <span className="font-bold text-foreground block text-sm">VirusTotal Intelligence API</span>
              <span className="text-muted-foreground leading-relaxed block">
                Cross-checks recruiter domains and links against 70+ cybersecurity vendors.
              </span>
            </div>
            <div className="p-3.5 rounded-xl bg-secondary/30 border border-border space-y-1">
              <span className="font-bold text-foreground block text-sm">FastAPI & Python 3.12</span>
              <span className="text-muted-foreground leading-relaxed block">
                High-performance modular backend with strict decoupled architecture.
              </span>
            </div>
            <div className="p-3.5 rounded-xl bg-secondary/30 border border-border space-y-1">
              <span className="font-bold text-foreground block text-sm">Vite & Tailwind CSS</span>
              <span className="text-muted-foreground leading-relaxed block">
                Fast, responsive client interface with zero tracking scripts, clean typography, and full dark mode support.
              </span>
            </div>
          </div>
        </div>

        {/* Section: Emergency 1930 Helpline Banner */}
        <div className="p-5 rounded-2xl bg-secondary/50 border border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-primary" />
              National Cyber Crime Reporting Helpline (1930)
            </h3>
            <p className="text-xs text-muted-foreground leading-relaxed">
              If you have transferred funds to a fraudulent account, dial 1930 immediately or file a report at cybercrime.gov.in within the Golden Hour (first 2–3 hours) for maximum fund freeze success.
            </p>
          </div>
          <a
            href="tel:1930"
            className="px-5 py-2.5 rounded-full bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-colors shrink-0 shadow-xs cursor-pointer"
          >
            Call 1930 Free
          </a>
        </div>

        {/* Section: Action Buttons */}
        <div className="pt-6 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-3">
          <Link
            to="/"
            className="w-full sm:w-auto px-7 py-3 rounded-full bg-primary hover:bg-primary/90 text-primary-foreground text-sm font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer shadow-xs"
          >
            <span>Check an Offer Now</span>
            <ArrowRight className="w-4 h-4" />
          </Link>

          <Link
            to="/privacy"
            className="w-full sm:w-auto px-6 py-3 rounded-full border border-border bg-card hover:bg-secondary text-foreground text-sm font-semibold flex items-center justify-center gap-2 transition-colors cursor-pointer"
          >
            <span>Read Privacy Policy</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
