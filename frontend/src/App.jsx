import { useState } from 'react'
import './App.css'

function App() {
  const [description, setDescription] = useState('')
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!description.trim()) return

    setMessages([])
    setIsLoading(true)

    const ws = new WebSocket('ws://localhost:8001/ws/estimate')

    ws.onopen = () => {
      ws.send(JSON.stringify({ description }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMessages(prev => [...prev, data])

      if (data.type === 'complete' || data.type === 'error') {
        setIsLoading(false)
        ws.close()
      }
    }

    ws.onerror = () => {
      setMessages(prev => [...prev, { type: 'error', error: 'Connection failed' }])
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>GoodFood</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Describe your meal..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Estimating...' : 'Estimate'}
        </button>
      </form>

      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className="message">
            {msg.type === 'start' && <p>Starting estimation for: {msg.description}</p>}
            {msg.type === 'iteration' && <p>Iteration {msg.iteration}/{msg.max}</p>}
            {msg.type === 'status' && <p>Status: {msg.status}</p>}
            {msg.type === 'estimates' && <p>Got {msg.count} nutrient estimates</p>}
            {msg.type === 'verification' && <p>Approval: {msg.approval}%</p>}
            {msg.type === 'complete' && (
              <div>
                <p><strong>Complete! All nutrients:</strong></p>
                <pre style={{fontSize: '12px', maxHeight: '400px', overflow: 'auto'}}>
                  {JSON.stringify(msg.result.estimates, null, 2)}
                </pre>
              </div>
            )}
            {msg.type === 'error' && <p style={{color: 'red'}}>Error: {msg.error}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
