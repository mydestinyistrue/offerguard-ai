import React from 'react';
import { ShieldCheck, PhoneCall, ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="mt-20 border-t border-border bg-card/60 backdrop-blur-md py-12 px-4 text-muted-foreground text-xs transition-colors duration-200">
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        {/* Brand Col */}
        <div className="space-y-3 md:col-span-2">
          <div className="flex items-center gap-2.5">
            <img
              src="/emblem.png"
              alt="OfferGuard AI"
              className="w-7 h-7 rounded-lg object-contain shadow-xs"
            />
            <span className="font-bold text-foreground text-base tracking-tight">OfferGuard AI</span>
          </div>
          <p className="text-muted-foreground max-w-md leading-relaxed">
            A free, instant tool to check job offers, tasks, and recruiter messages before you send money or share sensitive details.
          </p>
          <p className="text-xs text-muted-foreground/80">
            Private by design · Messages are never saved or stored.
          </p>
        </div>

        {/* Helpline Col */}
        <div className="space-y-2">
          <h4 className="font-bold text-foreground uppercase tracking-wider text-[11px]">Helpline & Support</h4>
          <ul className="space-y-2">
            <li>
              <a
                href="tel:1930"
                className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-all shadow-xs"
              >
                <PhoneCall className="w-3.5 h-3.5" />
                <span>Helpline 1930 (Toll Free)</span>
              </a>
            </li>
            <li>
              <a
                href="https://cybercrime.gov.in"
                target="_blank"
                rel="noreferrer"
                className="hover:text-foreground inline-flex items-center gap-1 transition-colors"
              >
                cybercrime.gov.in <ExternalLink className="w-3 h-3" />
              </a>
            </li>
            <li>
              <a
                href="https://www.mca.gov.in"
                target="_blank"
                rel="noreferrer"
                className="hover:text-foreground inline-flex items-center gap-1 transition-colors"
              >
                mca.gov.in (Company Registry) <ExternalLink className="w-3 h-3" />
              </a>
            </li>
          </ul>
        </div>

        {/* Quick Links Col */}
        <div className="space-y-2">
          <h4 className="font-bold text-foreground uppercase tracking-wider text-[11px]">Pages</h4>
          <ul className="space-y-2">
            <li>
              <Link to="/eval" className="hover:text-foreground transition-colors">
                Benchmark Results (60 Cases)
              </Link>
            </li>
            <li>
              <Link to="/privacy" className="hover:text-foreground transition-colors">
                Privacy Policy
              </Link>
            </li>
            <li>
              <Link to="/about" className="hover:text-foreground transition-colors">
                About & Data Sources
              </Link>
            </li>
          </ul>
        </div>
      </div>

      <div className="max-w-6xl mx-auto pt-6 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-3 text-muted-foreground text-[11px]">
        <p>© 2026 OfferGuard AI. All rights reserved.</p>
        <p>Built to protect job seekers from online employment fraud.</p>
      </div>
    </footer>
  );
}
