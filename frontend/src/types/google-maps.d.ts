declare namespace google.maps {
  class Autocomplete {
    constructor(inputField: HTMLInputElement, opts?: AutocompleteOptions);
    addListener(eventName: string, handler: () => void): void;
    getPlace(): Place;
  }

  interface AutocompleteOptions {
    types?: string[];
    componentRestrictions?: {
      country: string;
    };
  }

  interface Place {
    formatted_address?: string;
    geometry?: {
      location: {
        lat(): number;
        lng(): number;
      };
    };
  }

  namespace event {
    function clearInstanceListeners(instance: any): void;
  }
}
