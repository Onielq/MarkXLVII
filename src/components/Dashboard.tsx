import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// TypeScript declaration for voice-orb custom element
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'voice-orb': React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          state?: 'idle' | 'listening' | 'thinking' | 'speaking';
          particles?: number;
          recording?: boolean;
        },
        HTMLElement
      >;
    }
  }
}

interface LogEntry {
  id: number;
  speaker: 'user' | 'jarvis' | 'system';
  text: string;
  timestamp: string;
}

const sampleLogs: LogEntry[] = [
  { id: 1, speaker: 'system', text: 'JARVIS online. All systems nominal.', timestamp: '09:00:01' },
  { id: 2, speaker: 'jarvis', text: 'Good morning, sir. It\'s 9:00 AM. Fetching today\'s news headlines now.', timestamp: '09:00:02' },
  { id: 3, speaker: 'system', text: 'Briefing phase 2 (news) sent.', timestamp: '09:00:03' },
  { id: 4, speaker: 'user', text: 'What\'s the weather like today?', timestamp: '09:01:15' },
  { id: 5, speaker: 'jarvis', text: 'Currently 22°C and partly cloudy in your area, sir. Expect clear skies through the afternoon.', timestamp: '09:01:18' },
  { id: 6, speaker: 'user', text: 'Open Chrome and search for the latest tech news.', timestamp: '09:02:30' },
  { id: 7, speaker: 'jarvis', text: 'Opening Chrome and searching for latest tech news, sir.', timestamp: '09:02:31' },
  { id: 8, speaker: 'system', text: 'browser_control: go_to → google.com/search?q=latest+tech+news', timestamp: '09:02:32' },
];

const systemMetrics = {
  cpu: 23,
  ram: 45,
  gpu: 12,
  temp: 52,
};

export default function Dashboard() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [metrics, setMetrics] = useState(systemMetrics);
  const [state, setState] = useState<'LISTENING' | 'SPEAKING' | 'THINKING'>('LISTENING');
  const [inputText, setInputText] = useState('');
  const orbRef = useRef<any>(null);
  
  // Map dashboard state to orb state
  const orbState = state === 'LISTENING' ? 'listening' : state === 'SPEAKING' ? 'speaking' : 'thinking';

  useEffect(() => {
    // Animate logs appearing one by one
    let i = 0;
    const interval = setInterval(() => {
      if (i < sampleLogs.length) {
        setLogs((prev) => [...prev, sampleLogs[i]]);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 800);
    return () => clearInterval(interval);
  }, []);

  // Waveform removed - using voice orb instead

  useEffect(() => {
    // Simulate metric changes
    const interval = setInterval(() => {
      setMetrics({
        cpu: Math.max(10, Math.min(80, metrics.cpu + (Math.random() - 0.5) * 10)),
        ram: Math.max(30, Math.min(70, metrics.ram + (Math.random() - 0.5) * 5)),
        gpu: Math.max(5, Math.min(60, metrics.gpu + (Math.random() - 0.5) * 8)),
        temp: Math.max(40, Math.min(75, metrics.temp + (Math.random() - 0.5) * 3)),
      });
    }, 2000);
    return () => clearInterval(interval);
  }, [metrics]);

  const handleSend = () => {
    if (!inputText.trim()) return;
    const newLog: LogEntry = {
      id: Date.now(),
      speaker: 'user',
      text: inputText,
      timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
    };
    setLogs((prev) => [...prev, newLog]);
    setInputText('');

    // Simulate JARVIS response
    setTimeout(() => {
      setState('THINKING');
      setTimeout(() => {
        setState('SPEAKING');
        setLogs((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            speaker: 'jarvis',
            text: 'Processing your request, sir. This is a demo interface — the full assistant runs locally with Gemini Live API.',
            timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
          },
        ]);
        setTimeout(() => setState('LISTENING'), 2000);
      }, 1000);
    }, 300);
  };

  return (
    <section id="dashboard" className="relative py-24 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="text-[#00d4ff] font-mono text-sm tracking-widest uppercase">
            Live Interface
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-4 mb-6">
            Interactive{' '}
            <span className="bg-gradient-to-r from-[#00d4ff] to-[#7ef0c1] bg-clip-text text-transparent">
              Dashboard
            </span>
          </h2>
          <p className="text-[#9bb6bd] text-lg max-w-2xl mx-auto">
            A preview of the JARVIS HUD interface. In production, this runs as a PyQt6 desktop application 
            with real-time voice interaction.
          </p>
        </motion.div>

        {/* Dashboard Mock */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="rounded-2xl border border-[#1d3c4a] bg-[#0a1520] overflow-hidden shadow-2xl shadow-[#00d4ff]/5"
        >
          {/* Title bar */}
          <div className="flex items-center justify-between px-4 py-3 bg-[#0d1c27] border-b border-[#1d3c4a]">
            <div className="flex items-center gap-3">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
              </div>
              <span className="text-xs font-mono text-[#9bb6bd]">JARVIS — Mark XLVIII</span>
            </div>
            <div className="flex items-center gap-3">
              <span className={`px-2 py-0.5 rounded text-xs font-mono ${
                state === 'LISTENING' ? 'bg-[#7ef0c1]/20 text-[#7ef0c1]' :
                state === 'SPEAKING' ? 'bg-[#00d4ff]/20 text-[#00d4ff]' :
                'bg-yellow-500/20 text-yellow-400'
              }`}>
                {state}
              </span>
            </div>
          </div>

          <div className="grid lg:grid-cols-3 gap-0">
            {/* Main panel - Waveform + Log */}
            <div className="lg:col-span-2 p-4">
              {/* Voice Orb */}
              <div className="mb-4 p-4 rounded-xl bg-[#071018] border border-[#1d3c4a]/40">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-mono text-[#9bb6bd]">VOICE ORB</span>
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${state === 'LISTENING' ? 'bg-[#7ef0c1] animate-pulse' : state === 'SPEAKING' ? 'bg-[#00d4ff] animate-pulse' : 'bg-yellow-400'}`}></div>
                    <span className="text-xs font-mono text-[#9bb6bd]">{state}</span>
                  </div>
                </div>
                <div className="flex items-center justify-center h-48">
                  <voice-orb 
                    ref={orbRef}
                    state={orbState} 
                    style={{ width: '180px', height: '180px' }}
                  />
                </div>
              </div>

              {/* Log panel */}
              <div className="rounded-xl bg-[#071018] border border-[#1d3c4a]/40 overflow-hidden">
                <div className="px-4 py-2 border-b border-[#1d3c4a]/40 flex items-center justify-between">
                  <span className="text-xs font-mono text-[#9bb6bd]">CONVERSATION LOG</span>
                  <span className="text-xs font-mono text-[#1d3c4a]">{logs.length} entries</span>
                </div>
                <div className="h-64 overflow-y-auto p-3 space-y-2 scrollbar-thin">
                  <AnimatePresence>
                    {logs.map((log) => (
                      <motion.div
                        key={log.id}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        className={`flex items-start gap-2 text-xs font-mono ${
                          log.speaker === 'user' ? 'text-[#7ef0c1]' :
                          log.speaker === 'jarvis' ? 'text-[#00d4ff]' :
                          'text-[#9bb6bd]'
                        }`}
                      >
                        <span className="text-[#1d3c4a] flex-shrink-0">{log.timestamp}</span>
                        <span className="flex-shrink-0">
                          {log.speaker === 'user' ? 'You:' : log.speaker === 'jarvis' ? 'Jarvis:' : 'SYS:'}
                        </span>
                        <span className="break-all">{log.text}</span>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>

                {/* Input */}
                <div className="p-3 border-t border-[#1d3c4a]/40">
                  <div className="flex items-center gap-2">
                    <input
                      type="text"
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                      placeholder="Type a command..."
                      className="flex-1 px-3 py-2 rounded-lg bg-[#0d1c27] border border-[#1d3c4a] text-sm text-[#e6f7fb] placeholder-[#9bb6bd]/50 focus:outline-none focus:border-[#00d4ff]/50"
                    />
                    <button
                      onClick={handleSend}
                      className="px-4 py-2 rounded-lg bg-[#00d4ff]/20 border border-[#00d4ff]/30 text-[#00d4ff] text-sm font-medium hover:bg-[#00d4ff]/30 transition-colors"
                    >
                      <i className="fas fa-paper-plane"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Side panel - System metrics */}
            <div className="p-4 border-l border-[#1d3c4a]/40 space-y-4">
              <div className="text-xs font-mono text-[#9bb6bd] mb-2">SYSTEM TELEMETRY</div>
              
              {[
                { label: 'CPU', value: metrics.cpu, color: '#00d4ff', icon: 'fas fa-microchip' },
                { label: 'RAM', value: metrics.ram, color: '#7ef0c1', icon: 'fas fa-memory' },
                { label: 'GPU', value: metrics.gpu, color: '#00d4ff', icon: 'fas fa-tv' },
                { label: 'TEMP', value: metrics.temp, color: metrics.temp > 65 ? '#f87171' : '#7ef0c1', icon: 'fas fa-thermometer-half' },
              ].map((metric, i) => (
                <div key={i} className="p-3 rounded-lg bg-[#071018] border border-[#1d3c4a]/40">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <i className={`${metric.icon} text-xs`} style={{ color: metric.color }}></i>
                      <span className="text-xs font-mono text-[#9bb6bd]">{metric.label}</span>
                    </div>
                    <span className="text-xs font-mono font-bold" style={{ color: metric.color }}>
                      {Math.round(metric.value)}%
                    </span>
                  </div>
                  <div className="h-1.5 rounded-full bg-[#1d3c4a]/40 overflow-hidden">
                    <motion.div
                      animate={{ width: `${metric.value}%` }}
                      transition={{ duration: 0.5 }}
                      className="h-full rounded-full"
                      style={{ backgroundColor: metric.color }}
                    />
                  </div>
                </div>
              ))}

              {/* Quick actions */}
              <div className="pt-4 border-t border-[#1d3c4a]/40">
                <div className="text-xs font-mono text-[#9bb6bd] mb-3">QUICK ACTIONS</div>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    { label: 'Interrupt', icon: 'fas fa-stop', color: '#f87171' },
                    { label: 'Mute', icon: 'fas fa-volume-mute', color: '#fbbf24' },
                    { label: 'Camera', icon: 'fas fa-camera', color: '#00d4ff' },
                    { label: 'Remote', icon: 'fas fa-mobile-alt', color: '#7ef0c1' },
                  ].map((action, i) => (
                    <button
                      key={i}
                      className="flex items-center gap-1.5 px-2 py-1.5 rounded-lg bg-[#0d1c27] border border-[#1d3c4a] text-xs hover:border-[#00d4ff]/30 transition-colors"
                    >
                      <i className={`${action.icon} text-[10px]`} style={{ color: action.color }}></i>
                      <span className="text-[#e6f7fb]">{action.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Connection info */}
              <div className="pt-4 border-t border-[#1d3c4a]/40">
                <div className="text-xs font-mono text-[#9bb6bd] mb-2">CONNECTION</div>
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#9bb6bd]">Model</span>
                    <span className="font-mono text-[#7ef0c1]">Gemini 2.5 Flash</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#9bb6bd]">Latency</span>
                    <span className="font-mono text-[#00d4ff]">~45ms</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#9bb6bd]">Session</span>
                    <span className="font-mono text-[#7ef0c1]">Active</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
