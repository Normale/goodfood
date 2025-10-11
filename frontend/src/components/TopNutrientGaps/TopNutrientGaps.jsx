import { motion } from 'framer-motion';
import { TrendingDownIcon } from '../ui/Icons';
import './TopNutrientGaps.css';

// Sample nutrients data structure
const sampleNutrients = [
  { id: 'vitamin_d', name: 'Vitamin D', unit: 'mcg', dailyTarget: 20 },
  { id: 'fiber', name: 'Fiber', unit: 'g', dailyTarget: 30 },
  { id: 'iron', name: 'Iron', unit: 'mg', dailyTarget: 18 },
  { id: 'calcium', name: 'Calcium', unit: 'mg', dailyTarget: 1000 },
  { id: 'vitamin_b12', name: 'Vitamin B12', unit: 'mcg', dailyTarget: 2.4 },
  { id: 'omega_3', name: 'Omega-3', unit: 'g', dailyTarget: 1.6 },
];

const TopNutrientGaps = ({ nutrientData = {}, maxGaps = 5 }) => {
  const getTopDeficiencies = () => {
    const deficiencies = sampleNutrients
      .map(nutrient => {
        const current = nutrientData[nutrient.id] || 0;
        const target = nutrient.dailyTarget || 100;
        const percentage = (current / target) * 100;
        return { ...nutrient, current, percentage, deficit: target - current };
      })
      .filter(n => n.percentage < 80)
      .sort((a, b) => a.percentage - b.percentage)
      .slice(0, maxGaps);
    return deficiencies;
  };

  const topDeficiencies = getTopDeficiencies();

  if (topDeficiencies.length === 0) {
    return (
      <div className="nutrient-gaps-card optimal">
        <div className="gaps-header">
          <div className="gaps-icon optimal">
            <TrendingDownIcon />
          </div>
          <div className="gaps-header-content">
            <h3>Nutrient Status</h3>
            <p className="optimal-text">All nutrients are optimal!</p>
          </div>
        </div>
        <p className="gaps-message">
          Great job! All your tracked nutrients are at 80% or above their daily targets.
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
              <h4>{nutrient.name}</h4>
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
                {nutrient.current.toFixed(1)} / {nutrient.dailyTarget} {nutrient.unit}
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
