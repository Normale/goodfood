import { motion } from "framer-motion";
import { ChefHatIcon } from "../ui/Icons";
import "./NextMealSuggestion.css";

const NextMealSuggestion = () => {
  const meals = [
    { name: "Salmon & Spinach Bowl", nutrients: "High in Omega-3, Iron, Vitamin K" },
    { name: "Almond Berry Smoothie", nutrients: "Rich in Vitamin E, Polyphenols" },
    { name: "Quinoa Buddha Bowl", nutrients: "Complete amino acids, Magnesium" },
    { name: "Egg & Avocado Toast", nutrients: "Choline, B12, Healthy fats" },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="suggestion-container group"
    >
      <div className="glow-effect"></div>

      <div className="suggestion-card">
        {/* Header */}
        <div className="suggestion-header">
          <div className="header-icon">
            <ChefHatIcon />
          </div>
          <div className="header-content">
            <h2>Recommended Meals</h2>
            <p>Based on your nutrient gaps</p>
          </div>
        </div>

        {/* List of Recommended Meals */}
        <div className="recommendation-list">
          {meals.map((meal, index) => (
            <motion.div
              key={meal.name}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="recommendation-item"
            >
              <div className="recommendation-dot"></div>
              <div className="recommendation-content">
                <h4>{meal.name}</h4>
                <p>{meal.nutrients}</p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Subtle Pulse Indicator */}
        <motion.div
          className="pulse-indicator"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.5, 1, 0.5]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          <div className="pulse-dot"></div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default NextMealSuggestion;
