import { AppleIcon, MoonIcon, UtensilsIcon, DatabaseIcon, UserIcon } from '../ui/Icons';
import './Header.css';

const Header = ({ totalCalories, totalProtein, onThemeToggle, activeTab, onTabChange }) => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-content">
          <div className="brand">
            <div className="brand-icon">
              <AppleIcon />
            </div>
            <div className="brand-text">
              <h1>GoodFood</h1>
              <p>Advanced nutrition tracking</p>
            </div>
          </div>

          <div className="header-actions">
            <div className="nav-buttons">
              <button
                className={`nav-button ${activeTab === 'tracker' ? 'active' : ''}`}
                onClick={() => onTabChange('tracker')}
                aria-label="Nutrition Tracker"
              >
                <UtensilsIcon />
                <span>Tracker</span>
              </button>
              <button
                className={`nav-button ${activeTab === 'database' ? 'active' : ''}`}
                onClick={() => onTabChange('database')}
                aria-label="Food Database"
              >
                <DatabaseIcon />
                <span>Database</span>
              </button>
              <button
                className={`nav-button ${activeTab === 'personalization' ? 'active' : ''}`}
                onClick={() => onTabChange('personalization')}
                aria-label="Personalization"
              >
                <UserIcon />
                <span>Profile</span>
              </button>
            </div>

            <div className="stats-container">
              <div className="stat">
                <p className="stat-label">Today's Calories</p>
                <p className="stat-value">{totalCalories}</p>
              </div>
              <div className="stat-divider"></div>
              <div className="stat">
                <p className="stat-label">Protein</p>
                <p className="stat-value">{totalProtein}g</p>
              </div>
            </div>

            <button
              className="theme-toggle"
              onClick={onThemeToggle}
              aria-label="Toggle theme"
            >
              <MoonIcon />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
