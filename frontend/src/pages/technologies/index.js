import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const Technologies = () => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - Технологии" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Технологии</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Технологии, которые применены в этом проекте:</h2>
          <div className={styles.text}>
            <ul className={styles.textItem}>
              <li className={styles.textItem}>
                Python
              </li>
              <li className={styles.textItem}>
                Django
              </li>
              <li className={styles.textItem}>
                Django REST Framework
              </li>
              <li className={styles.textItem}>
                Djoser
              </li>
            </ul>
          </div>
        </div>
      </div>

      <hr></hr>
      <table align = 'center'>
        <tr>
          <td><img src="https://shulikin.com/images/py.png" alt="Python" ></img></td>
          <td><img src="https://shulikin.com/images/django.png" alt="Django" ></img></td>
          <td><img src="https://shulikin.com/images/rest.png" alt="Django REST Framework" ></img></td>
        </tr>
      </table>
      <hr></hr>

    </Container>
  </Main>
}

export default Technologies

