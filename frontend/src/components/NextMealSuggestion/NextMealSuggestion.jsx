import { LightbulbIcon, SparklesIcon, BulbIcon } from '../ui/Icons';
import './NextMealSuggestion.css';

const NextMealSuggestion = ({ suggestion }) => {
  return (
    <div className="suggestion-container">
      <div className="glow-wrapper">
        <div className="glow-effect"></div>
        <div className="suggestion-card">
          <div className="suggestion-header">
            <div className="header-icon">
              <LightbulbIcon />
            </div>
            <div className="header-content">
              <h2>Next Meal Suggestion</h2>
              <p>AI-powered recommendation</p>
            </div>
          </div>

          <div className="suggestion-content">
            <div className="suggestion-title">
              <SparklesIcon />
              <h3>{suggestion.meal}</h3>
            </div>
            <p className="suggestion-reasoning">{suggestion.reasoning}</p>
          </div>

          <div className="suggestion-footer">
            <BulbIcon />
            <span>Based on your current nutritional intake and goals</span>
          </div>

          <div className="pulse-indicator"></div>
        </div>
      </div>
    </div>
  );
};

export default NextMealSuggestion;
