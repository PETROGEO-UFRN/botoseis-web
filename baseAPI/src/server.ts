import appFactory from '@/app'
import { getEnvironment } from '@/config/environment'

const PORT = Number(process.env.PORT) || 5000

const app = appFactory({ environment: getEnvironment() })

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`)
})
