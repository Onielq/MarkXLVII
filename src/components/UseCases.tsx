import { motion } from 'framer-motion';
import { useState } from 'react';

const useCases = [
  {
    id: 'remote',
    title: 'Remote Access',
    subtitle: 'Control JARVIS from anywhere',
    icon: 'fas fa-mobile-alt',
    color: '#00d4ff',
    scenarios: [
      {
        title: 'Phone Control',
        description: 'Use the Remote Dashboard to send voice commands from your phone. JARVIS will execute them on your computer.',
        steps: [
          'Run JARVIS on your PC',
          'Click "Remote Control" in the UI',
          'Scan the QR code with your phone',
          'Send voice or text commands remotely',
        ],
      },
      {
        title: 'Persistent Sessions',
        description: 'Your phone stays paired. Next time you open the dashboard, it auto-reconnects without re-scanning.',
        steps: [
          'Pair once via QR code',
          'Device token is saved locally',
          'Auto-login on subsequent visits',
          'Revoke devices anytime for security',
        ],
      },
      {
        title: 'Text Fallback Mode',
        description: 'No microphone? Use text commands through the dashboard. JARVIS responds via text or optional LLM fallback.',
        steps: [
          'Open dashboard in browser',
          'Type commands in the chat interface',
          'Get text responses from JARVIS',
          'Works even without audio hardware',
        ],
      },
    ],
  },
  {
    id: 'persistence',
    title: 'Persistence & Memory',
    subtitle: 'JARVIS remembers everything',
    icon: 'fas fa-brain',
    color: '#7ef0c1',
    scenarios: [
      {
        title: 'Persistent Memory',
        description: 'JARVIS stores your preferences, projects, and context. Close your computer, restart days later — it remembers.',
        steps: [
          'Memory auto-saves to disk',
          'Loads on every startup',
          'Context carries across sessions',
          'No cloud dependency',
        ],
      },
      {
        title: 'OS-Native Reminders',
        description: 'Set reminders that trigger even when JARVIS isn\'t running. Uses Task Scheduler (Windows), LaunchAgent (macOS), or systemd (Linux).',
        steps: [
          'Say "Remind me tomorrow at 9am to call mom"',
          'JARVIS creates OS-level scheduled task',
          'Notification fires at the exact time',
          'Works independently of JARVIS process',
        ],
      },
      {
        title: 'Language Detection',
        description: 'JARVIS detects your spoken language on first use and saves it. All future sessions adapt automatically.',
        steps: [
          'Speak in your preferred language',
          'Language is detected and saved',
          'All responses adapt to your language',
          'Silent detection — no prompts needed',
        ],
      },
    ],
  },
  {
    id: 'extend',
    title: 'Extend & Customize',
    subtitle: 'Add your own capabilities',
    icon: 'fas fa-puzzle-piece',
    color: '#00d4ff',
    scenarios: [
      {
        title: 'Add New Actions',
        description: 'Create custom action modules in the actions/ folder. JARVIS will automatically discover and use them.',
        steps: [
          'Create actions/my_action.py',
          'Define function with tool signature',
          'Register in main.py TOOL_DECLARATIONS',
          'JARVIS calls it when relevant',
        ],
      },
      {
        title: 'Custom Prompts',
        description: 'Modify core/prompt.txt to change JARVIS personality, tool routing, or add domain-specific knowledge.',
        steps: [
          'Edit core/prompt.txt',
          'Define personality traits',
          'Specify tool usage rules',
          'Restart JARVIS to apply',
        ],
      },
      {
        title: 'Integrate APIs',
        description: 'Connect to any API: smart home, calendars, email, databases. Create wrapper actions for seamless integration.',
        steps: [
          'Get API credentials',
          'Create action wrapper',
          'Add to tool declarations',
          'JARVIS handles the rest',
        ],
      },
    ],
  },
];

export default function UseCases() {
  const [activeCase, setActiveCase] = useState('remote');
  const [expandedScenario, setExpandedScenario] = useState<number | null>(null);

  const currentCase = useCases.find(c => c.id === activeCase)!;

  return (
    <section id="usecases" className="relative py-24 px-6">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(0,212,255,0.03)_0%,transparent_50%)]" />
      
      <div className="relative max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="text-[#00d4ff] font-mono text-sm tracking-widest uppercase">
            Real-World Usage
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-4 mb-6">
            Use It{' '}
            <span className="bg-gradient-to-r from-[#00d4ff] to-[#7ef0c1] bg-clip-text text-transparent">
              Your Way
            </span>
          </h2>
          <p className="text-[#9bb6bd] text-lg max-w-2xl mx-auto">
            Whether you're at your desk or across the world, JARVIS adapts to your workflow.
            Close your computer, open it days later — everything persists.
          </p>
        </motion.div>

        {/* Tabs */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {useCases.map((useCase) => (
            <button
              key={useCase.id}
              onClick={() => {
                setActiveCase(useCase.id);
                setExpandedScenario(null);
              }}
              className={`px-6 py-3 rounded-xl font-medium transition-all ${
                activeCase === useCase.id
                  ? 'bg-gradient-to-r from-[#00d4ff]/20 to-[#7ef0c1]/20 border border-[#00d4ff]/50 text-[#e6f7fb]'
                  : 'bg-[#0d1c27] border border-[#1d3c4a] text-[#9bb6bd] hover:text-[#e6f7fb] hover:border-[#00d4ff]/30'
              }`}
            >
              <i className={`${useCase.icon} mr-2`} style={{ color: useCase.color }}></i>
              {useCase.title}
            </button>
          ))}
        </div>

        {/* Content */}
        <motion.div
          key={activeCase}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="grid md:grid-cols-3 gap-6"
        >
          {currentCase.scenarios.map((scenario, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="group p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60 hover:border-[#00d4ff]/30 transition-all cursor-pointer"
              onClick={() => setExpandedScenario(expandedScenario === i ? null : i)}
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-lg font-bold text-[#e6f7fb]">{scenario.title}</h3>
                <i className={`fas fa-chevron-down text-xs text-[#9bb6bd] transition-transform ${
                  expandedScenario === i ? 'rotate-180' : ''
                }`}></i>
              </div>
              <p className="text-sm text-[#9bb6bd] leading-relaxed mb-4">
                {scenario.description}
              </p>

              <motion.div
                initial={false}
                animate={{ height: expandedScenario === i ? 'auto' : 0, opacity: expandedScenario === i ? 1 : 0 }}
                transition={{ duration: 0.3 }}
                className="overflow-hidden"
              >
                <div className="pt-4 border-t border-[#1d3c4a]/40">
                  <div className="text-xs font-mono text-[#9bb6bd] mb-3">HOW IT WORKS</div>
                  <ol className="space-y-2">
                    {scenario.steps.map((step, j) => (
                      <li key={j} className="flex items-start gap-2 text-sm">
                        <span className="flex-shrink-0 w-5 h-5 rounded-full bg-[#00d4ff]/10 border border-[#00d4ff]/30 flex items-center justify-center text-xs text-[#00d4ff] font-bold">
                          {j + 1}
                        </span>
                        <span className="text-[#e6f7fb]">{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>
              </motion.div>

              {expandedScenario !== i && (
                <div className="mt-4 text-xs text-[#00d4ff] font-medium">
                  Click to see details →
                </div>
              )}
            </motion.div>
          ))}
        </motion.div>

        {/* Code Example */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-12 p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60"
        >
          <h3 className="text-lg font-bold mb-4 flex items-center gap-3">
            <i className="fas fa-code text-[#7ef0c1]"></i>
            Example: Adding a Custom Action
          </h3>
          <div className="space-y-4">
            <div>
              <div className="text-xs font-mono text-[#9bb6bd] mb-2">1. Create actions/smart_home.py</div>
              <pre className="p-4 rounded-lg bg-[#071018] border border-[#1d3c4a] text-sm font-mono text-[#7ef0c1] overflow-x-auto">
{`def smart_home(action: str, device: str = "", value: str = ""):
    """Control smart home devices via voice."""
    if action == "turn_on":
        # Your smart home API call here
        return f"Turned on {device}"
    elif action == "set_brightness":
        # Set brightness level
        return f"Set {device} brightness to {value}%"
    return "Action not recognized"`}
              </pre>
            </div>
            <div>
              <div className="text-xs font-mono text-[#9bb6bd] mb-2">2. Register in main.py</div>
              <pre className="p-4 rounded-lg bg-[#071018] border border-[#1d3c4a] text-sm font-mono text-[#00d4ff] overflow-x-auto">
{`TOOL_DECLARATIONS = [
    # ... existing tools ...
    {
        "name": "smart_home",
        "description": "Control smart home devices",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action": {"type": "STRING", "description": "turn_on | turn_off | set_brightness"},
                "device": {"type": "STRING", "description": "Device name"},
                "value": {"type": "STRING", "description": "Value for brightness, etc."}
            },
            "required": ["action"]
        }
    }
]`}
              </pre>
            </div>
            <div className="text-sm text-[#9bb6bd]">
              <i className="fas fa-lightbulb text-[#7ef0c1] mr-2"></i>
              JARVIS will now automatically use this tool when you say things like "Turn on the living room lights" or "Set bedroom brightness to 50%".
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
