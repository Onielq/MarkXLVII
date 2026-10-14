// Global type declarations for custom elements
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'voice-orb': React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          state?: 'idle' | 'listening' | 'thinking' | 'speaking';
          particles?: number;
          recording?: boolean;
        },
        HTMLElement
      >;
    }
  }
}

export {};
