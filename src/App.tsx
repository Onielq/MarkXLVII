import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Hero from './components/Hero';
import Features from './components/Features';
import Architecture from './components/Architecture';
import Dashboard from './components/Dashboard';
import UseCases from './components/UseCases';
import ExtensionHub from './components/ExtensionHub';
import Setup from './components/Setup';
import Footer from './components/Footer';
import Navbar from './components/Navbar';
import ParticleBackground from './components/ParticleBackground';

function App() {
  const [activeSection, setActiveSection] = useState('home');
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
      const sections = ['home', 'features', 'architecture', 'dashboard', 'usecases', 'extensions', 'setup'];
      for (const section of sections) {
        const el = document.getElementById(section);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 150 && rect.bottom >= 150) {
            setActiveSection(section);
            break;
          }
        }
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="relative min-h-screen bg-[#071018] text-[#e6f7fb] overflow-x-hidden">
      <ParticleBackground />
      <Navbar activeSection={activeSection} scrollY={scrollY} />
      <main>
        <Hero />
        <Features />
        <Architecture />
        <Dashboard />
        <UseCases />
        <ExtensionHub />
        <Setup />
      </main>
      <Footer />
    </div>
  );
}

export default App;
