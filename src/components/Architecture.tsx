import { motion } from 'framer-motion';

const projectStructure = [
  { name: 'main.py', desc: 'Core loop — Gemini Live session, audio I/O, tool dispatch', icon: 'fas fa-play' },
  { name: 'ui.py', desc: 'PyQt6 HUD — waveform, log panel, interrupt button, camera feed', icon: 'fas fa-window-maximize' },
  { name: 'setup.py', desc: 'First-run configuration wizard', icon: 'fas fa-cog' },
  { name: 'actions/', desc: '20+ action modules for every capability', icon: 'fas fa-bolt', isFolder: true },
  { name: 'memory/', desc: 'Persistent key-value memory store', icon: 'fas fa-database' },
  { name: 'core/', desc: 'JARVIS personality and tool-routing rules', icon: 'fas fa-brain' },
  { name: 'config/', desc: 'API key and system configuration', icon: 'fas fa-key' },
  { name: 'dashboard/', desc: 'FastAPI web dashboard for remote control', icon: 'fas fa-globe' },
];

const actionModules = [
  'web_search.py', 'screen_processor.py', 'reminder.py', 'system_monitor.py',
  'computer_settings.py', 'computer_control.py', 'open_app.py', 'browser_control.py',
  'file_controller.py', 'file_processor.py', 'send_message.py', 'weather_report.py',
  'flight_finder.py', 'youtube_video.py', 'game_updater.py', 'code_helper.py',
  'dev_agent.py', 'desktop.py', 'proactive.py',
];

export default function Architecture() {
  return (
    <section id="architecture" className="relative py-24 px-6">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(0,212,255,0.03)_0%,transparent_60%)]" />
      
      <div className="relative max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="text-[#7ef0c1] font-mono text-sm tracking-widest uppercase">
            Project Structure
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-4 mb-6">
            Built for{' '}
            <span className="bg-gradient-to-r from-[#7ef0c1] to-[#00d4ff] bg-clip-text text-transparent">
              Power
            </span>
          </h2>
          <p className="text-[#9bb6bd] text-lg max-w-2xl mx-auto">
            A clean, modular architecture designed for extensibility. Each action is self-contained, 
            making it easy to add new capabilities.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Project Structure */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60"
          >
            <h3 className="text-lg font-bold mb-6 flex items-center gap-3">
              <i className="fas fa-folder-tree text-[#00d4ff]"></i>
              Project Structure
            </h3>
            <div className="space-y-3">
              {projectStructure.map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.05 }}
                  className="flex items-start gap-3 p-3 rounded-lg hover:bg-[#1d3c4a]/30 transition-colors group"
                >
                  <div className="w-8 h-8 rounded-lg bg-[#00d4ff]/10 flex items-center justify-center flex-shrink-0 group-hover:bg-[#00d4ff]/20 transition-colors">
                    <i className={`${item.icon} text-xs text-[#00d4ff]`}></i>
                  </div>
                  <div>
                    <span className="font-mono text-sm text-[#7ef0c1]">{item.name}</span>
                    <p className="text-xs text-[#9bb6bd] mt-0.5">{item.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Action Modules */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60"
          >
            <h3 className="text-lg font-bold mb-6 flex items-center gap-3">
              <i className="fas fa-puzzle-piece text-[#7ef0c1]"></i>
              Action Modules (20+)
            </h3>
            <div className="flex flex-wrap gap-2">
              {actionModules.map((mod, i) => (
                <motion.span
                  key={i}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.03 }}
                  className="px-3 py-1.5 rounded-lg bg-[#1d3c4a]/40 border border-[#1d3c4a] text-xs font-mono text-[#9bb6bd] hover:text-[#7ef0c1] hover:border-[#7ef0c1]/30 transition-all cursor-default"
                >
                  {mod}
                </motion.span>
              ))}
            </div>

            {/* Tech Stack */}
            <div className="mt-8 pt-6 border-t border-[#1d3c4a]/60">
              <h4 className="text-sm font-bold mb-4 text-[#9bb6bd]">TECH STACK</h4>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { name: 'Python 3.11+', icon: 'fab fa-python', color: '#00d4ff' },
                  { name: 'Gemini Live API', icon: 'fas fa-robot', color: '#7ef0c1' },
                  { name: 'PyQt6', icon: 'fas fa-window-maximize', color: '#00d4ff' },
                  { name: 'FastAPI', icon: 'fas fa-server', color: '#7ef0c1' },
                  { name: 'SoundDevice', icon: 'fas fa-volume-up', color: '#00d4ff' },
                  { name: 'DuckDuckGo', icon: 'fas fa-search', color: '#7ef0c1' },
                ].map((tech, i) => (
                  <div key={i} className="flex items-center gap-2 px-3 py-2 rounded-lg bg-[#071018] border border-[#1d3c4a]/40">
                    <i className={`${tech.icon} text-sm`} style={{ color: tech.color }}></i>
                    <span className="text-xs text-[#e6f7fb]">{tech.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Data Flow Diagram */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-8 p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60"
        >
          <h3 className="text-lg font-bold mb-6 flex items-center gap-3">
            <i className="fas fa-project-diagram text-[#00d4ff]"></i>
            Data Flow
          </h3>
          <div className="flex flex-wrap items-center justify-center gap-4 text-sm">
            {[
              { label: 'Microphone', icon: 'fas fa-microphone', color: '#00d4ff' },
              { label: '→', icon: '', color: '#1d3c4a' },
              { label: 'Gemini Live', icon: 'fas fa-cloud', color: '#7ef0c1' },
              { label: '→', icon: '', color: '#1d3c4a' },
              { label: 'Tool Dispatch', icon: 'fas fa-random', color: '#00d4ff' },
              { label: '→', icon: '', color: '#1d3c4a' },
              { label: 'Actions', icon: 'fas fa-bolt', color: '#7ef0c1' },
              { label: '→', icon: '', color: '#1d3c4a' },
              { label: 'Speaker', icon: 'fas fa-volume-up', color: '#00d4ff' },
            ].map((step, i) => (
              <div key={i} className="flex items-center gap-2">
                {step.icon && (
                  <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-[#071018] border border-[#1d3c4a]">
                    <i className={`${step.icon} text-sm`} style={{ color: step.color }}></i>
                    <span className="text-[#e6f7fb] font-medium">{step.label}</span>
                  </div>
                )}
                {!step.icon && (
                  <span className="text-[#1d3c4a] text-xl">→</span>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
