import { motion } from 'framer-motion';
import { TrendingDownIcon } from '../ui/Icons';
import { getNutrientDisplayName } from '../../utils/nutrientDisplay';
import './TopNutrientGaps.css';

const TopNutrientGaps = ({ nutrientData = [], maxGaps = 5 }) => {
  // nutrientData is now an array of gap objects from the backend
  // Each gap object has: { id, name, current, target, deficit, percentage, unit }
  // name contains the canonical key, we convert it to display name
  const topDeficiencies = Array.isArray(nutrientData)
    ? nutrientData.slice(0, maxGaps).map(gap => ({
        ...gap,
        displayName: getNutrientDisplayName(gap.name)
      }))
    : [];

  if (topDeficiencies.length === 0) {
    return (
      <div className="nutrient-gaps-card optimal">
        <div className="gaps-header">
          <div className="gaps-icon optimal">
            <TrendingDownIcon />
          </div>
          <div className="gaps-header-content">
            <h3>Nutrient Status</h3>
            <p className="optimal-text">Add meals to track gaps</p>
          </div>
        </div>
        <p className="gaps-message">
          Start tracking your meals to see which nutrients you need more of.
        </p>
      </div>
    );
  }

  return (
    <div className="nutrient-gaps-card">
      <div className="gaps-header">
        <div className="gaps-icon">
          <TrendingDownIcon />
        </div>
        <div className="gaps-header-content">
          <h3>Top Nutrient Gaps</h3>
          <p>Nutrients below 80% of daily target</p>
        </div>
      </div>

      <div className="gaps-grid">
        {topDeficiencies.map((nutrient, index) => (
          <motion.div
            key={nutrient.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="gap-item"
          >
            <div className="gap-item-header">
              <h4>{nutrient.displayName}</h4>
              <span className="gap-percentage">{nutrient.percentage.toFixed(0)}%</span>
            </div>

            <div className="gap-progress-container">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${nutrient.percentage}%` }}
                transition={{ duration: 0.5, delay: index * 0.1 + 0.2 }}
                className="gap-progress-bar"
              />
            </div>

            <div className="gap-item-footer">
              <p className="gap-current">
                {nutrient.current.toFixed(1)} / {nutrient.target} {nutrient.unit}
              </p>
              <p className="gap-deficit">
                Need {nutrient.deficit.toFixed(1)} {nutrient.unit}
              </p>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="gaps-tip">
        <p>💡 Tip: Focus on foods rich in these nutrients to optimize your intake</p>
      </div>
    </div>
  );
};

export default TopNutrientGaps;
