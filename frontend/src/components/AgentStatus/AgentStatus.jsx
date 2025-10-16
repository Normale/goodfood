import { motion, AnimatePresence } from 'framer-motion';
import { SparklesIcon, CheckCircleIcon } from '../ui/Icons';
import './AgentStatus.css';

const AgentStatus = ({ agents }) => {
  const getAgentIcon = (agentType) => {
    if (agentType === 'preprocessing') {
      return '🔍';
    } else if (agentType === 'estimator') {
      return '⚖️';
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
    } else if (agentType === 'detailed_analyzer') {
      return 'from-orange-500 to-red-600';
    } else if (agentType === 'final_estimates') {
      return 'from-emerald-500 to-teal-600';
    }
    return 'from-gray-500 to-gray-600';
  };

  return (
    <div className="agent-status-container">
      <AnimatePresence mode="popLayout">
        {agents.map((agent) => (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.3 } }}
            transition={{ type: 'spring', damping: 20, stiffness: 300 }}
            className="agent-status-card"
          >
            <div className={`agent-icon-container bg-gradient-to-br ${getAgentColor(agent.agent_type)}`}>
              <span className="agent-icon-emoji">{getAgentIcon(agent.agent_type)}</span>
              {agent.status === 'running' && (
                <motion.div
                  className="agent-spinner"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                >
                  <SparklesIcon className="w-4 h-4 text-white" />
                </motion.div>
              )}
              {agent.status === 'done' && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="agent-check"
                >
                  <CheckCircleIcon className="w-4 h-4 text-white" />
                </motion.div>
              )}
            </div>
            <div className="agent-content">
              <div className="agent-type">{agent.agent_type.replace(/_/g, ' ')}</div>
              <div className="agent-message">{agent.message}</div>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default AgentStatus;
