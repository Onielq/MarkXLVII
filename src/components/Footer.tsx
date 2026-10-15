import { motion } from 'framer-motion';

export default function Footer() {
  return (
    <footer className="relative border-t border-[#1d3c4a]/40 py-12 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#00d4ff] to-[#7ef0c1] flex items-center justify-center">
                <span className="text-[#00141b] font-bold text-sm">M</span>
              </div>
              <span className="font-bold text-lg">
                Mark <span className="text-[#00d4ff]">XLVIII</span>
              </span>
            </div>
            <p className="text-sm text-[#9bb6bd] max-w-xs">
              A cross-platform, real-time voice AI assistant built on the Gemini Live API.
              Personal and non-commercial use.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-semibold text-[#e6f7fb] mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-[#9bb6bd]">
              <li>
                <a href="https://github.com/Onielq/Mark-XLVII" target="_blank" rel="noopener noreferrer" className="hover:text-[#00d4ff] transition-colors flex items-center gap-2">
                  <i className="fab fa-github text-xs"></i> GitHub Repository
                </a>
              </li>
              <li>
                <a href="https://github.com/Onielq/Mark-XLVII/blob/main/REMOTE_SETUP.md" target="_blank" rel="noopener noreferrer" className="hover:text-[#00d4ff] transition-colors flex items-center gap-2">
                  <i className="fas fa-book text-xs"></i> Remote Setup Guide
                </a>
              </li>
              <li>
                <a href="https://aistudio.google.com" target="_blank" rel="noopener noreferrer" className="hover:text-[#00d4ff] transition-colors flex items-center gap-2">
                  <i className="fas fa-key text-xs"></i> Get Gemini API Key
                </a>
              </li>
            </ul>
          </div>

          {/* Creator */}
          <div>
            <h4 className="font-semibold text-[#e6f7fb] mb-4">Creator</h4>
            <p className="text-sm text-[#9bb6bd] mb-3">
              Engineered by Hasan — building a real-world JARVIS-style assistant.
            </p>
            <div className="flex items-center gap-3">
              <a href="https://github.com/lumendev8" target="_blank" rel="noopener noreferrer" className="w-8 h-8 rounded-lg bg-[#0d1c27] border border-[#1d3c4a] flex items-center justify-center hover:border-[#00d4ff]/50 transition-colors">
                <i className="fab fa-github text-sm text-[#9bb6bd] hover:text-[#00d4ff]"></i>
              </a>
              <a href="https://x.com/lumendev8" target="_blank" rel="noopener noreferrer" className="w-8 h-8 rounded-lg bg-[#0d1c27] border border-[#1d3c4a] flex items-center justify-center hover:border-[#00d4ff]/50 transition-colors">
                <i className="fab fa-x-twitter text-sm text-[#9bb6bd] hover:text-[#00d4ff]"></i>
              </a>
              <a href="https://www.linkedin.com/company/lumendev8" target="_blank" rel="noopener noreferrer" className="w-8 h-8 rounded-lg bg-[#0d1c27] border border-[#1d3c4a] flex items-center justify-center hover:border-[#00d4ff]/50 transition-colors">
                <i className="fab fa-linkedin text-sm text-[#9bb6bd] hover:text-[#00d4ff]"></i>
              </a>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-[#1d3c4a]/40 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-[#9bb6bd]">
            © 2026 Mark XLVIII. Licensed under{' '}
            <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noopener noreferrer" className="text-[#00d4ff] hover:underline">
              CC BY-NC 4.0
            </a>
            . Personal and non-commercial use only.
          </p>
          <div className="flex items-center gap-2 text-xs text-[#1d3c4a]">
            <i className="fas fa-shield-alt text-[#7ef0c1]/50"></i>
            <span>Configure your Gemini API key locally; never commit it to GitHub.</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
