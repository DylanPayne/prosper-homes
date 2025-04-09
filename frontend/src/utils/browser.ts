import { debug } from './debug';

declare global {
  interface Window {
    DEBUG: typeof debug;
  }
}

function initializeDebug() {
  // Only run in browser environment
  if (typeof window === 'undefined') return;

  // Only initialize once
  if (window.DEBUG) return;

  console.log('🚀 Initializing debug utility in browser...');
  window.DEBUG = debug;
  debug.init();
}

// Wait for the browser environment to be ready
if (typeof window !== 'undefined') {
  // Try on script load
  initializeDebug();
  
  // Also try on window load
  window.addEventListener('load', initializeDebug);
  
  // And try on DOM content loaded
  document.addEventListener('DOMContentLoaded', initializeDebug);
}

export {};
