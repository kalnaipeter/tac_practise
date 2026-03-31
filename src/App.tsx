import { useState, useEffect } from 'react'
import CountryTable from './components/CountryTable'
import LoadingSpinner from './components/LoadingSpinner'
import ThemeToggle from './components/ThemeToggle'

function App() {
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 3000)
    return () => clearTimeout(timer)
  }, [])

  if (loading) return <LoadingSpinner />
  return (
    <>
      <ThemeToggle />
      <CountryTable />
    </>
  )
}

export default App
