/**
 * Nutrient Display Names - converts canonical keys to human-readable labels
 *
 * This is the ONLY place where nutrient display names are defined.
 */

export const NUTRIENT_DISPLAY_NAMES = {
  // Macronutrients
  "carbohydrates": "Carbohydrates",
  "protein": "Protein",
  "total-fats": "Total Fats",
  "fiber": "Fiber",

  // Essential Fatty Acids
  "alpha-linolenic-acid": "Alpha-Linolenic Acid (ALA)",
  "linoleic-acid": "Linoleic Acid (LA)",
  "epa-dha": "EPA+DHA",

  // Water-soluble vitamins
  "vitamin-c": "Vitamin C",
  "thiamine": "Thiamine (B1)",
  "riboflavin": "Riboflavin (B2)",
  "niacin": "Niacin (B3)",
  "pantothenic-acid": "Pantothenic Acid (B5)",
  "pyridoxine": "Pyridoxine (B6)",
  "biotin": "Biotin (B7)",
  "folate": "Folate (B9)",
  "vitamin-b12": "Vitamin B12",

  // Fat-soluble vitamins
  "vitamin-a": "Vitamin A",
  "vitamin-d": "Vitamin D",
  "vitamin-e": "Vitamin E",
  "vitamin-k": "Vitamin K",

  // Major minerals
  "calcium": "Calcium",
  "phosphorus": "Phosphorus",
  "magnesium": "Magnesium",
  "potassium": "Potassium",
  "sodium": "Sodium",
  "chloride": "Chloride",

  // Trace elements
  "iron": "Iron",
  "zinc": "Zinc",
  "copper": "Copper",
  "selenium": "Selenium",
  "manganese": "Manganese",
  "iodine": "Iodine",
  "chromium": "Chromium",
  "molybdenum": "Molybdenum",

  // Amino acids
  "leucine": "Leucine",
  "lysine": "Lysine",
  "valine": "Valine",
  "isoleucine": "Isoleucine",
  "threonine": "Threonine",
  "methionine": "Methionine",
  "phenylalanine": "Phenylalanine",
  "histidine": "Histidine",
  "tryptophan": "Tryptophan",

  // Beneficial compounds
  "choline": "Choline",
  "taurine": "Taurine",
  "coenzyme-q10": "Coenzyme Q10",
  "alpha-lipoic-acid": "Alpha-Lipoic Acid",
  "beta-glucan": "Beta-Glucan",
  "resistant-starch": "Resistant Starch",

  // Carotenoids
  "beta-carotene": "Beta-Carotene",
  "lycopene": "Lycopene",
  "lutein": "Lutein",
  "zeaxanthin": "Zeaxanthin",

  // Polyphenols
  "polyphenols": "Polyphenols",
  "quercetin": "Quercetin",
  "sulforaphane": "Sulforaphane",
  "allicin": "Allicin",
  "curcumin": "Curcumin",

  // Water
  "water": "Water",
};

/**
 * Get display name for a nutrient
 * @param {string} key - Canonical nutrient key (e.g., "alpha-linolenic-acid")
 * @returns {string} - Human-readable name (e.g., "Alpha-Linolenic Acid (ALA)")
 */
export function getNutrientDisplayName(key) {
  return NUTRIENT_DISPLAY_NAMES[key] || key;
}

/**
 * Convert a nutrient data object to use display names
 * @param {Object} nutrientData - Object with canonical keys
 * @returns {Object} - Object with display names as keys
 */
export function convertToDisplayNames(nutrientData) {
  const result = {};
  for (const [key, value] of Object.entries(nutrientData)) {
    const displayName = getNutrientDisplayName(key);
    result[displayName] = value;
  }
  return result;
}
