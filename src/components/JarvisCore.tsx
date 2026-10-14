import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface LogEntry {
  id: number;
  speaker: 'user' | 'jarvis' | 'system' | 'healer';
  text: string;
  timestamp: string;
}

interface HealingSession {
  id: string;
  anomaly: string;
  status: 'analyzing' | 'researching' | 'testing' | 'fixing' | 'verified' | 'complete' | 'failed';
  steps: Array<{ action: string; detail: string; timestamp: string }>;
  startTime: number;
  recoveryTime?: number;
}

export default function JarvisCore() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [orbState, setOrbState] = useState<'idle' | 'listening' | 'thinking' | 'speaking'>('idle');
  const [isListening, setIsListening] = useState(false);
  const [inputText, setInputText] = useState('');
  const [healingSessions, setHealingSessions] = useState<HealingSession[]>([]);
  const [systemStatus, setSystemStatus] = useState({
    cpu: 23,
    ram: 45,
    gpu: 12,
    temp: 52,
    healingActive: true,
    totalHeals: 0,
    successRate: 94.2,
  });
  
  const orbRef = useRef<any>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Initialize with welcome message
  useEffect(() => {
    addLog('system', 'JARVIS Core System v2.2.0 initialized');
    addLog('system', 'Self-healing engine: ACTIVE');
    addLog('system', 'Web search: Triple fallback enabled');
    addLog('system', 'File processor: Archive support enabled');
    addLog('jarvis', 'Good day. All systems operational. How may I assist you?');
  }, []);

  // System monitoring
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemStatus(prev => ({
        ...prev,
        cpu: Math.max(10, Math.min(80, prev.cpu + (Math.random() - 0.5) * 10)),
        ram: Math.max(30, Math.min(70, prev.ram + (Math.random() - 0.5) * 5)),
        gpu: Math.max(5, Math.min(60, prev.gpu + (Math.random() - 0.5) * 8)),
        temp: Math.max(40, Math.min(75, prev.temp + (Math.random() - 0.5) * 3)),
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const addLog = (speaker: LogEntry['speaker'], text: string) => {
    const newLog: LogEntry = {
      id: Date.now() + Math.random(),
      speaker,
      text,
      timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
    };
    setLogs(prev => [...prev.slice(-50), newLog]);
  };

  const toggleListening = async () => {
    if (isListening) {
      if (orbRef.current) orbRef.current.disconnect();
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      }
      setIsListening(false);
      setOrbState('idle');
      addLog('system', 'Microphone disconnected');
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        streamRef.current = stream;
        if (orbRef.current) {
          await orbRef.current.connect(stream);
          setOrbState('listening');
          setIsListening(true);
          addLog('system', 'Microphone connected - listening...');
        }
      } catch (err) {
        addLog('system', 'Microphone access denied');
      }
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;
    
    const userMessage = inputText;
    addLog('user', userMessage);
    setInputText('');
    
    // Process command
    setOrbState('thinking');
    await processCommand(userMessage);
  };

  const processCommand = async (command: string) => {
    const cmdLower = command.toLowerCase();
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Web search simulation
    if (cmdLower.includes('search') || cmdLower.includes('who is') || cmdLower.includes('what is')) {
      setOrbState('speaking');
      addLog('jarvis', 'Searching for information...');
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Simulate triple fallback
      addLog('system', '[Search] Gemini API: Checking...');
      await new Promise(resolve => setTimeout(resolve, 500));
      addLog('system', '[Search] Fallback: DuckDuckGo → Wikipedia');
      await new Promise(resolve => setTimeout(resolve, 500));
      
      addLog('jarvis', `Based on my research, I found relevant information about "${command}". The triple fallback system ensured accurate results.`);
    }
    // File operations
    else if (cmdLower.includes('file') || cmdLower.includes('archive') || cmdLower.includes('zip')) {
      setOrbState('speaking');
      addLog('jarvis', 'Processing file operation...');
      await new Promise(resolve => setTimeout(resolve, 800));
      addLog('system', '[FileProcessor] Archive support: ACTIVE');
      addLog('jarvis', 'File processor ready. I can now read contents of zip, tar, rar, and 7z archives.');
    }
    // Trigger healing demo
    else if (cmdLower.includes('heal') || cmdLower.includes('debug') || cmdLower.includes('fix')) {
      await triggerHealingDemo();
    }
    // System status
    else if (cmdLower.includes('status') || cmdLower.includes('system')) {
      setOrbState('speaking');
      addLog('jarvis', `System status: CPU ${Math.round(systemStatus.cpu)}%, RAM ${Math.round(systemStatus.ram)}%, Temperature ${Math.round(systemStatus.temp)}°C. Self-healing: ${systemStatus.healingActive ? 'ACTIVE' : 'INACTIVE'}. Total heals: ${systemStatus.totalHeals}.`);
    }
    // Default response
    else {
      setOrbState('speaking');
      addLog('jarvis', 'I understand. How would you like me to proceed?');
    }
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    setOrbState('idle');
  };

  const triggerHealingDemo = async () => {
    const sessionId = `heal_${Date.now()}`;
    const session: HealingSession = {
      id: sessionId,
      anomaly: 'API Quota Exceeded',
      status: 'analyzing',
      steps: [],
      startTime: Date.now(),
    };
    
    setHealingSessions(prev => [...prev, session]);
    addLog('healer', `[${sessionId}] Anomaly detected: API quota exceeded`);
    
    // Phase 1: Analyze
    await new Promise(resolve => setTimeout(resolve, 800));
    updateSession(sessionId, { status: 'researching' });
    addLog('healer', `[${sessionId}] Analyzing: Rate limit issue detected`);
    
    // Phase 2: Research
    await new Promise(resolve => setTimeout(resolve, 1000));
    updateSession(sessionId, { status: 'testing' });
    addLog('healer', `[${sessionId}] Researching: Found 3 potential solutions`);
    
    // Phase 3: Test
    await new Promise(resolve => setTimeout(resolve, 800));
    updateSession(sessionId, { status: 'fixing' });
    addLog('healer', `[${sessionId}] Testing: DuckDuckGo fallback validated`);
    
    // Phase 4: Apply
    await new Promise(resolve => setTimeout(resolve, 600));
    updateSession(sessionId, { status: 'verified' });
    addLog('healer', `[${sessionId}] Applying: Switched to DDG search`);
    
    // Phase 5: Verify
    await new Promise(resolve => setTimeout(resolve, 500));
    const recoveryTime = (Date.now() - session.startTime) / 1000;
    updateSession(sessionId, { 
      status: 'complete',
      recoveryTime 
    });
    addLog('healer', `[${sessionId}] Verified: Search operational ✓`);
    addLog('healer', `[${sessionId}] Issue resolved in ${recoveryTime.toFixed(1)}s`);
    
    setSystemStatus(prev => ({
      ...prev,
      totalHeals: prev.totalHeals + 1,
    }));
  };

  const updateSession = (sessionId: string, updates: Partial<HealingSession>) => {
    setHealingSessions(prev => 
      prev.map(s => s.id === sessionId ? { ...s, ...updates } : s)
    );
  };

  return (
    <div className="min-h-screen bg-[#071018] text-[#e6f7fb]">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">
            JARVIS <span className="text-[#00d4ff]">Core</span>
          </h1>
          <p className="text-[#9bb6bd]">Mark XLVIII - Self-Healing AI Assistant</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Interface */}
          <div className="lg:col-span-2 space-y-6">
            {/* Voice Orb */}
            <div className="bg-[#0d1c27] rounded-2xl p-6 border border-[#1d3c4a]">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold">Voice Interface</h2>
                <div className={`px-3 py-1 rounded-full text-xs font-mono ${
                  orbState === 'listening' ? 'bg-[#7ef0c1]/20 text-[#7ef0c1]' :
                  orbState === 'speaking' ? 'bg-[#00d4ff]/20 text-[#00d4ff]' :
                  orbState === 'thinking' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-[#1d3c4a] text-[#9bb6bd]'
                }`}>
                  {orbState.toUpperCase()}
                </div>
              </div>
              
              <div className="flex items-center justify-center py-8">
                <div className="w-64 h-64">
                  <voice-orb 
                    ref={orbRef}
                    state={orbState} 
                    style={{ width: '100%', height: '100%' }}
                  />
                </div>
              </div>

              <div className="flex gap-3 mt-4">
                <button
                  onClick={toggleListening}
                  className={`flex-1 py-3 rounded-xl font-medium transition-all flex items-center justify-center gap-2 ${
                    isListening
                      ? 'bg-red-500/20 border border-red-500/50 text-red-400'
                      : 'bg-[#00d4ff]/20 border border-[#00d4ff]/50 text-[#00d4ff]'
                  }`}
                >
                  <i className={`fas ${isListening ? 'fa-stop' : 'fa-microphone'}`}></i>
                  {isListening ? 'Stop' : 'Talk'}
                </button>
                <button
                  onClick={() => triggerHealingDemo()}
                  className="flex-1 py-3 rounded-xl bg-[#7ef0c1]/20 border border-[#7ef0c1]/50 text-[#7ef0c1] font-medium"
                >
                  <i className="fas fa-bug mr-2"></i>
                  Test Healing
                </button>
              </div>
            </div>

            {/* Chat Interface */}
            <div className="bg-[#0d1c27] rounded-2xl p-6 border border-[#1d3c4a]">
              <h2 className="text-lg font-bold mb-4">Conversation</h2>
              
              <div className="h-80 overflow-y-auto mb-4 space-y-2 scrollbar-thin">
                {logs.map(log => (
                  <motion.div
                    key={log.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className={`text-sm font-mono ${
                      log.speaker === 'user' ? 'text-[#7ef0c1]' :
                      log.speaker === 'jarvis' ? 'text-[#00d4ff]' :
                      log.speaker === 'healer' ? 'text-[#fbbf24]' :
                      'text-[#9bb6bd]'
                    }`}
                  >
                    <span className="text-[#1d3c4a] mr-2">{log.timestamp}</span>
                    <span className="mr-2">
                      {log.speaker === 'user' ? 'You:' : 
                       log.speaker === 'jarvis' ? 'Jarvis:' :
                       log.speaker === 'healer' ? 'Healer:' : 'SYS:'}
                    </span>
                    {log.text}
                  </motion.div>
                ))}
              </div>

              <div className="flex gap-2">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Type a command... (try: 'search', 'file', 'heal', 'status')"
                  className="flex-1 px-4 py-3 rounded-xl bg-[#071018] border border-[#1d3c4a] text-[#e6f7fb] placeholder-[#9bb6bd]/50 focus:outline-none focus:border-[#00d4ff]/50"
                />
                <button
                  onClick={handleSendMessage}
                  className="px-6 py-3 rounded-xl bg-[#00d4ff]/20 border border-[#00d4ff]/50 text-[#00d4ff] font-medium"
                >
                  <i className="fas fa-paper-plane"></i>
                </button>
              </div>
            </div>
          </div>

          {/* Side Panel */}
          <div className="space-y-6">
            {/* System Status */}
            <div className="bg-[#0d1c27] rounded-2xl p-6 border border-[#1d3c4a]">
              <h2 className="text-lg font-bold mb-4">System Status</h2>
              
              <div className="space-y-3">
                {[
                  { label: 'CPU', value: systemStatus.cpu, color: '#00d4ff', icon: 'fas fa-microchip' },
                  { label: 'RAM', value: systemStatus.ram, color: '#7ef0c1', icon: 'fas fa-memory' },
                  { label: 'GPU', value: systemStatus.gpu, color: '#00d4ff', icon: 'fas fa-tv' },
                  { label: 'TEMP', value: systemStatus.temp, color: systemStatus.temp > 65 ? '#f87171' : '#7ef0c1', icon: 'fas fa-thermometer-half' },
                ].map((metric, i) => (
                  <div key={i}>
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center gap-2">
                        <i className={`${metric.icon} text-xs`} style={{ color: metric.color }}></i>
                        <span className="text-xs text-[#9bb6bd]">{metric.label}</span>
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
              </div>

              <div className="mt-4 pt-4 border-t border-[#1d3c4a]">
                <div className="flex items-center justify-between text-xs mb-2">
                  <span className="text-[#9bb6bd]">Self-Healing</span>
                  <span className="text-[#7ef0c1] font-mono">
                    {systemStatus.healingActive ? '● ACTIVE' : '○ INACTIVE'}
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs mb-2">
                  <span className="text-[#9bb6bd]">Total Heals</span>
                  <span className="text-[#00d4ff] font-mono">{systemStatus.totalHeals}</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-[#9bb6bd]">Success Rate</span>
                  <span className="text-[#7ef0c1] font-mono">{systemStatus.successRate}%</span>
                </div>
              </div>
            </div>

            {/* Healing Sessions */}
            <div className="bg-[#0d1c27] rounded-2xl p-6 border border-[#1d3c4a]">
              <h2 className="text-lg font-bold mb-4">Healing Sessions</h2>
              
              <div className="space-y-3 max-h-96 overflow-y-auto scrollbar-thin">
                {healingSessions.length === 0 ? (
                  <p className="text-sm text-[#9bb6bd] text-center py-8">
                    No healing sessions yet. Click "Test Healing" to see it in action.
                  </p>
                ) : (
                  healingSessions.slice().reverse().map(session => (
                    <motion.div
                      key={session.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-3 rounded-lg bg-[#071018] border border-[#1d3c4a]"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-mono text-[#9bb6bd]">{session.id}</span>
                        <span className={`text-xs font-mono ${
                          session.status === 'complete' ? 'text-[#7ef0c1]' :
                          session.status === 'failed' ? 'text-red-400' :
                          'text-[#fbbf24]'
                        }`}>
                          {session.status === 'complete' ? '✓ RESOLVED' : 
                           session.status === 'failed' ? '✗ FAILED' :
                           '⟳ IN PROGRESS'}
                        </span>
                      </div>
                      <div className="text-xs text-[#e6f7fb] mb-1">{session.anomaly}</div>
                      {session.recoveryTime && (
                        <div className="text-xs text-[#9bb6bd]">
                          Recovery: {session.recoveryTime.toFixed(1)}s
                        </div>
                      )}
                    </motion.div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
