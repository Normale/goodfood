import { TargetIcon, CheckIcon, AlertTriangleIcon } from '../ui/Icons';
import './DailyGoals.css';

const GoalItem = ({ goal }) => {
  const percentage = (goal.current / goal.target) * 100;
  const isWarning = percentage >= 85;
  const statusClass = isWarning ? 'status-warning' : 'status-on-track';
  const progressClass = isWarning ? 'progress-bar-warning' : 'progress-bar-on-track';

  return (
    <div className="goal-item">
      <div className="goal-header">
        <div className="goal-name-wrapper">
          <span className="goal-name">{goal.name}</span>
          <span className={`status-badge ${statusClass}`}>
            {isWarning ? <AlertTriangleIcon /> : <CheckIcon />}
            {isWarning ? 'High' : 'On track'}
          </span>
        </div>
        <span className="goal-values">
          {goal.current}{goal.unit} / {goal.target}{goal.unit}
        </span>
      </div>
      <div className="progress-bar-container">
        <div className={`progress-bar ${progressClass}`} style={{ width: `${Math.min(percentage, 100)}%` }}>
          <div className="progress-shimmer"></div>
        </div>
      </div>
      <div className="goal-footer">
        <span>{Math.round(percentage)}% of daily goal</span>
        <span>{Math.max(0, goal.target - goal.current)}{goal.unit} remaining</span>
      </div>
    </div>
  );
};

const DailyGoals = ({ goals }) => {
  return (
    <div className="goals-container">
      <div className="goals-card">
        <div className="goals-header">
          <div className="header-icon">
            <TargetIcon />
          </div>
          <div className="header-content">
            <h2>Daily Goals</h2>
            <p>Track your progress</p>
          </div>
        </div>

        <div className="goals-list">
          {goals.map((goal, index) => (
            <GoalItem key={goal.name} goal={goal} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default DailyGoals;
