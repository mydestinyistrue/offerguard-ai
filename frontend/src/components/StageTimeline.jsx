import React, { useState } from 'react';
import { ShieldAlert, AlertCircle, CheckCircle2, HelpCircle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function StageTimeline({ currentStage = 0, verdict = 'SUSPICIOUS' }) {
  const { t } = useLanguage();
  const [activeTooltip, setActiveTooltip] = useState(null);

  const isGenuine = verdict === 'LIKELY_GENUINE';

  const stages = [
    {
      id: 0,
      title: 'Initial Bait',
      fullName: 'Stage 0: Initial Contact (Bait)',
      desc: 'Unsolicited WhatsApp/Telegram or SMS message promising high daily earnings (₹2,000–₹8,000) for simple online tasks without any interview.',
      scamAction: 'Sends random invitations, shares fake company credentials, and invites target to complete a free trial task.',
      redFlag: 'No interview, lucrative daily pay promise, communication via personal WhatsApp or Telegram.',
      tip: 'Never respond or click unfamiliar links. Legitimate firms do not recruit via unsolicited WhatsApp messaging.',
    },
    {
      id: 1,
      title: 'Trust Hook',
      fullName: 'Stage 1: Trust Building (Small Payout)',
      desc: 'Victim completes 2-3 trivial sample tasks (e.g. liking YouTube videos or rating hotels) and actually receives a real small payout (₹150–₹500) via UPI.',
      scamAction: 'Credits nominal money to build false trust and prove the task scheme is "authentic".',
      redFlag: 'Paid immediately for trivial clicks, then pushed into a Telegram VIP or Merchant channel.',
      tip: 'Do not be fooled by the initial ₹150–₹300 payout. Keep the token payment, block the sender, and never deposit any money.',
    },
    {
      id: 2,
      title: 'Deposit Trap',
      fullName: 'Stage 2: Prepaid Deposit Trap',
      desc: 'Scammer instructs the victim to deposit advance funds (₹1,000 to ₹10,000+) into a merchant account to unlock "exclusive high-yield orders".',
      scamAction: 'Displays simulated phantom profits on a fake dashboard to entice escalating deposit sizes.',
      redFlag: 'Demands advance deposit to continue working or unlock commission payout.',
      tip: 'Stop immediately. Legitimate employment never requires transferring money to work.',
    },
    {
      id: 3,
      title: 'Funds Locked',
      fullName: 'Stage 3: Account Freeze & Extortion',
      desc: 'When attempting to withdraw earned balance, the transaction fails. Scammer claims a system glitch or tax issue, demanding 30%–50% extra to unfreeze.',
      scamAction: 'Fabricates "tax clearance codes", "credit score penalties", or "GST release fees".',
      redFlag: 'Requests more money to release already earned funds; threats of losing entire balance.',
      tip: 'Never pay any unfreeze fee. It is a secondary extortion trick. Call 1930 immediately.',
    },
    {
      id: 4,
      title: 'Blocked / Exit',
      fullName: 'Stage 4: Blocked & Recovery Scam',
      desc: 'Victim is abruptly deleted from the group and blocked. Soon after, fake "cyber lawyers" or "recovery experts" reach out claiming they can recover the lost money.',
      scamAction: 'Complete ghosting followed by secondary extortion via fake recovery agencies.',
      redFlag: 'Group admin blocks victim; unsolicited offers from "ethical hackers" asking for recovery fees.',
      tip: 'Report immediately to cybercrime.gov.in and your bank. Never pay secondary recovery agents.',
    },
  ];

  // Clamp stage between 0 and 4; if genuine, progression is 0
  const safeStage = isGenuine ? 0 : Math.max(0, Math.min(4, Number(currentStage) || 0));
  const progressPercent = isGenuine ? 0 : (safeStage / 4) * 100;

  return (
    <div className="bg-card border border-border rounded-2xl p-5 md:p-6 transition-colors duration-200 shadow-xs space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 className="text-sm md:text-base font-bold text-foreground flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${isGenuine ? 'bg-emerald-500' : 'bg-primary animate-pulse'}`} />
            Scam Stage Progression
          </h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            {isGenuine
              ? 'No scam detected'
              : 'Hover over any stage circle to view typical scammer tactics and safety advice'}
          </p>
        </div>

        {isGenuine ? (
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20 text-xs font-semibold self-start sm:self-auto">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>No Scam</span>
          </div>
        ) : (
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20 text-xs font-semibold self-start sm:self-auto">
            <span>Detected: Stage {safeStage} ({stages[safeStage]?.title})</span>
          </div>
        )}
      </div>

      {/* Interactive Timeline Stepper */}
      <div className="pt-10 pb-6 px-4 sm:px-12 select-none">
        <div className="relative">
          {/* Dummy background track behind all stages */}
          <div className="absolute top-5 left-0 right-0 h-1 bg-secondary rounded-full -translate-y-1/2 z-0" />

          {/* Active progress bar that reaches up to currentStage */}
          <div
            className="absolute top-5 left-0 h-1 bg-primary rounded-full -translate-y-1/2 transition-all duration-500 ease-out z-0 shadow-xs"
            style={{ width: `${progressPercent}%` }}
          />

          {/* 5 Stage Nodes */}
          <div className="relative flex justify-between items-start z-10">
            {stages.map((st) => {
              const isCurrent = !isGenuine && st.id === safeStage;
              const isPassed = !isGenuine && st.id < safeStage;
              const isUpcoming = isGenuine || st.id > safeStage;
              const isOpen = activeTooltip === st.id;

              // Positioning tooltip container alignment so edges don't clip
              const tooltipAlign =
                st.id === 0
                  ? 'left-0 translate-x-0'
                  : st.id === 4
                  ? 'right-0 translate-x-0'
                  : 'left-1/2 -translate-x-1/2';

              return (
                <div
                  key={st.id}
                  className="relative group flex flex-col items-center cursor-pointer"
                  onClick={() => setActiveTooltip(isOpen ? null : st.id)}
                  onMouseEnter={() => setActiveTooltip(st.id)}
                  onMouseLeave={() => setActiveTooltip(null)}
                >
                  {/* Circle Center with Stage Number */}
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-extrabold text-sm transition-all duration-300 shadow-sm ${
                      isGenuine
                        ? 'bg-card text-muted-foreground/60 border-2 border-border'
                        : isCurrent
                        ? 'bg-primary text-primary-foreground ring-4 ring-primary/25 scale-110'
                        : isPassed
                        ? 'bg-primary text-primary-foreground border-2 border-primary'
                        : 'bg-card text-muted-foreground border-2 border-border group-hover:border-primary/50 group-hover:text-foreground'
                    }`}
                  >
                    {st.id}
                  </div>

                  {/* Stage Title below circle */}
                  <div className="mt-2.5 flex flex-col items-center">
                    <span
                      className={`text-[11px] sm:text-xs font-semibold text-center leading-tight transition-colors ${
                        isGenuine
                          ? 'text-muted-foreground'
                          : isCurrent
                          ? 'text-primary font-bold'
                          : isPassed
                          ? 'text-foreground'
                          : 'text-muted-foreground group-hover:text-foreground'
                      }`}
                    >
                      {st.title}
                    </span>
                    {!isGenuine && isCurrent && (
                      <span className="mt-1 text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.2 bg-primary/10 text-primary rounded-full">
                        Current
                      </span>
                    )}
                  </div>

                  {/* Hover Tooltip: Absolute container explaining the stage */}
                  <div
                    className={`absolute bottom-full mb-3.5 ${tooltipAlign} w-72 sm:w-80 p-4 rounded-xl bg-card border border-border shadow-xl text-left transition-all duration-200 z-40 ${
                      isOpen
                        ? 'opacity-100 pointer-events-auto visible transform translate-y-0'
                        : 'opacity-0 pointer-events-none invisible transform translate-y-1'
                    }`}
                  >
                    {/* Tooltip Header */}
                    <div className="flex items-center justify-between pb-2 mb-2 border-b border-border">
                      <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-secondary text-foreground">
                        Stage {st.id}
                      </span>
                      {isGenuine ? (
                        <span className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3" /> No Scam
                        </span>
                      ) : isCurrent ? (
                        <span className="text-[11px] font-bold text-amber-600 dark:text-amber-400 flex items-center gap-1">
                          <AlertCircle className="w-3 h-3" /> Current Match
                        </span>
                      ) : isPassed ? (
                        <span className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3" /> Prior Step
                        </span>
                      ) : (
                        <span className="text-[11px] font-semibold text-muted-foreground">
                          Subsequent Risk
                        </span>
                      )}
                    </div>

                    {/* Tooltip Title & Description */}
                    <h4 className="text-xs font-bold text-foreground mb-1">
                      {st.fullName}
                    </h4>
                    <p className="text-[11px] text-muted-foreground leading-relaxed mb-2.5">
                      {st.desc}
                    </p>

                    {/* Scammer Tactic */}
                    <div className="bg-secondary/40 rounded-lg p-2 mb-2 border border-border text-[11px] space-y-1">
                      <span className="font-semibold text-foreground block">
                        Typical Scammer Action:
                      </span>
                      <span className="text-muted-foreground leading-normal block">
                        {st.scamAction}
                      </span>
                    </div>

                    {/* Safety Tip */}
                    <div className="text-[11px] text-primary font-medium flex items-start gap-1.5 pt-1">
                      <ShieldAlert className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                      <span>{st.tip}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
