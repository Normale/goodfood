import { motion, AnimatePresence } from 'framer-motion';
import { SparklesIcon, CheckCircleIcon } from '../ui/Icons';
import './AgentStatus.css';

const AgentStatus = ({ agents, isThinking }) => {
  const getAgentIcon = (agentType) => {
    if (agentType === 'preprocessing') {
      return '🔍';
    } else if (agentType === 'estimator') {
      return '⚖️';
    } else if (agentType === 'validator') {
      return '✓';
    } else if (agentType === 'detailed_analyzer') {
      return '🔬';
    } else if (agentType === 'final_estimates') {
      return '✅';
    }
    return '🤖';
  };

  const getAgentColor = (agentType) => {
    if (agentType === 'preprocessing') {
      return 'from-blue-500 to-cyan-600';
    } else if (agentType === 'estimator') {
      return 'from-purple-500 to-pink-600';
    } else if (agentType === 'validator') {
      return 'from-green-500 to-emerald-600';
    } else if (agentType === 'detailed_analyzer') {
      return 'from-orange-500 to-red-600';
    } else if (agentType === 'final_estimates') {
      return 'from-emerald-500 to-teal-600';
    }
    return 'from-gray-500 to-gray-600';
  };

  // Show "Thinking..." when no agents but workflow is active
  if (isThinking && agents.length === 0) {
    return (
      <div className="agent-status-wrapper">
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="agent-thinking"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            className="thinking-spinner"
          >
            <SparklesIcon className="w-4 h-4 text-cyan-400" />
          </motion.div>
          <span className="thinking-text">Thinking...</span>
        </motion.div>
      </div>
    );
  }

  // Don't show anything if no agents
  if (agents.length === 0) {
    return null;
  }

  return (
    <div className="agent-status-wrapper">
      <AnimatePresence mode="popLayout">
        {agents.map((agent) => (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, height: 0, marginBottom: 0 }}
            animate={{ opacity: 1, height: 'auto', marginBottom: 6 }}
            exit={{ opacity: 0, height: 0, marginBottom: 0 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="agent-status-item"
          >
            <div className={`agent-icon-mini bg-gradient-to-br ${getAgentColor(agent.agent_type)}`}>
              {agent.status === 'running' ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
                  className="w-3 h-3"
                >
                  <SparklesIcon className="w-3 h-3 text-white" />
                </motion.div>
              ) : (
                <CheckCircleIcon className="w-3 h-3 text-white" />
              )}
            </div>
            <div className="agent-text">
              <span className="agent-message-compact">{agent.message}</span>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default AgentStatus;
