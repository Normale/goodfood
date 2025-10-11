import { ClockIcon, FlameIcon, DrumstickIcon, WheatIcon, DropletIcon, TrashIcon } from '../ui/Icons';
import './MealsList.css';

const MealItem = ({ meal, onDelete }) => {
  return (
    <div className="meal-item">
      <div className="meal-card">
        <div className="meal-content">
          <div className="meal-info">
            <div className="meal-time">{meal.time}</div>
            <div className="meal-description">{meal.description}</div>
            <div className="nutrition-grid">
              <div className="nutrition-item">
                <FlameIcon />
                <div>
                  <div className="nutrition-label">Calories</div>
                  <div className="nutrition-value">{meal.calories}</div>
                </div>
              </div>
              <div className="nutrition-item">
                <DrumstickIcon />
                <div>
                  <div className="nutrition-label">Protein</div>
                  <div className="nutrition-value">{meal.protein}g</div>
                </div>
              </div>
              <div className="nutrition-item">
                <WheatIcon />
                <div>
                  <div className="nutrition-label">Carbs</div>
                  <div className="nutrition-value">{meal.carbs}g</div>
                </div>
              </div>
              <div className="nutrition-item">
                <DropletIcon />
                <div>
                  <div className="nutrition-label">Fat</div>
                  <div className="nutrition-value">{meal.fat}g</div>
                </div>
              </div>
            </div>
          </div>
          <button className="delete-button" onClick={() => onDelete(meal.id)}>
            <TrashIcon />
          </button>
        </div>
      </div>
    </div>
  );
};

const EmptyState = () => (
  <div className="empty-state">
    <div className="empty-icon">
      <ClockIcon />
    </div>
    <p className="empty-text">No meals logged yet</p>
    <p className="empty-subtext">Start tracking your nutrition above</p>
  </div>
);

const MealsList = ({ meals, onDeleteMeal }) => {
  return (
    <div className="meals-container">
      <div className="meals-card">
        <div className="meals-header">
          <div className="header-icon">
            <ClockIcon />
          </div>
          <div className="header-content">
            <h2>Today's Meals</h2>
            <p>{meals.length} meal{meals.length !== 1 ? 's' : ''} logged</p>
          </div>
        </div>

        <div className="meals-list">
          {meals.length === 0 ? (
            <EmptyState />
          ) : (
            meals.map((meal) => (
              <MealItem key={meal.id} meal={meal} onDelete={onDeleteMeal} />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default MealsList;
