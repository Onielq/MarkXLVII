import { motion } from 'framer-motion';
import { useState } from 'react';

const steps = [
  {
    step: 1,
    title: 'Clone the Repository',
    command: 'git clone https://github.com/Onielq/Mark-XLVII.git',
    description: 'Download the complete project source code to your local machine.',
    icon: 'fas fa-download',
  },
  {
    step: 2,
    title: 'Navigate to Project',
    command: 'cd Mark-XLVII',
    description: 'Enter the project directory.',
    icon: 'fas fa-folder-open',
  },
  {
    step: 3,
    title: 'Install Dependencies',
    command: 'pip install -r requirements.txt',
    description: 'Install all required Python packages. Some OS-specific deps may need manual install.',
    icon: 'fas fa-box',
  },
  {
    step: 4,
    title: 'Configure API Key',
    command: 'python setup.py',
    description: 'Run the setup wizard to configure your free Gemini API key. Get one at aistudio.google.com.',
    icon: 'fas fa-key',
  },
  {
    step: 5,
    title: 'Launch JARVIS',
    command: 'python main.py',
    description: 'Start the assistant. It will greet you, fetch news, and begin listening for commands.',
    icon: 'fas fa-play',
  },
];

const requirements = [
  { name: 'OS', value: 'Windows 10/11, macOS, or Linux', icon: 'fas fa-laptop' },
  { name: 'Python', value: '3.11 or 3.12', icon: 'fab fa-python' },
  { name: 'Microphone', value: 'Required for voice interaction', icon: 'fas fa-microphone' },
  { name: 'API Key', value: 'Free Gemini API key', icon: 'fas fa-key' },
];

export default function Setup() {
  const [copiedStep, setCopiedStep] = useState<number | null>(null);

  const copyCommand = (command: string, step: number) => {
    navigator.clipboard.writeText(command);
    setCopiedStep(step);
    setTimeout(() => setCopiedStep(null), 2000);
  };

  return (
    <section id="setup" className="relative py-24 px-6">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_100%,rgba(126,240,193,0.03)_0%,transparent_50%)]" />
      
      <div className="relative max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="text-[#7ef0c1] font-mono text-sm tracking-widest uppercase">
            Quick Start
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-4 mb-6">
            Get Started in{' '}
            <span className="bg-gradient-to-r from-[#7ef0c1] to-[#00d4ff] bg-clip-text text-transparent">
              5 Minutes
            </span>
          </h2>
          <p className="text-[#9bb6bd] text-lg max-w-2xl mx-auto">
            Follow these steps to get Mark XLVIII running on your machine. No subscriptions, no cloud dependencies.
          </p>
        </motion.div>

        {/* Requirements */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-12 p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60"
        >
          <h3 className="text-lg font-bold mb-4 flex items-center gap-3">
            <i className="fas fa-clipboard-check text-[#00d4ff]"></i>
            Requirements
          </h3>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {requirements.map((req, i) => (
              <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-[#071018] border border-[#1d3c4a]/40">
                <i className={`${req.icon} text-[#00d4ff]`}></i>
                <div>
                  <div className="text-xs text-[#9bb6bd]">{req.name}</div>
                  <div className="text-sm text-[#e6f7fb] font-medium">{req.value}</div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Steps */}
        <div className="space-y-4">
          {steps.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="group p-5 rounded-xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60 hover:border-[#00d4ff]/30 transition-all"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-[#00d4ff]/20 to-[#7ef0c1]/20 border border-[#00d4ff]/30 flex items-center justify-center">
                  <span className="text-sm font-bold text-[#00d4ff]">{step.step}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="font-semibold text-[#e6f7fb] mb-1 flex items-center gap-2">
                    <i className={`${step.icon} text-xs text-[#7ef0c1]`}></i>
                    {step.title}
                  </h4>
                  <p className="text-sm text-[#9bb6bd] mb-3">{step.description}</p>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 px-3 py-2 rounded-lg bg-[#071018] border border-[#1d3c4a] text-sm font-mono text-[#7ef0c1] overflow-x-auto">
                      $ {step.command}
                    </code>
                    <button
                      onClick={() => copyCommand(step.command, step.step)}
                      className="flex-shrink-0 px-3 py-2 rounded-lg bg-[#1d3c4a]/40 border border-[#1d3c4a] text-xs text-[#9bb6bd] hover:text-[#00d4ff] hover:border-[#00d4ff]/30 transition-all"
                    >
                      {copiedStep === step.step ? (
                        <><i className="fas fa-check text-[#7ef0c1]"></i> Copied</>
                      ) : (
                        <><i className="fas fa-copy"></i> Copy</>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Optional dashboard deps */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-8 p-5 rounded-xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60 border-l-3 border-l-[#7ef0c1]"
        >
          <div className="flex items-start gap-3">
            <i className="fas fa-info-circle text-[#7ef0c1] mt-0.5"></i>
            <div>
              <h4 className="font-semibold text-[#e6f7fb] mb-1">Optional: Remote Dashboard</h4>
              <p className="text-sm text-[#9bb6bd] mb-2">
                For the web dashboard (control JARVIS from your phone), install additional dependencies:
              </p>
              <code className="px-3 py-2 rounded-lg bg-[#071018] border border-[#1d3c4a] text-sm font-mono text-[#7ef0c1]">
                pip install fastapi "uvicorn[standard]" cryptography
              </code>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
