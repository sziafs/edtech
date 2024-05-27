import { useContext } from 'react'
import { CountdownContext } from '../contexts/CountdownContext'
import styles from '../styles/components/Countdown.module.css'

export function Countdown() {
  const { 
    minutes, 
    seconds, 
    hasFinished, 
    isActive, 
    startCountdown, 
    resetCountdown, 
    pomodoro,
    shortBreak,
    longBreak
  } = useContext(CountdownContext)

  const [minuteLeft, minuteRight] = String(minutes).padStart(2, '0').split('')
  const [secondLeft, secondRight] = String(seconds).padStart(2, '0').split('')

  return (
    <div>
      <div className={styles.countdownContainer}>
        <div>
          <span>{minuteLeft}</span>
          <span>{minuteRight}</span>
        </div>
        <span>:</span>
        <div>
          <span>{secondLeft}</span>
          <span>{secondRight}</span>
        </div>
      </div>

      <div className={styles.optionsBarContainer}>
        <button className={styles.optionsButton} onClick={pomodoro}>Pomodoro</button>
        <button className={styles.optionsButton} onClick={shortBreak}>Break Curto</button>
        <button className={styles.optionsButton} onClick={longBreak}>Break Longo</button>
      </div>

      {hasFinished ? (
        <button disabled className={styles.countdownButton}>
          Ciclo encerrado
        </button>
      ) : (
        <>
          {isActive ? (
            <button
              type="button"
              className={`${styles.countdownButton} ${styles.countdownButtonActive}`}
              onClick={resetCountdown}
            >
              Abandonar ciclo
            </button>
          ) : (
            <button type="button" className={styles.countdownButton} onClick={startCountdown}>
              Iniciar um ciclo
            </button>
          )}
        </>
      )}
    </div>
  )
}
