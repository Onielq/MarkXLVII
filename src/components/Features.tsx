import { motion } from 'framer-motion';

const features = [
  {
    icon: 'fas fa-microphone',
    title: 'Real-time Voice',
    description: 'Ultra-low latency conversation in any language via Gemini Live API with native audio streaming.',
    color: '#00d4ff',
  },
  {
    icon: 'fas fa-desktop',
    title: 'System Control',
    description: 'Launch apps, adjust volume/brightness, WiFi, shortcuts, power — all by voice command.',
    color: '#7ef0c1',
  },
  {
    icon: 'fas fa-robot',
    title: 'Autonomous Tasks',
    description: 'High-level planning for complex multi-step goals via agent mode with full reasoning.',
    color: '#00d4ff',
  },
  {
    icon: 'fas fa-eye',
    title: 'Visual Awareness',
    description: 'Real-time screen capture and webcam vision piped into your main Gemini session.',
    color: '#7ef0c1',
  },
  {
    icon: 'fas fa-brain',
    title: 'Persistent Memory',
    description: 'Deeply remembers projects, preferences, and personal context across all sessions.',
    color: '#00d4ff',
  },
  {
    icon: 'fas fa-keyboard',
    title: 'Hybrid Input',
    description: 'Seamlessly switch between keyboard typing and voice commands without friction.',
    color: '#7ef0c1',
  },
  {
    icon: 'fas fa-sun',
    title: 'Morning Briefing',
    description: 'On first boot: greets you, reads the time, fetches live news headlines, and checks weather.',
    color: '#00d4ff',
  },
  {
    icon: 'fas fa-bell',
    title: 'Proactive Check-ins',
    description: 'After 15 minutes of silence, JARVIS checks context and offers something genuinely useful.',
    color: '#7ef0c1',
  },
  {
    icon: 'fas fa-microchip',
    title: 'Hardware Monitoring',
    description: 'Continuous CPU, RAM, GPU and temperature telemetry with localized voice alerts.',
    color: '#00d4ff',
  },
  {
    icon: 'fas fa-cloud-sun',
    title: 'Weather Report',
    description: 'Live weather data for your city, personalized from your stored memory and preferences.',
    color: '#7ef0c1',
  },
  {
    icon: 'fas fa-search',
    title: 'Multi-Mode Web Search',
    description: 'news / research / price / compare / search — Gemini Grounded first, DDG fallback.',
    color: '#00d4ff',
  },
  {
    icon: 'fas fa-clock',
    title: 'Smart Reminders',
    description: 'OS-native scheduled notifications via Task Scheduler, LaunchAgent, or systemd.',
    color: '#7ef0c1',
  },
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Features() {
  return (
    <section id="features" className="relative py-24 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="text-[#00d4ff] font-mono text-sm tracking-widest uppercase">
            Capabilities
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-4 mb-6">
            Everything You Need,{' '}
            <span className="bg-gradient-to-r from-[#00d4ff] to-[#7ef0c1] bg-clip-text text-transparent">
              By Voice
            </span>
          </h2>
          <p className="text-[#9bb6bd] text-lg max-w-2xl mx-auto">
            Mark XLVIII isn't just an assistant — it's an extension of your digital life.
            Every capability is accessible through natural conversation.
          </p>
        </motion.div>

        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              variants={item}
              className="group p-5 rounded-xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60 hover:border-[#00d4ff]/30 transition-all duration-300 hover:shadow-lg hover:shadow-[#00d4ff]/5"
            >
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center mb-4 transition-transform group-hover:scale-110"
                style={{ backgroundColor: `${feature.color}15` }}
              >
                <i className={`${feature.icon} text-lg`} style={{ color: feature.color }}></i>
              </div>
              <h3 className="font-semibold text-[#e6f7fb] mb-2">{feature.title}</h3>
              <p className="text-sm text-[#9bb6bd] leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
