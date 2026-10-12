import { motion } from 'framer-motion';

interface NavbarProps {
  activeSection: string;
  scrollY: number;
}

const navItems = [
  { id: 'home', label: 'Home' },
  { id: 'features', label: 'Features' },
  { id: 'architecture', label: 'Architecture' },
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'usecases', label: 'Use Cases' },
  { id: 'extensions', label: 'Extensions' },
  { id: 'setup', label: 'Setup' },
];

export default function Navbar({ activeSection, scrollY }: NavbarProps) {
  const isScrolled = scrollY > 50;

  const scrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'bg-[#071018]/90 backdrop-blur-xl border-b border-[#1d3c4a]/50'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#00d4ff] to-[#7ef0c1] flex items-center justify-center">
            <span className="text-[#00141b] font-bold text-sm">M</span>
          </div>
          <span className="font-bold text-lg tracking-tight">
            Mark <span className="text-[#00d4ff]">XLVIII</span>
          </span>
        </div>

        <div className="hidden md:flex items-center gap-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => scrollTo(item.id)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeSection === item.id
                  ? 'text-[#00d4ff] bg-[#00d4ff]/10'
                  : 'text-[#9bb6bd] hover:text-[#e6f7fb] hover:bg-white/5'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        <a
          href="https://github.com/Onielq/Mark-XLVII"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#0d1c27] border border-[#1d3c4a] hover:border-[#00d4ff]/50 transition-all text-sm"
        >
          <i className="fab fa-github text-lg"></i>
          <span className="hidden sm:inline">GitHub</span>
        </a>
      </div>
    </motion.nav>
  );
}
