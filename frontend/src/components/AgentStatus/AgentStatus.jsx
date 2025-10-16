import React from 'react';
import {
  Loader2,
  CheckCircle,
  Search,
  Utensils,
  Shield,
  ShieldAlert
} from 'lucide-react';
import './AgentStatus.css';

const AgentStatus = ({ agents = [], isThinking = false }) => {
  // Convert agent data to items format for rendering
  const convertAgentToItem = (agent) => {
    // Determine icon based on agent type and status
    let icon = 'loader';
    let status = 'active';

    if (agent.status === 'done') {
      icon = 'check';
      status = 'done';
    } else if (agent.agent_type === 'preprocessing') {
      icon = 'search';
      status = 'active';
    } else if (agent.agent_type === 'estimator') {
      icon = 'utensils';
      status = 'active';
    } else if (agent.agent_type === 'validator') {
      icon = 'shield';
      status = 'validating';
    } else if (agent.agent_type === 'detailed_analyzer') {
      icon = 'loader';
      status = 'active';
    }

    return {
      icon,
      status,
      text: agent.message || `${agent.agent_type} running...`
    };
  };

  const items = agents.map(convertAgentToItem);

  const getIcon = (iconType, status) => {
    const iconStyle = {
      width: '14px',
      height: '14px',
      color: status === 'done' ? '#10b981' :
             status === 'active' ? '#06b6d4' :
             status === 'validating' ? '#f59e0b' :
             '#a855f7',
      animation: status === 'active' && iconType === 'loader' ? 'spin 1s linear infinite' : 'none'
    };

    switch (iconType) {
      case 'loader':
        return <Loader2 style={iconStyle} />;
      case 'check':
        return <CheckCircle style={{ ...iconStyle, color: '#10b981' }} />;
      case 'search':
        return <Search style={iconStyle} />;
      case 'utensils':
        return <Utensils style={{ ...iconStyle, color: '#a855f7' }} />;
      case 'shield':
        return <Shield style={{ ...iconStyle, color: '#f59e0b' }} />;
      default:
        return <Loader2 style={iconStyle} />;
    }
  };

  const getItemStyle = (status) => {
    if (status === 'done') {
      return {
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderColor: 'rgba(16, 185, 129, 0.2)'
      };
    } else {
      return {
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderColor: 'rgba(255, 255, 255, 0.1)'
      };
    }
  };

  const getTextStyle = (status) => {
    return {
      color: status === 'done' ? '#6ee7b7' : 'rgba(255, 255, 255, 0.8)',
      fontSize: '12px',
      fontWeight: '500',
      margin: 0
    };
  };

  const styles = {
    statusContainer: {
      marginTop: '16px',
      paddingTop: '16px',
      borderTop: '1px solid rgba(255, 255, 255, 0.1)'
    },
    emptyState: {
      color: 'rgba(255, 255, 255, 0.4)',
      fontSize: '14px'
    },
    itemsContainer: {
      display: 'flex',
      flexDirection: 'column',
      gap: '8px'
    },
    statusItem: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '8px 12px',
      borderRadius: '8px',
      border: '1px solid',
      transition: 'all 0.3s'
    },
    iconWrapper: {
      flexShrink: 0
    }
  };

  // Don't render if there's nothing to show
  if (!isThinking && items.length === 0) {
    return null;
  }

  return (
    <>
      <style>
        {`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }

          * {
            box-sizing: border-box;
            font-family: system-ui, -apple-system, sans-serif;
          }
        `}
      </style>

      <div style={styles.statusContainer}>
        {items.length === 0 && isThinking ? (
          <div style={styles.emptyState}>Thinking...</div>
        ) : (
          <div style={styles.itemsContainer}>
            {items.map((item, index) => (
              <div
                key={index}
                style={{
                  ...styles.statusItem,
                  ...getItemStyle(item.status)
                }}
              >
                <div style={styles.iconWrapper}>
                  {getIcon(item.icon, item.status)}
                </div>
                <p style={getTextStyle(item.status)}>
                  {item.text}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default AgentStatus;
