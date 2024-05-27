import { createContext, ReactNode, useContext, useEffect, useState } from 'react'
import { ChallengesContext } from './ChallengesContext'

interface CountdownContextData {
  minutes: number
  seconds: number
  hasFinished: boolean
  isActive: boolean
  startCountdown: () => void
  resetCountdown: () => void
  pomodoro: () => void
  shortBreak: () => void
  longBreak: () => void
}

interface CountdownsProviderProps {
  children: ReactNode
}

export const CountdownContext = createContext({} as CountdownContextData)

let countdownTimeout: NodeJS.Timeout

export function CountdownProvider({ children }: CountdownsProviderProps) {
  const { startNewChallenge } = useContext(ChallengesContext)

  const [isActive, setIsActive] = useState(false)
  const [hasFinished, setHasFinished] = useState(false)

  const [isPomodoro, setIsPomodoro] = useState(false)
  const [time, setTime] = useState(25 * 60)
  const minutes = Math.floor(time / 60)
  const seconds = time % 60

  function pomodoro() {
    setIsPomodoro(true)
    setTime(25 * 60)
    clearTimeout(countdownTimeout)
    setIsActive(false)
  }

  function shortBreak() {
    setIsPomodoro(false)
    setTime(5 * 60)
    clearTimeout(countdownTimeout)
    setIsActive(false)
  }

  function longBreak() {
    setIsPomodoro(false)
    setTime(10 * 60)
    clearTimeout(countdownTimeout)
    setIsActive(false)
  }

  function startCountdown() {
    setIsActive(true)
  }

  function resetCountdown() {
    clearTimeout(countdownTimeout)
    setIsActive(false)
    setTime(25 * 60)
    setHasFinished(false)
  }

  useEffect(() => {
    if (isActive && time > 0) {
      countdownTimeout = setTimeout(() => {
        setTime(time - 1)
      }, 1000)
    } 
    else if (isActive && isPomodoro && time === 0) {
      setHasFinished(true)
      setIsActive(false)
      startNewChallenge()
    } 
    else if (isActive && !isPomodoro && time === 0) {
      new Audio('/notification.mp3').play()
      if (Notification.permission == 'granted') {
        new Notification('Pausa finalizada.', {
          body: 'Volte ao Pomodoro para ganhar pontos!',
        })
      }
    }
  }, [isActive, time])

  return (
    <CountdownContext.Provider value={{ 
      minutes, 
      seconds, 
      hasFinished, 
      isActive, 
      startCountdown, 
      resetCountdown, 
      pomodoro,
      shortBreak,
      longBreak 
      }}>
      {children}
    </CountdownContext.Provider>
  )
}
