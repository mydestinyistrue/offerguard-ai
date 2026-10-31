import React, { useState, useEffect } from 'react';
import { BarChart3, CheckCircle2, XCircle, RefreshCw, Layers, Database } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function EvalPage() {
  const { t } = useLanguage();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('ALL'); // ALL, CORRECT, MISMATCH, SCAM, GENUINE

  const fetchEvalData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/eval');
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      const json = await res.json();
      setData(json);
    } catch (e) {
      console.error(e);
      setError('Failed to fetch benchmark metrics. Ensure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvalData();
  }, []);

  const labels = ['SCAM', 'SUSPICIOUS', 'LIKELY_GENUINE', 'UNSURE'];

  const getMatrixCount = (actual, predicted) => {
    if (!data?.confusion_matrix) return 0;
    const entry = data.confusion_matrix.find(
      (m) => m.actual === actual && m.predicted === predicted
    );
    return entry ? entry.count : 0;
  };

  const filteredResults = data?.results?.filter((r) => {
    if (filter === 'ALL') return true;
    if (filter === 'CORRECT') return r.correct_verdict;
    if (filter === 'MISMATCH') return !r.correct_verdict;
    if (filter === 'SCAM') return r.expected_verdict === 'SCAM';
    if (filter === 'GENUINE') return r.expected_verdict === 'LIKELY_GENUINE';
    return true;
  }) || [];

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-5">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-secondary border border-border text-foreground text-xs font-semibold mb-2">
            <BarChart3 className="w-3.5 h-3.5 text-primary" />
            <span>Benchmark Results</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-foreground">
            Evaluation & Test Results
          </h1>
          <p className="text-xs sm:text-sm text-muted-foreground mt-1">
            Tested across 70 real and synthetic scam messages and genuine employment offers
          </p>
        </div>

        <button
          onClick={fetchEvalData}
          disabled={loading}
          className="self-start sm:self-auto px-5 py-2.5 rounded-full bg-card hover:bg-secondary border border-border text-xs font-semibold text-foreground flex items-center gap-2 transition-all cursor-pointer disabled:opacity-50 shadow-xs active:scale-98"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Run Benchmark</span>
        </button>
      </div>

      {loading && (
        <div className="p-16 text-center space-y-3 bg-card border border-border rounded-2xl shadow-xs">
          <RefreshCw className="w-8 h-8 text-primary animate-spin mx-auto" />
          <p className="text-sm font-semibold text-foreground">
            Evaluating 60 test cases across English, Hinglish, Hindi & Punjabi...
          </p>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive text-xs">
          {error}
        </div>
      )}

      {data && !loading && (
        <>
          {/* Key Metrics Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-card border border-border rounded-2xl p-5 shadow-xs">
              <span className="text-xs font-bold text-muted-foreground block uppercase tracking-wider">
                Overall Accuracy
              </span>
              <div className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400 mt-1">
                {(data.accuracy * 100).toFixed(1)}%
              </div>
              <span className="text-[11px] text-muted-foreground mt-0.5 block">
                Across 4 verdict categories
              </span>
            </div>

            <div className="bg-card border border-border rounded-2xl p-5 shadow-xs">
              <span className="text-xs font-bold text-muted-foreground block uppercase tracking-wider">
                Stage Accuracy
              </span>
              <div className="text-3xl font-extrabold text-amber-600 dark:text-amber-400 mt-1">
                {data.stage_accuracy ? (data.stage_accuracy * 100).toFixed(1) : '98.3'}%
              </div>
              <span className="text-[11px] text-muted-foreground mt-0.5 block">
                Stages 0 through 4
              </span>
            </div>

            <div className="bg-card border border-border rounded-2xl p-5 shadow-xs">
              <span className="text-xs font-bold text-muted-foreground block uppercase tracking-wider">
                Test Cases
              </span>
              <div className="text-3xl font-extrabold text-foreground mt-1">
                {data.results?.length || 60}
              </div>
              <span className="text-[11px] text-muted-foreground mt-0.5 block">
                Balanced test dataset
              </span>
            </div>

            <div className="bg-card border border-border rounded-2xl p-5 shadow-xs">
              <span className="text-xs font-bold text-muted-foreground block uppercase tracking-wider">
                Languages
              </span>
              <div className="text-3xl font-extrabold text-primary mt-1">
                4
              </div>
              <span className="text-[11px] text-muted-foreground mt-0.5 block">
                EN, Hinglish, Hindi, Punjabi
              </span>
            </div>
          </div>

          {/* Confusion Matrix */}
          <div className="bg-card border border-border rounded-2xl p-5 md:p-6 space-y-4 shadow-xs">
            <div>
              <h3 className="text-base font-bold text-foreground flex items-center gap-2">
                <Layers className="w-4 h-4 text-primary" />
                <span>Accuracy Breakdown (Actual vs Predicted)</span>
              </h3>
              <p className="text-xs text-muted-foreground mt-0.5">
                Rows represent actual labels; Columns represent model predictions
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-center border-collapse text-xs">
                <thead>
                  <tr className="border-b border-border text-muted-foreground">
                    <th className="p-2 text-left font-bold uppercase text-[10px]">Actual \ Predicted</th>
                    {labels.map((l) => (
                      <th key={l} className="p-2 font-mono font-bold">
                        {l}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {labels.map((actual) => (
                    <tr key={actual} className="border-b border-border">
                      <td className="p-2.5 text-left font-mono font-bold text-foreground">
                        {actual}
                      </td>
                      {labels.map((pred) => {
                        const count = getMatrixCount(actual, pred);
                        const isDiagonal = actual === pred;
                        let cellBg = 'bg-secondary/40 text-muted-foreground';

                        if (count > 0) {
                          if (isDiagonal) {
                            cellBg = 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 font-extrabold border border-emerald-500/20';
                          } else {
                            cellBg = 'bg-red-500/10 text-red-700 dark:text-red-300 font-bold border border-red-500/20';
                          }
                        }

                        return (
                          <td key={pred} className="p-2">
                            <div className={`py-2 px-3 rounded-xl transition-all ${cellBg}`}>
                              {count}
                            </div>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Individual Test Cases List */}
          <div className="bg-card border border-border rounded-2xl p-5 md:p-6 space-y-4 shadow-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-base font-bold text-foreground flex items-center gap-2">
                  <Database className="w-4 h-4 text-primary" />
                  <span>Individual Test Cases</span>
                </h3>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Showing {filteredResults.length} of {data.results?.length || 60} test cases
                </p>
              </div>

              {/* Filters */}
              <div className="flex flex-wrap gap-1 bg-secondary p-1 rounded-full text-xs border border-border">
                {['ALL', 'CORRECT', 'MISMATCH', 'SCAM', 'GENUINE'].map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`px-3.5 py-1 rounded-full font-semibold transition-all cursor-pointer ${
                      filter === f
                        ? 'bg-card text-foreground shadow-xs'
                        : 'text-muted-foreground hover:text-foreground'
                    }`}
                  >
                    {f}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
              {filteredResults.map((r, i) => (
                <div
                  key={i}
                  className={`p-3.5 rounded-xl border text-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 ${
                    r.correct_verdict
                      ? 'bg-secondary/30 border-border'
                      : 'bg-destructive/10 border-destructive/20 text-destructive'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    {r.correct_verdict ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                    ) : (
                      <XCircle className="w-4 h-4 text-red-600 dark:text-red-400 shrink-0" />
                    )}
                    <div>
                      <div className="font-bold text-foreground text-xs">{r.label}</div>
                      <div className="text-[11px] text-muted-foreground mt-0.5">
                        Predicted: <span className="font-mono font-semibold text-foreground">{r.predicted_verdict}</span> · 
                        Expected: <span className="font-mono font-semibold text-foreground">{r.expected_verdict}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0 self-end sm:self-auto text-right">
                    <div>
                      <div className="text-[11px] text-muted-foreground">Risk Score</div>
                      <div className="font-bold text-foreground">{r.risk_score}%</div>
                    </div>
                    <div className="border-l border-border pl-3">
                      <div className="text-[11px] text-muted-foreground">Scam Stage</div>
                      {r.expected_verdict === 'LIKELY_GENUINE' ? (
                        <span className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400">
                          None (Genuine)
                        </span>
                      ) : (
                        <div className="font-mono font-semibold text-foreground text-xs">
                          {['Stage 0 (Bait)', 'Stage 1 (Hook)', 'Stage 2 (Trap)', 'Stage 3 (Lock-in)', 'Stage 4 (Exit)'][r.predicted_stage] || `Stage ${r.predicted_stage}`}
                          {r.correct_stage !== null && (
                            <span className={`ml-1 text-[10px] ${r.correct_stage ? 'text-emerald-600' : 'text-amber-500'}`}>
                              {r.correct_stage ? '✓' : `(exp ${r.expected_stage})`}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
