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
    const iconProps = {
      className: `w-3.5 h-3.5 ${
        status === 'done' ? 'text-emerald-400' :
        status === 'active' ? 'text-cyan-400 animate-spin' :
        status === 'validating' ? 'text-amber-400' :
        'text-purple-400'
      }`
    };

    switch (iconType) {
      case 'loader':
        return <Loader2 {...iconProps} />;
      case 'check':
        return <CheckCircle {...iconProps} className="w-3.5 h-3.5 text-emerald-400" />;
      case 'search':
        return <Search {...iconProps} />;
      case 'utensils':
        return <Utensils {...iconProps} className="w-3.5 h-3.5 text-purple-400" />;
      case 'shield':
        return <Shield {...iconProps} className="w-3.5 h-3.5 text-amber-400" />;
      default:
        return <Loader2 {...iconProps} />;
    }
  };

  const getItemStyle = (status) => {
    if (status === 'done') {
      return 'bg-emerald-500/10 border-emerald-500/20';
    } else if (status === 'validating') {
      return 'bg-white/5 border-white/10';
    } else {
      return 'bg-white/5 border-white/10';
    }
  };

  const getTextStyle = (status) => {
    if (status === 'done') {
      return 'text-emerald-300';
    } else {
      return 'text-white/80';
    }
  };

  const handlePlay = () => {
    setCurrentStep(0);
    setIsPlaying(true);
  };

  const handleStepClick = (index) => {
    setCurrentStep(index);
    setIsPlaying(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-4">Multi-Step Status Sequence</h2>
          
          {/* Controls */}
          <div className="flex items-center gap-4 mb-6">
            <button
              onClick={handlePlay}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              {isPlaying ? 'Playing...' : 'Play Animation'}
            </button>
            <button
              onClick={() => { setCurrentStep(0); setIsPlaying(false); }}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              Reset
            </button>
            <span className="text-white/60 text-sm">
              Step {currentStep + 1} of {steps.length}
            </span>
          </div>

          {/* Step navigation */}
          <div className="flex gap-1 mb-6 overflow-x-auto pb-2">
            {steps.map((step, index) => (
              <button
                key={step.id}
                onClick={() => handleStepClick(index)}
                className={`px-3 py-1 text-xs rounded transition-colors ${
                  currentStep === index
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                }`}
              >
                {index + 1}
              </button>
            ))}
          </div>

          {/* Current step title */}
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-cyan-400">
              {steps[currentStep].title}
            </h3>
          </div>

          {/* Status items */}
          <div className="mt-4 pt-4 border-t border-white/10">
            {steps[currentStep].items.length === 0 ? (
              <div className="text-white/40 text-sm">No status items yet...</div>
            ) : (
              <div className="space-y-2">
                {steps[currentStep].items.map((item, index) => (
                  <div
                    key={index}
                    className={`flex items-center gap-2 px-3 py-2 rounded-lg border transition-all duration-300 ${getItemStyle(item.status)}`}
                  >
                    <div className="flex-shrink-0">
                      {getIcon(item.icon, item.status)}
                    </div>
                    <p className={`text-xs font-medium ${getTextStyle(item.status)}`}>
                      {item.text}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Legend */}
          <div className="mt-8 pt-4 border-t border-white/10">
            <h4 className="text-sm font-medium text-white/60 mb-2">Status Legend:</h4>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-cyan-400"></div>
                <span className="text-white/60">Active (spinning)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                <span className="text-white/60">Completed</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-purple-400"></div>
                <span className="text-white/60">Estimating</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-amber-400"></div>
                <span className="text-white/60">Validating</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatusSequenceComponent;