import { motion } from 'framer-motion';
import { useState, useEffect, useRef } from 'react';

export default function Hero() {
  const [statusText, setStatusText] = useState('INITIALIZING...');
  const [pulse, setPulse] = useState(false);
  const [orbState, setOrbState] = useState<'idle' | 'listening' | 'thinking' | 'speaking'>('idle');
  const [isListening, setIsListening] = useState(false);
  const orbRef = useRef<any>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    const statuses = [
      'SYSTEM ONLINE',
      'GEMINI LIVE CONNECTED',
      'VOICE MODULE ACTIVE',
      'VISION ENGINE READY',
      'ALL SYSTEMS NOMINAL',
    ];
    let i = 0;
    const interval = setInterval(() => {
      i = (i + 1) % statuses.length;
      setStatusText(statuses[i]);
      setPulse(true);
      setTimeout(() => setPulse(false), 500);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const toggleListening = async () => {
    if (isListening) {
      // Stop listening
      if (orbRef.current) {
        orbRef.current.disconnect();
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      }
      setIsListening(false);
      setOrbState('idle');
    } else {
      // Start listening
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        streamRef.current = stream;
        if (orbRef.current) {
          await orbRef.current.connect(stream);
          setOrbState('listening');
          setIsListening(true);
        }
      } catch (err) {
        console.error('Microphone access denied:', err);
        alert('Microphone access is required to talk to JARVIS');
      }
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center pt-20">
      {/* Radial gradient overlay */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_0%,#123846_0%,#071018_45%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_80%,rgba(0,212,255,0.05)_0%,transparent_50%)]" />

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-20 grid lg:grid-cols-2 gap-16 items-center">
        {/* Left: Text content */}
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#00d4ff]/10 border border-[#00d4ff]/20 mb-6">
            <span className={`w-2 h-2 rounded-full ${pulse ? 'bg-[#7ef0c1]' : 'bg-[#00d4ff]'} transition-colors`}></span>
            <span className="text-xs font-mono text-[#00d4ff] tracking-wider">{statusText}</span>
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold leading-tight mb-6">
            Meet{' '}
            <span className="bg-gradient-to-r from-[#00d4ff] to-[#7ef0c1] bg-clip-text text-transparent">
              Mark XLVIII
            </span>
          </h1>

          <p className="text-xl text-[#9bb6bd] mb-8 max-w-lg leading-relaxed">
            The ultimate cross-platform personal AI assistant. It can hear, see, understand, and control your digital workspace — built on Gemini Live API.
          </p>

          <div className="flex flex-wrap gap-4">
            <a
              href="https://github.com/Onielq/Mark-XLVII"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#00d4ff] text-[#00141b] font-bold hover:bg-[#7ef0c1] transition-all shadow-lg shadow-[#00d4ff]/20"
            >
              <i className="fab fa-github"></i>
              View on GitHub
            </a>
            <button
              onClick={() => document.getElementById('setup')?.scrollIntoView({ behavior: 'smooth' })}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl border border-[#1d3c4a] text-[#e6f7fb] font-medium hover:border-[#00d4ff]/50 hover:bg-[#0d1c27] transition-all"
            >
              <i className="fas fa-rocket"></i>
              Quick Start
            </button>
          </div>

          <div className="mt-10 flex items-center gap-6 text-sm text-[#9bb6bd]">
            <div className="flex items-center gap-2">
              <i className="fab fa-python text-[#00d4ff]"></i>
              <span>Python 3.11+</span>
            </div>
            <div className="flex items-center gap-2">
              <i className="fas fa-microphone text-[#7ef0c1]"></i>
              <span>Real-time Voice</span>
            </div>
            <div className="flex items-center gap-2">
              <i className="fas fa-eye text-[#00d4ff]"></i>
              <span>Visual AI</span>
            </div>
          </div>
        </motion.div>

        {/* Right: Voice Orb */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="hidden lg:flex flex-col items-center gap-6"
        >
          <div className="w-80 h-80 relative">
            <voice-orb 
              ref={orbRef}
              state={orbState} 
              style={{ width: '100%', height: '100%' }}
            />
          </div>
          
          {/* Voice Orb Controls */}
          <div className="flex flex-col items-center gap-4">
            <button
              onClick={toggleListening}
              className={`px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-3 ${
                isListening
                  ? 'bg-red-500/20 border border-red-500/50 text-red-400 hover:bg-red-500/30'
                  : 'bg-[#00d4ff]/20 border border-[#00d4ff]/50 text-[#00d4ff] hover:bg-[#00d4ff]/30'
              }`}
            >
              <i className={`fas ${isListening ? 'fa-stop' : 'fa-microphone'}`}></i>
              <span>{isListening ? 'Stop Listening' : 'Talk to JARVIS'}</span>
            </button>
            
            <div className="flex gap-2">
              {(['idle', 'listening', 'thinking', 'speaking'] as const).map((state) => (
                <button
                  key={state}
                  onClick={() => setOrbState(state)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all capitalize ${
                    orbState === state
                      ? 'bg-[#00d4ff]/20 border border-[#00d4ff]/50 text-[#00d4ff]'
                      : 'bg-[#0d1c27] border border-[#1d3c4a] text-[#9bb6bd] hover:text-[#e6f7fb]'
                  }`}
                >
                  {state}
                </button>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <i className="fas fa-chevron-down text-[#00d4ff]/50 text-xl"></i>
      </motion.div>
    </section>
  );
}
