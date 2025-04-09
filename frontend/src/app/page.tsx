'use client';

import dynamic from 'next/dynamic';
import MultiStepForm from '@/components/MultiStepForm';
import { useState, useEffect } from 'react';

const Script = dynamic(() => import('next/script'), { ssr: false });

export default function Home() {
  const [isScriptLoaded, setIsScriptLoaded] = useState(false);
  const [scriptLoadError, setScriptLoadError] = useState<string | null>(null);

  useEffect(() => {
    console.log('Available env vars:', {
      key: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
      hasKey: !!process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
      envKeys: Object.keys(process.env).filter(key => key.includes('GOOGLE'))
    });

    if (!process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY) {
      setScriptLoadError('Google Maps API key is missing. Please check your .env.local file.');
      return;
    }

    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}&libraries=places`;
    script.async = true;
    script.onload = () => setIsScriptLoaded(true);
    script.onerror = (e) => setScriptLoadError('Failed to load Google Maps API. Please check your API key.');
    document.head.appendChild(script);

    return () => {
      script.remove();
    };
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between text-center">
        <h1 className="text-4xl font-bold mb-4">Prosper Homes</h1>
        
        <div className="mt-8">
          {scriptLoadError ? (
            <div className="text-red-600 p-4 bg-red-50 rounded-md">
              {scriptLoadError}
              <pre className="mt-2 text-sm text-left whitespace-pre-wrap">
                {JSON.stringify({
                  hasKey: !!process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
                  envKeys: Object.keys(process.env).filter(key => key.includes('GOOGLE'))
                }, null, 2)}
              </pre>
            </div>
          ) : isScriptLoaded ? (
            <MultiStepForm />
          ) : (
            <div className="w-full h-12 flex items-center justify-center">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
