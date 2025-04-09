import { useEffect } from 'react';

export default function DebugInitializer() {
  useEffect(() => {
    // Import debug utilities only on client side
    import('../utils/browser').then(() => {
      console.log('✨ Debug utilities loaded');
    });
  }, []);

  return null;
}
