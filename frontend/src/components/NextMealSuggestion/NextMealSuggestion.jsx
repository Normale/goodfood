import { motion } from "framer-motion";
import { ChefHatIcon } from "../ui/Icons";
import "./NextMealSuggestion.css";

const NextMealSuggestion = ({ suggestion }) => {
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
            <h2>Recommended Next Meal</h2>
            <p>Based on your nutrient gaps</p>
          </div>
        </div>

        {/* Recommended Meal */}
        {suggestion && (
          <div className="recommendation-list">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="recommendation-item"
            >
              <div className="recommendation-dot"></div>
              <div className="recommendation-content">
                <h4>{suggestion.meal}</h4>
                <p>{suggestion.reasoning}</p>
                {suggestion.nutrients && (
                  <div style={{ marginTop: '8px', fontSize: '0.85em', color: 'rgba(255,255,255,0.6)' }}>
                    <span>Calories: {suggestion.nutrients.calories} | </span>
                    <span>Protein: {suggestion.nutrients.protein}g | </span>
                    <span>Omega-3: {suggestion.nutrients.omega_3}g</span>
                  </div>
                )}
              </div>
            </motion.div>
          </div>
        )}

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
