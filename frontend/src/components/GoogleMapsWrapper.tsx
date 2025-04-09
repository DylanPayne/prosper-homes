'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

const Script = dynamic(() => import('next/script'), { ssr: false });

interface GoogleMapsWrapperProps {
  children: React.ReactNode;
}

export default function GoogleMapsWrapper({ children }: GoogleMapsWrapperProps) {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const handleLoad = () => {
      setIsLoaded(true);
    };

    window.addEventListener('google-maps-loaded', handleLoad);

    return () => {
      window.removeEventListener('google-maps-loaded', handleLoad);
    };
  }, []);

  return (
    <>
      <Script
        id="google-maps"
        strategy="afterInteractive"
        onReady={() => {}}
      >
        {`
          (function() {
            const script = document.createElement('script');
            script.src = "https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}&libraries=places";
            script.async = true;
            script.onload = function() {
              window.dispatchEvent(new Event('google-maps-loaded'));
            };
            document.head.appendChild(script);
          })();
        `}
      </Script>
      {isLoaded ? children : (
        <div className="w-full h-12 flex items-center justify-center">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
        </div>
      )}
    </>
  );
}
