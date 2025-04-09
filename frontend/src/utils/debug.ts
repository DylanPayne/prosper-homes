type LogLevel = 'error' | 'warn' | 'info' | 'debug';

interface DebugConfig {
  enabled: boolean;
  level: LogLevel;
  modules: {
    [key: string]: boolean;
  };
}

// Default configuration
const config: DebugConfig = {
  enabled: true,
  level: 'debug',
  modules: {
    places: true,
    form: true,
    api: true,
    debug: true
  }
};

const LOG_LEVELS: { [key in LogLevel]: number } = {
  error: 0,
  warn: 1,
  info: 2,
  debug: 3
};

let isInitialized = false;

export const debug = {
  init: () => {
    if (isInitialized) return;
    
    console.log('%c🔍 Debug Utility Initializing...', 'color: #4CAF50; font-weight: bold; font-size: 14px;');
    console.log('%cCurrent configuration:', 'color: #2196F3; font-weight: bold;', config);
    console.log('%cTo control debugging, use these commands in console:', 'color: #2196F3;');
    console.log('%c  DEBUG.configure({ level: "debug" | "info" | "warn" | "error" })', 'color: #666;');
    console.log('%c  DEBUG.enableModule("places")', 'color: #666;');
    console.log('%c  DEBUG.disableModule("places")', 'color: #666;');
    console.log('%c  DEBUG.configure({ enabled: false })', 'color: #666;');
    
    isInitialized = true;
    debug.info('debug', 'Debug utility initialized');
  },

  // Configure debug settings
  configure: (newConfig: Partial<DebugConfig>) => {
    Object.assign(config, newConfig);
    console.log('%cDebug configuration updated:', 'color: #2196F3; font-weight: bold;', config);
  },

  // Enable/disable specific modules
  enableModule: (module: string) => {
    config.modules[module] = true;
    console.log(`%cModule "${module}" enabled`, 'color: #4CAF50; font-weight: bold;');
  },

  disableModule: (module: string) => {
    config.modules[module] = false;
    console.log(`%cModule "${module}" disabled`, 'color: #F44336; font-weight: bold;');
  },

  // Get current configuration
  getConfig: () => ({ ...config }),

  // Main logging function
  log: (module: string, level: LogLevel, ...args: any[]) => {
    if (!config.enabled || !config.modules[module]) return;
    if (LOG_LEVELS[level] > LOG_LEVELS[config.level]) return;

    const timestamp = new Date().toLocaleTimeString();
    const prefix = `[${timestamp}] [${module.toUpperCase()}] [${level.toUpperCase()}]`;
    
    const style = 'color: #666; font-weight: bold;';
    const resetStyle = 'color: inherit; font-weight: normal;';

    switch (level) {
      case 'error':
        console.error(`%c${prefix}%c`, style, resetStyle, ...args);
        break;
      case 'warn':
        console.warn(`%c${prefix}%c`, style, resetStyle, ...args);
        break;
      case 'info':
        console.info(`%c${prefix}%c`, style, resetStyle, ...args);
        break;
      case 'debug':
        console.debug(`%c${prefix}%c`, style, resetStyle, ...args);
        break;
    }
  },

  // Convenience methods
  error: (module: string, ...args: any[]) => debug.log(module, 'error', ...args),
  warn: (module: string, ...args: any[]) => debug.log(module, 'warn', ...args),
  info: (module: string, ...args: any[]) => debug.log(module, 'info', ...args),
  debug: (module: string, ...args: any[]) => debug.log(module, 'debug', ...args),
};

// Log initial configuration
if (typeof window !== 'undefined') {
  debug.init();
}
