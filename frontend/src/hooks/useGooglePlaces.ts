import { useState, useEffect } from 'react';

export const useGooglePlaces = (options?: { onLoad?: () => void }) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('🔍 useGooglePlaces hook running...');

    // If the script is already loaded
    if (window.google?.maps?.places) {
      console.log('✅ Google Places already loaded');
      setIsLoaded(true);
      options?.onLoad?.();
      return;
    }

    const script = document.createElement('script');
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY;
    
    if (!apiKey) {
      const errorMsg = '❌ No Google Places API key found! Please check your .env.local file.';
      console.error(errorMsg);
      setError(errorMsg);
      return;
    }

    console.log('📝 Creating Google Places script...');
    // Only load the Places library to minimize API usage
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&v=weekly`;
    script.async = true;
    script.defer = true;

    // Add error event listener to window for Google Maps errors
    const handleGoogleMapsError = (event: ErrorEvent) => {
      if (event.message.includes('Google Maps JavaScript API error')) {
        const errorMsg = `❌ Google Maps API Error: ${event.error?.message || event.message}`;
        console.error(errorMsg);
        setError(errorMsg);
      }
    };
    window.addEventListener('error', handleGoogleMapsError);

    const handleScriptLoad = () => {
      console.log('✅ Google Places script loaded');
      if (window.google?.maps?.places) {
        setIsLoaded(true);
        setError(null);
        options?.onLoad?.();
      } else {
        const errorMsg = '❌ Google Places not available after script load';
        console.error(errorMsg);
        setError(errorMsg);
      }
    };

    script.addEventListener('load', handleScriptLoad);
    script.addEventListener('error', (event) => {
      const errorMsg = '❌ Error loading Google Places script';
      console.error(errorMsg, event);
      setError(errorMsg);
    });

    console.log('🚀 Injecting Google Places script...');
    document.body.appendChild(script);

    return () => {
      console.log('🧹 Cleaning up Google Places script');
      window.removeEventListener('error', handleGoogleMapsError);
      script.removeEventListener('load', handleScriptLoad);
      if (script.parentNode) {
        script.parentNode.removeChild(script);
      }
    };
  }, [options]);

  return { isLoaded, error };
};
