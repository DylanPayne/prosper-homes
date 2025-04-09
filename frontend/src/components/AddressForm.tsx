'use client';

import { useEffect, useRef } from 'react';

interface AddressFormProps {
  onAddressSelect: (address: string, lat: number, lng: number) => void;
}

export default function AddressForm({ onAddressSelect }: AddressFormProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);

  useEffect(() => {
    if (!inputRef.current) return;

    autocompleteRef.current = new google.maps.places.Autocomplete(inputRef.current, {
      types: ['address'],
      componentRestrictions: { country: 'us' }
    });

    autocompleteRef.current.addListener('place_changed', () => {
      const place = autocompleteRef.current?.getPlace();
      if (place?.geometry?.location) {
        onAddressSelect(
          place.formatted_address || '',
          place.geometry.location.lat(),
          place.geometry.location.lng()
        );
      }
    });

    return () => {
      google.maps.event.clearInstanceListeners(autocompleteRef.current!);
    };
  }, [onAddressSelect]);

  return (
    <div className="w-full max-w-md mx-auto relative">
      <input
        ref={inputRef}
        type="text"
        placeholder="Enter your address"
        className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-gray-900 bg-white"
      />
      <style dangerouslySetInnerHTML={{
        __html: `
          .pac-container {
            border-radius: 0.5rem;
            margin-top: 0.25rem;
            border: 1px solid #e5e7eb;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
          }
          .pac-item {
            padding: 0.75rem 1rem;
            color: #1f2937;
            font-size: 0.875rem;
          }
          .pac-item:hover {
            background-color: #f3f4f6;
          }
          .pac-item-selected {
            background-color: #e5e7eb;
          }
          .pac-icon {
            margin-right: 0.75rem;
          }
          .pac-item-query {
            font-size: 0.875rem;
            color: #111827;
          }
        `
      }} />
    </div>
  );
}
