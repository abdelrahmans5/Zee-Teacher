import { useState } from 'react'
import { api, API_BASE } from './api'

export default function App() {
  const [email, setEmail] = useState('admin@zee.local')
  const [password, setPassword] = useState('Admin@123')
  const [token, setToken] = useState('')
  const [me, setMe] = useState(null)
  const [health, setHealth] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])
  const [error, setError] = useState('')

  const login = async () => {
    try {
      setError('')
      const data = await api('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      setToken(data.token)
    } catch (e) {
      setError(e.message)
    }
  }

  const loadMe = async () => {
    try {
      setError('')
      setMe(await api('/auth/me', {}, token))
    } catch (e) {
      setError(e.message)
    }
  }

  const loadHealth = async () => {
    try {
      setError('')
      setHealth(await api('/health'))
    } catch (e) {
      setError(e.message)
    }
  }

  const loadLeaderboard = async () => {
    try {
      setError('')
      setLeaderboard(await api('/leaderboard/top?limit=5'))
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <main style={{ maxWidth: 860, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>Zee Teacher Dashboard Starter</h1>
      <p>API Base: {API_BASE}</p>

      <section style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, marginBottom: 16 }}>
        <h2>Login</h2>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />{' '}
        <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="password" />{' '}
        <button onClick={login}>Login</button>
        <p><b>Token:</b> {token ? `${token.slice(0, 18)}...` : 'not logged in'}</p>
      </section>

      <section style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, marginBottom: 16 }}>
        <h2>Quick Checks</h2>
        <button onClick={loadHealth}>Health</button>{' '}
        <button onClick={loadMe} disabled={!token}>Who Am I</button>{' '}
        <button onClick={loadLeaderboard}>Leaderboard</button>
        <pre>{JSON.stringify({ health, me, leaderboard }, null, 2)}</pre>
      </section>

      {error && <p style={{ color: 'crimson' }}>{error}</p>}
    </main>
  )
}
