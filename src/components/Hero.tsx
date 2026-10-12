import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

export default function Hero() {
  const [statusText, setStatusText] = useState('INITIALIZING...');
  const [pulse, setPulse] = useState(false);

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

        {/* Right: Animated HUD visualization */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="hidden lg:block"
        >
          <HUDVisualization />
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

function HUDVisualization() {
  return (
    <div className="relative w-full aspect-square max-w-md mx-auto">
      {/* Outer ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 30, repeat: Infinity, ease: 'linear' }}
        className="absolute inset-0 rounded-full border border-[#00d4ff]/20"
      >
        <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-[#00d4ff]"></div>
      </motion.div>

      {/* Middle ring */}
      <motion.div
        animate={{ rotate: -360 }}
        transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
        className="absolute inset-8 rounded-full border border-[#7ef0c1]/20"
      >
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 w-2 h-2 rounded-full bg-[#7ef0c1]"></div>
      </motion.div>

      {/* Inner ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 15, repeat: Infinity, ease: 'linear' }}
        className="absolute inset-16 rounded-full border border-[#00d4ff]/30"
      >
        <div className="absolute top-1/2 right-0 translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#00d4ff]"></div>
      </motion.div>

      {/* Center core */}
      <div className="absolute inset-24 rounded-full bg-gradient-to-br from-[#00d4ff]/10 to-[#7ef0c1]/10 border border-[#00d4ff]/30 flex items-center justify-center">
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="w-16 h-16 rounded-full bg-gradient-to-br from-[#00d4ff] to-[#7ef0c1] flex items-center justify-center shadow-lg shadow-[#00d4ff]/30"
        >
          <i className="fas fa-brain text-[#00141b] text-2xl"></i>
        </motion.div>
      </div>

      {/* Floating labels */}
      <motion.div
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 3, repeat: Infinity }}
        className="absolute top-4 right-4 px-3 py-1 rounded-full bg-[#0d1c27] border border-[#1d3c4a] text-xs font-mono text-[#00d4ff]"
      >
        VOICE: ACTIVE
      </motion.div>

      <motion.div
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 3, repeat: Infinity, delay: 1 }}
        className="absolute bottom-4 left-4 px-3 py-1 rounded-full bg-[#0d1c27] border border-[#1d3c4a] text-xs font-mono text-[#7ef0c1]"
      >
        VISION: READY
      </motion.div>

      <motion.div
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 3, repeat: Infinity, delay: 2 }}
        className="absolute top-1/2 left-0 -translate-x-2 -translate-y-1/2 px-3 py-1 rounded-full bg-[#0d1c27] border border-[#1d3c4a] text-xs font-mono text-[#00d4ff]"
      >
        API: LIVE
      </motion.div>
    </div>
  );
}
