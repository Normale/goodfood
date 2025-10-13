import { useState } from 'react';
import { UtensilsIcon, SparklesIcon } from '../ui/Icons';
import './MealInput.css';

const MealInput = ({ onSubmit }) => {
  const [mealText, setMealText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (mealText.trim()) {
      setIsAnalyzing(true);

      try {
        await onSubmit(mealText);
        setMealText('');
      } finally {
        setIsAnalyzing(false);
      }
    }
  };

  return (
    <div className="meal-input-container">
      <form onSubmit={handleSubmit}>
        <div className="glow-wrapper">
          <div className="glow-effect"></div>
          <div className="meal-input-card">
            <div className="input-header">
              <div className="icon-container">
                <UtensilsIcon />
              </div>
              <div className="input-content">
                <label className="input-label" htmlFor="mealInput">
                  What did you eat today?
                </label>
                <textarea
                  id="mealInput"
                  className="meal-textarea"
                  placeholder="e.g., Grilled salmon with quinoa and roasted vegetables..."
                  value={mealText}
                  onChange={(e) => setMealText(e.target.value)}
                  disabled={isAnalyzing}
                />
              </div>
            </div>
            <div className="input-footer">
              <p className="footer-text">
                AI will analyze nutritional content automatically
              </p>
              <button
                type="submit"
                className={`submit-button ${isAnalyzing ? 'analyzing' : ''}`}
                disabled={!mealText.trim() || isAnalyzing}
              >
                <SparklesIcon />
                <span>{isAnalyzing ? 'Analyzing...' : 'Log Meal'}</span>
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};

export default MealInput;
