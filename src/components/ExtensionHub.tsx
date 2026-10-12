import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';

interface Skill {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: string;
  color: string;
  installed?: boolean;
  author?: string;
  downloads?: string;
  type: 'action' | 'knowledge' | 'command' | 'integration';
}

const marketplaceSkills: Skill[] = [
  { id: '1', name: 'Smart Home Hub', description: 'Control Philips Hue, LIFX, and HomeKit devices by voice', category: 'Smart Home', icon: 'fas fa-house-signal', color: '#fbbf24', installed: true, author: 'Community', downloads: '12.4k', type: 'integration' },
  { id: '2', name: 'Spotify Control', description: 'Play, pause, search, and control Spotify playlists', category: 'Media', icon: 'fab fa-spotify', color: '#1db954', installed: true, author: 'Official', downloads: '28.1k', type: 'integration' },
  { id: '3', name: 'Home Assistant', description: 'Full Home Assistant integration for automation', category: 'Smart Home', icon: 'fas fa-home', color: '#00d4ff', author: 'Community', downloads: '8.7k', type: 'integration' },
  { id: '4', name: 'Calendar Sync', description: 'Google Calendar & Outlook integration', category: 'Productivity', icon: 'fas fa-calendar-alt', color: '#7ef0c1', author: 'Official', downloads: '15.2k', type: 'integration' },
  { id: '5', name: 'Email Assistant', description: 'Read, compose, and send emails via Gmail/Outlook', category: 'Productivity', icon: 'fas fa-envelope', color: '#00d4ff', author: 'Community', downloads: '9.3k', type: 'integration' },
  { id: '6', name: 'Stock Tracker', description: 'Real-time stock prices and portfolio tracking', category: 'Finance', icon: 'fas fa-chart-line', color: '#7ef0c1', author: 'Community', downloads: '6.8k', type: 'action' },
  { id: '7', name: 'Recipe Master', description: 'Find recipes, create meal plans, shopping lists', category: 'Lifestyle', icon: 'fas fa-utensils', color: '#fbbf24', author: 'Community', downloads: '4.2k', type: 'action' },
  { id: '8', name: 'Fitness Coach', description: 'Track workouts, set goals, exercise guidance', category: 'Lifestyle', icon: 'fas fa-dumbbell', color: '#f87171', author: 'Community', downloads: '5.1k', type: 'action' },
  { id: '9', name: 'Translation Pro', description: 'Real-time translation in 100+ languages', category: 'Language', icon: 'fas fa-language', color: '#00d4ff', author: 'Official', downloads: '22.5k', type: 'action' },
  { id: '10', name: 'Notion Sync', description: 'Read and write to Notion databases and pages', category: 'Productivity', icon: 'fas fa-book', color: '#7ef0c1', author: 'Community', downloads: '7.9k', type: 'integration' },
  { id: '11', name: 'Discord Bridge', description: 'Send/receive Discord messages by voice', category: 'Social', icon: 'fab fa-discord', color: '#5865f2', author: 'Community', downloads: '11.3k', type: 'integration' },
  { id: '12', name: 'Crypto Wallet', description: 'Check balances, prices, and transaction history', category: 'Finance', icon: 'fab fa-bitcoin', color: '#f7931a', author: 'Community', downloads: '3.8k', type: 'action' },
];

const categories = ['All', 'Smart Home', 'Media', 'Productivity', 'Finance', 'Lifestyle', 'Language', 'Social'];

const uploadTypes = [
  {
    id: 'skill',
    title: 'Skill File (.py)',
    description: 'Upload Python action modules. Auto-detected and registered.',
    icon: 'fab fa-python',
    color: '#00d4ff',
    accept: '.py',
  },
  {
    id: 'knowledge',
    title: 'Knowledge Base (.txt, .pdf, .md)',
    description: 'Upload books, research, instructions. JARVIS learns from them.',
    icon: 'fas fa-book-open',
    color: '#7ef0c1',
    accept: '.txt,.pdf,.md,.docx',
  },
  {
    id: 'commands',
    title: 'Command Pack (.json)',
    description: 'Pre-defined voice commands and responses bundle.',
    icon: 'fas fa-terminal',
    color: '#fbbf24',
    accept: '.json',
  },
  {
    id: 'config',
    title: 'Integration Config (.yaml)',
    description: 'API credentials and service configurations.',
    icon: 'fas fa-cogs',
    color: '#f87171',
    accept: '.yaml,.yml',
  },
];

export default function ExtensionHub() {
  const [activeTab, setActiveTab] = useState<'marketplace' | 'upload' | 'installed' | 'builder'>('marketplace');
  const [activeCategory, setActiveCategory] = useState('All');
  const [skills, setSkills] = useState(marketplaceSkills);
  const [dragOver, setDragOver] = useState<string | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<Array<{ name: string; type: string; status: string }>>([]);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredSkills = skills.filter(skill => {
    const matchesCategory = activeCategory === 'All' || skill.category === activeCategory;
    const matchesSearch = skill.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         skill.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const toggleInstall = (id: string) => {
    setSkills(skills.map(s => s.id === id ? { ...s, installed: !s.installed } : s));
  };

  const handleDrop = (type: string) => {
    setDragOver(null);
    const fakeFiles = [
      { name: 'smart_lock.py', type: 'skill' },
      { name: 'ai_research.txt', type: 'knowledge' },
      { name: 'voice_commands.json', type: 'commands' },
    ];
    const randomFile = fakeFiles[Math.floor(Math.random() * fakeFiles.length)];
    setUploadedFiles(prev => [...prev, { ...randomFile, status: 'installing' }]);
    setTimeout(() => {
      setUploadedFiles(prev => prev.map(f => f.status === 'installing' ? { ...f, status: 'installed' } : f));
    }, 2000);
  };

  return (
    <section id="extensions" className="relative py-24 px-6">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_30%,rgba(126,240,193,0.04)_0%,transparent_50%)]" />
      
      <div className="relative max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <span className="text-[#7ef0c1] font-mono text-sm tracking-widest uppercase">
            No-Code Extension System
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-4 mb-6">
            Extend JARVIS{' '}
            <span className="bg-gradient-to-r from-[#7ef0c1] to-[#00d4ff] bg-clip-text text-transparent">
              Without Code
            </span>
          </h2>
          <p className="text-[#9bb6bd] text-lg max-w-2xl mx-auto">
            Upload skills, knowledge bases, command packs, or install from the community marketplace.
            Drag, drop, done.
          </p>
        </motion.div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap justify-center gap-2 mb-8 p-1.5 rounded-2xl bg-[#0d1c27]/60 border border-[#1d3c4a]/60 max-w-2xl mx-auto">
          {[
            { id: 'marketplace', label: 'Marketplace', icon: 'fas fa-store' },
            { id: 'upload', label: 'Upload Files', icon: 'fas fa-cloud-upload-alt' },
            { id: 'installed', label: 'Installed', icon: 'fas fa-check-circle' },
            { id: 'builder', label: 'Skill Builder', icon: 'fas fa-wand-magic-sparkles' },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex-1 min-w-[140px] px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center justify-center gap-2 ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-[#00d4ff]/20 to-[#7ef0c1]/20 text-[#e6f7fb] border border-[#00d4ff]/30'
                  : 'text-[#9bb6bd] hover:text-[#e6f7fb]'
              }`}
            >
              <i className={`${tab.icon} text-xs`}></i>
              {tab.label}
            </button>
          ))}
        </div>

        {/* Marketplace Tab */}
        <AnimatePresence mode="wait">
          {activeTab === 'marketplace' && (
            <motion.div
              key="marketplace"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {/* Search & Filter */}
              <div className="flex flex-col sm:flex-row gap-3 mb-6">
                <div className="flex-1 relative">
                  <i className="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-[#9bb6bd]"></i>
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search skills, integrations..."
                    className="w-full pl-11 pr-4 py-3 rounded-xl bg-[#0d1c27] border border-[#1d3c4a] text-[#e6f7fb] placeholder-[#9bb6bd]/50 focus:outline-none focus:border-[#00d4ff]/50"
                  />
                </div>
              </div>

              <div className="flex flex-wrap gap-2 mb-6">
                {categories.map(cat => (
                  <button
                    key={cat}
                    onClick={() => setActiveCategory(cat)}
                    className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
                      activeCategory === cat
                        ? 'bg-[#00d4ff]/20 text-[#00d4ff] border border-[#00d4ff]/30'
                        : 'bg-[#0d1c27] text-[#9bb6bd] border border-[#1d3c4a] hover:text-[#e6f7fb]'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>

              {/* Skills Grid */}
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {filteredSkills.map((skill, i) => (
                  <motion.div
                    key={skill.id}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: i * 0.03 }}
                    className="group p-5 rounded-xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60 hover:border-[#00d4ff]/30 transition-all"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div
                        className="w-12 h-12 rounded-xl flex items-center justify-center"
                        style={{ backgroundColor: `${skill.color}15` }}
                      >
                        <i className={`${skill.icon} text-xl`} style={{ color: skill.color }}></i>
                      </div>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[#1d3c4a]/40 text-[#9bb6bd] uppercase">
                        {skill.type}
                      </span>
                    </div>
                    <h3 className="font-bold text-[#e6f7fb] mb-1">{skill.name}</h3>
                    <p className="text-xs text-[#9bb6bd] mb-3 leading-relaxed">{skill.description}</p>
                    <div className="flex items-center justify-between text-xs text-[#9bb6bd] mb-3">
                      <span><i className="fas fa-user mr-1"></i>{skill.author}</span>
                      <span><i className="fas fa-download mr-1"></i>{skill.downloads}</span>
                    </div>
                    <button
                      onClick={() => toggleInstall(skill.id)}
                      className={`w-full py-2 rounded-lg text-xs font-medium transition-all ${
                        skill.installed
                          ? 'bg-[#7ef0c1]/10 border border-[#7ef0c1]/30 text-[#7ef0c1] hover:bg-red-500/10 hover:border-red-500/30 hover:text-red-400'
                          : 'bg-[#00d4ff]/10 border border-[#00d4ff]/30 text-[#00d4ff] hover:bg-[#00d4ff]/20'
                      }`}
                    >
                      {skill.installed ? (
                        <><i className="fas fa-check mr-1"></i>Installed · Click to Remove</>
                      ) : (
                        <><i className="fas fa-download mr-1"></i>Install</>
                      )}
                    </button>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Upload Tab */}
          {activeTab === 'upload' && (
            <motion.div
              key="upload"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid md:grid-cols-2 gap-4 mb-6">
                {uploadTypes.map((type) => (
                  <motion.div
                    key={type.id}
                    onDragOver={(e) => { e.preventDefault(); setDragOver(type.id); }}
                    onDragLeave={() => setDragOver(null)}
                    onDrop={(e) => { e.preventDefault(); handleDrop(type.id); }}
                    className={`relative p-6 rounded-2xl border-2 border-dashed transition-all cursor-pointer ${
                      dragOver === type.id
                        ? 'border-[#00d4ff] bg-[#00d4ff]/5'
                        : 'border-[#1d3c4a] bg-[#0d1c27]/60 hover:border-[#00d4ff]/50'
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <div
                        className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                        style={{ backgroundColor: `${type.color}15` }}
                      >
                        <i className={`${type.icon} text-xl`} style={{ color: type.color }}></i>
                      </div>
                      <div className="flex-1">
                        <h3 className="font-bold text-[#e6f7fb] mb-1">{type.title}</h3>
                        <p className="text-xs text-[#9bb6bd] mb-3">{type.description}</p>
                        <div className="flex items-center gap-2 text-xs text-[#9bb6bd]">
                          <i className="fas fa-cloud-upload-alt" style={{ color: type.color }}></i>
                          <span>Drop files here or click to browse</span>
                        </div>
                        <div className="mt-2 text-[10px] font-mono text-[#1d3c4a]">
                          Accepts: {type.accept}
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Upload Queue */}
              {uploadedFiles.length > 0 && (
                <div className="p-5 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60">
                  <h3 className="text-sm font-bold mb-3 flex items-center gap-2">
                    <i className="fas fa-list text-[#00d4ff]"></i>
                    Upload Queue
                  </h3>
                  <div className="space-y-2">
                    {uploadedFiles.map((file, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="flex items-center justify-between p-3 rounded-lg bg-[#071018] border border-[#1d3c4a]/40"
                      >
                        <div className="flex items-center gap-3">
                          <i className="fas fa-file-code text-[#7ef0c1]"></i>
                          <span className="text-sm font-mono text-[#e6f7fb]">{file.name}</span>
                        </div>
                        <span className={`text-xs font-mono ${
                          file.status === 'installed' ? 'text-[#7ef0c1]' : 'text-[#fbbf24]'
                        }`}>
                          {file.status === 'installed' ? (
                            <><i className="fas fa-check-circle mr-1"></i>Installed</>
                          ) : (
                            <><i className="fas fa-spinner fa-spin mr-1"></i>Installing...</>
                          )}
                        </span>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {/* Auto-Discovery Info */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="mt-6 p-5 rounded-2xl bg-gradient-to-r from-[#00d4ff]/5 to-[#7ef0c1]/5 border border-[#00d4ff]/20"
              >
                <div className="flex items-start gap-3">
                  <i className="fas fa-magic text-[#00d4ff] mt-1"></i>
                  <div>
                    <h4 className="font-bold text-[#e6f7fb] mb-1">Auto-Discovery Engine</h4>
                    <p className="text-sm text-[#9bb6bd] leading-relaxed">
                      JARVIS automatically scans uploaded files, extracts function signatures and docstrings, 
                      then registers them as tools. No manual configuration needed — just drop the file and start using it.
                    </p>
                    <div className="mt-3 flex flex-wrap gap-2 text-xs">
                      {['Function parsing', 'Docstring extraction', 'Auto-registration', 'Type validation', 'Dependency check'].map((feat, i) => (
                        <span key={i} className="px-2 py-1 rounded-md bg-[#071018] border border-[#1d3c4a] text-[#7ef0c1]">
                          {feat}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}

          {/* Installed Tab */}
          {activeTab === 'installed' && (
            <motion.div
              key="installed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {skills.filter(s => s.installed).map((skill, i) => (
                  <motion.div
                    key={skill.id}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: i * 0.05 }}
                    className="p-5 rounded-xl bg-[#0d1c27]/80 border border-[#7ef0c1]/20"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div
                          className="w-10 h-10 rounded-lg flex items-center justify-center"
                          style={{ backgroundColor: `${skill.color}15` }}
                        >
                          <i className={skill.icon} style={{ color: skill.color }}></i>
                        </div>
                        <div>
                          <h3 className="font-bold text-[#e6f7fb] text-sm">{skill.name}</h3>
                          <span className="text-xs text-[#7ef0c1]">● Active</span>
                        </div>
                      </div>
                    </div>
                    <p className="text-xs text-[#9bb6bd] mb-3">{skill.description}</p>
                    <div className="flex gap-2">
                      <button className="flex-1 py-1.5 rounded-lg bg-[#1d3c4a]/40 text-xs text-[#9bb6bd] hover:text-[#e6f7fb] transition-colors">
                        <i className="fas fa-cog mr-1"></i>Configure
                      </button>
                      <button
                        onClick={() => toggleInstall(skill.id)}
                        className="flex-1 py-1.5 rounded-lg bg-red-500/10 text-xs text-red-400 hover:bg-red-500/20 transition-colors"
                      >
                        <i className="fas fa-trash mr-1"></i>Remove
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
              {skills.filter(s => s.installed).length === 0 && (
                <div className="text-center py-16 text-[#9bb6bd]">
                  <i className="fas fa-box-open text-4xl mb-4 text-[#1d3c4a]"></i>
                  <p>No skills installed yet. Visit the Marketplace to get started.</p>
                </div>
              )}
            </motion.div>
          )}

          {/* Visual Builder Tab */}
          {activeTab === 'builder' && (
            <motion.div
              key="builder"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid lg:grid-cols-2 gap-6">
                {/* Builder Interface */}
                <div className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <i className="fas fa-wand-magic-sparkles text-[#7ef0c1]"></i>
                    Visual Skill Builder
                  </h3>
                  <p className="text-sm text-[#9bb6bd] mb-6">
                    Create custom skills without writing a single line of code. Define triggers, actions, and responses visually.
                  </p>

                  <div className="space-y-4">
                    <div>
                      <label className="text-xs font-mono text-[#9bb6bd] mb-2 block">SKILL NAME</label>
                      <input
                        type="text"
                        defaultValue="Morning Routine"
                        className="w-full px-3 py-2 rounded-lg bg-[#071018] border border-[#1d3c4a] text-sm text-[#e6f7fb] focus:outline-none focus:border-[#00d4ff]/50"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-mono text-[#9bb6bd] mb-2 block">VOICE TRIGGER</label>
                      <input
                        type="text"
                        defaultValue='"start my morning" / "good morning routine"'
                        className="w-full px-3 py-2 rounded-lg bg-[#071018] border border-[#1d3c4a] text-sm text-[#7ef0c1] font-mono focus:outline-none focus:border-[#00d4ff]/50"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-mono text-[#9bb6bd] mb-2 block">ACTIONS (drag to reorder)</label>
                      <div className="space-y-2">
                        {[
                          { icon: 'fas fa-lightbulb', label: 'Turn on bedroom lights to 50%', color: '#fbbf24' },
                          { icon: 'fas fa-coffee', label: 'Start coffee machine', color: '#7ef0c1' },
                          { icon: 'fas fa-newspaper', label: 'Read today\'s headlines', color: '#00d4ff' },
                          { icon: 'fas fa-calendar', label: 'Summarize today\'s calendar', color: '#f87171' },
                        ].map((action, i) => (
                          <motion.div
                            key={i}
                            drag
                            dragConstraints={{ top: 0, bottom: 0, left: 0, right: 0 }}
                            className="flex items-center gap-3 p-3 rounded-lg bg-[#071018] border border-[#1d3c4a] cursor-grab active:cursor-grabbing"
                          >
                            <i className="fas fa-grip-vertical text-[#1d3c4a]"></i>
                            <i className={action.icon} style={{ color: action.color }}></i>
                            <span className="text-sm text-[#e6f7fb] flex-1">{action.label}</span>
                            <span className="text-xs text-[#1d3c4a]">#{i + 1}</span>
                          </motion.div>
                        ))}
                        <button className="w-full py-2 rounded-lg border border-dashed border-[#1d3c4a] text-xs text-[#9bb6bd] hover:border-[#00d4ff]/50 hover:text-[#00d4ff] transition-all">
                          <i className="fas fa-plus mr-1"></i>Add Action
                        </button>
                      </div>
                    </div>

                    <button className="w-full py-3 rounded-xl bg-gradient-to-r from-[#00d4ff] to-[#7ef0c1] text-[#00141b] font-bold hover:opacity-90 transition-opacity">
                      <i className="fas fa-save mr-2"></i>Save Skill
                    </button>
                  </div>
                </div>

                {/* Preview / Generated Code */}
                <div className="space-y-4">
                  <div className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60">
                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                      <i className="fas fa-eye text-[#00d4ff]"></i>
                      Live Preview
                    </h3>
                    <div className="p-4 rounded-xl bg-[#071018] border border-[#1d3c4a]">
                      <div className="flex items-center gap-2 mb-3 text-xs text-[#9bb6bd]">
                        <i className="fas fa-microphone text-[#7ef0c1]"></i>
                        <span>You:</span>
                        <span className="text-[#e6f7fb]">"Start my morning"</span>
                      </div>
                      <div className="space-y-2 pl-4 border-l-2 border-[#00d4ff]/30">
                        {[
                          'Turning on bedroom lights to 50%...',
                          'Starting coffee machine...',
                          'Here are today\'s headlines...',
                          'You have 3 meetings today...',
                        ].map((line, i) => (
                          <motion.div
                            key={i}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.3 }}
                            className="text-xs text-[#7ef0c1] font-mono flex items-center gap-2"
                          >
                            <i className="fas fa-check-circle text-[10px]"></i>
                            {line}
                          </motion.div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60">
                    <h3 className="text-sm font-bold mb-3 flex items-center gap-2">
                      <i className="fas fa-code text-[#7ef0c1]"></i>
                      Auto-Generated Code
                      <span className="ml-auto text-[10px] font-mono text-[#9bb6bd]">morning_routine.py</span>
                    </h3>
                    <pre className="p-3 rounded-lg bg-[#071018] border border-[#1d3c4a] text-xs font-mono text-[#7ef0c1] overflow-x-auto leading-relaxed">
{`def morning_routine():
    """Start my morning — voice-triggered routine."""
    smart_home.set_brightness("bedroom", 50)
    smart_home.turn_on("coffee_machine")
    news = web_search(mode="news",
                      query="top headlines today")
    calendar = calendar_sync.get_today()
    return f"""Good morning! Here's your day:
    {news.summary}
    You have {len(calendar)} meetings."""`}
                    </pre>
                    <p className="text-xs text-[#9bb6bd] mt-3">
                      <i className="fas fa-info-circle text-[#00d4ff] mr-1"></i>
                      This code is auto-generated from your visual builder. No coding required.
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Bottom Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          {[
            { label: 'Community Skills', value: '240+', icon: 'fas fa-puzzle-piece', color: '#00d4ff' },
            { label: 'Active Users', value: '18.5k', icon: 'fas fa-users', color: '#7ef0c1' },
            { label: 'Auto-Discovery', value: 'Instant', icon: 'fas fa-bolt', color: '#fbbf24' },
            { label: 'Zero Code', value: '100%', icon: 'fas fa-magic', color: '#f87171' },
          ].map((stat, i) => (
            <div key={i} className="p-4 rounded-xl bg-[#0d1c27]/60 border border-[#1d3c4a]/60 text-center">
              <i className={`${stat.icon} text-xl mb-2`} style={{ color: stat.color }}></i>
              <div className="text-2xl font-bold text-[#e6f7fb]">{stat.value}</div>
              <div className="text-xs text-[#9bb6bd]">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
