import { useState, useEffect } from 'react';

// Import localization files
import nlTranslations from '../localization/nl.json';
import enTranslations from '../localization/en.json';

const translations = {
  nl: nlTranslations,
  en: enTranslations
};

type Language = 'nl' | 'en';

export const useLocalization = (language: Language = 'nl') => {
  const [currentLanguage, setCurrentLanguage] = useState<Language>(language);

  useEffect(() => {
    setCurrentLanguage(language);
  }, [language]);

  const t = (key: string): string => {
    const keys = key.split('.');
    let value: any = translations[currentLanguage];

    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        // Fallback to English if key not found in current language
        value = translations.en;
        for (const fallbackKey of keys) {
          if (value && typeof value === 'object' && fallbackKey in value) {
            value = value[fallbackKey];
          } else {
            return key; // Return key if not found in any language
          }
        }
        break;
      }
    }

    return typeof value === 'string' ? value : key;
  };

  return {
    t,
    currentLanguage,
    setLanguage: setCurrentLanguage,
    availableLanguages: ['nl', 'en'] as Language[]
  };
};