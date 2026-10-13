import { motion } from 'framer-motion';
import { useState } from 'react';

export default function BugFixes() {
  const [activeFix, setActiveFix] = useState<'search' | 'files'>('search');

  return (
    <section id="fixes" className="relative py-24 px-6">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_50%,rgba(248,113,113,0.03)_0%,transparent_50%)]" />
      
      <div className="relative max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <span className="text-red-400 font-mono text-sm tracking-widest uppercase">
            Critical Fixes Applied
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold mt-4 mb-6">
            Bugs{' '}
            <span className="bg-gradient-to-r from-red-400 to-[#7ef0c1] bg-clip-text text-transparent">
              Squashed
            </span>
          </h2>
          <p className="text-[#9bb6bd] text-lg max-w-2xl mx-auto">
            Fixed critical issues with web search and file processing. JARVIS now handles factual queries 
            and can read any file type including archives.
          </p>
        </motion.div>

        {/* Fix Toggle */}
        <div className="flex justify-center gap-3 mb-8">
          <button
            onClick={() => setActiveFix('search')}
            className={`px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 ${
              activeFix === 'search'
                ? 'bg-gradient-to-r from-[#00d4ff]/20 to-[#7ef0c1]/20 border border-[#00d4ff]/50 text-[#e6f7fb]'
                : 'bg-[#0d1c27] border border-[#1d3c4a] text-[#9bb6bd] hover:text-[#e6f7fb]'
            }`}
          >
            <i className="fas fa-search text-[#00d4ff]"></i>
            Web Search Fix
          </button>
          <button
            onClick={() => setActiveFix('files')}
            className={`px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 ${
              activeFix === 'files'
                ? 'bg-gradient-to-r from-[#00d4ff]/20 to-[#7ef0c1]/20 border border-[#00d4ff]/50 text-[#e6f7fb]'
                : 'bg-[#0d1c27] border border-[#1d3c4a] text-[#9bb6bd] hover:text-[#e6f7fb]'
            }`}
          >
            <i className="fas fa-file-archive text-[#7ef0c1]"></i>
            File Processing Fix
          </button>
        </div>

        {/* Web Search Fix */}
        {activeFix === 'search' && (
          <motion.div
            key="search"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="space-y-6"
          >
            {/* Problem */}
            <div className="p-6 rounded-2xl bg-red-500/5 border border-red-500/20">
              <h3 className="text-lg font-bold mb-3 flex items-center gap-2 text-red-400">
                <i className="fas fa-exclamation-triangle"></i>
                Problem: Limited Search Ability
              </h3>
              <div className="bg-[#071018] rounded-lg p-4 mb-3">
                <div className="text-xs font-mono text-[#9bb6bd] mb-2">User:</div>
                <div className="text-sm text-[#e6f7fb]">"Who is the president in East Africa?"</div>
              </div>
              <div className="bg-[#071018] rounded-lg p-4">
                <div className="text-xs font-mono text-red-400 mb-2">Jarvis (BEFORE):</div>
                <div className="text-sm text-red-300">
                  "I seem to be unable to retrieve that information at this time, sir."
                </div>
              </div>
              <p className="text-sm text-[#9bb6bd] mt-3">
                <strong>Cause:</strong> When Gemini API fails (quota/rate limit), DDG fallback wasn't robust enough 
                for factual queries. No third fallback existed.
              </p>
            </div>

            {/* Solution */}
            <div className="p-6 rounded-2xl bg-[#7ef0c1]/5 border border-[#7ef0c1]/20">
              <h3 className="text-lg font-bold mb-3 flex items-center gap-2 text-[#7ef0c1]">
                <i className="fas fa-check-circle"></i>
                Solution: Triple Fallback Chain
              </h3>
              <div className="grid md:grid-cols-3 gap-4 mb-4">
                {[
                  { step: 1, name: 'Gemini Grounded Search', desc: 'Primary: Google-powered factual answers', color: '#00d4ff' },
                  { step: 2, name: 'DuckDuckGo + Query Enhancement', desc: 'Smart query improvement for facts', color: '#7ef0c1' },
                  { step: 3, name: 'Wikipedia API', desc: 'Final fallback for encyclopedic knowledge', color: '#fbbf24' },
                ].map((item, i) => (
                  <div key={i} className="p-4 rounded-xl bg-[#071018] border border-[#1d3c4a]">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold" 
                            style={{ backgroundColor: `${item.color}20`, color: item.color }}>
                        {item.step}
                      </span>
                      <span className="text-sm font-bold text-[#e6f7fb]">{item.name}</span>
                    </div>
                    <p className="text-xs text-[#9bb6bd]">{item.desc}</p>
                  </div>
                ))}
              </div>
              
              <div className="bg-[#071018] rounded-lg p-4">
                <div className="text-xs font-mono text-[#7ef0c1] mb-2">Jarvis (AFTER):</div>
                <div className="text-sm text-[#e6f7fb]">
                  "The current presidents of East African countries include: William Ruto (Kenya), 
                  Samia Suluhu Hassan (Tanzania), Yoweri Museveni (Uganda), and others. 
                  Would you like details about a specific country?"
                </div>
              </div>
            </div>

            {/* Key Improvements */}
            <div className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <i className="fas fa-bolt text-[#fbbf24]"></i>
                Key Improvements
              </h3>
              <ul className="space-y-2 text-sm text-[#9bb6bd]">
                {[
                  'Added Wikipedia API as third fallback for factual queries',
                  'Smart query enhancement: detects factual keywords (who, what, president, etc.)',
                  'Auto-adds "current" to time-sensitive queries',
                  'Better error handling and graceful degradation',
                  'Works even when all APIs are down (returns helpful message)',
                ].map((item, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <i className="fas fa-check text-[#7ef0c1] mt-1 text-xs"></i>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}

        {/* File Processing Fix */}
        {activeFix === 'files' && (
          <motion.div
            key="files"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="space-y-6"
          >
            {/* Problem */}
            <div className="p-6 rounded-2xl bg-red-500/5 border border-red-500/20">
              <h3 className="text-lg font-bold mb-3 flex items-center gap-2 text-red-400">
                <i className="fas fa-exclamation-triangle"></i>
                Problem: Can't Read Zip Files
              </h3>
              <div className="bg-[#071018] rounded-lg p-4 mb-3">
                <div className="text-xs font-mono text-[#9bb6bd] mb-2">User:</div>
                <div className="text-sm text-[#e6f7fb]">"Read the contents of project.zip"</div>
              </div>
              <div className="bg-[#071018] rounded-lg p-4">
                <div className="text-xs font-mono text-red-400 mb-2">Jarvis (BEFORE):</div>
                <div className="text-sm text-red-300">
                  "Archive contains 15 files: readme.txt, main.py, config.json... 
                  [Only lists files, can't read contents]"
                </div>
              </div>
              <p className="text-sm text-[#9bb6bd] mt-3">
                <strong>Cause:</strong> Archive support only had "list" and "extract" actions. 
                No way to read file contents without extracting first.
              </p>
            </div>

            {/* Solution */}
            <div className="p-6 rounded-2xl bg-[#7ef0c1]/5 border border-[#7ef0c1]/20">
              <h3 className="text-lg font-bold mb-3 flex items-center gap-2 text-[#7ef0c1]">
                <i className="fas fa-check-circle"></i>
                Solution: Full Archive Content Reading
              </h3>
              <div className="grid md:grid-cols-2 gap-4 mb-4">
                {[
                  { icon: 'fas fa-eye', title: 'Read Individual Files', desc: 'Read any text file inside zip/tar/rar/7z without extracting', color: '#00d4ff' },
                  { icon: 'fas fa-search', title: 'Search Inside Archives', desc: 'Find text across all files in an archive', color: '#7ef0c1' },
                  { icon: 'fas fa-book-open', title: 'Read All Text Files', desc: 'Batch read all text files in one command', color: '#fbbf24' },
                  { icon: 'fas fa-brain', title: 'AI Summarize Archive', desc: 'Gemini summarizes contents of entire archive', color: '#f87171' },
                ].map((item, i) => (
                  <div key={i} className="p-4 rounded-xl bg-[#071018] border border-[#1d3c4a]">
                    <div className="flex items-center gap-2 mb-2">
                      <i className={item.icon} style={{ color: item.color }}></i>
                      <span className="text-sm font-bold text-[#e6f7fb]">{item.title}</span>
                    </div>
                    <p className="text-xs text-[#9bb6bd]">{item.desc}</p>
                  </div>
                ))}
              </div>

              <div className="bg-[#071018] rounded-lg p-4 mb-3">
                <div className="text-xs font-mono text-[#9bb6bd] mb-2">User:</div>
                <div className="text-sm text-[#e6f7fb]">"Read readme.txt from project.zip"</div>
              </div>
              <div className="bg-[#071018] rounded-lg p-4">
                <div className="text-xs font-mono text-[#7ef0c1] mb-2">Jarvis (AFTER):</div>
                <div className="text-sm text-[#e6f7fb] font-mono">
                  📄 readme.txt<br/><br/>
                  # Project Mark XLVIII<br/>
                  A cross-platform AI assistant...<br/>
                  [Full file content displayed]
                </div>
              </div>
            </div>

            {/* Supported Formats */}
            <div className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <i className="fas fa-file-archive text-[#00d4ff]"></i>
                Supported Archive Formats
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { ext: '.zip', libs: 'Built-in', color: '#00d4ff' },
                  { ext: '.tar.gz', libs: 'Built-in', color: '#7ef0c1' },
                  { ext: '.rar', libs: 'pip install rarfile', color: '#fbbf24' },
                  { ext: '.7z', libs: 'pip install py7zr', color: '#f87171' },
                ].map((fmt, i) => (
                  <div key={i} className="p-3 rounded-lg bg-[#071018] border border-[#1d3c4a]">
                    <div className="text-sm font-mono font-bold mb-1" style={{ color: fmt.color }}>
                      {fmt.ext}
                    </div>
                    <div className="text-xs text-[#9bb6bd]">{fmt.libs}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* New Commands */}
            <div className="p-6 rounded-2xl bg-[#0d1c27]/80 border border-[#1d3c4a]/60">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <i className="fas fa-terminal text-[#7ef0c1]"></i>
                New Voice Commands
              </h3>
              <div className="space-y-2">
                {[
                  { cmd: '"List files in backup.zip"', desc: 'Shows all files with sizes and types' },
                  { cmd: '"Read config.json from project.zip"', desc: 'Reads specific file without extracting' },
                  { cmd: '"Search for API_KEY in my_project.zip"', desc: 'Finds text across all files' },
                  { cmd: '"Summarize what\'s in this archive"', desc: 'AI-powered archive summary' },
                  { cmd: '"Extract main.py from code.zip"', desc: 'Extract single file only' },
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-[#071018] border border-[#1d3c4a]/40">
                    <i className="fas fa-microphone text-[#7ef0c1] mt-0.5"></i>
                    <div className="flex-1">
                      <div className="text-sm text-[#e6f7fb] font-medium">{item.cmd}</div>
                      <div className="text-xs text-[#9bb6bd]">{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {/* Download Fixed Files */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-12 p-6 rounded-2xl bg-gradient-to-r from-[#00d4ff]/10 to-[#7ef0c1]/10 border border-[#00d4ff]/30"
        >
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <i className="fas fa-download text-[#00d4ff]"></i>
            Apply the Fixes
          </h3>
          <p className="text-sm text-[#9bb6bd] mb-4">
            Download the fixed files and replace the originals in your Mark XLVIII installation:
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <a
              href="/fixed_web_search.py"
              download
              className="flex items-center gap-3 p-4 rounded-xl bg-[#0d1c27] border border-[#1d3c4a] hover:border-[#00d4ff]/50 transition-all"
            >
              <i className="fab fa-python text-2xl text-[#00d4ff]"></i>
              <div>
                <div className="font-bold text-[#e6f7fb]">fixed_web_search.py</div>
                <div className="text-xs text-[#9bb6bd]">Replace actions/web_search.py</div>
              </div>
              <i className="fas fa-download ml-auto text-[#9bb6bd]"></i>
            </a>
            <a
              href="/fixed_file_processor.py"
              download
              className="flex items-center gap-3 p-4 rounded-xl bg-[#0d1c27] border border-[#1d3c4a] hover:border-[#00d4ff]/50 transition-all"
            >
              <i className="fab fa-python text-2xl text-[#7ef0c1]"></i>
              <div>
                <div className="font-bold text-[#e6f7fb]">fixed_file_processor.py</div>
                <div className="text-xs text-[#9bb6bd]">Replace actions/file_processor.py</div>
              </div>
              <i className="fas fa-download ml-auto text-[#9bb6bd]"></i>
            </a>
          </div>
          <div className="mt-4 p-3 rounded-lg bg-[#071018] border border-[#1d3c4a]">
            <div className="text-xs font-mono text-[#9bb6bd] mb-1">Installation:</div>
            <code className="text-xs font-mono text-[#7ef0c1]">
              # Backup originals, then replace:<br/>
              mv actions/web_search.py actions/web_search.py.backup<br/>
              mv fixed_web_search.py actions/web_search.py<br/>
              mv actions/file_processor.py actions/file_processor.py.backup<br/>
              mv fixed_file_processor.py actions/file_processor.py
            </code>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
