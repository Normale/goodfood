import { ActivityIcon, AlertCircleIcon, CheckCircleIcon, TrendingUpIcon } from '../ui/Icons';
import './NutrientAnalysis.css';

const NutrientItem = ({ nutrient, compact = false }) => {
  const statusIcons = {
    deficient: <AlertCircleIcon />,
    adequate: <CheckCircleIcon />,
    excessive: <TrendingUpIcon />
  };

  return (
    <div className={`nutrient-item ${nutrient.status}`}>
      <div className="glow-effect"></div>
      <div className={`nutrient-card ${compact ? 'compact' : ''}`}>
        <div className={`nutrient-content ${compact ? 'compact' : ''}`}>
          <div className={`nutrient-icon ${nutrient.status} ${compact ? 'compact' : ''}`}>
            {statusIcons[nutrient.status]}
          </div>
          <div className="nutrient-info">
            {!compact && (
              <div className="nutrient-header">
                <h4 className="nutrient-name">{nutrient.name}</h4>
                <span className={`nutrient-badge ${nutrient.status}`}>
                  {nutrient.status.charAt(0).toUpperCase() + nutrient.status.slice(1)}
                </span>
              </div>
            )}
            {compact && (
              <h4 className="nutrient-name compact">{nutrient.name}</h4>
            )}
            <p className={`nutrient-note ${compact ? 'compact' : ''}`}>
              {nutrient.note}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const NutrientAnalysis = ({ analysis }) => {
  return (
    <div className="analysis-container">
      <div className="analysis-card">
        <div className="analysis-header">
          <div className="header-icon">
            <ActivityIcon />
          </div>
          <div className="header-content">
            <h2>Nutrient Analysis</h2>
            <p>AI-powered insights</p>
          </div>
        </div>

        <div className="analysis-sections">
          {analysis.deficient && analysis.deficient.length > 0 && (
            <div>
              <h3 className="section-title deficient">
                <AlertCircleIcon />
                Needs Attention
              </h3>
              <div className="nutrient-list">
                {analysis.deficient.map((nutrient) => (
                  <NutrientItem key={nutrient.name} nutrient={nutrient} />
                ))}
              </div>
            </div>
          )}

          {analysis.adequate && analysis.adequate.length > 0 && (
            <div>
              <h3 className="section-title adequate">
                <CheckCircleIcon />
                On Track
              </h3>
              <div className="nutrient-list">
                {analysis.adequate.map((nutrient) => (
                  <NutrientItem key={nutrient.name} nutrient={nutrient} compact />
                ))}
              </div>
            </div>
          )}

          {analysis.excessive && analysis.excessive.length > 0 && (
            <div>
              <h3 className="section-title excessive">
                <TrendingUpIcon />
                Watch Out
              </h3>
              <div className="nutrient-list">
                {analysis.excessive.map((nutrient) => (
                  <NutrientItem key={nutrient.name} nutrient={nutrient} compact />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default NutrientAnalysis;
