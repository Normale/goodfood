import React, { useState, useEffect } from 'react';
import { 
  Loader2, 
  CheckCircle, 
  Search, 
  Utensils, 
  Shield, 
  ShieldAlert 
} from 'lucide-react';

const StatusSequenceComponent = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  const steps = [
    {
      id: 'initial',
      title: 'Initial State',
      items: []
    },
    {
      id: 'analyzing',
      title: 'Step 1: Analyzing ingredients',
      items: [
        { status: 'active', icon: 'loader', text: 'Analyzing ingredients' }
      ]
    },
    {
      id: 'analyzed',
      title: 'Step 1: Complete',
      items: [
        { status: 'done', icon: 'check', text: 'Analyzing ingredients' }
      ]
    },
    {
      id: 'found',
      title: 'Step 2: Found ingredients',
      items: [
        { status: 'done', icon: 'check', text: 'Analyzing ingredients' },
        { status: 'active', icon: 'search', text: 'Found 5 ingredients' }
      ]
    },
    {
      id: 'found-complete',
      title: 'Step 2: Complete',
      items: [
        { status: 'done', icon: 'check', text: 'Analyzing ingredients' },
        { status: 'done', icon: 'check', text: 'Found 5 ingredients' }
      ]
    },
    {
      id: 'estimating',
      title: 'Step 3: Estimating (all appear)',
      items: [
        { status: 'done', icon: 'check', text: 'Analyzing ingredients' },
        { status: 'done', icon: 'check', text: 'Found 5 ingredients' },
        { status: 'active', icon: 'utensils', text: 'Estimating (1 egg, 50g)' },
        { status: 'active', icon: 'utensils', text: 'Estimating (2 slices bread, 60g)' },
        { status: 'active', icon: 'utensils', text: 'Estimating (1 tbsp butter, 14g)' },
        { status: 'active', icon: 'utensils', text: 'Estimating (1 tomato, 100g)' },
        { status: 'active', icon: 'utensils', text: 'Estimating (50ml milk)' }
      ]
    },
    {
      id: 'validating',
      title: 'Step 4: Validating (all change)',
      items: [
        { status: 'done', icon: 'check', text: 'Analyzing ingredients' },
        { status: 'done', icon: 'check', text: 'Found 5 ingredients' },
        { status: 'validating', icon: 'shield', text: 'Validating (1 egg, 50g)' },
        { status: 'validating', icon: 'shield', text: 'Validating (2 slices bread, 60g)' },
        { status: 'validating', icon: 'shield', text: 'Validating (1 tbsp butter, 14g)' },
        { status: 'validating', icon: 'shield', text: 'Validating (1 tomato, 100g)' },
        { status: 'validating', icon: 'shield', text: 'Validating (50ml milk)' }
      ]
    },
    {
      id: 'validated',
      title: 'Step 5: All validated',
      items: [
        { status: 'done', icon: 'check', text: 'Analyzing ingredients' },
        { status: 'done', icon: 'check', text: 'Found 5 ingredients' },
        { status: 'done', icon: 'check', text: 'Validating (1 egg, 50g)' },
        { status: 'done', icon: 'check', text: 'Validating (2 slices bread, 60g)' },
        { status: 'done', icon: 'check', text: 'Validating (1 tbsp butter, 14g)' },
        { status: 'done', icon: 'check', text: 'Validating (1 tomato, 100g)' },
        { status: 'done', icon: 'check', text: 'Validating (50ml milk)' }
      ]
    },
    {
      id: 'interactions',
      title: 'Step 6: Investigating interactions',
      items: [
        { status: 'done', icon: 'check', text: 'Analyzing ingredients' },
        { status: 'done', icon: 'check', text: 'Found 5 ingredients' },
        { status: 'done', icon: 'check', text: 'Validating (1 egg, 50g)' },
        { status: 'done', icon: 'check', text: 'Validating (2 slices bread, 60g)' },
        { status: 'done', icon: 'check', text: 'Validating (1 tbsp butter, 14g)' },
        { status: 'done', icon: 'check', text: 'Validating (1 tomato, 100g)' },
        { status: 'done', icon: 'check', text: 'Validating (50ml milk)' },
        { status: 'active', icon: 'loader', text: 'Investigating potential interactions' }
      ]
    },
    {
      id: 'complete',
      title: 'Step 7: Complete',
      items: [
        { status: 'done', icon: 'check', text: 'Analyzing ingredients' },
        { status: 'done', icon: 'check', text: 'Found 5 ingredients' },
        { status: 'done', icon: 'check', text: 'Validating (1 egg, 50g)' },
        { status: 'done', icon: 'check', text: 'Validating (2 slices bread, 60g)' },
        { status: 'done', icon: 'check', text: 'Validating (1 tbsp butter, 14g)' },
        { status: 'done', icon: 'check', text: 'Validating (1 tomato, 100g)' },
        { status: 'done', icon: 'check', text: 'Validating (50ml milk)' },
        { status: 'done', icon: 'check', text: 'Investigating potential interactions' }
      ]
    }
  ];

  useEffect(() => {
    if (isPlaying && currentStep < steps.length - 1) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => prev + 1);
      }, 1500);
      return () => clearTimeout(timer);
    } else if (isPlaying && currentStep >= steps.length - 1) {
      setIsPlaying(false);
    }
  }, [isPlaying, currentStep, steps.length]);

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

  const handlePlay = () => {
    setCurrentStep(0);
    setIsPlaying(true);
  };

  const handleStepClick = (index) => {
    setCurrentStep(index);
    setIsPlaying(false);
  };

  const styles = {
    container: {
      minHeight: '100vh',
      backgroundColor: '#111827',
      padding: '32px'
    },
    wrapper: {
      maxWidth: '672px',
      margin: '0 auto'
    },
    card: {
      backgroundColor: 'rgba(31, 41, 55, 0.5)',
      backdropFilter: 'blur(4px)',
      borderRadius: '12px',
      border: '1px solid #374151',
      padding: '24px'
    },
    title: {
      fontSize: '20px',
      fontWeight: 'bold',
      color: '#ffffff',
      marginBottom: '16px',
      margin: 0
    },
    controls: {
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
      marginBottom: '24px'
    },
    playButton: {
      padding: '8px 16px',
      backgroundColor: '#3b82f6',
      color: '#ffffff',
      borderRadius: '8px',
      border: 'none',
      cursor: 'pointer',
      fontSize: '14px',
      transition: 'background-color 0.2s'
    },
    resetButton: {
      padding: '8px 16px',
      backgroundColor: '#4b5563',
      color: '#ffffff',
      borderRadius: '8px',
      border: 'none',
      cursor: 'pointer',
      fontSize: '14px',
      transition: 'background-color 0.2s'
    },
    stepCounter: {
      color: 'rgba(255, 255, 255, 0.6)',
      fontSize: '14px'
    },
    stepNav: {
      display: 'flex',
      gap: '4px',
      marginBottom: '24px',
      overflowX: 'auto',
      paddingBottom: '8px'
    },
    stepButton: {
      padding: '4px 12px',
      fontSize: '12px',
      borderRadius: '4px',
      border: 'none',
      cursor: 'pointer',
      transition: 'all 0.2s'
    },
    currentStepTitle: {
      marginBottom: '16px'
    },
    stepTitle: {
      fontSize: '18px',
      fontWeight: '600',
      color: '#06b6d4',
      margin: 0
    },
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
    },
    legend: {
      marginTop: '32px',
      paddingTop: '16px',
      borderTop: '1px solid rgba(255, 255, 255, 0.1)'
    },
    legendTitle: {
      fontSize: '14px',
      fontWeight: '500',
      color: 'rgba(255, 255, 255, 0.6)',
      marginBottom: '8px',
      margin: '0 0 8px 0'
    },
    legendGrid: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '8px',
      fontSize: '12px'
    },
    legendItem: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px'
    },
    legendDot: {
      width: '8px',
      height: '8px',
      borderRadius: '50%'
    },
    legendText: {
      color: 'rgba(255, 255, 255, 0.6)'
    }
  };

  return (
    <>
      <style>
        {`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          
          button:hover {
            opacity: 0.9;
          }
          
          * {
            box-sizing: border-box;
            font-family: system-ui, -apple-system, sans-serif;
          }
        `}
      </style>
      
      <div style={styles.container}>
        <div style={styles.wrapper}>
          <div style={styles.card}>
            <h2 style={styles.title}>Multi-Step Status Sequence</h2>
            
            <div style={styles.controls}>
              <button
                onClick={handlePlay}
                style={styles.playButton}
              >
                {isPlaying ? 'Playing...' : 'Play Animation'}
              </button>
              <button
                onClick={() => { setCurrentStep(0); setIsPlaying(false); }}
                style={styles.resetButton}
              >
                Reset
              </button>
              <span style={styles.stepCounter}>
                Step {currentStep + 1} of {steps.length}
              </span>
            </div>

            <div style={styles.stepNav}>
              {steps.map((step, index) => (
                <button
                  key={step.id}
                  onClick={() => handleStepClick(index)}
                  style={{
                    ...styles.stepButton,
                    backgroundColor: currentStep === index ? '#3b82f6' : '#374151',
                    color: currentStep === index ? '#ffffff' : '#9ca3af'
                  }}
                >
                  {index + 1}
                </button>
              ))}
            </div>

            <div style={styles.currentStepTitle}>
              <h3 style={styles.stepTitle}>
                {steps[currentStep].title}
              </h3>
            </div>

            <div style={styles.statusContainer}>
              {steps[currentStep].items.length === 0 ? (
                <div style={styles.emptyState}>No status items yet...</div>
              ) : (
                <div style={styles.itemsContainer}>
                  {steps[currentStep].items.map((item, index) => (
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

            <div style={styles.legend}>
              <h4 style={styles.legendTitle}>Status Legend:</h4>
              <div style={styles.legendGrid}>
                <div style={styles.legendItem}>
                  <div style={{ ...styles.legendDot, backgroundColor: '#06b6d4' }}></div>
                  <span style={styles.legendText}>Active (spinning)</span>
                </div>
                <div style={styles.legendItem}>
                  <div style={{ ...styles.legendDot, backgroundColor: '#10b981' }}></div>
                  <span style={styles.legendText}>Completed</span>
                </div>
                <div style={styles.legendItem}>
                  <div style={{ ...styles.legendDot, backgroundColor: '#a855f7' }}></div>
                  <span style={styles.legendText}>Estimating</span>
                </div>
                <div style={styles.legendItem}>
                  <div style={{ ...styles.legendDot, backgroundColor: '#f59e0b' }}></div>
                  <span style={styles.legendText}>Validating</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default StatusSequenceComponent;