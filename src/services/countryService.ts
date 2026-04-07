import type { Country } from "../types/Country";

const countries: Country[] = [
  {
    name: "Hungary",
    capital: "Budapest",
    population: 9_600_000,
    area: 93_030,
    continent: "Europe",
    language: "Hungarian",
    currency: "HUF",
    countryCode: "hu",
  },
  {
    name: "Germany",
    capital: "Berlin",
    population: 83_200_000,
    area: 357_022,
    continent: "Europe",
    language: "German",
    currency: "EUR",
    countryCode: "de",
  },
  {
    name: "Japan",
    capital: "Tokyo",
    population: 125_800_000,
    area: 377_975,
    continent: "Asia",
    language: "Japanese",
    currency: "JPY",
    countryCode: "jp",
  },
  {
    name: "Brazil",
    capital: "Brasília",
    population: 214_000_000,
    area: 8_515_767,
    continent: "South America",
    language: "Portuguese",
    currency: "BRL",
    countryCode: "br",
  },
  {
    name: "Australia",
    capital: "Canberra",
    population: 26_000_000,
    area: 7_692_024,
    continent: "Oceania",
    language: "English",
    currency: "AUD",
    countryCode: "au",
  },
  {
    name: "Canada",
    capital: "Ottawa",
    population: 39_000_000,
    area: 9_984_670,
    continent: "North America",
    language: "English/French",
    currency: "CAD",
    countryCode: "ca",
  },
  {
    name: "Egypt",
    capital: "Cairo",
    population: 104_000_000,
    area: 1_002_450,
    continent: "Africa",
    language: "Arabic",
    currency: "EGP",
    countryCode: "eg",
  },
  {
    name: "South Korea",
    capital: "Seoul",
    population: 51_700_000,
    area: 100_210,
    continent: "Asia",
    language: "Korean",
    currency: "KRW",
    countryCode: "kr",
  },
];

export function getCountries(): Country[] {
  return countries;
}

export function getCountryByName(name: string): Country | undefined {
  return countries.find(
    (c) => c.name.toLowerCase() === name.toLowerCase()
  );
}

export function getCountriesByContinent(continent: string): Country[] {
  return countries.filter(
    (c) => c.continent.toLowerCase() === continent.toLowerCase()
  );
}
