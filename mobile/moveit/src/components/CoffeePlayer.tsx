
import styles from '../styles/components/CoffeePlayer.module.css'

export function CoffeePlayer() {
  function playMusic() {
    new Audio('/coffeetivity/brazil-bistro.mp3').play()
  }

  return (
    <div className={styles.coffeePlayerContainer}>

      {/* <div className={styles.info}>
        <span className={styles.artist}>Flume</span>
        <span className={styles.name}>Say it</span>
        <div className={styles.progresBar}>
        <div className={styles.bar}></div>
        </div>
      </div> */}

      <div id="control-panel" className={styles.controlPanel}>
        <div className={styles.controls}>
          <div className={styles.prev}></div>
          <div id="play" className={styles.play} onClick={() => playMusic()}></div>
          <div className={styles.next}></div>
        </div>
      </div>

    </div>
  )
}
