import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShieldCheck, BarChart3, Lock, Info, Menu, X, Sun, Moon, PhoneCall } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function Navbar() {
  const { toggleTheme, isDark } = useTheme();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { to: '/', label: 'Verify Offer', icon: ShieldCheck },
    { to: '/eval', label: 'Benchmark', icon: BarChart3 },
    { to: '/privacy', label: 'Privacy', icon: Lock },
    { to: '/about', label: 'About', icon: Info },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/60 px-4 sm:px-6 transition-colors duration-200">
      <div className="max-w-6xl mx-auto h-16 flex items-center justify-between">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <img
            src="/emblem.png"
            alt="OfferGuard AI"
            className="w-8 h-8 rounded-lg object-contain shadow-xs group-hover:scale-105 transition-transform"
          />
          <span className="font-bold text-base tracking-tight text-foreground">
            OfferGuard <span className="text-primary font-semibold">AI</span>
          </span>
        </Link>

        {/* Desktop Nav Links */}
        <div className="hidden md:flex items-center gap-1 bg-secondary/60 p-1 rounded-full border border-border/60">
          {navLinks.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-card text-foreground shadow-xs font-semibold'
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {item.label}
              </Link>
            );
          })}
        </div>

        {/* Actions (Helpline + Theme Toggle) */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Helpline 1930 */}
          <a
            href="tel:1930"
            className="hidden sm:inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs font-semibold bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-all shadow-xs"
            title="National Cyber Crime Reporting Helpline"
          >
            <PhoneCall className="w-3.5 h-3.5" />
            <span>Helpline 1930</span>
          </a>

          {/* Light / Dark Mode Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-full text-muted-foreground hover:text-foreground hover:bg-secondary border border-border/40 transition-colors cursor-pointer"
            title={isDark ? "Switch to Day Mode" : "Switch to Dark Mode"}
            aria-label="Toggle theme"
          >
            {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-foreground" />}
          </button>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-xl text-muted-foreground hover:bg-secondary cursor-pointer"
            aria-label="Open menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden pb-4 pt-2 border-t border-border flex flex-col gap-1.5 animate-fade-in">
          {navLinks.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-sm font-medium ${
                  isActive
                    ? 'bg-primary/10 text-primary font-semibold'
                    : 'text-foreground hover:bg-secondary'
                }`}
              >
                <Icon className="w-4 h-4" />
                {item.label}
              </Link>
            );
          })}
          <a
            href="tel:1930"
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium text-red-600 dark:text-red-400 bg-red-500/10 mt-1"
          >
            <PhoneCall className="w-4 h-4" />
            <span>Call Helpline 1930</span>
          </a>
        </div>
      )}
    </nav>
  );
}
