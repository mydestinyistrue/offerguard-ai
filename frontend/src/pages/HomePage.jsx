import React, { useState, useEffect, useRef } from 'react';
import { 
  ShieldCheck, 
  Upload, 
  FileText, 
  Trash2, 
  ArrowRight, 
  ArrowLeft,
  Loader2, 
  CheckCircle2, 
  X, 
  Search,
  AlertTriangle,
  Building2,
  PhoneCall,
  Globe,
  FileCheck2,
  Lock,
  Eye,
  CreditCard,
  Plus,
  Image as ImageIcon
} from 'lucide-react';
import { processImageFile, processPdfFile } from '../utils/ocrService';
import VerdictBanner from '../components/VerdictBanner';
import StageTimeline from '../components/StageTimeline';
import NextMoveCard from '../components/NextMoveCard';
import EvidenceCard from '../components/EvidenceCard';
import CompanyCheck from '../components/CompanyCheck';
import AdviceSection from '../components/AdviceSection';
import ReportPack from '../components/ReportPack';

const DEMO_PRESETS = [
  {
    id: 'demo-hook',
    label: '1. YouTube Like Scam (Trial ₹150)',
    badge: 'Paid ₹150 Bait',
    badgeColor: 'text-amber-600 dark:text-amber-400 bg-amber-500/10 border-amber-500/20',
    text: `[29/10/2026, 11:00 AM] @Priya_HR: Welcome to Taskforce Digital E-Services! I am your mentor.
[29/10/2026, 11:01 AM] @Priya_HR: Here is Task 1: Open this link, like the video and send screenshot. You will get ₹150 trial bonus.
[29/10/2026, 11:05 AM] User: Done, sent screenshot of liked video.
[29/10/2026, 11:06 AM] @Priya_HR: Send your UPI ID or GPay number to receive payment.
[29/10/2026, 11:07 AM] User: myupi99@oksbi
[29/10/2026, 11:10 AM] @Priya_HR: ₹150 has been credited to your account! Please check your bank SMS.
[29/10/2026, 11:11 AM] User: Yes got ₹150! Thank you!
[29/10/2026, 11:12 AM] @Priya_HR: Great! Adding you to our VIP Task Channel. We have merchant commission tasks coming up.`,
  },
  {
    id: 'demo-prepaid',
    label: '2. Prepaid Task Scam (Deposit ₹1,000)',
    badge: 'Deposit Demand',
    badgeColor: 'text-red-600 dark:text-red-400 bg-red-500/10 border-red-500/20',
    text: `[30/10/2026, 12:00 PM] Mentor Rohit: You have completed novice tasks. Now starting Merchant Prepaid Task.
[30/10/2026, 12:01 PM] Mentor Rohit: Package A: Deposit ₹1,000 -> Return ₹1,300 within 15 minutes.
[30/10/2026, 12:01 PM] Mentor Rohit: Package B: Deposit ₹5,000 -> Return ₹6,800.
[30/10/2026, 12:02 PM] User: Why do I have to deposit my own money? This was supposed to be a job.
[30/10/2026, 12:03 PM] Mentor Rohit: This is a merchant security deposit to place mock orders. The money is 100% safe and refunded with 30% profit immediately.
[30/10/2026, 12:04 PM] Mentor Rohit: Pay ₹1,000 to merchant UPI ID: rajeshkumar8472@ybl and send screenshot immediately. Only 2 slots left!`,
  },
  {
    id: 'demo-lockin',
    label: '3. Frozen Withdrawal (Tax Demand ₹58k)',
    badge: 'Money Blocked',
    badgeColor: 'text-purple-600 dark:text-purple-400 bg-purple-500/10 border-purple-500/20',
    text: `[30/10/2026, 04:30 PM] User: I tried to withdraw my balance of ₹1,54,000 from the platform but it says 'WITHDRAWAL FROZEN'. Please help!
[30/10/2026, 04:32 PM] Finance Dept: Sir, your account has triggered anti-money laundering audit. As per Indian Income Tax regulations, you must pay 18% GST and 20% TDS (₹58,520) before withdrawal can be approved.
[30/10/2026, 04:34 PM] User: Can't you just deduct the tax from my ₹1.54 Lakh balance and give me the rest?
[30/10/2026, 04:35 PM] Finance Dept: No, the system cannot deduct automatically. You must deposit ₹58,520 from your own bank account to our clearing account within 2 hours or your account will be permanently frozen and reported to police!`,
  },
  {
    id: 'demo-genuine',
    label: '4. Genuine Offer (Campus Placement)',
    badge: 'Legitimate',
    badgeColor: 'text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
    text: `INFOSYS LIMITED
CIN: L85110KA1981PLC013115
Electronic City, Hosur Road, Bangalore - 560100
Date: October 15, 2026
Dear Student,
Sub: Offer of Employment - Systems Engineer
Further to our campus recruitment drive and subsequent technical & HR interviews conducted on October 5, 2026, we are pleased to offer you the role of Systems Engineer.
Annual Gross Salary: INR 3,60,000 per annum.
Please note:
- Infosys does not charge any application, processing, or training fee at any stage of recruitment.
- Please verify your offer letter on our official portal: https://career.infosys.com
- Your official reporting date is January 12, 2027 at Infosys Mysore Campus.
Warm regards,
HR Recruitment Team, Infosys Limited
recruitment@infosys.com`,
  },
];

const HOW_IT_WORKS_STEPS = [
  {
    icon: Upload,
    title: 'Paste or Upload',
    description: 'Share the text of a WhatsApp chat, SMS, or attach an offer letter screenshot or PDF.',
  },
  {
    icon: Search,
    title: 'Instant Verification',
    description: 'We inspect for upfront task deposit demands, verify registered company MCA records, and check link safety.',
  },
  {
    icon: CheckCircle2,
    title: 'Clear Verdict & Action',
    description: 'See your risk score, preview what the sender will ask next, and generate a 1930 complaint report if needed.',
  },
];

const WHAT_WE_CHECK_FOR = [
  {
    icon: CreditCard,
    color: 'bg-red-500/10 text-red-600 dark:text-red-400',
    title: 'Prepaid Task & Fee Detection',
    description: 'Flags security deposit demands, paid YouTube rating schemes, merchant commissions, and fake training charges before you transfer money.',
  },
  {
    icon: Building2,
    color: 'bg-blue-500/10 text-blue-600 dark:text-blue-400',
    title: 'Government MCA Registry',
    description: 'Validates claimed employers and Corporate Identification Numbers (CIN) directly against the Ministry of Corporate Affairs database.',
  },
  {
    icon: Globe,
    color: 'bg-purple-500/10 text-purple-600 dark:text-purple-400',
    title: 'Website & Link Safety',
    description: 'Scans recruiter domains and short links against global threat intelligence to catch new, suspicious, or malicious phishing pages.',
  },
  {
    icon: FileText,
    color: 'bg-amber-500/10 text-amber-600 dark:text-amber-400',
    title: 'Client-Side Screenshot OCR',
    description: 'Reads offer letters and chat screenshots directly inside your browser. Your images and documents are never stored on external servers.',
  },
  {
    icon: Eye,
    color: 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400',
    title: 'Next-Move Script Foresight',
    description: 'Deconstructs the conversation into known scam phases to predict what the fraudster will ask next so you can break the trap early.',
  },
  {
    icon: PhoneCall,
    color: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
    title: 'Helpline 1930 Reporting Kit',
    description: 'Formats suspect UPI handles, telephone numbers, and timeline evidence into a structured complaint draft ready for the 1930 portal.',
  },
];

export default function HomePage() {
  const [viewMode, setViewMode] = useState('main'); // 'main' | 'report'
  const [activeTab, setActiveTab] = useState('text'); // 'text' | 'upload' | 'presets'
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [scanStep, setScanStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showResultDialog, setShowResultDialog] = useState(false);
  const [isExplanationExpanded, setIsExplanationExpanded] = useState(false);

  // Multi-file state: [{ id, file, name, size, type: 'image' | 'pdf', previewUrl, text, status }]
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [ocrLoading, setOcrLoading] = useState(false);
  const [ocrStatusText, setOcrStatusText] = useState('');

  const scannerRef = useRef(null);

  // Helper to consolidate text from all completed files
  const updateConsolidatedText = (files) => {
    const doneFiles = files.filter((f) => f.text && f.text.trim());
    if (doneFiles.length === 0) {
      return;
    }
    if (doneFiles.length === 1) {
      setInputText(doneFiles[0].text);
    } else {
      const combined = doneFiles
        .map((f, idx) => `--- File ${idx + 1}: ${f.name} ---\n${f.text}`)
        .join('\n\n');
      setInputText(combined);
    }
  };

  // Clipboard paste (Ctrl+V) listener - appends all pasted images without replacing existing ones!
  useEffect(() => {
    const handlePaste = (e) => {
      const items = e.clipboardData?.items;
      if (!items) return;
      const filesToProcess = [];
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const file = items[i].getAsFile();
          if (file) {
            filesToProcess.push(file);
          }
        }
      }
      if (filesToProcess.length > 0) {
        handleFilesAdded(filesToProcess);
      }
    };
    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, []);

  // Handle adding one or multiple files (images or PDFs)
  const handleFilesAdded = async (fileList) => {
    if (!fileList || fileList.length === 0) return;
    setError(null);
    setActiveTab('upload');

    // Filter valid image files and PDFs
    const validFiles = Array.from(fileList).filter((f) => {
      const isImg = f.type && f.type.startsWith('image/');
      const isPdf = f.type === 'application/pdf' || (f.name && f.name.toLowerCase().endsWith('.pdf'));
      return isImg || isPdf;
    });

    if (validFiles.length === 0) {
      setError('Please upload valid screenshot images (PNG, JPG, WebP) or PDF documents.');
      return;
    }

    const newItems = validFiles.map((f) => ({
      id: `${Date.now()}_${Math.random().toString(36).substring(2, 9)}`,
      file: f,
      name: f.name || 'Screenshot',
      size: f.size || 0,
      type: f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf') ? 'pdf' : 'image',
      previewUrl: f.type.startsWith('image/') ? URL.createObjectURL(f) : null,
      text: '',
      status: 'processing',
    }));

    // Append to existing files list! Never replace earlier screenshots!
    setUploadedFiles((prev) => [...prev, ...newItems]);
    setOcrLoading(true);

    for (let i = 0; i < newItems.length; i++) {
      const item = newItems[i];
      const countPrefix = newItems.length > 1 ? `(${i + 1}/${newItems.length}) ` : '';
      setOcrStatusText(`${countPrefix}Processing ${item.name}...`);

      try {
        let extracted = '';
        if (item.type === 'pdf') {
          // Extracts digital text AND runs OCR on scanned / image-based PDF pages via canvas!
          extracted = await processPdfFile(item.file, (status) =>
            setOcrStatusText(`${countPrefix}${status}`)
          );
        } else {
          // Extracts text from screenshot image
          extracted = await processImageFile(item.file, (status) =>
            setOcrStatusText(`${countPrefix}${status}`)
          );
        }

        setUploadedFiles((prev) => {
          const updated = prev.map((f) =>
            f.id === item.id ? { ...f, text: extracted, status: 'done' } : f
          );
          updateConsolidatedText(updated);
          return updated;
        });
      } catch (err) {
        console.error(`Error processing ${item.name}:`, err);
        setUploadedFiles((prev) =>
          prev.map((f) => (f.id === item.id ? { ...f, status: 'error', error: err.message } : f))
        );
      }
    }

    setOcrLoading(false);
    setOcrStatusText('Extraction complete.');
  };

  // Remove a single file from the uploaded list
  const handleRemoveFile = (idToRemove) => {
    setUploadedFiles((prev) => {
      const target = prev.find((f) => f.id === idToRemove);
      if (target?.previewUrl) {
        URL.revokeObjectURL(target.previewUrl);
      }
      const updated = prev.filter((f) => f.id !== idToRemove);
      if (updated.length === 0) {
        setInputText('');
      } else {
        updateConsolidatedText(updated);
      }
      return updated;
    });
  };

  const handleClear = () => {
    uploadedFiles.forEach((f) => {
      if (f.previewUrl) URL.revokeObjectURL(f.previewUrl);
    });
    setUploadedFiles([]);
    setInputText('');
    setResult(null);
    setError(null);
    setShowResultDialog(false);
    setIsExplanationExpanded(false);
  };

  const handleAnalyze = async () => {
    if (!inputText.trim() && uploadedFiles.length === 0) {
      setError('Please paste text, upload screenshots/PDF, or pick a sample scenario.');
      return;
    }

    if (ocrLoading) {
      setError('Please wait while text is being extracted from your uploaded files.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setShowResultDialog(false);
    setIsExplanationExpanded(false);
    setScanStep(1);

    const timer1 = setTimeout(() => setScanStep(2), 400);
    const timer2 = setTimeout(() => setScanStep(3), 850);

    try {
      const payload = {
        raw_text: inputText,
        language: 'en',
      };
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      clearTimeout(timer1);
      clearTimeout(timer2);

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Server returned code ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
      // Open the result dialogue box
      setShowResultDialog(true);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'Unable to check message right now. Please try again.');
    } finally {
      setLoading(false);
      setScanStep(0);
    }
  };

  const scrollToScanner = () => {
    scannerRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const openDetailedReport = () => {
    setShowResultDialog(false);
    setViewMode('report');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // =========================================================================
  // VIEW MODE: DETAILED REPORT DIV ONLY
  // (Shown only when chosen from the dialogue box, not stacked on main page)
  // =========================================================================
  if (viewMode === 'report' && result) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-6 animate-fade-in">
        {/* Navigation & Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setViewMode('main')}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-secondary hover:bg-secondary/80 text-foreground text-xs font-semibold border border-border cursor-pointer transition-colors active:scale-98"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Scanner</span>
            </button>
            <span className="text-xs text-muted-foreground hidden sm:inline">
              Offer Analysis Report
            </span>
          </div>

          <div className="flex items-center gap-3">
            <span className={`text-xs font-bold px-3 py-1 rounded-full border ${
              result.verdict === 'SCAM'
                ? 'bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20'
                : result.verdict === 'SUSPICIOUS'
                ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20'
                : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20'
            }`}>
              {result.verdict === 'SCAM' ? 'High Risk Scam' : result.verdict === 'SUSPICIOUS' ? 'Suspicious Offer' : 'Likely Genuine'}
            </span>
            <span className="text-xs font-mono font-bold text-foreground">
              {result.risk_score}% Risk
            </span>
          </div>
        </div>

        {/* Detailed Sections */}
        <div className="space-y-6">
          <EvidenceCard signals={result.signals} />
          {result.company && <CompanyCheck company={result.company} />}
          <StageTimeline currentStage={result.stage} verdict={result.verdict} />
          <NextMoveCard nextMove={result.next_likely_move} verdict={result.verdict} />
          <AdviceSection advice={result.advice} verdict={result.verdict} />
          {result.verdict !== 'LIKELY_GENUINE' && (
            <ReportPack
              text={inputText}
              messages={result.signals?.map((s) => ({ sender: 'Suspect', text: s.evidence }))}
              result={result}
            />
          )}
        </div>

        {/* Bottom Back & Reset Actions */}
        <div className="pt-6 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-3">
          <button
            onClick={() => setViewMode('main')}
            className="w-full sm:w-auto px-6 py-2.5 rounded-full bg-secondary hover:bg-secondary/80 text-foreground text-xs font-semibold border border-border cursor-pointer transition-colors"
          >
            ← Return to Home
          </button>
          <button
            onClick={() => {
              handleClear();
              setViewMode('main');
            }}
            className="w-full sm:w-auto px-6 py-2.5 rounded-full bg-primary hover:bg-primary/90 text-primary-foreground text-xs font-semibold transition-colors cursor-pointer"
          >
            Check Another Offer
          </button>
        </div>
      </div>
    );
  }

  // =========================================================================
  // VIEW MODE: MAIN LANDING PAGE WITH RESTORED SECTION 3 & DEMO TOOL
  // =========================================================================
  return (
    <div className="space-y-24 pb-24">
      {/* =========================================================================
          HERO SECTION (Clean, Minimal, Non-Agentic)
         ========================================================================= */}
      <section className="relative pt-14 md:pt-24 pb-6 overflow-hidden flex flex-col items-center text-center px-4">
        {/* Hero Title */}
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-foreground max-w-3xl leading-[1.15]">
          Check if a job offer is real <br className="hidden sm:inline" />
          <span className="text-primary">before you send money.</span>
        </h1>

        {/* Hero Subtitle */}
        <p className="text-base sm:text-lg text-muted-foreground max-w-xl mx-auto font-normal mt-5 leading-relaxed">
          Paste a WhatsApp message or upload an offer letter. We check for upfront payment traps, verify registered company records, and help you stay safe.
        </p>

        {/* Hero Action Buttons */}
        <div className="mt-8 flex flex-col sm:flex-row gap-3.5 justify-center w-full max-w-md">
          <button
            onClick={scrollToScanner}
            className="px-7 py-3 rounded-full bg-primary text-primary-foreground font-semibold flex items-center justify-center gap-2 hover:bg-primary/90 transition-all shadow-sm active:scale-98 cursor-pointer text-sm"
          >
            <span>Check an Offer Free</span>
            <ArrowRight className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              setInputText(DEMO_PRESETS[1].text);
              setActiveTab('text');
              scrollToScanner();
            }}
            className="px-6 py-3 rounded-full border border-border bg-card hover:bg-secondary text-foreground font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer text-sm"
          >
            <span>Try Sample Scams</span>
          </button>
        </div>

        {/* Trust Points */}
        <div className="flex flex-wrap items-center justify-center gap-6 mt-9 text-xs text-muted-foreground">
          <span>Free to use</span>
          <span>•</span>
          <span>No sign-up required</span>
          <span>•</span>
          <span>Chats are never stored</span>
        </div>
      </section>

      {/* =========================================================================
          INTERACTIVE APP WINDOW (The Core Tool)
         ========================================================================= */}
      <section ref={scannerRef} className="max-w-4xl mx-auto px-4 sm:px-6">
        <div className="bg-card border border-border rounded-2xl md:rounded-3xl shadow-lg overflow-hidden transition-all">
          {/* Simple Clean Window Bar */}
          <div className="h-10 bg-secondary/50 border-b border-border flex items-center justify-between px-4 sm:px-6 select-none">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-red-400/80" />
              <div className="w-2.5 h-2.5 rounded-full bg-yellow-400/80" />
              <div className="w-2.5 h-2.5 rounded-full bg-green-400/80" />
              <span className="ml-2 text-xs font-semibold text-muted-foreground">
                Offer Verification
              </span>
            </div>
          </div>

          {/* Window Body */}
          <div className="p-5 sm:p-7 space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border">
              <div>
                <h2 className="text-base font-bold text-foreground">
                  Provide the message or letter
                </h2>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Paste the text or attach a screenshot to analyze
                </p>
              </div>

              {/* Tabs */}
              <div className="flex items-center gap-1 bg-secondary p-1 rounded-full text-xs font-medium self-start sm:self-auto border border-border">
                <button
                  onClick={() => setActiveTab('text')}
                  className={`px-4 py-1.5 rounded-full transition-all cursor-pointer ${
                    activeTab === 'text'
                      ? 'bg-card text-foreground shadow-xs font-semibold'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  Paste Text
                </button>
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`px-4 py-1.5 rounded-full transition-all cursor-pointer ${
                    activeTab === 'upload'
                      ? 'bg-card text-foreground shadow-xs font-semibold'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  Screenshot / PDF
                </button>
                <button
                  onClick={() => setActiveTab('presets')}
                  className={`px-4 py-1.5 rounded-full transition-all cursor-pointer ${
                    activeTab === 'presets'
                      ? 'bg-card text-foreground shadow-xs font-semibold'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  Examples
                </button>
              </div>
            </div>

            {/* TAB 1: Paste Text */}
            {activeTab === 'text' && (
              <div className="space-y-2.5">
                <div className="relative">
                  <textarea
                    rows={6}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Paste WhatsApp messages, Telegram chats, SMS, or job offer details here..."
                    className="w-full text-xs sm:text-sm p-4 rounded-xl bg-secondary/30 border border-border text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary transition-colors leading-relaxed"
                  />
                  {inputText && (
                    <button
                      onClick={handleClear}
                      className="absolute top-3 right-3 text-xs text-muted-foreground hover:text-foreground flex items-center gap-1 bg-card px-3.5 py-1 rounded-full border border-border cursor-pointer shadow-2xs transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                      Clear
                    </button>
                  )}
                </div>
                <div className="flex items-center justify-between text-[11px] text-muted-foreground">
                  <span>Tip: You can also paste screenshots directly with Ctrl+V</span>
                  <span>{inputText.length} characters</span>
                </div>
              </div>
            )}

            {/* TAB 2: Upload File / OCR (Supports Multiple Screenshots & Scanned/Image PDFs) */}
            {activeTab === 'upload' && (
              <div className="space-y-4">
                {/* Upload Zone / Dropzone */}
                <label
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault();
                    if (e.dataTransfer.files?.length) {
                      handleFilesAdded(e.dataTransfer.files);
                    }
                  }}
                  className="flex flex-col items-center justify-center p-6 sm:p-8 border-2 border-dashed border-border hover:border-primary/50 rounded-2xl bg-secondary/20 hover:bg-secondary/30 cursor-pointer transition-all text-center select-none"
                >
                  <input
                    type="file"
                    multiple
                    accept="image/*,application/pdf"
                    onChange={(e) => {
                      if (e.target.files?.length) {
                        handleFilesAdded(e.target.files);
                        e.target.value = '';
                      }
                    }}
                    className="hidden"
                  />
                  <div className="w-11 h-11 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-3 shadow-xs">
                    <Upload className="w-5 h-5" />
                  </div>
                  <p className="text-xs sm:text-sm font-bold text-foreground">
                    Click to select or drag screenshots & PDF offer letters
                  </p>
                  <p className="text-[11px] text-muted-foreground mt-1 max-w-sm">
                    Supports multiple images (PNG, JPG, WebP) and PDF documents. You can add multiple screenshots of chat conversations.
                  </p>
                  <div className="mt-3 flex flex-wrap justify-center items-center gap-2">
                    <span className="text-[10px] font-semibold px-2.5 py-0.5 rounded-full bg-secondary text-foreground border border-border">
                      Multiple Images Allowed
                    </span>
                    <span className="text-[10px] font-semibold px-2.5 py-0.5 rounded-full bg-secondary text-foreground border border-border">
                      Scanned PDF & Image OCR
                    </span>
                  </div>
                </label>

                {/* OCR Loading Banner */}
                {ocrLoading && (
                  <div className="p-3 bg-secondary/60 rounded-xl border border-border flex items-center gap-3 animate-pulse">
                    <Loader2 className="w-4 h-4 text-primary animate-spin shrink-0" />
                    <span className="text-xs font-medium text-foreground">
                      {ocrStatusText || 'Extracting text from files...'}
                    </span>
                  </div>
                )}

                {/* Uploaded Files Queue / Grid */}
                {uploadedFiles.length > 0 && (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-xs pb-1 border-b border-border">
                      <span className="font-bold text-foreground flex items-center gap-1.5">
                        <span>Attached Files ({uploadedFiles.length})</span>
                      </span>
                      <div className="flex items-center gap-2">
                        <label
                          htmlFor="add-more-screenshots"
                          className="px-3 py-1 rounded-full bg-primary/10 hover:bg-primary/20 text-primary font-semibold text-[11px] cursor-pointer transition-colors inline-flex items-center gap-1"
                        >
                          <Plus className="w-3 h-3" />
                          <span>Add More</span>
                        </label>
                        <input
                          id="add-more-screenshots"
                          type="file"
                          multiple
                          accept="image/*,application/pdf"
                          onChange={(e) => {
                            if (e.target.files?.length) {
                              handleFilesAdded(e.target.files);
                              e.target.value = '';
                            }
                          }}
                          className="hidden"
                        />
                        <button
                          type="button"
                          onClick={handleClear}
                          className="text-[11px] text-muted-foreground hover:text-destructive cursor-pointer transition-colors"
                        >
                          Clear All
                        </button>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                      {uploadedFiles.map((f, idx) => (
                        <div
                          key={f.id}
                          className="flex items-center justify-between p-2.5 rounded-xl bg-secondary/40 border border-border text-xs group hover:border-primary/30 transition-all"
                        >
                          <div className="flex items-center gap-2.5 min-w-0">
                            {f.type === 'image' && f.previewUrl ? (
                              <img
                                src={f.previewUrl}
                                alt={f.name}
                                className="w-10 h-10 object-cover rounded-lg border border-border shrink-0 bg-background"
                              />
                            ) : (
                              <div className="w-10 h-10 rounded-lg bg-red-500/10 text-red-500 flex flex-col items-center justify-center font-bold text-[10px] shrink-0 border border-red-500/20">
                                <FileText className="w-4 h-4" />
                                <span>PDF</span>
                              </div>
                            )}

                            <div className="min-w-0">
                              <p className="font-semibold text-foreground truncate max-w-[150px] sm:max-w-[170px]" title={f.name}>
                                {idx + 1}. {f.name}
                              </p>
                              <div className="flex items-center gap-1.5 text-[10px] text-muted-foreground mt-0.5">
                                <span>{(f.size / 1024).toFixed(1)} KB</span>
                                <span>•</span>
                                {f.status === 'processing' ? (
                                  <span className="text-primary font-medium flex items-center gap-1">
                                    <Loader2 className="w-2.5 h-2.5 animate-spin" /> Reading...
                                  </span>
                                ) : f.status === 'error' ? (
                                  <span className="text-destructive font-semibold">Error</span>
                                ) : (
                                  <span className="text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-1">
                                    <CheckCircle2 className="w-2.5 h-2.5" />
                                    {f.text ? `${f.text.length} chars` : 'No text'}
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>

                          <button
                            type="button"
                            onClick={() => handleRemoveFile(f.id)}
                            className="p-1 rounded-full text-muted-foreground hover:text-destructive hover:bg-secondary cursor-pointer transition-colors ml-2"
                            title="Remove this file"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Consolidated Recognized Text Container */}
                {inputText && (
                  <div className="space-y-1.5 pt-1">
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span className="font-medium text-foreground">
                        Consolidated Extracted Text ({inputText.length} characters):
                      </span>
                      <button
                        onClick={() => setActiveTab('text')}
                        className="text-primary hover:underline cursor-pointer font-semibold text-[11px]"
                      >
                        Edit in Text Tab →
                      </button>
                    </div>
                    <textarea
                      rows={5}
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      placeholder="Extracted text from screenshots will appear here..."
                      className="w-full text-xs p-3 rounded-xl bg-secondary/30 border border-border text-foreground focus:outline-none focus:border-primary transition-colors leading-relaxed"
                    />
                  </div>
                )}
              </div>
            )}

            {/* TAB 3: Sample Presets */}
            {activeTab === 'presets' && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {DEMO_PRESETS.map((preset) => (
                  <button
                    key={preset.id}
                    onClick={() => {
                      setInputText(preset.text);
                      uploadedFiles.forEach((f) => {
                        if (f.previewUrl) URL.revokeObjectURL(f.previewUrl);
                      });
                      setUploadedFiles([]);
                      setActiveTab('text');
                    }}
                    className="p-3.5 text-left rounded-xl border border-border hover:border-primary/40 bg-secondary/30 hover:bg-card transition-all cursor-pointer group"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${preset.badgeColor}`}>
                        {preset.badge}
                      </span>
                      <span className="text-[10px] text-muted-foreground group-hover:text-primary flex items-center gap-1 font-semibold">
                        Load <ArrowRight className="w-3 h-3" />
                      </span>
                    </div>
                    <div className="text-xs font-semibold text-foreground">
                      {preset.label}
                    </div>
                  </button>
                ))}
              </div>
            )}

            {/* Action Row */}
            <div className="pt-3 border-t border-border flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
              <span className="text-xs text-muted-foreground">
                Names and phone numbers are automatically hidden before checking
              </span>

              <button
                onClick={handleAnalyze}
                disabled={loading || ocrLoading || (!inputText.trim() && uploadedFiles.length === 0)}
                className="px-8 py-3 rounded-full bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs sm:text-sm transition-all shadow-sm flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed active:scale-98"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Checking...</span>
                  </>
                ) : ocrLoading ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Extracting Text...</span>
                  </>
                ) : (
                  <>
                    <Search className="w-3.5 h-3.5" />
                    <span>Run Check</span>
                  </>
                )}
              </button>
            </div>

            {/* Live Progress Indicator */}
            {loading && (
              <div className="p-3.5 rounded-xl bg-secondary/40 border border-border space-y-2 animate-fade-in">
                <div className="flex items-center justify-between text-xs font-medium text-foreground">
                  <span className="flex items-center gap-2">
                    <Loader2 className="w-3.5 h-3.5 text-primary animate-spin" />
                    {scanStep === 1 && "Reading message..."}
                    {scanStep === 2 && "Checking company records & links..."}
                    {scanStep === 3 && "Analyzing risk..."}
                  </span>
                  <span className="font-mono text-muted-foreground">{scanStep * 33}%</span>
                </div>
                <div className="w-full bg-secondary h-1.5 rounded-full overflow-hidden">
                  <div
                    className="bg-primary h-full transition-all duration-500 rounded-full"
                    style={{ width: `${scanStep * 33}%` }}
                  />
                </div>
              </div>
            )}

            {error && (
              <div className="p-3 rounded-xl bg-destructive/10 border border-destructive/20 text-xs text-destructive flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 3: HOW IT WORKS
         ========================================================================= */}
      <section id="how-it-works" className="py-16 md:py-24 bg-background">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          {/* Section Header */}
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
              How it works
            </h2>
            <p className="text-base sm:text-lg text-muted-foreground">
              Verify any suspicious job offer or task scheme in three simple steps.
            </p>
          </div>

          {/* 3 Step Cards Grid with Connecting Gradient Line */}
          <div className="grid md:grid-cols-3 gap-8 relative">
            {/* Desktop Connecting Line behind icons */}
            <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-gradient-to-r from-border via-primary/30 to-border z-0" />

            {HOW_IT_WORKS_STEPS.map((step, idx) => {
              const Icon = step.icon;
              return (
                <div key={idx} className="relative z-10 flex flex-col items-center text-center group">
                  {/* Rotated 3D Icon Box */}
                  <div className="w-24 h-24 rounded-2xl bg-card border border-border shadow-xs flex items-center justify-center mb-6 group-hover:border-primary/50 group-hover:shadow-md transition-all duration-300 relative">
                    <div className="absolute inset-0 bg-secondary/60 rounded-2xl transform rotate-3 group-hover:rotate-6 transition-transform -z-10" />
                    <Icon className="h-10 w-10 text-primary" />
                    {/* Number Badge */}
                    <div className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm border-4 border-background shadow-xs">
                      {idx + 1}
                    </div>
                  </div>

                  {/* Title & Description */}
                  <h3 className="text-lg md:text-xl font-semibold mb-2.5 text-foreground">
                    {step.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed max-w-xs text-xs sm:text-sm">
                    {step.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 4: WHAT WE CHECK FOR
         ========================================================================= */}
      <section id="features" className="py-16 md:py-24 bg-background border-t border-border/40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
              What we check for
            </h2>
            <p className="text-base sm:text-lg text-muted-foreground">
              Six specialized verification layers designed to keep your money and identity safe.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
            {WHAT_WE_CHECK_FOR.map((feature, idx) => {
              const Icon = feature.icon;
              return (
                <div
                  key={idx}
                  className="group p-7 sm:p-8 rounded-2xl bg-secondary/30 border border-border hover:border-primary/40 transition-all hover:shadow-lg hover:shadow-primary/5 flex flex-col justify-between"
                >
                  <div>
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 ${feature.color}`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <h3 className="text-lg md:text-xl font-semibold mb-2.5 text-foreground">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground leading-relaxed text-xs sm:text-sm">
                      {feature.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 5: PRE-FOOTER CALL TO ACTION
         ========================================================================= */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-card border border-border rounded-2xl md:rounded-3xl p-8 md:p-14 text-center relative overflow-hidden shadow-md space-y-4">
          <h3 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
            Unsure about a job message?
          </h3>
          <p className="text-muted-foreground text-xs sm:text-sm max-w-md mx-auto">
            Check it before sharing any money, documents, or bank details.
          </p>
          <div className="pt-2">
            <button
              onClick={scrollToScanner}
              className="px-7 py-3 rounded-full bg-primary text-primary-foreground font-semibold hover:bg-primary/90 transition-all shadow-sm active:scale-98 cursor-pointer text-xs sm:text-sm"
            >
              Check an Offer Free
            </button>
          </div>
        </div>
      </section>

      {/* =========================================================================
          DIALOGUE BOX (MODAL POPUP FOR DEMO CHECK RESULT)
          Instead of adding another card below the demo, this dialog appears!
         ========================================================================= */}
      {showResultDialog && result && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-card border border-border rounded-3xl max-w-sm sm:max-w-md w-full p-5 sm:p-6 shadow-2xl relative animate-fade-in space-y-4">
            {/* Top Close Button */}
            <button
              onClick={() => {
                setShowResultDialog(false);
                setIsExplanationExpanded(false);
              }}
              className="absolute top-4 right-4 p-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-secondary cursor-pointer transition-colors"
              aria-label="Close dialog"
            >
              <X className="w-4 h-4" />
            </button>

            {/* Header info */}
            <div className="text-center">
              <span className="text-[11px] uppercase font-bold tracking-wider text-muted-foreground">
                Verification Result
              </span>
            </div>

            {/* Prominent Risk Score Ring */}
            <div className="flex flex-col items-center justify-center">
              <div className="relative w-24 h-24 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  {/* Background track circle with clear greyness */}
                  <circle
                    cx="50"
                    cy="50"
                    r="40"
                    className="stroke-gray-300 dark:stroke-neutral-700"
                    strokeWidth="8"
                    fill="transparent"
                  />
                  <circle
                    cx="50"
                    cy="50"
                    r="40"
                    stroke={
                      result.risk_score >= 70 ? '#dc2626' : result.risk_score >= 35 ? '#d97706' : '#16a34a'
                    }
                    strokeWidth="8"
                    fill="transparent"
                    strokeDasharray={251.2}
                    strokeDashoffset={251.2 - ((result.risk_score || 0) / 100) * 251.2}
                    strokeLinecap="round"
                    className="transition-all duration-1000 ease-out"
                  />
                </svg>

                {/* Perfectly Centered Percentage and Label inside Circle */}
                <div className="absolute inset-0 flex flex-col items-center justify-center text-center pointer-events-none select-none">
                  <span className="text-2xl font-extrabold text-foreground tracking-tight leading-none">
                    {result.risk_score}%
                  </span>
                  <span className="text-[9px] uppercase font-bold text-muted-foreground tracking-wider leading-none mt-1">
                    Risk
                  </span>
                </div>
              </div>

              {/* Verdict Badge */}
              <div className="mt-3">
                <span className={`text-[11px] font-semibold px-3 py-0.5 rounded-full border ${
                  result.verdict === 'SCAM'
                    ? 'bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20'
                    : result.verdict === 'SUSPICIOUS'
                    ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20'
                    : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20'
                }`}>
                  {result.verdict === 'SCAM' ? 'High Risk Scam' : result.verdict === 'SUSPICIOUS' ? 'Suspicious Offer' : 'Likely Genuine'}
                </span>
              </div>

              {/* Verdict Title */}
              <h3 className="text-sm sm:text-base font-bold text-foreground text-center mt-2 leading-snug">
                {result.verdict === 'SCAM'
                  ? 'Do Not Transfer Any Money or Share Details'
                  : result.verdict === 'SUSPICIOUS'
                  ? 'Be Careful Before Sharing Money'
                  : 'Appears to be a Standard Job Offer'}
              </h3>

              {/* Limited Wording / Read More (Scroll added to text container only, not overlay) */}
              {(() => {
                const explanation = result.explanation_simple || "Pattern analysis completed.";
                const isLong = explanation.length > 110;
                return (
                  <div className="w-full max-w-sm mx-auto text-center mt-2">
                    <div
                      className={`text-xs text-muted-foreground leading-relaxed transition-all duration-200 ${
                        isExplanationExpanded
                          ? 'max-h-24 sm:max-h-28 overflow-y-auto pr-1 text-left bg-secondary/30 p-2.5 rounded-xl border border-border/50'
                          : 'line-clamp-2'
                      }`}
                    >
                      {explanation}
                    </div>
                    {isLong && (
                      <button
                        type="button"
                        onClick={() => setIsExplanationExpanded(!isExplanationExpanded)}
                        className="mt-1 text-[11px] font-semibold text-primary hover:underline cursor-pointer inline-flex items-center gap-0.5"
                      >
                        {isExplanationExpanded ? 'Read less' : 'Read more'}
                      </button>
                    )}
                  </div>
                );
              })()}
            </div>

            {/* Warning strip if SCAM */}
            {result.verdict === 'SCAM' && (
              <div className="p-2.5 rounded-xl bg-destructive/10 border border-destructive/20 text-xs text-destructive flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                  <span className="text-[11px] leading-tight">Never pay to get a job. Real employers never charge.</span>
                </div>
                <a href="tel:1930" className="font-bold underline shrink-0 hover:opacity-80 text-[11px]">
                  Call 1930
                </a>
              </div>
            )}

            {/* Actions: View Detailed Report OR Close */}
            <div className="space-y-2 pt-1">
              <button
                onClick={openDetailedReport}
                className="w-full px-6 py-2.5 rounded-full bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs transition-all shadow-xs flex items-center justify-center gap-2 cursor-pointer active:scale-98"
              >
                <span>View Detailed Report</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => {
                  setShowResultDialog(false);
                  setIsExplanationExpanded(false);
                }}
                className="w-full px-5 py-2 rounded-full bg-secondary hover:bg-secondary/80 text-foreground border border-border text-xs font-medium transition-colors cursor-pointer"
              >
                Close & Check Another
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
