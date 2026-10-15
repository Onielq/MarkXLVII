import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';

interface DebugStep {
  id: number;
  action: string;
  status: 'analyzing' | 'researching' | 'testing' | 'fixing' | 'verified' | 'complete';
  detail: string;
  timestamp: string;
}

const debugScenarios = [
  {
    name: 'Web Search Failure Recovery',
    icon: 'fas fa-search',
    color: '#00d4ff',
    steps: [
      { action: 'Detecting anomaly', status: 'analyzing', detail: 'Search query returned empty results', timestamp: '00:00.1' },
      { action: 'Analyzing error pattern', status: 'analyzing', detail: 'Gemini API quota exceeded (429)', timestamp: '00:00.3' },
      { action: 'Researching alternatives', status: 'researching', detail: 'Scanning fallback chain: DDG → Wikipedia → Cached', timestamp: '00:00.8' },
      { action: 'Testing DDG fallback', status: 'testing', detail: 'DuckDuckGo rate limit check...', timestamp: '00:01.2' },
      { action: 'Applying query enhancement', status: 'fixing', detail: 'Adding "current" keyword for factual queries', timestamp: '00:01.5' },
      { action: 'Executing Wikipedia fallback', status: 'fixing', detail: 'Fetching from Wikipedia API...', timestamp: '00:02.1' },
      { action: 'Verifying response quality', status: 'verified', detail: 'Response contains factual data ✓', timestamp: '00:02.8' },
      { action: 'Issue resolved', status: 'complete', detail: 'Self-healed: 2.8s recovery time', timestamp: '00:03.0' },
    ]
  },
  {
    name: 'Archive Processing Recovery',
    icon: 'fas fa-file-archive',
    color: '#7ef0c1',
    steps: [
      { action: 'Detecting file type', status: 'analyzing', detail: 'Unknown archive format: .rar', timestamp: '00:00.1' },
      { action: 'Analyzing dependencies', status: 'analyzing', detail: 'rarfile module not found', timestamp: '00:00.2' },
      { action: 'Researching solutions', status: 'researching', detail: 'Checking pip availability...', timestamp: '00:00.5' },
      { action: 'Auto-installing dependency', status: 'fixing', detail: 'pip install rarfile --quiet', timestamp: '00:01.8' },
      { action: 'Testing installation', status: 'testing', detail: 'Import verification...', timestamp: '00:02.5' },
      { action: 'Retrying operation', status: 'fixing', detail: 'Re-attempting archive read...', timestamp: '00:02.8' },
      { action: 'Verifying output', status: 'verified', detail: 'Successfully read 15 files from archive ✓', timestamp: '00:03.5' },
      { action: 'Issue resolved', status: 'complete', detail: 'Self-healed: 3.5s recovery time', timestamp: '00:03.8' },
    ]
  },
  {
    name: 'Memory Corruption Recovery',
    icon: 'fas fa-brain',
    color: '#fbbf24',
    steps: [
      { action: 'Detecting anomaly', status: 'analyzing', detail: 'Memory read returned corrupted JSON', timestamp: '00:00.1' },
      { action: 'Analyzing corruption', status: 'analyzing', detail: 'Invalid UTF-8 sequence at byte 2048', timestamp: '00:00.3' },
      { action: 'Researching backup', status: 'researching', detail: 'Scanning for memory backups...', timestamp: '00:00.6' },
      { action: 'Locating backup file', status: 'testing', detail: 'Found: memory_backup_20260115.json', timestamp: '00:01.0' },
      { action: 'Validating backup integrity', status: 'testing', detail: 'Checksum verification...', timestamp: '00:01.3' },
      { action: 'Restoring from backup', status: 'fixing', detail: 'Loading 847 memory entries...', timestamp: '00:01.8' },
      { action: 'Verifying restoration', status: 'verified', detail: 'All user preferences intact ✓', timestamp: '00:02.5' },
      { action: 'Issue resolved', status: 'complete', detail: 'Self-healed: 2.5s recovery time', timestamp: '00:02.8' },
    ]
  },
  {
    name: 'Network Timeout Recovery',
    icon: 'fas fa-wifi',
    color: '#f87171',
    steps: [
      { action: 'Detecting timeout', status: 'analyzing', detail: 'Gemini Live connection lost after 30s', timestamp: '00:00.1' },
      { action: 'Analyzing network state', status: 'analyzing', detail: 'DNS resolution failure detected', timestamp: '00:00.4' },
      { action: 'Researching connectivity', status: 'researching', detail: 'Pinging alternative endpoints...', timestamp: '00:00.8' },
      { action: 'Testing fallback DNS', status: 'testing', detail: 'Switching to 8.8.8.8 resolver...', timestamp: '00:01.5' },
      { action: 'Re-establishing connection', status: 'fixing', detail: 'Reconnecting to Gemini API...', timestamp: '00:02.2' },
      { action: 'Verifying session state', status: 'testing', detail: 'Restoring conversation context...', timestamp: '00:03.0' },
      { action: 'Confirming stability', status: 'verified', detail: 'Connection stable, latency 45ms ✓', timestamp: '00:03.8' },
      { action: 'Issue resolved', status: 'complete', detail: 'Self-healed: 3.8s recovery time', timestamp: '00:04.2' },
    ]
  },
];

export default function CoreSystem() {
  const [activeScenario, setActiveScenario] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning) return;
    
    const scenario = debugScenarios[activeScenario];
    if (currentStep >= scenario.steps.length) {
      setIsRunning(false);
      return;
    }

    const timer = setTimeout(() => {
      setCurrentStep(prev => prev + 1);
    }, 1200);

    return () => clearTimeout(timer);
  }, [isRunning, currentStep, activeScenario]);

  const startDebug = () => {
    setCurrentStep(0);
    setIsRunning(true);
  };

  const resetDebug = () => {
    setCurrentStep(0);
    setIsRunning(false);
  };

  const scenario = debugScenarios[activeScenario];

  return (
    <section id="coresystem" className="relative py-24 px-6">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(0,212,255,0.04)_0%,transparent_50%)]" />
      
      <div className="relative max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <span className="text-[#00d4ff] font-mono text-sm tracking-widest uppercase">
            Autonomous Intelligence
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-4 mb-6">
            Core{' '}
            <span className="bg-gradient-to-r from-[#00d4ff] to-[#7ef0c1] bg-clip-text text-transparent">
              Self-Healing System
            </span>
          </h2>
          <p className="text-[#9bb6bd] text-lg max-w-2xl mx-auto">
            FBI/CIA-level autonomous debugging. JARVIS researches issues, analyzes root causes, 
            tests solutions, and self-heals until everything works perfectly.
          </p>
        </motion.div>

        {/* System Capabilities */}
        <div className="grid md:grid-cols-4 gap-4 mb-12">
          {[
            { icon: 'fas fa-microscope', title: 'Deep Analysis', desc: 'Multi-layer issue detection', color: '#00d4ff' },
            { icon: 'fas fa-search-dollar', title: 'Research Mode', desc: 'Autonomous solution finding', color: '#7ef0c1' },
            { icon: 'fas fa-flask', title: 'Self-Testing', desc: 'Validates every fix', color: '#fbbf24' },
            { icon: 'fas fa-heartbeat', title: 'Self-Healing', desc: 'Auto-recovery in seconds', color: '#f87171' },
          ].map((cap, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="p-5 rounded-xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60 hover:border-[#00d4ff]/30 transition-all"
            >
              <div className="w-12 h-12 rounded-xl flex items-center justify-center mb-3" style={{ backgroundColor: `${cap.color}15` }}>
                <i className={`${cap.icon} text-xl`} style={{ color: cap.color }}></i>
              </div>
              <h3 className="font-bold text-[#e6f7fb] mb-1">{cap.title}</h3>
              <p className="text-xs text-[#9bb6bd]">{cap.desc}</p>
            </motion.div>
          ))}
        </div>

        {/* Live Debug Demo */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold flex items-center gap-2">
              <i className="fas fa-bug text-[#f87171]"></i>
              Live Debug Session
            </h3>
            <div className="flex gap-2">
              <button
                onClick={startDebug}
                disabled={isRunning}
                className="px-4 py-2 rounded-lg bg-[#00d4ff]/20 border border-[#00d4ff]/30 text-[#00d4ff] text-sm font-medium hover:bg-[#00d4ff]/30 transition-colors disabled:opacity-50"
              >
                <i className="fas fa-play mr-2"></i>
                {isRunning ? 'Running...' : 'Start Debug'}
              </button>
              <button
                onClick={resetDebug}
                className="px-4 py-2 rounded-lg bg-[#1d3c4a]/40 border border-[#1d3c4a] text-[#9bb6bd] text-sm font-medium hover:text-[#e6f7fb] transition-colors"
              >
                <i className="fas fa-redo mr-2"></i>
                Reset
              </button>
            </div>
          </div>

          {/* Scenario Selector */}
          <div className="flex flex-wrap gap-2 mb-6">
            {debugScenarios.map((s, i) => (
              <button
                key={i}
                onClick={() => { setActiveScenario(i); resetDebug(); }}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
                  activeScenario === i
                    ? 'bg-gradient-to-r from-[#00d4ff]/20 to-[#7ef0c1]/20 border border-[#00d4ff]/50 text-[#e6f7fb]'
                    : 'bg-[#071018] border border-[#1d3c4a] text-[#9bb6bd] hover:text-[#e6f7fb]'
                }`}
              >
                <i className={s.icon} style={{ color: s.color }}></i>
                {s.name}
              </button>
            ))}
          </div>

          {/* Debug Timeline */}
          <div className="relative">
            <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-[#1d3c4a]"></div>
            
            <div className="space-y-3">
              {scenario.steps.map((step, i) => {
                const isActive = i === currentStep && isRunning;
                const isComplete = i < currentStep || (!isRunning && currentStep === scenario.steps.length);
                
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ 
                      opacity: isComplete || isActive ? 1 : 0.3,
                      x: 0 
                    }}
                    transition={{ duration: 0.3 }}
                    className="relative flex items-start gap-4 pl-4"
                  >
                    {/* Timeline dot */}
                    <div className={`relative z-10 w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      isComplete ? 'bg-[#7ef0c1]' : isActive ? 'bg-[#00d4ff] animate-pulse' : 'bg-[#1d3c4a]'
                    }`}>
                      {isComplete ? (
                        <i className="fas fa-check text-[#00141b] text-xs"></i>
                      ) : isActive ? (
                        <i className="fas fa-spinner fa-spin text-[#00141b] text-xs"></i>
                      ) : (
                        <span className="text-xs font-bold text-[#9bb6bd]">{i + 1}</span>
                      )}
                    </div>

                    {/* Step content */}
                    <div className="flex-1 pb-2">
                      <div className="flex items-center gap-3 mb-1">
                        <span className={`text-sm font-bold ${
                          isComplete ? 'text-[#7ef0c1]' : isActive ? 'text-[#00d4ff]' : 'text-[#9bb6bd]'
                        }`}>
                          {step.action}
                        </span>
                        <span className="text-xs font-mono text-[#1d3c4a]">{step.timestamp}</span>
                      </div>
                      <div className="text-xs text-[#9bb6bd]">{step.detail}</div>
                      {isActive && (
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: '100%' }}
                          transition={{ duration: 1.2 }}
                          className="h-0.5 bg-gradient-to-r from-[#00d4ff] to-[#7ef0c1] mt-2 rounded-full"
                        />
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>

          {/* Stats */}
          {currentStep === scenario.steps.length && !isRunning && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 p-4 rounded-xl bg-[#7ef0c1]/10 border border-[#7ef0c1]/30"
            >
              <div className="flex items-center gap-3">
                <i className="fas fa-check-circle text-2xl text-[#7ef0c1]"></i>
                <div>
                  <div className="font-bold text-[#e6f7fb]">Issue Resolved</div>
                  <div className="text-sm text-[#9bb6bd]">
                    Self-healed in {scenario.steps[scenario.steps.length - 1].timestamp} • 
                    No user intervention required • System integrity maintained
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* Architecture Integration */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-8 p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60"
        >
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <i className="fas fa-project-diagram text-[#00d4ff]"></i>
            Self-Healing Architecture
          </h3>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              {
                title: 'Detection Layer',
                icon: 'fas fa-radar',
                color: '#00d4ff',
                items: ['Error pattern recognition', 'Anomaly detection', 'Performance monitoring', 'Health checks']
              },
              {
                title: 'Analysis Engine',
                icon: 'fas fa-brain',
                color: '#7ef0c1',
                items: ['Root cause analysis', 'Impact assessment', 'Solution research', 'Fallback chain evaluation']
              },
              {
                title: 'Recovery System',
                icon: 'fas fa-shield-alt',
                color: '#fbbf24',
                items: ['Auto-fix application', 'Backup restoration', 'Dependency installation', 'Connection recovery']
              },
            ].map((layer, i) => (
              <div key={i} className="p-4 rounded-xl bg-[#071018] border border-[#1d3c4a]/40">
                <div className="flex items-center gap-2 mb-3">
                  <i className={layer.icon} style={{ color: layer.color }}></i>
                  <span className="font-bold text-[#e6f7fb]">{layer.title}</span>
                </div>
                <ul className="space-y-1.5">
                  {layer.items.map((item, j) => (
                    <li key={j} className="text-xs text-[#9bb6bd] flex items-start gap-2">
                      <i className="fas fa-chevron-right text-[8px] mt-1" style={{ color: layer.color }}></i>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
